import serial
from threading import Thread
from time import sleep
from serial.tools.list_ports import comports
from queue import Queue
import colorama
from colorama import Fore, Back, Style
from CoDrone_mini.storage import *
from CoDrone_mini.receiver import *
from CoDrone_mini.system import *
from CoDrone_mini.crc import *
import random


def convertByteArrayToString(dataArray):
    if dataArray is None:
        return ""
    string = ""
    if isinstance(dataArray, bytes) or isinstance(dataArray, bytearray) or not isinstance(dataArray, list):
        for data in dataArray:
            string += "{0:02X} ".format(data)
    return string


class CoDrone:

    def __init__(self, debug=False, background_flag=True,
                 error_flag=False, log_flag=False, transfer_flag=False, receive_flag=False):

        self._serialport = None
        self._bufferQueue = Queue(4096)
        self._bufferHandler = bytearray()
        self._index = 0
        self._thread = None
        self._flagThreadRun = False
        self._receiver = Receiver()
        self._flagCheckBackground = background_flag
        self._flagShowErrorMessage = error_flag
        self._flagShowLogMessage = log_flag
        self._flagShowTransferData = transfer_flag
        self._flagShowReceiveData = receive_flag
        self._debug_print =  debug
        self._eventHandler = EventHandler()
        self._storageHeader = StorageHeader()
        self._storage = Storage()
        self._storageCount = StorageCount()
        self._parser = Parser()
        self._data = Data()
        self._set_all_event_handler()
        self._base_height = 0

        self.timeStartProgram = time.time()  # 프로그램 시작 시각 기록
        self.systemTimeMonitorData = 0
        self.monitorData = []
        self._control = self.Control()
        for i in range(0, 36):
            self.monitorData.append(i)
        colorama.init()

    def __del__(self):
        self.close()

    def _print_debug(self, message):
        if self._debug_print and message is not None:
            print("{}".format(message))

    def _set_all_event_handler(self):
        self._eventHandler.d[DataType.Attitude] = self._data.event_attitude
        self._eventHandler.d[DataType.State] = self._data.event_battery
        self._eventHandler.d[DataType.Altitude] = self._data.event_altitude
        self._eventHandler.d[DataType.Trim] = self._data.event_trim

    class Control:
        def __init__(self):
            self.roll = 0
            self.pitch = 0
            self.yaw = 0
            self.throttle = 0

        def reset(self):
            self.roll = self.pitch = self.yaw = self.throttle = 0

        def get_all(self):
            return self.roll, self.pitch, self.yaw, self.throttle

    def check_type(self, _type=None, args=None):
        for item in args:
            if not isinstance(item, _type):
                return False
        return True

    def _receiving(self):
        while self._flagThreadRun:
            self._bufferQueue.put(self._serialport.read())
            # 수신 데이터 백그라운드 확인이 활성화 된 경우 데이터 자동 업데이트
            if self._flagCheckBackground:
                while self.check() != DataType.None_:
                    pass

    def isOpen(self):
        if self._serialport is not None:
            return self._serialport.isOpen()
        else:
            return False

    def pair(self, port_name=None):

        if port_name is None:
            port_list = set()
            nodes = comports()
            if len(nodes) == 0:
                print("device not found")
                return False
            for item in nodes:
                if item.vid == 6790:
                    port_list.add(item.device)
                    temp = item.device
                    if "wch" in temp:
                        temp = temp.replace("cu.", "tty.")
                    else:
                        temp = temp.replace("cu.", "tty.wch")
                    temp = temp.replace("-", "")
                    port_list.add(temp)

            if len(port_list) == 0:
                print("CoDrone controller not found")
                return False
            port_list = list(port_list)
            port_list.sort()
        else:
            port_list = list()
            port_list.append(port_name)

        for trying_port in port_list:
            try:
                print("Tried to pair with port \'{}\'".format(trying_port))
                self._serialport = serial.Serial(port=trying_port, baudrate=57600)
                if self.isOpen():
                    self._flagThreadRun = True
                    self._thread = Thread(target=self._receiving, args=(), daemon=True)
                    self._thread.start()

                    # 로그 출력
                    print("Successfully paired with CoDrone Mini remote at port \'{}\'".format(trying_port))
                    self._printLog("Connected.({0})".format(trying_port))
                    sleep(1)
                    self._get_data_while(DeviceType.Drone, DataType.Altitude)
                    self._base_height = self._data.height
                    self.set_speed(3)
                    return True
                else:
                    print("port \'{}\' is closed".format(trying_port))
                    # 오류 메세지 출력
                    self._printError("port \'{}\' is closed".format(trying_port))

            except:
                # 오류 메세지 출력
                print("port \'{}\' is busy".format(trying_port))
                # 오류 메세지 출력
                self._printError("port \'{}\' is busy".format(trying_port))
        print("Failed to pair to CoDrone Mini remote.")
        return False

    def close(self):
        # 로그 출력
        if self.isOpen():
            self._printLog("Closing serial port.")
        self._printLog("Thread Flag False.")
        if self._flagThreadRun:
            self._flagThreadRun = False
            sleep(0.1)
        self._printLog("Thread Join.")
        if self._thread is not None:
            self._thread.join(timeout=1)
        self._printLog("Port Close.")

        if self.isOpen():
            self._serialport.close()
            sleep(0.2)

    def makeTransferDataArray(self, header, data):
        if header is None or data is None:
            return None

        if not isinstance(header, Header):
            return None

        if isinstance(data, ISerializable):
            data = data.toArray()

        crc16 = CRC16.calc(header.toArray(), 0)
        crc16 = CRC16.calc(data, crc16)

        data_array = bytearray()
        data_array.extend((0x0A, 0x55))
        data_array.extend(header.toArray())
        data_array.extend(data)
        data_array.extend(pack('H', crc16))
        return data_array

    def transfer(self, header, data):
        if not self.isOpen():
            return
        dataArray = self.makeTransferDataArray(header, data)
        self._serialport.write(dataArray)
        # 송신 데이터 출력
        self._printTransferData(dataArray)
        return dataArray

    def check(self):
        while not self._bufferQueue.empty():
            dataArray = self._bufferQueue.get_nowait()
            self._bufferQueue.task_done()

            if dataArray is not None and len(dataArray) > 0:
                # 수신 데이터 출력
                self._printReceiveData(dataArray)
                self._bufferHandler.extend(dataArray)

        while len(self._bufferHandler) > 0:
            stateLoading = self._receiver.call(self._bufferHandler.pop(0))
            # 오류 출력
            if stateLoading == StateLoading.Failure:
                self._printReceiveDataEnd()
                self._printError(self._receiver.message)
            # 로그 출력
            if stateLoading == StateLoading.Loaded:
                self._printReceiveDataEnd()
                self._printLog(self._receiver.message)
            if self._receiver.state == StateLoading.Loaded:
                self._handler(self._receiver.header, self._receiver.data)
                return self._receiver.header.dataType

        return DataType.None_

    def checkDetail(self):
        while not self._bufferQueue.empty():
            dataArray = self._bufferQueue.get_nowait()
            self._bufferQueue.task_done()
            if dataArray is not None and len(dataArray) > 0:
                # 수신 데이터 출력
                self._printReceiveData(dataArray)
                self._bufferHandler.extend(dataArray)

        while len(self._bufferHandler) > 0:
            stateLoading = self._receiver.call(self._bufferHandler.pop(0))
            # 오류 출력
            if stateLoading == StateLoading.Failure:
                # 수신 데이터 출력(줄넘김)
                self._printReceiveDataEnd()
                # 오류 메세지 출력
                self._printError(self._receiver.message)

            # 로그 출력
            if stateLoading == StateLoading.Loaded:
                # 수신 데이터 출력(줄넘김)
                self._printReceiveDataEnd()
                # 로그 출력
                self._printLog(self._receiver.message)

            if self._receiver.state == StateLoading.Loaded:
                self._handler(self._receiver.header, self._receiver.data)
                return self._receiver.header, self._receiver.data
        return None, None

    def _handler(self, header, dataArray):

        self._runHandler(header, dataArray)
        self._runEventHandler(header.dataType)
        self._receiver.checked()

        return header.dataType

    def _runHandler(self, header, dataArray):
        # 일반 데이터 처리
        if self._parser.d[header.dataType] is not None:
            self._storageHeader.d[header.dataType] = header
            self._storage.d[header.dataType] = self._parser.d[header.dataType](dataArray)
            self._storageCount.d[header.dataType] += 1

    def _runEventHandler(self, dataType):
        if isinstance(dataType, DataType) and self._eventHandler.d[dataType] is not None and \
                self._storage.d[dataType] is not None:
            return self._eventHandler.d[dataType](self._storage.d[dataType])
        else:
            return None

    def setEventHandler(self, dataType, eventHandler):
        if not isinstance(dataType, DataType):
            return
        self._eventHandler.d[dataType] = eventHandler

    def getHeader(self, dataType):
        if not isinstance(dataType, DataType):
            return None
        return self._storageHeader.d[dataType]

    def getData(self, dataType):
        if not isinstance(dataType, DataType):
            return None
        return self._storage.d[dataType]

    def getCount(self, dataType):
        if not isinstance(dataType, DataType):
            return None
        return self._storageCount.d[dataType]

    def _printLog(self, message):
        if self._flagShowLogMessage and message is not None:
            print(Fore.GREEN + "[{0:10.03f}] {1}".format((time.time() - self.timeStartProgram),
                                                         message) + Style.RESET_ALL)

    def _printError(self, message):
        if self._flagShowErrorMessage and message is not None:
            print(
                Fore.RED + "[{0:10.03f}] {1}".format((time.time() - self.timeStartProgram), message) + Style.RESET_ALL)

    def _printTransferData(self, dataArray):
        if self._flagShowTransferData and dataArray is not None and len(dataArray) > 0:
            print(Back.YELLOW + Fore.BLACK + convertByteArrayToString(dataArray) + Style.RESET_ALL)

    def _printReceiveData(self, dataArray):
        if self._flagShowReceiveData and dataArray != None and len(dataArray) > 0:
            print(Back.CYAN + Fore.BLACK + convertByteArrayToString(dataArray) + Style.RESET_ALL, end='')

    def _printReceiveDataEnd(self):

        # 수신 데이터 출력(줄넘김)
        if self._flagShowReceiveData:
            print("")

    # BaseFunctions End

    def sendPing(self, deviceType):
        if not isinstance(deviceType, DeviceType):
            return None
        header = Header(DataType.Ping, Ping.getSize(), DeviceType.Base, deviceType)
        data = Ping(0)
        return self.transfer(header, data)

    def sendRequest(self, deviceType, dataType):
        if not isinstance(deviceType, DeviceType) or not isinstance(dataType, DataType):
            return None
        header = Header(DataType.Request, Request.getSize(), DeviceType.Base, deviceType)
        data = Request(dataType)
        return self.transfer(header, data)

    def _get_data_while(self, device_type, data_type):
        """This function checks if a request arrived or not and requests again maximum 3 times, 0.15sec

        Args:
            data_type: member values in the DataType class
            timer: member values in the Timer class
        """
        time_start = time.time()
        header = Header(DataType.Request, Request.getSize(), DeviceType.Base, device_type)
        data = Request()
        data.dataType = data_type

        # Break the loop if request time is over 0.15sec, send the request maximum 3 times
        receiving_flag = self._storageCount.d[data_type]
        resend_flag = 1
        self.transfer(header, data)
        while self._storageCount.d[data_type] == receiving_flag:
            interval = time.time() - time_start
            if interval > 0.05 * resend_flag and resend_flag < 3:
                self.transfer(header, data)
                resend_flag += 1
            elif interval > 0.15:
                break
            sleep(0.01)
        return self._storageCount.d[data_type] > receiving_flag

    def get_height(self):
        self._print_debug("request height")
        self._get_data_while(DeviceType.Drone, DataType.Altitude)
        return round((self._data.height - self._base_height) * 100, 1)

    def get_pressure(self):
        self._print_debug("request pressure")
        self._get_data_while(DeviceType.Drone, DataType.Altitude)
        return self._data.pressure

    def get_drone_temp(self):
        self._print_debug("request temperature")
        self._get_data_while(DeviceType.Drone, DataType.Altitude)
        return self._data.temperature

    def get_battery_percentage(self):
        self._print_debug("request battery")
        self._get_data_while(DeviceType.Drone, DataType.State)
        return self._data.battery

    def get_angle(self):
        self._print_debug("request angles")
        self._get_data_while(DeviceType.Drone, DataType.Attitude)
        return self._data.attitude

    def get_trim(self):
        self._print_debug("request trim")
        self._get_data_while(DeviceType.Drone, DataType.Trim)
        return self._data.trim

    def sendPairing(self, deviceType, address0, address1, address2, scramble, channel0, channel1, channel2, channel3):
        int_item = [address0, address1, address2, scramble, channel0, channel1, channel2, channel3]
        if not isinstance(deviceType, DeviceType) or not self.check_type(int, int_item):
            return None
        header = Header(DataType.Pairing, Pairing.getSize(), DeviceType.Base, deviceType)
        data = Pairing(address0, address1, address2, scramble, channel0, channel1, channel2, channel3)
        return self.transfer(header, data)


    # Control Start
    def takeoff(self):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.FlightEvent
        data.option = FlightEvent.TakeOff.value
        self.transfer(header, data)
        self._print_debug("takeoff")
        time.sleep(4)

    def land(self):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.FlightEvent
        data.option = FlightEvent.Landing.value
        self._print_debug("land")

        for loop in range(5):
            self.transfer(header, data)
            time.sleep(random.randint(3, 6)*0.01)

    def emergency_stop(self):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.Stop
        data.option = 0
        self._print_debug("emergency stop")

        for loop in range(5):
            self.transfer(header, data)
            time.sleep(random.randint(1, 5) * 0.01)

    def set_speed(self, speed):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.ControlSpeed
        data.option = speed
        for loop in range(5):
            self.transfer(header, data)
            time.sleep(random.randint(1, 5) * 0.01)

    def headless_on(self):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.Headless
        data.option = 1
        for loop in range(5):
            self.transfer(header, data)
            time.sleep(random.randint(1, 5) * 0.01)
        self._print_debug("Headless mode on")

    def headless_off(self):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.Headless
        data.option = 2
        for loop in range(5):
            self.transfer(header, data)
            time.sleep(random.randint(1, 5) * 0.01)
        self._print_debug("Headless mode off")

    def reset_sensor(self):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.ClearBias
        data.option = 0
        for loop in range(5):
            self.transfer(header, data)
            time.sleep(random.randint(1, 5) * 0.01)

    def set_roll(self, power):
        self._print_debug("set roll to {}".format(power))
        self._control.roll = power

    def set_pitch(self, power):
        self._print_debug("set pitch to {}".format(power))
        self._control.pitch = power

    def set_yaw(self, power):
        self._print_debug("set yaw to {}".format(power))
        self._control.yaw = power

    def set_throttle(self, power):
        self._print_debug("set throttle to {}".format(power))
        self._control.throttle = power

    def get_roll(self):
        self._print_debug("request roll")
        return self._control.roll

    def get_pitch(self):
        self._print_debug("request pitch")
        return self._control.pitch

    def get_yaw(self):
        self._print_debug("request yaw")
        return self._control.yaw

    def get_throttle(self):
        self._print_debug("request throttle")
        return self._control.throttle

    def reset_rpyt(self):
        self._control.reset()

    def send_control(self, roll, pitch, yaw, throttle):
        if not self.check_type(int, [roll, pitch, yaw, throttle]):
            return None

        header = Header(DataType.Control, ControlQuad8.getSize(), DeviceType.Base, DeviceType.Drone)
        data = ControlQuad8(roll, pitch, yaw*(-1), throttle)
        return self.transfer(header, data)

    def flip(self, direction=Direction.FORWARD):
        header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Command()
        data.commandType = CommandType.FlightEvent
        if direction is Direction.FORWARD:
            data.option = FlightEvent.FlipFront.value
            self._print_debug("flip forward")
        elif direction is Direction.BACKWARD:
            data.option = FlightEvent.FlipRear.value
            self._print_debug("flip backward")
        elif direction is Direction.LEFT:
            data.option = FlightEvent.FlipLeft.value
            self._print_debug("flip left")
        elif direction is Direction.RIGHT:
            data.option = FlightEvent.FlipRight.value
            self._print_debug("flip right")

        return self.transfer(header, data)

    def send_control_with_duration(self, roll, pitch, yaw, throttle, duration):
        if not self.check_type(int, [roll, pitch, yaw, throttle]):
            return None

        start_time = time.perf_counter()
        while time.perf_counter() - start_time < duration:
            self.send_control(roll, pitch, yaw, throttle)
            time.sleep(random.randint(3, 6)*0.01)
        sleep(0.02)

    def move(self, *args):
        if len(args) == 0:  # move()
            self._print_debug("move()")
            self.send_control_with_duration(*self._control.get_all(), 0.2)
        elif len(args) == 1:  # move(duration)
            self._print_debug("move for {} seconds".format(args[0]))
            self.send_control_with_duration(*self._control.get_all(), args[0])
            self.hover(1)
        if len(args) == 4:  # move(roll, pitch, yaw, throttle)
            self._print_debug("move at roll : {} pitch : {} yaw : {} throttle : {}".format(*args))
            self.send_control_with_duration(*args, 0.2)
        elif len(args) == 5:  # move(duration, roll, pitch, yaw, throttle)
            self._print_debug("move for {} seconds\n roll : {} pitch : {} yaw : {} throttle : {}".format(*args))
            self.send_control_with_duration(args[1], args[2], args[3], args[4], args[0])
            self.hover(1)

    def go(self, direction, duration=0, power=50):
        # power or -power
        pitch = ((direction == Direction.FORWARD) - (direction == Direction.BACKWARD)) * power
        roll = ((direction == Direction.RIGHT) - (direction == Direction.LEFT)) * power
        throttle = ((direction == Direction.UP) - (direction == Direction.DOWN)) * power
        if duration > 0:
            self._print_debug("go {} for {} seconds with power {}".format(direction.name, duration, power))
            self.send_control_with_duration(roll, pitch, 0, throttle, duration)
            self.hover(1)
        else:
            self._print_debug("go {} with power {}".format(direction.name, power))
            self.send_control(roll, pitch, 0, throttle, 0.2)

    def hover(self, duration=0):
        start_time = time.perf_counter()
        self._print_debug("hover for {} seconds".format(duration))
        while time.perf_counter() - start_time < duration+0.2:
            self.send_control(0, 0, 0, 0)
            sleep(0.02)
        return self.send_control(0, 0, 0, 0)

    def turn(self, direction, duration=None, power=50):
        if direction == Direction.LEFT:
            power = power * (-1)
        if duration is None:
            self._print_debug("turn {} with power {}".format(direction.name, power))
            self.send_control_with_duration(0, 0, power, 0, 0.2)
        else:
            self._print_debug("turn {} for {} seconds with power {}".format(direction.name, duration, power))
            self.send_control_with_duration(0, 0, power, 0, duration)
            self.hover(1)

    def set_trim(self, roll, pitch):
        if not self.check_type(int, [roll, pitch]):
            return None
        header = Header(DataType.Trim, Trim.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Trim()
        data.roll = roll
        data.pitch = pitch
        data.yaw = 0
        data.throttle = 0
        self._print_debug("Set trim to roll : {} pitch : {} ".format(roll, pitch))
        return self.transfer(header, data)

    def reset_trim(self):
        header = Header(DataType.Trim, Trim.getSize(), DeviceType.Base, DeviceType.Drone)
        data = Trim()
        data.roll = data.pitch = data.yaw = data.throttle = 0
        self._print_debug("Reset trim to roll : {} pitch : {} yaw : {} throttle : {}".format(roll, pitch, yaw, throttle))


        return self.transfer(header, data)

    # Control End

    # FLIGHT SEQUENCES -------- START

    def fly_sequence(self, sequence):
        """This function makes the drone fly in a given pattern, then land.

        Args:
            Member values in the Sequence class. Sequence class has SQUARE, CIRCLE, SPIRAL, TRIANGLE, HOP, SWAY, ZIG_ZAG
        """
        if sequence == Sequence.SQUARE:
            self._print_debug("Fly square sequence")
            self.fly_square()
        elif sequence == Sequence.CIRCLE:
            self._print_debug("Fly circle sequence")
            self.fly_circle()
        elif sequence == Sequence.SPIRAL:
            self._print_debug("Fly spiral sequence")
            self.fly_spiral()
        elif sequence == Sequence.TRIANGLE:
            self._print_debug("Fly triangle sequence")
            self.fly_triangle()
        elif sequence == Sequence.HOP:
            self._print_debug("Fly hop sequence")
            self.fly_hop()
        elif sequence == Sequence.SWAY:
            self._print_debug("Fly sway sequence")
            self.fly_sway()
        elif sequence == Sequence.ZIGZAG:
            self._print_debug("Fly zigzag sequence")
            self.fly_zigzag()
        else:
            return None

    def fly_square(self):
        self.send_control_with_duration(30, 0, 0, 0, 1.5)
        self.send_control_with_duration(0, 30, 0, 0, 1.5)
        self.send_control_with_duration(-30, 0, 0, 0, 1.5)
        self.send_control_with_duration(0, -30, 0, 0, 1.5)
        self.hover(1)

    def fly_circle(self):
        # todo
        pass

    def fly_spiral(self):

        for i in range(12):
            self.send_control(10 + 2 * i, 0, -30, 0)
            sleep(0.5)
        self.hover(1)

    def fly_triangle(self):
        self.send_control_with_duration(-40, 40, 0, 0, 1)
        time.sleep(1)
        self.send_control_with_duration(50, 0, 0, 0, 1)
        time.sleep(1)
        self.send_control_with_duration(-40, -40, 0, 0, 0.8)
        self.hover(1)

    def fly_hop(self):

        self.send_control_with_duration(0, 30, 0, 50, 1)
        self.send_control_with_duration(0, 30, 0, -50, 1)

        self.hover(1)

    def fly_sway(self):

        self.send_control_with_duration(-40, 0, 0, 0, 1)
        self.send_control_with_duration(40, 0, 0, 0, 2)
        self.send_control_with_duration(-40, 0, 0, 0, 2)
        self.send_control_with_duration(40, 0, 0, 0, 1)

        self.hover(1)

    def fly_zigzag(self):

        for i in range(2):
            self.send_control_with_duration(-40, 30, 0, 0, 1)
            self.send_control_with_duration(40, 30, 0, 0, 1)
        self.hover(1)

    # FLIGHT SEQUENCES -------- END



    # # Setup Start
    # def sendCommand(self, commandType, option=0):
    #     if not isinstance(commandType, CommandType) or not isinstance(option, int):
    #         return None
    #
    #     header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
    #     data = Command()
    #     data.commandType = commandType
    #     data.option = option
    #
    #     return self.transfer(header, data)
    #
    # def sendModeControlFlight(self, modeControlFlight):
    #     if not isinstance(modeControlFlight, ModeControlFlight):
    #         return None
    #
    #     header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
    #     data = Command()
    #     data.commandType = CommandType.ModeControlFlight
    #     data.option = modeControlFlight.value
    #
    #     return self.transfer(header, data)
    #
    # def sendHeadless(self, headless):
    #
    #     if not isinstance(headless, Headless):
    #         return None
    #
    #     header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
    #
    #     data = Command()
    #
    #     data.commandType = CommandType.Headless
    #     data.option = headless.value
    #
    #     return self.transfer(header, data)
    #
    # def sendWeight(self, weight):
    #
    #     header = Header(DataType.Weight, Weight.getSize(), DeviceType.Base, DeviceType.Drone)
    #     data = Weight()
    #     data.weight = weight
    #     return self.transfer(header, data)
    #
    # def sendClearBias(self):
    #     header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
    #     data = Command(CommandType.ClearBias, 0)
    #
    #     return self.transfer(header, data)
    #
    # def sendSetDefault(self, deviceType):
    #     if not isinstance(deviceType, DeviceType):
    #         return None
    #     header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
    #     data = Command(CommandType.SetDefault, 0)
    #
    #     return self.transfer(header, data)
    #
    # def sendBacklight(self, flagPower):
    #     if not isinstance(flagPower, bool):
    #         return None
    #
    #     header = Header(DataType.Command, Command.getSize(), DeviceType.Base, DeviceType.Drone)
    #     data = Command(CommandType.Backlight, int(flagPower))
    #
    #     return self.transfer(header, data)

    # Setup End

    # Light Start

    def send_led_process(self, dataType, *args):

        length = len(args)

        # check datatype parameter
        if not isinstance(dataType, DataType) or not isinstance(args[0], LightModeDrone):
            return None

        # generate Header object
        header = Header(dataType, LightModeColor.getSize(), DeviceType.Base, DeviceType.Drone)
        # not use
        if length == 3:
            # data = LightModeColors()
            # data.mode.mode = lightMode.value
            # data.mode.interval = interval
            # data.colors = colors

            data = LightModeColors()
            header.length = data.getSize()
            data.mode.mode = args[0].value
            data.colors = args[1]
            data.mode.interval = args[2]
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < 0.2:
                self.transfer(header, data)
                time.sleep(random.randint(3, 6) * 0.01)
            sleep(0.02)

        elif length == 5:
            # LightModeColor
            # data.mode.mode = lightMode.value
            # data.mode.interval = interval
            # data.color.r = r
            # data.color.g = g
            # data.color.b = b

            data = LightModeColor()
            data.mode.mode = args[0].value
            data.color.r = args[1]
            data.color.g = args[2]
            data.color.b = args[3]
            data.mode.interval = args[4]
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < 0.2:
                self.transfer(header, data)
                time.sleep(random.randint(3, 6) * 0.01)
            sleep(0.02)

        return None

    def LED_color(self, r=-1, g=-1, b=-1, brightness=100):
        brightness = brightness * 2
        try:
            self._print_debug("Set LED to R: {} G: {} B: {} Brightness: {}".format(r,g,b,brightness))
            self.send_led_process(DataType.LightDefault, LightModeDrone(Mode.SOLID.value),
                                      r, g, b, brightness)
        except:
            pass  # self._print_error(">>> you put wrong parameter")  # print error message

    def LED_pattern(self, r=-1, g=-1, b=-1, pattern=-1, interval=5):
        interval = 255 - (interval * 25)
        try:
            self._print_debug("Set LED Pattern: {} R: {} G: {} B: {} Interval: {}".format(pattern,r,g,b,interval))
            self.send_led_process(DataType.LightDefault, LightModeDrone(pattern.value), r, g, b, interval)
        except:
            print(">>> Incorrect parameters")  # print error message

    def turn_off_LED(self):
        self._print_debug("Turn off LED")
        self.send_led_process(DataType.LightDefault, LightModeDrone(Mode.OFF.value), 0, 0, 0, 0)

    def reset_LED(self):
        self._print_debug("Reset LED to default")
        self.send_led_process(DataType.LightDefault, LightModeDrone(Mode.SOLID.value), 255, 0, 0, 255)

# Light End
