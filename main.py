import mouse
import time

stepover = 130
stepdown = 150

def fill_line(i):
	if i > 0:
		mouse.click('left')
	for i in range(7):
		mouse.move(stepover, 0, absolute=False, duration=0.05)
		mouse.click('left')

def doit():
	print('Stash it!')
	x_old, y_old = mouse.get_position()
	for i in range(4):
		mouse.move(x_old, y_old + i * stepdown, absolute=True, duration=0.05)
		fill_line(i)
	mouse.move(x_old, y_old, absolute=True, duration=0.05)

on = False

def toggle():
	global on
	on = not on
	mouse.unhook_all()
	if on:
		print('Toggling on')
		mouse.on_right_click(lambda: doit())
	else:
		print('Toggling off')

toggle()