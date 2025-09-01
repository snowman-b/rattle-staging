# Add yellow color
YELLOW = (255, 215, 0)
# Add bright blue color
BRIGHT_BLUE = (0, 150, 255)

import csv
def load_six_letter_word_for_today():
	import datetime
	today = datetime.datetime.now().strftime('%-m/%-d/%Y')
	csv_path = os.path.join(os.path.dirname(__file__), 'word-list.csv')
	word = None
	try:
		with open(csv_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['date'] == today:
					word = row['word']
					break
	except Exception:
		pass
	if not word:
		# Fallback: pick a default word
		word = 'animal'
	return word



# Classic Snake game using Pygame
import pygame
import random
import sys
import os
# Load word set for validation


# Use wordfreq for word validation
from wordfreq import zipf_frequency

def is_valid_word(word):
	word = word.strip()
	if len(word) == 1:
		return word.upper() in {"A", "I"}
	# Accept English words with zipf_frequency > 2
	return zipf_frequency(word.lower(), 'en') > 2.0


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
		word = load_six_letter_word_for_today()
		# Arrange letters identically for each date by using a fixed seed
		import datetime
		today = datetime.datetime.now().strftime('%Y-%m-%d')
		rng = random.Random(today)
		chars = list(word)
		rng.shuffle(chars)
		row = GRID_HEIGHT // 2  # Middle row
		spacing = GRID_WIDTH // (len(chars) + 1)
		foods = []
		for i, char in enumerate(chars):
			x = spacing * (i + 1)
			foods.append([x, row, char])
		return foods

def main():
	# Track invalid word letters for garbage can
	garbage_letters = []
	global DKGREEN
	# Timer setup
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Snake Game')
	clock = pygame.time.Clock()

	# Landing page loop
	landing = True
	# Track if Time Trial has been played in this session
	if not hasattr(main, "time_trial_played"):
		main.time_trial_played = False
	import datetime
	while landing:
		screen.fill(WHITE)
		# Draw game name 'RATTLE' at the top
		font_rattle = pygame.font.SysFont("Avenir Next", 96, bold=True)
		rattle_surf = font_rattle.render("RATTLE", True, DKGREEN)
		rattle_shadow = font_rattle.render("RATTLE", True, BLACK)
		rattle_x = (WIDTH - rattle_surf.get_width()) // 2
		rattle_y = 40
		screen.blit(rattle_shadow, (rattle_x+4, rattle_y+4))
		screen.blit(rattle_surf, (rattle_x, rattle_y))
		# Draw today's date under RATTLE
		today = datetime.datetime.now().strftime('%B %d, %Y')
		font_date = pygame.font.SysFont("Avenir Next", 36)
		date_surf = font_date.render(today, True, BLACK)
		date_x = (WIDTH - date_surf.get_width()) // 2
		date_y = rattle_y + rattle_surf.get_height() + 10
		screen.blit(date_surf, (date_x, date_y))
		# Draw two smaller sets side by side
		# Set sizes
		logo_size = 80
		title_size = 36
		btn_size = 32
		button_w, button_h = 150, 40
		# Left set
		left_center_x = WIDTH//4
		logo_y = date_y + date_surf.get_height() + 30
		font_logo = pygame.font.SysFont("Avenir Next", logo_size, bold=True)
		logo_surf = font_logo.render("S", True, DKGREEN)
		logo_shadow = font_logo.render("S", True, BLACK)
		logo_x = left_center_x - logo_surf.get_width()//2
		screen.blit(logo_shadow, (logo_x+3, logo_y+3))
		screen.blit(logo_surf, (logo_x, logo_y))
		font_title = pygame.font.SysFont("Avenir Next", title_size, bold=True)
		title_surf = font_title.render("Time Trial", True, BLACK)
		title_x = left_center_x - title_surf.get_width()//2
		title_y = logo_y + logo_surf.get_height() + 10
		screen.blit(title_surf, (title_x, title_y))
		# Add instruction text under Time Trial
		font_instr_left = pygame.font.SysFont("Avenir Next", 20)
		instr_text_left1 = "Quickly find six words"
		instr_text_left2 = "from the scrambled letters"
		instr_surf_left1 = font_instr_left.render(instr_text_left1, True, (80, 80, 80))
		instr_surf_left2 = font_instr_left.render(instr_text_left2, True, (80, 80, 80))
		instr_x_left1 = left_center_x - instr_surf_left1.get_width()//2
		instr_x_left2 = left_center_x - instr_surf_left2.get_width()//2
		instr_y_left1 = title_y + title_surf.get_height() + 8
		instr_y_left2 = instr_y_left1 + instr_surf_left1.get_height() + 2
		screen.blit(instr_surf_left1, (instr_x_left1, instr_y_left1))
		screen.blit(instr_surf_left2, (instr_x_left2, instr_y_left2))
		# Lower the Play button in the left box
		button_x = left_center_x - button_w//2
		button_y = instr_y_left2 + instr_surf_left2.get_height() + 20
		button_rect_left = pygame.Rect(button_x, button_y, button_w, button_h)
		pygame.draw.rect(screen, BLACK, button_rect_left, border_radius=20)
		font_btn = pygame.font.SysFont("Avenir Next", btn_size, bold=True)
		btn_surf = font_btn.render("Play", True, WHITE)
		btn_x = button_x + (button_w - btn_surf.get_width()) // 2
		btn_y = button_y + (button_h - btn_surf.get_height()) // 2
		screen.blit(btn_surf, (btn_x, btn_y))
		# Right set
		right_center_x = 3*WIDTH//4
		logo_x_r = right_center_x - logo_surf.get_width()//2
		screen.blit(logo_shadow, (logo_x_r+3, logo_y+3))
		screen.blit(logo_surf, (logo_x_r, logo_y))
		font_title_right = pygame.font.SysFont("Avenir Next", title_size, bold=True)
		title_surf_right = font_title_right.render("Endless Mode", True, BLACK)
		title_x_r = right_center_x - title_surf_right.get_width()//2
		screen.blit(title_surf_right, (title_x_r, title_y))
		# Add instruction text under Highest Score
		font_instr_right = pygame.font.SysFont("Avenir Next", 20)
		instr_text_right1 = "Find as many words as possible"
		instr_text_right2 = "from the scrambled letters"
		instr_surf_right1 = font_instr_right.render(instr_text_right1, True, (80, 80, 80))
		instr_surf_right2 = font_instr_right.render(instr_text_right2, True, (80, 80, 80))
		instr_x_right1 = right_center_x - instr_surf_right1.get_width()//2
		instr_x_right2 = right_center_x - instr_surf_right2.get_width()//2
		instr_y_right1 = title_y + title_surf_right.get_height() + 8
		instr_y_right2 = instr_y_right1 + instr_surf_right1.get_height() + 2
		screen.blit(instr_surf_right1, (instr_x_right1, instr_y_right1))
		screen.blit(instr_surf_right2, (instr_x_right2, instr_y_right2))
		button_x_r = right_center_x - button_w//2
		button_rect_right = pygame.Rect(button_x_r, button_y, button_w, button_h)
		# Enable Endless Mode button if Time Trial has been played
		if main.time_trial_played:
			pygame.draw.rect(screen, BLACK, button_rect_right, border_radius=20)
			btn_surf = font_btn.render("Play", True, WHITE)
			btn_x_r = button_x_r + (button_w - btn_surf.get_width()) // 2
			btn_y = button_y + (button_h - btn_surf.get_height()) // 2
			screen.blit(btn_surf, (btn_x_r, btn_y))
		else:
			# Gray-out and disable Endless Mode button
			disabled_color = (180, 180, 180)
			pygame.draw.rect(screen, disabled_color, button_rect_right, border_radius=20)
			btn_surf_disabled = font_btn.render("Play", True, (120, 120, 120))
			btn_x_r = button_x_r + (button_w - btn_surf_disabled.get_width()) // 2
			btn_y = button_y + (button_h - btn_surf_disabled.get_height()) // 2
			screen.blit(btn_surf_disabled, (btn_x_r, btn_y))
		# Change cursor and show tooltip for Endless Mode button
		mouse_pos = pygame.mouse.get_pos()
		if button_rect_left.collidepoint(mouse_pos):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		elif button_rect_right.collidepoint(mouse_pos):
			if main.time_trial_played:
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
			else:
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
				# Tooltip for Endless Mode
				tooltip_text = "First play the Time Trial to unlock Endless Mode"
				font_tooltip = pygame.font.SysFont("Avenir Next", 18, bold=True)
				tooltip_surf = font_tooltip.render(tooltip_text, True, (80, 80, 80))
				tooltip_bg = pygame.Surface((tooltip_surf.get_width()+16, tooltip_surf.get_height()+12))
				tooltip_bg.fill((240, 240, 240))
				pygame.draw.rect(tooltip_bg, (180,180,180), tooltip_bg.get_rect(), 2, border_radius=8)
				tooltip_bg.blit(tooltip_surf, (8,6))
				# Position tooltip above the button
				tooltip_x = button_rect_right.centerx - tooltip_bg.get_width()//2
				tooltip_y = button_rect_right.top - tooltip_bg.get_height() - 8
				screen.blit(tooltip_bg, (tooltip_x, tooltip_y))
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
		pygame.display.flip()
		endless_mode = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if button_rect_left.collidepoint(event.pos):
					landing = False
					endless_mode = False
				elif button_rect_right.collidepoint(event.pos) and main.time_trial_played:
					landing = False
					endless_mode = True

	# Game setup after landing page
	start_ticks = pygame.time.get_ticks()
	elapsed_seconds = 0
	# Snake spawns 3 segments deep into the arena, three snake-widths above the bottom border
	start_y = GRID_HEIGHT - 3
	snake = [[3, start_y], [2, start_y], [1, start_y]]
	direction = (1, 0)
	direction_queue = []
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

	found_words = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
	win = False
	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				# Add valid direction changes to the queue, but don't allow reversing
				if event.key == pygame.K_UP and (not direction_queue and direction != (0, 1) or direction_queue and direction_queue[-1] != (0, 1)):
					direction_queue.append((0, -1))
				elif event.key == pygame.K_DOWN and (not direction_queue and direction != (0, -1) or direction_queue and direction_queue[-1] != (0, -1)):
					direction_queue.append((0, 1))
				elif event.key == pygame.K_LEFT and (not direction_queue and direction != (1, 0) or direction_queue and direction_queue[-1] != (1, 0)):
					direction_queue.append((-1, 0))
				elif event.key == pygame.K_RIGHT and (not direction_queue and direction != (-1, 0) or direction_queue and direction_queue[-1] != (-1, 0)):
					direction_queue.append((1, 0))

		# Apply the next direction in the queue, if any
		if direction_queue:
			next_dir = direction_queue.pop(0)
			# Prevent reversing into itself
			if (next_dir[0] != -direction[0] or next_dir[1] != -direction[1]):
				direction = next_dir
		# Move snake
		new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]



		# Portal logic for blue and yellow border
		blue_x = GRID_WIDTH - 1
		blue_y_start = GRID_HEIGHT - 4
		blue_y_end = GRID_HEIGHT - 1
		yellow_x = 0

		# If snake head is on blue border section, teleport next frame
		portal_used = False
		if snake[0][0] == blue_x and blue_y_start <= snake[0][1] < blue_y_end and direction[0] == 1:
			# Teleport after drawing on blue
			new_head[0] = yellow_x
			portal_used = True
			# On portal, submit collected letters to bottom margin
			if collected_letters:
				word = ''.join(collected_letters)
				l = len(word)
				if l in found_words and not found_words[l] and is_valid_word(word):
					found_words[l] = word
				else:
					# Add invalid letters to garbage can
					garbage_letters += list(word)
			if not endless_mode:
				# Win only if all 6 word lengths are filled
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

		# Game over: wall or self (except for left wall emergence via portal)
		# Only allow passing through left wall if just teleported by portal
		if not portal_used:
			collided = (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or new_head in snake)
			if collided:
				if not endless_mode:  # Only for Time Trial
					# Pause for 2000 ms, keeping snake in final-collision state and updating timer
					pause_start = pygame.time.get_ticks()
					while pygame.time.get_ticks() - pause_start < 2000:
						# Draw everything as usual, but do not update snake position
						# --- Begin full redraw ---
						screen.fill(WHITE)
						# Draw 'RATTLE' at the top
						DKGREEN = (0, 100, 0)
						try:
							font_rattle = pygame.font.SysFont("Avenir Next", 96, bold=True)
						except:
							font_rattle = pygame.font.SysFont(None, 96, bold=True)
						rattle_surf = font_rattle.render("RATTLE", True, DKGREEN)
						shadow = font_rattle.render("RATTLE", True, (0,0,0))
						rattle_x = (WIDTH - rattle_surf.get_width()) // 2
						rattle_y = (MARGIN_TOP - rattle_surf.get_height()) // 2
						screen.blit(shadow, (rattle_x+4, rattle_y+4))
						screen.blit(rattle_surf, (rattle_x, rattle_y))
						# Draw arena border
						border_rect = pygame.Rect(MARGIN_LEFT-10, MARGIN_TOP-10, ARENA_WIDTH+20, ARENA_HEIGHT+20)
						border_surf = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
						for i in range(10):
							alpha = 180 - i*15
							color = (30,30,30,alpha)
							pygame.draw.rect(border_surf, color, border_surf.get_rect().inflate(-i*2,-i*2), border_radius=0)
						pygame.draw.rect(border_surf, (10,10,10,255), border_surf.get_rect(), 4, border_radius=0)
						screen.blit(border_surf, (border_rect.x, border_rect.y))
						# Draw blue and yellow border segments
						blue_x = MARGIN_LEFT + ARENA_WIDTH
						blue_y_start = MARGIN_TOP + ARENA_HEIGHT - 4*CELL_SIZE
						blue_height = 3*CELL_SIZE
						pygame.draw.rect(
							screen, BRIGHT_BLUE,
							(blue_x, blue_y_start, 8, blue_height), border_radius=0
						)
						yellow_x = MARGIN_LEFT - 10
						yellow_y_start = blue_y_start
						yellow_height = blue_height
						pygame.draw.rect(
							screen, YELLOW,
							(yellow_x, yellow_y_start, 14, yellow_height), border_radius=0
						)
						# Fill arena background
						arena_rect = pygame.Rect(MARGIN_LEFT, MARGIN_TOP, ARENA_WIDTH, ARENA_HEIGHT)
						arena_surf = pygame.Surface((ARENA_WIDTH, ARENA_HEIGHT))
						for y in range(ARENA_HEIGHT):
							shade = 245 - int(20 * (y / ARENA_HEIGHT))
							pygame.draw.line(arena_surf, (shade, shade, 255), (0, y), (ARENA_WIDTH, y))
						screen.blit(arena_surf, (MARGIN_LEFT, MARGIN_TOP))
						# Draw food
						for food in foods:
							fx, fy, fchar = food
							try:
								font = pygame.font.SysFont("Avenir Next", 18, bold=True)
							except:
								font = pygame.font.SysFont(None, 18, bold=True)
							char_surf = font.render(str(fchar).upper(), True, BLACK)
							x = MARGIN_LEFT + fx*CELL_SIZE + (CELL_SIZE - char_surf.get_width())//2
							y = MARGIN_TOP + fy*CELL_SIZE + (CELL_SIZE - char_surf.get_height())//2
							screen.blit(char_surf, (x, y))
						# Draw snake in its final-collision state
						n = len(snake)
						m = len(collected_letters)
						for i, segment in enumerate(snake):
							color = (80, 200, 120)
							draw_rounded_rect(screen, color, segment, radius=8, shadow=True)
							if i < m:
								try:
									font_letter = pygame.font.SysFont("Avenir Next", 18, bold=True)
								except:
									font_letter = pygame.font.SysFont(None, 18, bold=True)
								letter_surf = font_letter.render(collected_letters[-(i+1)].upper(), True, BLACK)
								seg_x = MARGIN_LEFT + segment[0]*CELL_SIZE
								seg_y = MARGIN_TOP + segment[1]*CELL_SIZE
								x = seg_x + (CELL_SIZE - letter_surf.get_width()) // 2 + 1
								y = seg_y + (CELL_SIZE - letter_surf.get_height()) // 2 + 3
								screen.blit(letter_surf, (x, y))
						# Draw score
						try:
							font = pygame.font.SysFont("Avenir Next", 36, bold=True)
						except:
							font = pygame.font.SysFont(None, 36, bold=True)
						score_surf = font.render(f'Score: {score}', True, (40,40,40))
						shadow = font.render(f'Score: {score}', True, (200,200,200))
						screen.blit(shadow, (14, 14))
						screen.blit(score_surf, (10, 10))
						# Draw word collection boxes
						try:
							font_box = pygame.font.SysFont("Avenir Next", 18, bold=True)
						except:
							font_box = pygame.font.SysFont(None, 18, bold=True)
						word_lengths = [6, 5, 4, 3, 2, 1]
						box_size = CELL_SIZE + 8
						box_radius = 8
						intra_spacing = 4
						list_x = MARGIN_LEFT + ARENA_WIDTH + 40 - 650
						list_y = MARGIN_TOP + 40 + 400
						for length in word_lengths:
							for j in range(length):
								rect = pygame.Rect(list_x + j * (box_size + intra_spacing), list_y, box_size, box_size)
								pygame.draw.rect(screen, (235,235,235), rect, border_radius=box_radius)
								pygame.draw.rect(screen, (40,40,40), rect, 3, border_radius=box_radius)
								if found_words.get(length) and j < len(found_words[length]):
									letter = found_words[length][j].upper()
									surf = font_box.render(letter, True, BLACK)
								else:
									surf = font_box.render('_', True, (120,120,120))
								sx = rect.x + (box_size - surf.get_width())//2
								sy = rect.y + (box_size - surf.get_height())//2 + 2
								screen.blit(surf, (sx, sy))
							list_y += box_size + 12
						# Draw garbage can
						garbage_can_w = int(90 * 1.2)
						garbage_can_h = int(120 * 1.2)
						garbage_can_x = MARGIN_LEFT + (ARENA_WIDTH//2) - (garbage_can_w//2) + 200
						garbage_can_y = list_y + 40 - 250
						brim_w = int(garbage_can_w * 1.7)
						base_w = garbage_can_w - 20
						brim_x = garbage_can_x - (brim_w - garbage_can_w)//2
						base_x = garbage_can_x + 10
						brim_y = garbage_can_y
						base_y = garbage_can_y + garbage_can_h
						points = [
							(brim_x, brim_y),
							(brim_x + brim_w, brim_y),
							(base_x + base_w, base_y),
							(base_x, base_y)
						]
						pygame.draw.polygon(screen, (180,150,90), points)
						pygame.draw.polygon(screen, (100,80,40), points, 4)
						for i in range(8):
							y = brim_y + int((base_y - brim_y) * i / 7)
							x1 = brim_x + int((brim_w - base_w) * (base_y - y) / (base_y - brim_y) / 2)
							x2 = brim_x + brim_w - int((brim_w - base_w) * (base_y - y) / (base_y - brim_y) / 2)
							pygame.draw.line(screen, (140,110,60), (x1, y), (x2, y), 2)
						for i in range(7):
							frac = i / 6
							x = brim_x + int(frac * brim_w)
							y1 = brim_y
							y2 = base_y
							pygame.draw.line(screen, (140,110,60), (x, y1), (base_x + int(frac * base_w), y2), 2)
						try:
							font_garbage = pygame.font.SysFont("Avenir Next", 32, bold=True)
						except:
							font_garbage = pygame.font.SysFont(None, 32, bold=True)
						for i, letter in enumerate(garbage_letters):
							seed = hash((letter, i))
							rng = random.Random(seed)
							frac_x = rng.uniform(0.15, 0.85)
							frac_y = rng.uniform(0.1, 0.85)
							x = brim_x + frac_x * brim_w - 16
							y = brim_y + frac_y * (base_y - brim_y) - 16
							angle = rng.randint(-35, 35)
							surf = font_garbage.render(letter, True, (80,80,80))
							surf = pygame.transform.rotate(surf, angle)
							screen.blit(surf, (int(x), int(y)))
						# Draw timer (clock keeps running)
						elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
						minutes = elapsed_seconds // 60
						seconds = elapsed_seconds % 60
						time_str = f"{minutes:02}:{seconds:02}"
						font_timer = pygame.font.SysFont("Avenir Next", 32, bold=False)
						timer_surf = font_timer.render(time_str, True, BLACK)
						timer_x = MARGIN_LEFT + ARENA_WIDTH + 80
						timer_y = MARGIN_TOP + ARENA_HEIGHT - 4*CELL_SIZE + 3*CELL_SIZE//2 - timer_surf.get_height() - 390
						screen.blit(timer_surf, (timer_x, timer_y))
						pygame.display.flip()
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								pygame.quit()
								sys.exit()
						clock.tick(FPS)
					# Respawn snake and food as if starting a new game, but retain submitted words, timer, and score
					start_y = GRID_HEIGHT - 3
					snake = [[3, start_y], [2, start_y], [1, start_y]]
					direction = (1, 0)
					direction_queue = []
					foods = [f.copy() for f in initial_foods]
					collected_letters = []
					pending_portal_respawn = False
					# Continue running (clock and score are retained)
					continue
				else:
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
		# Draw arena border as a thick rectangle with gradient, no rounded corners
		border_rect = pygame.Rect(MARGIN_LEFT-10, MARGIN_TOP-10, ARENA_WIDTH+20, ARENA_HEIGHT+20)
		border_surf = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
		for i in range(10):
			alpha = 180 - i*15
			color = (30,30,30,alpha)
			pygame.draw.rect(border_surf, color, border_surf.get_rect().inflate(-i*2,-i*2), border_radius=0)
		# Draw a solid dark border on top
		pygame.draw.rect(border_surf, (10,10,10,255), border_surf.get_rect(), 4, border_radius=0)
		screen.blit(border_surf, (border_rect.x, border_rect.y))
		# Draw bright blue segment on right border (rounded)
		blue_x = MARGIN_LEFT + ARENA_WIDTH
		blue_y_start = MARGIN_TOP + ARENA_HEIGHT - 4*CELL_SIZE
		blue_height = 3*CELL_SIZE
		pygame.draw.rect(
			screen, BRIGHT_BLUE,
			(blue_x, blue_y_start, 8, blue_height), border_radius=0
		)
		# Draw timer in right margin, moved up by 200 pixels
		if not win:
			elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
		minutes = elapsed_seconds // 60
		seconds = elapsed_seconds % 60
		time_str = f"{minutes:02}:{seconds:02}"
		font_timer = pygame.font.SysFont("Avenir Next", 32, bold=False)
		timer_surf = font_timer.render(time_str, True, BLACK)
		timer_x = blue_x + 80
		timer_y = blue_y_start + blue_height//2 - timer_surf.get_height() - 390
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
			(yellow_x, yellow_y_start, 14, yellow_height), border_radius=0
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
			color = (80, 200, 120)
			draw_rounded_rect(screen, color, segment, radius=8, shadow=True)
			if i < m:
				try:
					font_letter = pygame.font.SysFont("Avenir Next", 18, bold=True)
				except:
					font_letter = pygame.font.SysFont(None, 18, bold=True)
				letter_surf = font_letter.render(collected_letters[-(i+1)].upper(), True, BLACK)
				# Center the letter in the segment
				seg_x = MARGIN_LEFT + segment[0]*CELL_SIZE
				seg_y = MARGIN_TOP + segment[1]*CELL_SIZE
				x = seg_x + (CELL_SIZE - letter_surf.get_width()) // 2 + 1
				y = seg_y + (CELL_SIZE - letter_surf.get_height()) // 2 + 3
				screen.blit(letter_surf, (x, y))
		# Draw food as black letters, standing alone
		for food in foods:
			fx, fy, fchar = food
			try:
				font = pygame.font.SysFont("Avenir Next", 18, bold=True)
			except:
				font = pygame.font.SysFont(None, 18, bold=True)
			char_surf = font.render(str(fchar).upper(), True, BLACK)
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

		# Draw word collection boxes grouped by word length
		try:
			font_box = pygame.font.SysFont("Avenir Next", 18, bold=True)
		except:
			font_box = pygame.font.SysFont(None, 18, bold=True)
		word_lengths = [6, 5, 4, 3, 2, 1]
		box_size = CELL_SIZE + 8  # Only a little bigger than snake segment
		box_radius = 8
		group_spacing = 32
		intra_spacing = 4
		start_y = MARGIN_TOP + ARENA_HEIGHT + 80
		# Display submitted word list vertically, one word per line, from 6 to 1 letters
		list_x = MARGIN_LEFT + ARENA_WIDTH + 40 - 650
		list_y = MARGIN_TOP + 40 + 400
		for length in word_lengths:
			for j in range(length):
				rect = pygame.Rect(list_x + j * (box_size + intra_spacing), list_y, box_size, box_size)
				pygame.draw.rect(screen, (235,235,235), rect, border_radius=box_radius)
				pygame.draw.rect(screen, (40,40,40), rect, 3, border_radius=box_radius)
				if found_words.get(length) and j < len(found_words[length]):
					letter = found_words[length][j].upper()
					surf = font_box.render(letter, True, BLACK)
				else:
					surf = font_box.render('_', True, (120,120,120))
				sx = rect.x + (box_size - surf.get_width())//2
				sy = rect.y + (box_size - surf.get_height())//2 + 2
				screen.blit(surf, (sx, sy))
			list_y += box_size + 12

		# Draw garbage can underneath word boxes
		# Make garbage can 20% bigger overall
		garbage_can_w = int(90 * 1.2)
		garbage_can_h = int(120 * 1.2)
		garbage_can_x = MARGIN_LEFT + (ARENA_WIDTH//2) - (garbage_can_w//2) + 200
		# Place garbage can below the last word list row
		garbage_can_y = list_y + 40 - 250  # Move up 100 pixels
		# Draw can body as a trapezoid (brim much wider than base)
		brim_w = int(garbage_can_w * 1.7)  # much wider at top
		base_w = garbage_can_w - 20        # same width at bottom
		brim_x = garbage_can_x - (brim_w - garbage_can_w)//2
		base_x = garbage_can_x + 10
		brim_y = garbage_can_y
		base_y = garbage_can_y + garbage_can_h
		points = [
			(brim_x, brim_y),
			(brim_x + brim_w, brim_y),
			(base_x + base_w, base_y),
			(base_x, base_y)
		]
		pygame.draw.polygon(screen, (180,150,90), points)
		pygame.draw.polygon(screen, (100,80,40), points, 4)
		# Wicker-style pattern: draw horizontal and vertical lines
		for i in range(8):
			y = brim_y + int((base_y - brim_y) * i / 7)
			x1 = brim_x + int((brim_w - base_w) * (base_y - y) / (base_y - brim_y) / 2)
			x2 = brim_x + brim_w - int((brim_w - base_w) * (base_y - y) / (base_y - brim_y) / 2)
			pygame.draw.line(screen, (140,110,60), (x1, y), (x2, y), 2)
		for i in range(7):
			frac = i / 6
			x = brim_x + int(frac * brim_w)
			y1 = brim_y
			y2 = base_y
			pygame.draw.line(screen, (140,110,60), (x, y1), (base_x + int(frac * base_w), y2), 2)
		# Draw overlapping, lopsided, rotated invalid letters inside can
		try:
			font_garbage = pygame.font.SysFont("Avenir Next", 32, bold=True)
		except:
			font_garbage = pygame.font.SysFont(None, 32, bold=True)
		for i, letter in enumerate(garbage_letters):
			# Use a fixed seed per letter so position/rotation is static
			seed = hash((letter, i))
			rng = random.Random(seed)
			frac_x = rng.uniform(0.15, 0.85)
			frac_y = rng.uniform(0.1, 0.85)
			x = brim_x + frac_x * brim_w - 16
			y = brim_y + frac_y * (base_y - brim_y) - 16
			angle = rng.randint(-35, 35)
			surf = font_garbage.render(letter, True, (80,80,80))
			surf = pygame.transform.rotate(surf, angle)
			screen.blit(surf, (int(x), int(y)))

		# Draw leaderboard directly underneath the underscores
		# Leaderboard rendering (commented out)
		# try:
		# 	font_leader = pygame.font.SysFont("Avenir Next", 20, bold=True)
		# except:
		# 	font_leader = pygame.font.SysFont(None, 20, bold=True)
		# leaderboard_lines = [
		# 	"LEADERBOARD",
		# 	"benja       0:25",
		# 	"WCasp    1:44",
		# 	"DBrandt  1:48"
		# ]
		# leader_y = start_y + 170  # Move down another 20 pixels
		# for line in leaderboard_lines:
		# 	surf = font_leader.render(line, True, BLACK)
		# 	surf_x = (WIDTH - surf.get_width()) // 2
		# 	screen.blit(surf, (surf_x, leader_y))
		# 	leader_y += surf.get_height() + 5

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
		# Mark Time Trial as played
		main.time_trial_played = True
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
		# Mark Time Trial as played
		main.time_trial_played = True
	pygame.display.flip()
	pygame.time.wait(2000)
	# Instead of quitting, return to splash screen
	main()

if __name__ == "__main__":
	main()
