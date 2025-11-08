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
toggle_a = False
toggle_b = False
spinner_mult = -1
toggle_left_bumper = False
toggle_right_bumper = False
spinner_speed = 60
spinner_speed_change = 20
motor_spinner = Motor(gizmo.MOTOR_1)
motor_spinner.throttle = 0

# R.I.P
# conveyor_on: bool = False
# y_pressed: bool = False
# motor_conveyor = Motor(gizmo.MOTOR_2)

motor_left = Motor(gizmo.MOTOR_3)
motor_right = Motor(gizmo.MOTOR_4)

# R.I.P
# the_flipper = Servo(gizmo.SERVO_1) # Yeah I'm calling it a flipper
# flipper_angle = 0.0 
# flipper_rate = 0.8
# the_flipper.angle = 90

the_arm = Motor(gizmo.MOTOR_2)
the_arm.throttle = 0.0

the_claw_servo = Servo(gizmo.SERVO_1)
the_claw_clamp = Servo(gizmo.SERVO_4)
clamp_toggle = False
clamp_held = False


def check_spinner():
    global toggle_a
    global toggle_b
    global toggle_left_bumper
    global toggle_right_bumper
    global spinner_on
    global spinner_mult
    global spinner_speed
    global spinner_speed_change
    needs_update = False
    
    if gizmo.buttons.left_shoulder:
      if not toggle_left_bumper:
          toggle_left_bumper = True
          if (spinner_speed - spinner_speed_change) > 0:
            spinner_speed -= spinner_speed_change
            print(f"Spinner at {spinner_speed}% speed")
            needs_update = True
    else:
      toggle_left_bumper = False
 
    if gizmo.buttons.right_shoulder:
      if not toggle_right_bumper:
          toggle_right_bumper = True
          if (spinner_speed + spinner_speed_change) <= 100:
            spinner_speed += spinner_speed_change
            print(f"Spinner at {spinner_speed}% speed")
            needs_update = True
    else:
      toggle_right_bumper = False

    if gizmo.buttons.a:
      if not toggle_a:
          toggle_a = True
          spinner_on = not spinner_on
          needs_update = True
    else:
      toggle_a = False
 
    if gizmo.buttons.b:
      if not toggle_b:
          toggle_b = True
          spinner_mult *= -1
          needs_update = True
          print("Reversing spinner")
    else:
      toggle_b = False
             
    if needs_update:
      if spinner_on:
          motor_spinner.throttle = spinner_speed / 100 * spinner_mult
      else:
          motor_spinner.throttle = 0.0


# def check_conveyor():
#    if gizmo.buttons.y:
#        global y_pressed
#        global conveyor_on
#        if not y_pressed:
#            conveyor_on = not conveyor_on
#            print(f"Toggling conveyor (now {conveyor_on})")
#            y_pressed = True
#    else:
#        y_pressed = False

# def commit_flipper(): # No verb for flipper :( 
#    global the_flipper
#    global flipper_angle
#    global flipper_rate
#
#    flipper_angle += flipper_rate
#    if flipper_rate > 0.0:
#        if flipper_angle >= 90.0:
#            flipper_angle = 90.0
#            flipper_rate *= -1 else:
#        if flipper_angle <= 0.0:
#            flipper_angle = 0.0
#            flipper_rate *= -1
#
#    # Angle must be converted to int, otherwise we get OOB err.
#    # Actual variable is a float for precision
#    the_flipper.angle = int(flipper_angle) 

def handle_claw():
    global the_claw_servo
    global the_claw_clamp
    global clamp_toggle
    global clamp_held

    if gizmo.axes.dpad_x == 254:
        the_claw_servo.angle = 90
    elif gizmo.axes.dpad_x == 0:
        the_claw_servo.angle = 0

    if gizmo.buttons.right_trigger > 0:
        if not clamp_held:
          clamp_toggle = not clamp_toggle
          clamp_held = True
    else:
        clamp_held = False

    if clamp_toggle:
        the_claw_clamp.angle = 90
    else:
        the_claw_clamp.angle = gizmo.buttons.right_trigger * 90

def move_arm():
    global the_arm
    global arm_angle
    global arm_rate
    if gizmo.axes.dpad_y == 254:
        the_arm.throttle = 0.55
    elif gizmo.axes.dpad_y == 0:
        the_arm.throttle = -0.2
    else:
        the_arm.throttle = 0
    

while True:
    gizmo.refresh()
    
    # Motor movement
    speed = map_range(gizmo.axes.left_y, 0, 255, -1.0, 1.0)
    turning = map_range(gizmo.axes.left_x, 0, 255, -1.0, 1.0)
    motor_left.throttle = constrain( - speed + turning, -1.0, 1.0)
    motor_right.throttle = constrain( - speed - turning, -1.0, 1.0)

    check_spinner()
    
    # check_conveyor()
    # motor_conveyor.throttle = int(conveyor_on) / 5

    # commit_flipper()
    handle_claw()
    move_arm()
    time.sleep(0.01)
