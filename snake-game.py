# Add yellow color
YELLOW = (255, 215, 0)
# Add bright blue color
BRIGHT_BLUE = (0, 150, 255)
FOOD_CHARS = list("snake")


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
	while len(foods) < len(chars):
		pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
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
	foods = random_foods(snake, 5)
	score = 0
	running = True

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


		# Game over: wall or self
		# Allow the snake to emerge from the left wall (x < 2) without game over
		if new_head[0] >= 2:
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
		for food in foods:
			fx, fy, fchar = food
			if new_head == [fx, fy]:
				score += 1
				foods.remove(food)
				ate_food = True
				break
		if ate_food:
			if len(foods) == 0:
				foods = random_foods(snake, 5)
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
		for segment in snake:
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
		pygame.display.flip()

	# Game over screen
	font = pygame.font.SysFont(None, 48)
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
