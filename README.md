# Three Motor Xbox Control

This project provides a Python script to control three Dynamixel motors using an Xbox controller. The setup allows for interactive movement of two XM430-W350 motors and one XM540-W270 motor.

## What It Does

The script connects to an Xbox controller and maps its inputs to control three Dynamixel motors, enabling:
- **Left joystick control** for two XM430-W350 motors (for left and right motor control).
- **Bumper control** for the XM540-W270 motor.
- Real-time position feedback printed to the console.

## Setup and Requirements

1. **Python 3.6 or newer** is required.
2. Install the following libraries:

    ```bash
    pip install dynamixel-sdk pygame
    ```

3. **Dynamixel SDK**: Ensures communication with Dynamixel motors.
4. **Pygame**: Handles Xbox controller input.

### Additional Setup for Linux

- **SDL2**: Required for low-level I/O with Pygame. Install via:

    ```bash
    sudo apt install libsdl2-dev
    ```

- **Permissions**: Ensure appropriate permissions for USB port access. You may need to run the script with `sudo` if permissions are restricted.

## How to Use It

1. **Clone the Repository**

    ```bash
    git clone https://github.com/1ramihamada/dynamixel-xbox-controller.git
    cd dynamixel-xbox-controller
    ```

2. **Connect and Configure Hardware**

    - Plug in the Xbox controller.
    - Connect the Dynamixel motors via a USB2Dynamixel adapter (or compatible).
    - Ensure the motors are set to the correct IDs:
      - **ID 1**: Left XM430-W350 motor
      - **ID 2**: Right XM430-W350 motor
      - **ID 0**: XM540-W270 motor

3. **Run the Script**

    Execute the control script:

    ```bash
    python3 controller_control.py
    ```

4. **Control Options**

    - **Left Joystick X-axis**: Controls position of the left and right motors.
    - **Left Bumper**: Decreases position of the XM540-W270 motor.
    - **Right Bumper**: Increases position of the XM540-W270 motor.
    - **Real-Time Position**: Motor positions are printed to the console in real-time.

### Example Usage

After starting the script, use the left joystick to control the two main motors (XM430-W350), and use the bumpers to control the larger XM540-W270 motor.

## Troubleshooting

- **Joystick Turns Off**: This can happen due to inactivity. Try setting up a keep-alive routine or check if your joystick has a power-saving mode that can be disabled.
- **Motor Not Responding**: Verify motor ID settings, wiring, and connections.
- **Permission Denied**: Run the script with `sudo` if access issues occur.

## License

MIT License - open-source project.
