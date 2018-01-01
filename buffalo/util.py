""" buffalo.util
"""


# Compare with: `jstest /dev/input/js0`
def joystick_summary(joy):
    print
    print "Name of the joystick:", joy.get_name()
    print "Number of hats:", joy.get_numhats()
    print "Number of track balls:", joy.get_numballs()
    print "Number of axis:", joy.get_numaxes()
    print "Number of buttons:", joy.get_numbuttons()
    print
