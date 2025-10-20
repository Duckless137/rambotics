# import libraries
import time
import circuitpython_gizmo

# set variables for use
gizmo = circuitpython_gizmo.Gizmo()

# write robot code below
while True:
    gizmo.refresh()
    print(gizmo.buttons.a)
    time.sleep(0.01)
