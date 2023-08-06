import sys
import serial
import time

class CommandType:
    MOVE_FORWARD = 0x01
    TURN_LEFT = 0x02
    TURN_RIGHT = 0x03
    TURN_BACK = 0x04
    TOGGLE_LINERRACER = 0x05
    MOVE_FORWARD_SPEED = 0x06
    MOVE_LEFT_SPEED = 0x07
    MOVE_RIGHT_SPEED = 0x08
    MOVE_BACKWARD_SPEED = 0x09
    MOVE_FORWARD_LRSPEED = 0x0A
    MOVE_BACKWARD_LRSPEED = 0x0B
    STOP_KAMIBOT = 0x0C
    RESET_KAMIBOT = 0x0D
    SET_LED_COLOR = 0x0E
    SET_SERVER_MOTOR = 0x10
    GET_ULTRASONIC = 0x11
    GET_IR_1 = 0x12
    GET_IR_2 = 0x13
    GET_IR_3 = 0x14
    GET_IR_4 = 0x15
    GET_IR_5 = 0x16
    KAMIBOT_CLEAR = 0x17
    RESET = 0xFF


class PacketIndex:
    START = 0
    LENGTH = 1
    HWID = 2
    HWTYPE = 3
    COMMANDTYPE = 4
    MODETYPE = 5
    MODECOMMAND = 6
    DATA0 = 7
    DATA1 = 8
    DATA2 = 9
    DATA3 = 10
    DATA4 = 11
    DATA5 = 12
    DATA6 = 13
    INDEX = 14
    DATA7 = 15
    DATA8 = 16
    DATA9 = 17
    DATA10 = 18
    END = 19


class RETURN_PACKET:
    START = 0
    LENGTH = 1
    HWID = 2
    HWTYPE = 3
    CMDTYPE = 4
    CMD = 5
    RESULT = 6
    BATTERY = 7
    ULTRASONIC = 8
    LEFTIR1 = 9
    LEFTIR2 = 10
    CENTERIR = 11
    RIGHTIR1 = 12
    RIGHTIR2 = 13
    IDXBIT = 14
    DATA7 = 15
    DATA8 = 16
    DATA9 = 17
    DATA10 = 18
    END = 19


class ModeType:
    MAPBOARD = 0x01
    CONTROL = 0x02
    LINE = 0x12
    RGB = 0x03
    SERVOMOTOR = 0x04
    ULTRA_DISTANCE = 0x05
    ULTRA_REQ = 0x15
    IR = 0x06
    IR_REQ = 0x16
    BATTERY = 0x07
    BATTERY_REQ = 0x17
    VERSION = 0x08
    VERSION_REQ = 0x18
    ALLSENSOR = 0x09
    ALLSENSOR_REQ = 0x19
    REALTIME = 0x0a
    EMERGENCY_STOP = 0x11
    MOTOR_BALANCE = 0xaa


# Command Type
COMMANDTYPE_WRITE = 0x01
COMMANDTYPE_READ = 0x02
COMMANDTYPE_RETURN = 0x03

NULL_COMMAND_PACKET = [
    0x41, 0x14, 0x01, 0x01, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x5a
]

class Kamibot:
    __verbose = False

    def __init__(self, port=None, baud=57600, timeout=2, verbose=True):
        self.__verbose = verbose
        self.__cmdIndex = 1
        self.__battery = None
        self.__ultrasonic = None
        self.__ir = None

        try:
            if self.__verbose:
                print("\nPython Version %s" % sys.version)

            if not port:
                raise ValueError("Could not find port.")

            sr = serial.Serial(port, baud, timeout=timeout)
            sr.flush()
            self.sr = sr
        except KeyboardInterrupt:
            if self.__verbose:
                print("Program Aborted Before Kamibot Instantiated")
            sys.exit()

    def __index(self):
        self.__cmdIndex = self.__cmdIndex + 1
        if self.__cmdIndex > 255:
            self.__cmdIndex = 1
        return self.__cmdIndex

    def close(self):
        if self.sr.isOpen():
            self.sr.flush()
            self.sr.close()
        if self.__verbose:
            print("Kamibot close(): Calling sys.exit(0): Hope to see you soon!")
        sys.exit(0)

    def __process_return(self):
        data = []
        while len(data) < 20:
            if self.sr.inWaiting():
                c = self.sr.read()
                data.append(ord(c))
            else:
                time.sleep(.1)
        print('return data length {0}'.format(len(data)))
        if len(data) == 20:
            self.__battery = data[RETURN_PACKET.BATTERY]
            self.__ultrasonic = data[RETURN_PACKET.ULTRASONIC]
            lir1 = data[RETURN_PACKET.LEFTIR1]
            lir2 = data[RETURN_PACKET.LEFTIR2]
            cir = data[RETURN_PACKET.CENTERIR]
            rir1 = data[RETURN_PACKET.RIGHTIR1]
            rir2 = data[RETURN_PACKET.RIGHTIR2]
            self.__ir = (lir1, lir2, cir, rir1, rir2)
            print('battery={0} ultrasonic={1} ir={2}'.format(self.__battery, self.__ultrasonic, self.__ir))
        else:
            print('Return data error!') 

    # -------------------------------------------------------------------------------------------------------
    #  BLOCK ACTION
    # -------------------------------------------------------------------------------------------------------
    def delay(self, sec):
        time.sleep(sec)

    def move_forward(self, block=1):
        if self.__verbose:
            print("\n * move_forward")
        command = NULL_COMMAND_PACKET[:]
        # print("command bytes %s" % (''.join('\\x' + format(x, '02x') for x in command)))
        # print('\\x'.join(format(x, '02x') for x in command))

        command[PacketIndex.MODETYPE] = ModeType.MAPBOARD
        command[PacketIndex.MODECOMMAND] = 0x01  # 앞으로(맵보드)
        command[PacketIndex.DATA0] = block
        command[PacketIndex.INDEX] = self.__index()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_left(self):
        if self.__verbose:
            print("\n * turn_left")
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.MAPBOARD
        command[PacketIndex.MODECOMMAND] = 0x03  # 왼쪽(맵보드)
        command[PacketIndex.DATA0] = 1
        command[PacketIndex.INDEX] = self.__index()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_right(self):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.MAPBOARD
        command[PacketIndex.MODECOMMAND] = 0x02  # 오른쪽(맵보드)
        command[PacketIndex.DATA0] = 1
        command[PacketIndex.INDEX] = self.__index()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_back(self):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.MAPBOARD
        command[PacketIndex.MODECOMMAND] = 0x04  # 뒤로 돌기(맵보드)
        command[PacketIndex.DATA0] = 1
        command[PacketIndex.INDEX] = self.__index()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def go_forward_with_speed(self, right=100, left=100):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.CONTROL
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 0x00
        command[PacketIndex.DATA1] = right
        command[PacketIndex.DATA2] = 0x00
        command[PacketIndex.DATA3] = left
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def go_backward_with_speed(self, right=100, left=100):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.CONTROL
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 0x01
        command[PacketIndex.DATA1] = right
        command[PacketIndex.DATA2] = 0x01
        command[PacketIndex.DATA3] = left
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def go_with_speed(self, right=100, left=100, r_dir=0x00, l_dir=0x00):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.CONTROL
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = r_dir
        command[PacketIndex.DATA1] = right
        command[PacketIndex.DATA2] = l_dir
        command[PacketIndex.DATA3] = left
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_led(self, r=100, g=100, b=100):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.RGB
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = r
        command[PacketIndex.DATA1] = g
        command[PacketIndex.DATA2] = b
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def stop(self):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.CONTROL
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 0x02
        command[PacketIndex.DATA1] = 0x02
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def set_server_motor(self, pos=90):
        pos = 0 if pos < 0 else pos
        pos = 180 if pos > 180 else pos

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.SERVOMOTOR
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 180 - pos
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def ultrasonic(self):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.ULTRA_REQ
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return self.__ultrasonic

    def ir(self):
        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.IR_REQ
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.INDEX] = self.__index()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return self.__ir



