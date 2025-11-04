import board
import time
import pwmio
import digitalio
from adafruit_motor import servo, servo
from adafruit_simplemath import map_range, constrain 
from circuitpython_gizmo import Gizmo

# sets the parameters for our motors n stuff (can change as we go)
pwm_freq = 50  # Hertz
min_pulse = 1000  # milliseconds
max_pulse = 2000  # milliseconds
servo_range = 90  # degrees

# the Gizmo object provides access to the data that is held by the field management system and the gizmo system processor
gizmo = Gizmo()

class Motor(servo.ContinuousServo):
    def __init__(self, pin):
        super().__init__(
            pwmio.PWMOut(pin, frequency=pwm_freq),
            min_pulse=min_pulse,
            max_pulse=max_pulse
        ) 

class Servo(servo.Servo):
    def __init__(self, pin):
        super().__init__(
            pwmio.PWMOut(pin, frequency=pwm_freq),
            actuation_range=servo_range,
            min_pulse=min_pulse,
            max_pulse=max_pulse
        ) 

spinner_on = False
a_pressed = False
motor_spinner = Motor(gizmo.MOTOR_1)

conveyor_on: bool = False
y_pressed: bool = False
motor_conveyor = Motor(gizmo.MOTOR_2)

motor_left = Motor(gizmo.MOTOR_3)
motor_right = Motor(gizmo.MOTOR_4)

the_flipper = Servo(gizmo.SERVO_1) # Yeah I'm calling it a flipper
flipper_angle = 0.0 
flipper_rate = 0.8
the_flipper.angle = 90

the_claw = Servo(gizmo.SERVO_2)



def check_spinner():
    if gizmo.buttons.a:
        global a_pressed
        global spinner_on
        if not a_pressed:
            spinner_on = not spinner_on
            print(f"Toggling spinner (now {spinner_on})")
            a_pressed = True
    else:
        a_pressed = False

def check_conveyor():
    if gizmo.buttons.y:
        global y_pressed
        global conveyor_on
        if not y_pressed:
            conveyor_on = not conveyor_on
            print(f"Toggling conveyor (now {conveyor_on})")
            y_pressed = True
    else:
        y_pressed = False

def commit_flipper(): # No verb for flipper :( 
    global the_flipper
    global flipper_angle
    global flipper_rate

    flipper_angle += flipper_rate
    if flipper_rate > 0.0:
        if flipper_angle >= 90.0:
            flipper_angle = 90.0
            flipper_rate *= -1
    else:
        if flipper_angle <= 0.0:
            flipper_angle = 0.0
            flipper_rate *= -1

    # Angle must be converted to int, otherwise we get OOB err.
    # Actual variable is a float for precision
    the_flipper.angle = int(flipper_angle) 

def move_claw():
    if gizmo.axes.dpad_x == 254:
        the_claw.angle = 90
    if gizmo.axes.dpad_x == 0:
        the_claw.angle = 0
    pass

while True:
    gizmo.refresh()
    
    # Motor movement
    speed = map_range(gizmo.axes.left_y, 0, 255, -1.0, 1.0)
    turning = map_range(gizmo.axes.left_x, 0, 255, -1.0, 1.0)
    motor_left.throttle = constrain( - speed + turning, -1.0, 1.0)
    motor_right.throttle = constrain(speed + turning, -1.0, 1.0)

    check_spinner()
    motor_spinner.throttle = int(spinner_on)
    
    check_conveyor()
    motor_conveyor.throttle = int(conveyor_on) / 5

    commit_flipper()
    move_claw()
    time.sleep(0.01)
