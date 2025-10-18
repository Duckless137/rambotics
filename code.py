import board
import pwmio
import digitalio
from adafruit_motor import servo
from adafruit_simplemath import map_range, constrain
from circuitpython_gizmo import Gizmo

gizmo = Gizmo()

pwm_freq = 50 # Hertz
min_pulse = 1000 # milliseconds
max_pulse = 2000 # milliseconds
servo_range = 90  # degrees

motor_val = 0.0

motor = servo.ContinuousServo(
    pwmio.PWMOut(gizmo.MOTOR_1, frequency=pwm_freq),
    min_pulse=min_pulse,
    max_pulse=max_pulse
)

while True:
  builtin_led = digitalio.DigitalInOut(board.GP25)
  builtin_led.direction = digitalio.Direction.OUTPUT
  gizmo.refresh()

  motor_val += 0.01
  if motor_val > 1.0:
    motor_val = -1.0
    pass
  motor_left.throttle = motor_val
