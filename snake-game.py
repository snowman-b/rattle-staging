# Add yellow color
YELLOW = (255, 215, 0)
# Add bright blue color
BRIGHT_BLUE = (0, 150, 255)
FOOD_CHARS = list("rattle")


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


# Draw a rounded rectangle with optional shadow
def draw_rounded_rect(screen, color, pos, radius=8, shadow=True, shadow_offset=3, shadow_alpha=80):
	rect = pygame.Rect(
		MARGIN_LEFT + pos[0]*CELL_SIZE,
		MARGIN_TOP + pos[1]*CELL_SIZE,
		CELL_SIZE, CELL_SIZE)
	if shadow:
		shadow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
		pygame.draw.rect(shadow_surf, (0,0,0,shadow_alpha), shadow_surf.get_rect(), border_radius=radius)
		screen.blit(shadow_surf, (rect.x+shadow_offset, rect.y+shadow_offset))
	pygame.draw.rect(screen, color, rect, border_radius=radius)


import random
def get_fixed_foods():
	chars = FOOD_CHARS[:]
	random.shuffle(chars)
	row = GRID_HEIGHT // 2  # Middle row
	spacing = GRID_WIDTH // (len(chars) + 1)
	foods = []
	for i, char in enumerate(chars):
		x = spacing * (i + 1)
		foods.append([x, row, char])
	return foods

def main():
	# Timer setup
	start_ticks = pygame.time.get_ticks()
	elapsed_seconds = 0
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Snake Game')
	clock = pygame.time.Clock()

	# Snake spawns from the left border, three snake-widths above the bottom border
	start_y = GRID_HEIGHT - 3
	snake = [[0, start_y], [1, start_y], [2, start_y]]
	direction = (1, 0)
	# Generate and store initial food positions (evenly spaced)
	# Generate and store initial food positions and letter assignment (fixed for the game)
	initial_foods = get_fixed_foods()
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
			# Check win condition BEFORE respawning food
			if all(found_words.values()):
				win = True
				running = False
			collected_letters = []
			# Only respawn food if the game is not already over
			if not win and running:
				# Restore the original food positions and letter assignment
				foods = [f.copy() for f in initial_foods]
				pending_portal_respawn = False
			# If the game is won, do not respawn food
			# collected_letters already cleared above

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
		# Draw 'RATTLE' at the top with a modern font and drop shadow
		DKGREEN = (0, 100, 0)
		try:
			font_rattle = pygame.font.SysFont("Avenir Next", 96, bold=True)
		except:
			font_rattle = pygame.font.SysFont(None, 96, bold=True)
		rattle_surf = font_rattle.render("RATTLE", True, DKGREEN)
		# Drop shadow
		shadow = font_rattle.render("RATTLE", True, (0,0,0))
		rattle_x = (WIDTH - rattle_surf.get_width()) // 2
		rattle_y = (MARGIN_TOP - rattle_surf.get_height()) // 2
		screen.blit(shadow, (rattle_x+4, rattle_y+4))
		screen.blit(rattle_surf, (rattle_x, rattle_y))
		# Draw arena border as a thick rounded rectangle with gradient
		border_rect = pygame.Rect(MARGIN_LEFT-10, MARGIN_TOP-10, ARENA_WIDTH+20, ARENA_HEIGHT+20)
		border_surf = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
		for i in range(10):
			alpha = 180 - i*15
			color = (30,30,30,alpha)
			pygame.draw.rect(border_surf, color, border_surf.get_rect().inflate(-i*2,-i*2), border_radius=24)
		screen.blit(border_surf, (border_rect.x, border_rect.y))
		# Draw bright blue segment on right border (rounded)
		blue_x = MARGIN_LEFT + ARENA_WIDTH
		blue_y_start = MARGIN_TOP + ARENA_HEIGHT - 4*CELL_SIZE
		blue_height = 3*CELL_SIZE
		pygame.draw.rect(
			screen, BRIGHT_BLUE,
			(blue_x, blue_y_start, 14, blue_height), border_radius=7
		)
		# Draw timer in right margin, moved up by 200 pixels
		if not win:
			elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
		font_timer = pygame.font.SysFont(None, 36, bold=True)
		timer_surf = font_timer.render(f"Time: {elapsed_seconds}s", True, BLACK)
		timer_x = blue_x + 20
		timer_y = blue_y_start + blue_height//2 - timer_surf.get_height() - 210
		screen.blit(timer_surf, (timer_x, timer_y))

		# Draw 'submit word' text in right margin, aligned with blue border
		font_submit = pygame.font.SysFont(None, 36, bold=True)
		submit_surf = font_submit.render("submit word", True, BRIGHT_BLUE)
		submit_x = blue_x + 20
		submit_y = blue_y_start + blue_height//2 - submit_surf.get_height()//2
		screen.blit(submit_surf, (submit_x, submit_y))
		# Draw yellow segment on left border, same dimensions (rounded)
		yellow_x = MARGIN_LEFT - 10
		yellow_y_start = blue_y_start
		yellow_height = blue_height
		pygame.draw.rect(
			screen, YELLOW,
			(yellow_x, yellow_y_start, 14, yellow_height), border_radius=7
		)
		# Fill arena background with a soft gradient
		arena_rect = pygame.Rect(MARGIN_LEFT, MARGIN_TOP, ARENA_WIDTH, ARENA_HEIGHT)
		arena_surf = pygame.Surface((ARENA_WIDTH, ARENA_HEIGHT))
		for y in range(ARENA_HEIGHT):
			shade = 245 - int(20 * (y / ARENA_HEIGHT))
			pygame.draw.line(arena_surf, (shade, shade, 255), (0, y), (ARENA_WIDTH, y))
		screen.blit(arena_surf, (MARGIN_LEFT, MARGIN_TOP))
		# Draw snake with rounded segments and shadow
		n = len(snake)
		m = len(collected_letters)
		for i, segment in enumerate(snake):
			color = (60, 180, 90) if i == 0 else (80, 200, 120)
			draw_rounded_rect(screen, color, segment, radius=8, shadow=True)
			if i < m:
				try:
					font_letter = pygame.font.SysFont("Avenir Next", 24, bold=True)
				except:
					font_letter = pygame.font.SysFont(None, 24, bold=True)
				letter_surf = font_letter.render(collected_letters[-(i+1)], True, (255,255,255))
				x = MARGIN_LEFT + segment[0]*CELL_SIZE + (CELL_SIZE - letter_surf.get_width())//2
				y = MARGIN_TOP + segment[1]*CELL_SIZE + (CELL_SIZE - letter_surf.get_height())//2
				screen.blit(letter_surf, (x, y))
		# Draw food as rounded, shaded, and with modern font
		for food in foods:
			fx, fy, fchar = food
			draw_rounded_rect(screen, (255, 80, 80), (fx, fy), radius=10, shadow=True)
			try:
				font = pygame.font.SysFont("Avenir Next", 24, bold=True)
			except:
				font = pygame.font.SysFont(None, 24, bold=True)
			char_surf = font.render(fchar, True, (255,255,255))
			x = MARGIN_LEFT + fx*CELL_SIZE + (CELL_SIZE - char_surf.get_width())//2
			y = MARGIN_TOP + fy*CELL_SIZE + (CELL_SIZE - char_surf.get_height())//2
			screen.blit(char_surf, (x, y))
		# Draw score with modern font and shadow
		try:
			font = pygame.font.SysFont("Avenir Next", 36, bold=True)
		except:
			font = pygame.font.SysFont(None, 36, bold=True)
		score_surf = font.render(f'Score: {score}', True, (40,40,40))
		shadow = font.render(f'Score: {score}', True, (200,200,200))
		screen.blit(shadow, (14, 14))
		screen.blit(score_surf, (10, 10))

		# Draw word length underscores in the bottom margin, and fill with found words if any
		try:
			font_underscore = pygame.font.SysFont("Avenir Next", 48, bold=True)
		except:
			font_underscore = pygame.font.SysFont(None, 48, bold=True)
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

		# Draw leaderboard directly underneath the underscores
		try:
			font_leader = pygame.font.SysFont("Avenir Next", 40, bold=True)
		except:
			font_leader = pygame.font.SysFont(None, 40, bold=True)
		leaderboard_lines = [
			"LEADERBOARD",
			"benja       0:25",
			"WCasp    1:44",
			"DBrandt  1:48"
		]
		leader_y = start_y + 110
		for line in leaderboard_lines:
			surf = font_leader.render(line, True, BLACK)
			surf_x = (WIDTH - surf.get_width()) // 2
			screen.blit(surf, (surf_x, leader_y))
			leader_y += surf.get_height() + 5

		# Update the display every frame
		pygame.display.flip()

	# End screen with modern font and shadow
	try:
		font = pygame.font.SysFont("Avenir Next", 48, bold=True)
	except:
		font = pygame.font.SysFont(None, 48, bold=True)
	if win:
		# Split message into two lines
		msg_lines = ["Congratulations!", "You found all the words!"]
		msg_surfs = []
		outline_surfs = []
		color = (0, 180, 0)
		for line in msg_lines:
			# Render outline by drawing text multiple times offset by 2px in all directions
			outline = pygame.Surface((font.size(line)[0]+8, font.size(line)[1]+8), pygame.SRCALPHA)
			for dx in [-2, 0, 2]:
				for dy in [-2, 0, 2]:
					if dx != 0 or dy != 0:
						outline.blit(font.render(line, True, (0,0,0)), (dx+4, dy+4))
			msg = font.render(line, True, color)
			outline.blit(msg, (4,4))
			outline_surfs.append(outline)
		# Calculate total height
		total_height = sum(s.get_height() for s in outline_surfs)
		y = MARGIN_TOP + 20
		for surf in outline_surfs:
			x = (WIDTH - surf.get_width()) // 2
			screen.blit(surf, (x, y))
			y += surf.get_height() + 2
	else:
		msg = font.render(f'Game Over! Score: {score}', True, RED)
		# Render outline for game over
		outline = pygame.Surface((msg.get_width()+8, msg.get_height()+8), pygame.SRCALPHA)
		for dx in [-2, 0, 2]:
			for dy in [-2, 0, 2]:
				if dx != 0 or dy != 0:
					outline.blit(font.render(f'Game Over! Score: {score}', True, (0,0,0)), (dx+4, dy+4))
		outline.blit(msg, (4,4))
		msg_x = (WIDTH - outline.get_width()) // 2
		msg_y = MARGIN_TOP + 20
		screen.blit(outline, (msg_x, msg_y))
	pygame.display.flip()
	pygame.time.wait(2000)
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()
