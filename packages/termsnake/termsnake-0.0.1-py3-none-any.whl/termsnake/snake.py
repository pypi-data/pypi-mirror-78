#! /usr/bin/env python3
import random
import curses
import curses.textpad as textpad
import argparse


def create_food(snake, box):
	food = None

	while not food:
		food = [random.randint(box[0] + 1, box[2] - 1),
				random.randint(box[1] + 1, box[3] - 1)]

		if food in snake:
			food = None

	return food


def game(scr):
	SNAKE = '|' # '\N{FULL BLOCK}'
	FOOD = '\N{FLOWER PUNCTUATION MARK}'
	colors = [curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN,
			  curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_YELLOW]
	curses.curs_set(0)
	scr.nodelay(1)
	pause = False
	fg = random.choice(colors)
	not_ = False

	while not not_:
		bg = random.choice(colors)

		if fg == bg:
			bg = None
		else:
			not_ = True

	curses.init_pair(1, fg, bg)
	curses.init_pair(2, fg, bg)
	scr.timeout(100)
	h, w = scr.getmaxyx()
	box = [3, 3, h - 3, w - 3]
	textpad.rectangle(scr, *box)
	sc = 0
	snake = [[h // 2, w // 2 + 1], [h // 2, w // 2], [h // 2, w // 2 - 1]]
	score = [2, w // 2 - len(str(sc)) // 2, str(sc)]
	drc = curses.KEY_RIGHT
	opo = {curses.KEY_RIGHT: curses.KEY_LEFT, curses.KEY_LEFT: curses.KEY_RIGHT,
		   curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP}

	scr.attron(curses.color_pair(1))
	for y, x in snake:
		scr.addstr(y, x, SNAKE)
	scr.attroff(curses.color_pair(1))

	food = create_food(snake, box)
	scr.attron(curses.color_pair(2))
	scr.addstr(*food, FOOD)
	scr.attroff(curses.color_pair(2))
	scr.addstr(*score)

	while True:
		key = scr.getch()

		if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_RIGHT, curses.KEY_LEFT, ord('w'), ord('s'), ord('d'), ord('a')] and not pause:
			key = {ord('w'): curses.KEY_UP, ord('s'): curses.KEY_DOWN, ord(
				'd'): curses.KEY_RIGHT, ord('a'): curses.KEY_LEFT}.get(key) or key

			if drc != opo[key]:
				drc = key
		elif key == ord('q'):
			quit()
		elif key == ord(' '):
			if not pause:
				pause = True
			else:
				pause = False

		if not pause:
			tail = snake[0]

			if drc == curses.KEY_RIGHT:
				tail_ = [tail[0], tail[1] + 1]
			elif drc == curses.KEY_LEFT:
				tail_ = [tail[0], tail[1] - 1]
			elif drc == curses.KEY_UP:
				tail_ = [tail[0] - 1, tail[1]]
			elif drc == curses.KEY_DOWN:
				tail_ = [tail[0] + 1, tail[1]]

			snake.insert(0, tail_)
			scr.attron(curses.color_pair(1))
			scr.addstr(*tail_, SNAKE)
			scr.attroff(curses.color_pair(1))

			if snake[0] == food:
				food = create_food(snake, box)
				scr.attron(curses.color_pair(2))
				scr.addstr(*food, FOOD)
				scr.attroff(curses.color_pair(2))
				sc += 1
				score = [2, w // 2 - len(str(sc)) // 2, str(sc)]
				scr.addstr(*score)
			else:
				scr.addstr(snake[-1][0], snake[-1][1], ' ')
				snake.pop()

			if snake[0][0] in [box[0], box[2]] or snake[0][1] in [box[1], box[3]] or snake[0] in snake[1:]:
				msg = 'GAME OVER'
				scr.addstr(h // 2, w // 2 - len(msg) // 2, msg)
				scr.nodelay(0)
				scr.refresh()
				q = False

				while not q:
					key_ = scr.getch()

					if key_ == ord('q'):
						q = True

				break

		scr.refresh()


def main():
	parser = argparse.ArgumentParser(description='''\
A snake game for your terminal. Built with CURSES in Python.

GAME COMMANDS
=>
UP/W     - UP;
RIGHT/D  - RIGHT;
DOWN/S   - DOWN;
LEFT/A   - LEFT;
SPACE    - PLAY/PAUSE;
Q        - QUIT;\
''')
	args = parser.parse_args()
	if args == argparse.Namespace():
		curses.wrapper(game)


if __name__ == '__main__':
	main()
