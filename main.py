import mouse
import time
import numpy as np


on = False
calibration_points = None
stepover = (-1, -1)
grid_size = (-1, -1)


def register_calibration_point():
    global calibration_points
    if len(calibration_points) < 3:
        point = mouse.get_position()
        print(f'Registered {["first", "second", "third"][len(calibration_points)]} calibration point', point)
        calibration_points.append(point)
    if len(calibration_points) >= 3:
        mouse.unhook_all()
        calibration_points = np.array(calibration_points)


def calibrate():
    global calibration_points
    print('Beginning calibration...')
    calibration_points = []
    mouse.on_right_click(lambda: register_calibration_point())
    while len(calibration_points) < 3:
        try:
            time.sleep(0.25)
        except KeyboardInterrupt as e:
            print(e)
            return -1, -1
    # Compute stepovers from three neighboring points
    anchor = calibration_points[0,:]
    offsets_x, offsets_y = np.abs(calibration_points[1:,0] - anchor[0]), np.abs(calibration_points[1:,1] - anchor[1])
    offset_x, offset_y = np.max(offsets_x), np.max(offsets_y)
    calibration_points = None
    print(f'The offsets have been computed to be ({offset_x}, {offset_y}).')
    print('Call calibrate() or even setup() again to change the settings.')
    return offset_x, offset_y


def toggle():
    global on, step_x, step_y
    on = not on
    mouse.unhook_all()
    if on:
        print('Toggling on')
        mouse.on_right_click(lambda: doit())
    else:
        print('Toggling off')


def fill_line(i):
    global stepover, grid_size
    if i > 0:
        mouse.double_click('left')
    for i in range(grid_size[0]):
        mouse.move(stepover[0], 0, absolute=False, duration=0.05)
        mouse.double_click('left')


def doit():
    global stepover, grid_size
    print('Stash it!')
    x_old, y_old = mouse.get_position()
    for i in range(grid_size[1]):
        mouse.move(x_old, y_old + i * stepover[1], absolute=True, duration=0.05)
        fill_line(i)
    mouse.move(x_old, y_old, absolute=True, duration=0.05)


def setup():
    global stepover, grid_size
    print('Please enter the following parameters:')
    x_grid_size = int(input('x_grid_size: '))
    y_grid_size = int(input('y_grid_size: '))
    grid_size = (x_grid_size, y_grid_size)
    print('Now, the stepover in x and y will have to be calibrated.')
    print('For this right click the middles of three grid cells.')
    print('Do this at the programs target window size.')
    print('The second and third cell need to be exactly one cell from the first one (not diagonally).')
    stepover = calibrate()
    print('Setup done. Begin by entering \'toggle()\' in the console.\n\n')


setup()
