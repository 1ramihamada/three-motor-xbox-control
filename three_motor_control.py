from dynamixel_sdk import *  # Uses Dynamixel SDK library
import pygame
import threading

# Control table addresses
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_OPERATING_MODE = 11
ADDR_PRESENT_POSITION = 132
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108

# Default settings
PROTOCOL_VERSION = 2.0
BAUDRATE = 3000000  # Adjusted to 3 Mbps as specified
DEVICENAME = '/dev/ttyUSB1'
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
EXTENDED_POSITION_CONTROL_MODE = 4

# Dynamixel motor IDs
DXL_ID_LEFT = 1       # ID for left XM430-W350 motor
DXL_ID_RIGHT = 2      # ID for right XM430-W350 motor
DXL_ID_LARGER = 0     # ID for XM540-W270 motor

# Position limits and joystick sensitivity
MIN_POSITION = -1_000_000
MAX_POSITION = 1_000_000
POSITION_INCREMENT = 100 # Adjust as needed
v_target = 1000
a_target = 100

class DynamixelController:
    def __init__(self, dxl_id):
        self.dxl_id = dxl_id
        self.lock = threading.Lock()
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

        # Open port and set baudrate
        if self.portHandler.openPort():
            print(f"Port opened for motor ID {self.dxl_id}")
        else:
            raise Exception("Failed to open the port")

        if self.portHandler.setBaudRate(BAUDRATE):
            print("Baudrate set to 3 Mbps")
        else:
            raise Exception("Failed to set baudrate")

        # Set motor settings
        self.disable_torque()
        self.set_operating_mode(EXTENDED_POSITION_CONTROL_MODE)
        self.set_profile_velocity(v_target)
        self.set_profile_acceleration(a_target)
        self.enable_torque()

    def enable_torque(self):
        with self.lock:
            self.packetHandler.write1ByteTxRx(self.portHandler, self.dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)

    def disable_torque(self):
        with self.lock:
            self.packetHandler.write1ByteTxRx(self.portHandler, self.dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

    def set_operating_mode(self, mode):
        with self.lock:
            self.packetHandler.write1ByteTxRx(self.portHandler, self.dxl_id, ADDR_OPERATING_MODE, mode)

    def set_profile_velocity(self, velocity):
        with self.lock:
            self.packetHandler.write4ByteTxRx(self.portHandler, self.dxl_id, ADDR_PROFILE_VELOCITY, velocity)

    def set_profile_acceleration(self, acceleration):
        with self.lock:
            self.packetHandler.write4ByteTxRx(self.portHandler, self.dxl_id, ADDR_PROFILE_ACCELERATION, acceleration)

    def set_goal_position(self, goal_position):
        with self.lock:
            goal_position = max(min(goal_position, MAX_POSITION), MIN_POSITION)
            self.packetHandler.write4ByteTxRx(self.portHandler, self.dxl_id, ADDR_GOAL_POSITION, int(goal_position))

    def get_present_position(self):
        with self.lock:
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(
                self.portHandler, self.dxl_id, ADDR_PRESENT_POSITION)
            if dxl_comm_result == COMM_SUCCESS and dxl_error == 0:
                if dxl_present_position > 0x7FFFFFFF:
                    dxl_present_position -= (1 << 32)
                return dxl_present_position
            else:
                return None

    def __del__(self):
        self.disable_torque()
        if self.portHandler.is_open:
            self.portHandler.closePort()

# Initialize Pygame for joystick control
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize motors
left_motor = DynamixelController(DXL_ID_LEFT)
right_motor = DynamixelController(DXL_ID_RIGHT)
larger_motor = DynamixelController(DXL_ID_LARGER)

try:
    while True:
        pygame.event.pump()  # Process Pygame events

        # Get joystick inputs
        left_stick_x = -joystick.get_axis(0)  # Left joystick horizontal axis
        left_bumper = joystick.get_button(4)  # Left bumper
        right_bumper = joystick.get_button(5)  # Right bumper

        # Control XM430-W350 motors with left joystick X-axis
        if abs(left_stick_x) > 0.1:  # Dead zone threshold
            position_offset = int(left_stick_x * POSITION_INCREMENT)
            left_motor.set_goal_position(left_motor.get_present_position() + position_offset)
            right_motor.set_goal_position(right_motor.get_present_position() + position_offset)
        
        # Control XM540-W270 motor with bumpers
        if left_bumper:
            larger_motor.set_goal_position(larger_motor.get_present_position() - POSITION_INCREMENT)
        elif right_bumper:
            larger_motor.set_goal_position(larger_motor.get_present_position() + POSITION_INCREMENT)

        # Small delay to avoid overwhelming the controller
        pygame.time.wait(0)

except KeyboardInterrupt:
    # Cleanup on exit
    left_motor.__del__()
    right_motor.__del__()
    larger_motor.__del__()
    print("Exiting...")

pygame.quit()
