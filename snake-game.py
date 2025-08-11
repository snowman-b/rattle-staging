# Add yellow color
YELLOW = (255, 215, 0)
# Add bright blue color
BRIGHT_BLUE = (0, 150, 255)
FOOD_CHARS = list("python")


# Classic Snake game using Pygame
import pygame
import random
import sys


# Game settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
ARENA_WIDTH = CELL_SIZE * GRID_WIDTH
ARENA_HEIGHT = CELL_SIZE * GRID_HEIGHT
MARGIN_TOP = 100
MARGIN_LEFT = 200
MARGIN_RIGHT = 200
MARGIN_BOTTOM = 500
WIDTH = ARENA_WIDTH + MARGIN_LEFT + MARGIN_RIGHT
HEIGHT = ARENA_HEIGHT + MARGIN_TOP + MARGIN_BOTTOM
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DKGREEN = (0, 100, 0)
RED = (255, 0, 0)

def draw_rect(screen, color, pos):
	rect = pygame.Rect(
		MARGIN_LEFT + pos[0]*CELL_SIZE,
		MARGIN_TOP + pos[1]*CELL_SIZE,
		CELL_SIZE, CELL_SIZE)
	pygame.draw.rect(screen, color, rect)


def random_foods(snake, count=6):
	chars = FOOD_CHARS
	foods = set()
	min_y = 0
	max_y = GRID_HEIGHT - 4  # 4 snake widths from the bottom
	while len(foods) < 6:
		pos = (random.randint(0, GRID_WIDTH-1), random.randint(min_y, max_y-1))
		if list(pos) not in snake:
			foods.add(pos)
	foods = [list(f) for f in foods]
	return [food + [chars[i]] for i, food in enumerate(foods)]

def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Snake Game')
	clock = pygame.time.Clock()

	# Snake spawns from the left border, three snake-widths above the bottom border
	start_y = GRID_HEIGHT - 3
	snake = [[0, start_y], [1, start_y], [2, start_y]]
	direction = (1, 0)
	# Generate and store initial food positions
	initial_foods = random_foods(snake, 6)
	foods = [f.copy() for f in initial_foods]
	score = 0

	# Track collected letters in order
	collected_letters = []
	# Track if food should respawn after portal
	pending_portal_respawn = False
	running = True

	found_words = {3: None, 4: None, 5: None, 6: None}
	win = False
	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and direction != (0, 1):
					direction = (0, -1)
				elif event.key == pygame.K_DOWN and direction != (0, -1):
					direction = (0, 1)
				elif event.key == pygame.K_LEFT and direction != (1, 0):
					direction = (-1, 0)
				elif event.key == pygame.K_RIGHT and direction != (-1, 0):
					direction = (1, 0)

		# Move snake
		new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]



		# Portal logic for blue and yellow border
		blue_x = GRID_WIDTH - 1
		blue_y_start = GRID_HEIGHT - 4
		blue_y_end = GRID_HEIGHT - 1
		yellow_x = 0

		# If snake hits blue border section, teleport to yellow border at same y
		if new_head[0] == blue_x and blue_y_start <= new_head[1] < blue_y_end:
			new_head[0] = yellow_x
			# On portal, submit collected letters to bottom margin
			if collected_letters:
				word = ''.join(collected_letters)
				l = len(word)
				if l in found_words and not found_words[l]:
					found_words[l] = word
			# Always reset food to all 6 letters in the same positions
			foods = [f.copy() for f in initial_foods]
			pending_portal_respawn = False
			collected_letters = []
			# Check win condition
			if all(found_words.values()):
				win = True
				running = False

		# Game over: wall or self (except for left wall emergence and blue portal)
		if new_head[0] >= 2:
			# Game over if snake hits any black border or itself
			if (
				new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
				new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
				new_head in snake
			):
				running = False
				continue

		snake.insert(0, new_head)


		# Eat food (multiple foods)
		ate_food = False
		for food in foods[:]:
			fx, fy, fchar = food
			if new_head == [fx, fy]:
				score += 1
				foods.remove(food)
				collected_letters.append(fchar)
				ate_food = True
				break
		if ate_food:
			if len(foods) == 0:
				# Do not respawn food until blue portal is crossed
				pending_portal_respawn = True
		else:
			snake.pop()



		# Draw everything
		screen.fill(WHITE)
		# Draw 'RATTLE' at the top
		DKGREEN = (0, 100, 0)
		font_rattle = pygame.font.SysFont(None, 96, bold=True)
		rattle_surf = font_rattle.render("RATTLE", True, DKGREEN)
		rattle_x = (WIDTH - rattle_surf.get_width()) // 2
		rattle_y = (MARGIN_TOP - rattle_surf.get_height()) // 2
		screen.blit(rattle_surf, (rattle_x, rattle_y))
		# Draw arena border (10px black)
		pygame.draw.rect(
			screen, BLACK,
			(MARGIN_LEFT-10, MARGIN_TOP-10, ARENA_WIDTH+20, ARENA_HEIGHT+20), 10
		)
		# Draw bright blue segment on right border
		blue_x = MARGIN_LEFT + ARENA_WIDTH
		blue_y_start = MARGIN_TOP + ARENA_HEIGHT - 4*CELL_SIZE
		blue_height = 3*CELL_SIZE
		pygame.draw.rect(
			screen, BRIGHT_BLUE,
			(blue_x, blue_y_start, 10, blue_height)
		)
		# Draw yellow segment on left border, same dimensions
		yellow_x = MARGIN_LEFT - 10
		yellow_y_start = blue_y_start
		yellow_height = blue_height
		pygame.draw.rect(
			screen, YELLOW,
			(yellow_x, yellow_y_start, 10, yellow_height)
		)
		# Fill arena background white (inside border)
		pygame.draw.rect(
			screen, WHITE,
			(MARGIN_LEFT, MARGIN_TOP, ARENA_WIDTH, ARENA_HEIGHT)
		)
		# Draw snake
		n = len(snake)
		m = len(collected_letters)
		# Place collected_letters[0] on the head, collected_letters[1] next, ..., collected_letters[-1] further toward the tail
		for i, segment in enumerate(snake):
			if i < m:
				draw_rect(screen, DKGREEN, segment)
				font_letter = pygame.font.SysFont(None, 36, bold=True)
				letter_surf = font_letter.render(collected_letters[-(i+1)], True, WHITE)
				x = MARGIN_LEFT + segment[0]*CELL_SIZE + (CELL_SIZE - letter_surf.get_width())//2
				y = MARGIN_TOP + segment[1]*CELL_SIZE + (CELL_SIZE - letter_surf.get_height())//2
				screen.blit(letter_surf, (x, y))
			else:
				draw_rect(screen, DKGREEN, segment)
		# Draw food
		for food in foods:
			fx, fy, fchar = food
			font = pygame.font.SysFont(None, 36)
			char_surf = font.render(fchar, True, RED)
			screen.blit(char_surf, (MARGIN_LEFT + fx*CELL_SIZE, MARGIN_TOP + fy*CELL_SIZE))
		# Draw score
		font = pygame.font.SysFont(None, 36)
		score_surf = font.render(f'Score: {score}', True, WHITE)
		screen.blit(score_surf, (10, 10))

		# Draw word length underscores in the bottom margin, and fill with found words if any
		font_underscore = pygame.font.SysFont(None, 48)
		word_lengths = [3, 4, 5, 6]
		spacing = 60
		start_y = MARGIN_TOP + ARENA_HEIGHT + 80
		# Calculate total width for centering under the arena only
		surf_widths = []
		for length in word_lengths:
			underscores = ' '.join(['_' for _ in range(length)])
			surf = font_underscore.render(underscores, True, BLACK)
			surf_widths.append(surf.get_width())
		total_width = sum(surf_widths) + (len(word_lengths)-1)*spacing
		start_x = MARGIN_LEFT + (ARENA_WIDTH - total_width) // 2
		x = start_x
		for i, length in enumerate(word_lengths):
			underscores = ['_' for _ in range(length)]
			# If found_words has a word for this length, fill in the letters
			if found_words[length]:
				for j, letter in enumerate(found_words[length]):
					underscores[j] = letter
			underscores_str = ' '.join(underscores)
			surf = font_underscore.render(underscores_str, True, BLACK)
			screen.blit(surf, (x, start_y))
			x += surf.get_width() + spacing

		pygame.display.flip()

	# End screen
	font = pygame.font.SysFont(None, 48)
	if win:
		msg = font.render('Congratulations! You found all the words!', True, (0, 180, 0))
	else:
		msg = font.render(f'Game Over! Score: {score}', True, RED)
	# Center horizontally, place just below the arena
	msg_x = (WIDTH - msg.get_width()) // 2
	msg_y = MARGIN_TOP + ARENA_HEIGHT + ((MARGIN_BOTTOM - msg.get_height()) // 2)
	screen.blit(msg, (msg_x, msg_y))
	pygame.display.flip()
	pygame.time.wait(2000)
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()
