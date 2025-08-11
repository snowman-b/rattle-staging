def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = [[GRID_WIDTH//2, GRID_HEIGHT//2], [GRID_WIDTH//2-1, GRID_HEIGHT//2], [GRID_WIDTH//2-2, GRID_HEIGHT//2]]
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
            if new_head == food:
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
        screen.fill(BLACK)
        for segment in snake:
            draw_rect(screen, GREEN, segment)
        for food in foods:
            draw_rect(screen, RED, food)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    # Game over screen
    font = pygame.font.SysFont(None, 48)
    msg = font.render(f'Game Over! Score: {score}', True, WHITE)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()
