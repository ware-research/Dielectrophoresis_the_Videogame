import pygame
import random
import numpy as np

# Game dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
BLUE = (0,100,200)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)

# Circle properties
PLAYER_RADIUS = 10
ELECTRODE_RADIUS = 40
ENEMY_RADIUS = 15

# Circle movement speed
PLAYER_SPEED = 5
ENEMY_SPEED = 1
enemies = []
power_up_num = 0
power_ups = []
TEMPERATURE = 20

score = 0
voltage = 0
frequency = 0

def apply_powerup():
    power_id = random.randint(1,5)
    global TEMPERATURE
    global enemies

    if power_id == 1:# Heat
        display_text("HEATING!", RED)
        TEMPERATURE += 7
        return TEMPERATURE
    
    if power_id == 2:# Cool
        display_text("COOLING!", GREEN)
        if TEMPERATURE > 0:
            TEMPERATURE -= 7
            return TEMPERATURE
        
    if power_id == 3:# Push Off
        display_text("PUSH OFF!", RED)
        distances = []
        for enemy in enemies:
            enemy_x, enemy_y = enemy[0], enemy[1]
            enemy_voltage = enemy[4]
            nearest_electrode_distance = float('inf')
            for electrode in electrodes:
                electrode_x, electrode_y = electrode[0], electrode[1]
                distance = ((enemy_x - electrode_x) ** 2 + (enemy_y - electrode_y) ** 2) ** 0.5
                if distance < nearest_electrode_distance:
                    nearest_electrode_distance = distance
            distances.append((nearest_electrode_distance, enemy_voltage))

        # Move the enemy circles towards the nearest electrode if player voltage is greater
        for i, enemy in enumerate(enemies):
            nearest_electrode_distance, enemy_voltage = distances[i]
            if voltage > enemy_voltage:
                enemy_x, enemy_y = enemy[0], enemy[1]
                for electrode in electrodes:
                    electrode_x, electrode_y = electrode[0], electrode[1]
                    distance = ((enemy_x - electrode_x) ** 2 + (enemy_y - electrode_y) ** 2) ** 0.5
                    if distance == nearest_electrode_distance and nearest_electrode_distance != 0:
                        dx = (electrode_x - enemy_x) / nearest_electrode_distance
                        dy = (electrode_y - enemy_y) / nearest_electrode_distance
                        if distance <= 200 and np.abs(frequency-enemy[2])>np.abs(frequency-enemy[3]): #and np.abs(frequency-enemy[2])<50000:
                            enemy[0] -= dx * 70
                            enemy[1] -= dy * 70
                        break

    if power_id == 4: #Macrophage
        display_text("MACROPHAGE!", GREEN)
        global num_enemies
        global score
        n = 0
        if len(enemies) > score:
            for enemy in enemies:
                    if n < 10:
                        enemies.remove(enemy)
                        n += 1
            num_enemies -= 10
        return num_enemies
    
    if power_id == 5: #random player speed
        display_text("SPEED CHANGE!", RED)
        global PLAYER_SPEED
        PLAYER_SPEED = random.randint(1,10)
        return PLAYER_SPEED
        
def display_text(text, color):
    
    display_duration = 1000
    font = pygame.font.Font(None, 36)
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time < display_duration:
            surface = font.render(text, True, color)
            screen.blit(surface, (WIDTH//2, HEIGHT//2))
        else:
            # Text display duration has elapsed, exit the loop
            running = False

        pygame.display.update()

# Initialize Pygame
pygame.init()
# Initialize Pygame
pygame.init()

# Set up the screen for the title screen
title_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dielectrophoresis, the video game - Title Screen")

# Title screen loop
title_screen_running = True
while title_screen_running:
    title_screen.fill(BLUE)

    # Draw title and controls
    font_title = pygame.font.Font(None, 48)
    title_text = font_title.render("DIELECTROPHORESIS: The Videogame", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    font_controls = pygame.font.Font(None, 24)
    controls_text = font_controls.render("Controls:", True, WHITE)
    controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))

    w_text = font_controls.render("W - Move Up", True, WHITE)
    s_text = font_controls.render("S - Move Down", True, WHITE)
    a_text = font_controls.render("A - Move Left", True, WHITE)
    d_text = font_controls.render("D - Move Right", True, WHITE)
    up_text = font_controls.render("Up Arrow - Increase Voltage", True, WHITE)
    down_text = font_controls.render("Down Arrow - Decrease Voltage", True, WHITE)
    right_text = font_controls.render("Right Arrow - Increase Frequency", True, WHITE)
    left_text = font_controls.render("Left Arrow - Decrease Frequency", True, WHITE)

    # Draw the controls
    title_screen.blit(title_text, title_rect)
    title_screen.blit(controls_text, controls_rect)
    title_screen.blit(w_text, (WIDTH // 2 - 150, HEIGHT // 2))
    title_screen.blit(a_text, (WIDTH // 2 - 150, HEIGHT // 2 + 30))
    title_screen.blit(s_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))
    title_screen.blit(d_text, (WIDTH // 2 - 150, HEIGHT // 2 + 90))
    title_screen.blit(up_text, (WIDTH // 2 + 50, HEIGHT // 2))
    title_screen.blit(down_text, (WIDTH // 2 + 50, HEIGHT // 2 + 30))
    title_screen.blit(right_text, (WIDTH // 2 + 50, HEIGHT // 2 + 60))
    title_screen.blit(left_text, (WIDTH // 2 + 50, HEIGHT // 2 + 90))

    # Draw start button
    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 150, 100, 40)
    pygame.draw.rect(title_screen, GREEN, start_button)
    start_font = pygame.font.Font(None, 36)
    start_text = start_font.render("START", True, BLACK)
    start_rect = start_text.get_rect(center=start_button.center)
    title_screen.blit(start_text, start_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            title_screen_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_x, mouse_y):
                title_screen_running = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dielectrophoresis, the video game")
clock = pygame.time.Clock()

# Create the inlet and outlet ports
inlet_port = pygame.Rect(0, HEIGHT // 2, 30, 30)
outlet_port = pygame.Rect(WIDTH - 30, HEIGHT // 2, 30, 30)

# Create the player circle
player_pos = [15, HEIGHT // 2 + 15]

# Create the electrode circles
num_electrodes = 7
electrodes = []
for _ in range(num_electrodes):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    electrodes.append([x, y])

# Create the enemy circles
num_enemies = 15
enemies = []
for _ in range(num_enemies):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    e_pos_freq = random.randint(0, 99999)
    e_neg_freq = random.randint(0, 99999)
    e_voltage = random.randint(1, 19)
    enemies.append([x, y, e_pos_freq, e_neg_freq, e_voltage])

game_over = False

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the player circle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player_pos[1] += PLAYER_SPEED
    if keys[pygame.K_a]:
        player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player_pos[0] += PLAYER_SPEED
    if keys[pygame.K_UP] and voltage < 20:
        voltage += 0.1
    if keys[pygame.K_DOWN] and voltage > 0:
        voltage -= 0.1
    if keys[pygame.K_LEFT] and frequency > 0:
        frequency -= 1000
    if keys[pygame.K_RIGHT] and frequency < 100000:
        frequency += 1000

    # Teleport the player if they reach the outlet port
    if player_pos[0] > (WIDTH - 30) and player_pos[1] > (HEIGHT // 2) - 30 and player_pos[1] < (HEIGHT // 2) + 30:
        player_pos[0] = -PLAYER_RADIUS

        voltage = 0
        frequency = 0

        score += 1
        print(f"SCORE: {score}")

        num_enemies += 10
        enemies = []
        for _ in range(num_enemies):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            e_pos_freq = random.randint(0, 99999)
            e_neg_freq = random.randint(0, 99999)
            e_voltage = random.randint(1, 19)
            enemies.append([x, y, e_pos_freq, e_neg_freq, e_voltage])

        power_up_num += 1
        power_ups = []
        for _ in range(power_up_num):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            e_pos_freq = random.randint(0, 99999)
            e_neg_freq = random.randint(0, 99999)
            e_voltage = random.randint(1, 19)
            power_ups.append([x, y, e_pos_freq, e_neg_freq, e_voltage])

        num_electrodes += 1
        

        electrodes = []
        for _ in range(num_electrodes):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            electrodes.append([x, y])

    # Keep the player circle within the game window
    if player_pos[0] < 5:
        player_pos[0] = 5
    if player_pos[0] > WIDTH - 5:
        player_pos[0] = WIDTH - 5
    if player_pos[1] < 5:
        player_pos[1] = 5
    if player_pos[1] > HEIGHT - 5:
        player_pos[1] = HEIGHT - 5

    # Move the enemy circles randomly
    for enemy in enemies + power_ups:
        direction = random.choice([-1, 1])
        enemy[0] += direction * ENEMY_SPEED * TEMPERATURE /20
        direction = random.choice([-1, 1])
        enemy[1] += direction * ENEMY_SPEED * TEMPERATURE /20

        # Keep the enemy circles within the game window
        if enemy[0] < 45:
            enemy[0] = 45
        if enemy[0] > WIDTH - 45:
            enemy[0] = WIDTH - 45

        if enemy[1] < 0:
            enemy[1] = 0
        if enemy[1] > HEIGHT:
            enemy[1] = HEIGHT

    # Check for collisions with the electrode circles
    for electrode in electrodes:
        distance = ((player_pos[0] - electrode[0]) ** 2 + (player_pos[1] - electrode[1]) ** 2) ** 0.5
        if distance < ELECTRODE_RADIUS:
            # Apply a force to pull the player towards the electrode
            player_pos[0] += int((electrode[0] - player_pos[0]) / 100)
            player_pos[1] += int((electrode[1] - player_pos[1]) / 100)

    #Continuation:

    # Check for collisions with the enemy circles
    for enemy in enemies:
        distance = ((player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2) ** 0.5
        if distance < enemy[4] + 9:
            game_over = True

    for power_up in power_ups:
        distance = ((player_pos[0] - power_up[0]) ** 2 + (player_pos[1] - power_up[1]) ** 2) ** 0.5
        if distance < 20:
            apply_powerup()
            power_ups.remove(power_up)
            score += 1

    # Calculate the distances between each enemy and electrode
    distances = []
    for enemy in enemies + power_ups:
        enemy_x, enemy_y = enemy[0], enemy[1]
        enemy_voltage = enemy[4]
        nearest_electrode_distance = float('inf')
        for electrode in electrodes:
            electrode_x, electrode_y = electrode[0], electrode[1]
            distance = ((enemy_x - electrode_x) ** 2 + (enemy_y - electrode_y) ** 2) ** 0.5
            if distance < nearest_electrode_distance:
                nearest_electrode_distance = distance
        distances.append((nearest_electrode_distance, enemy_voltage))

    # Move the enemy circles towards the nearest electrode if player voltage is greater
    for i, enemy in enumerate(enemies + power_ups):
        nearest_electrode_distance, enemy_voltage = distances[i]
        if voltage > enemy_voltage:
            enemy_x, enemy_y = enemy[0], enemy[1]
            for electrode in electrodes:
                electrode_x, electrode_y = electrode[0], electrode[1]
                distance = ((enemy_x - electrode_x) ** 2 + (enemy_y - electrode_y) ** 2) ** 0.5
                if distance == nearest_electrode_distance and nearest_electrode_distance != 0:
                    dx = (electrode_x - enemy_x) / nearest_electrode_distance
                    dy = (electrode_y - enemy_y) / nearest_electrode_distance
                    if distance >= 50 and np.abs(frequency-enemy[2])>np.abs(frequency-enemy[3]): #and np.abs(frequency-enemy[2])<50000:
                        enemy[0] += dx/20 * voltage
                        enemy[1] += dy/20 * voltage
                    if distance >= 50 and np.abs(frequency-enemy[2])<np.abs(frequency-enemy[3]): #and np.abs(frequency-enemy[3])<50000:
                        enemy[0] -= dx/20 * voltage
                        enemy[1] -= dy/20 * voltage
                    break

    # Clear the screen
    screen.fill(BLUE)

    # Draw the electrode circles
    for electrode in electrodes:
        pygame.draw.circle(screen, GREY, electrode, ELECTRODE_RADIUS)

    # Draw the enemy circles
    for enemy in enemies:
        enemy_color = (int(enemy[2] / 100000 * 255), 0, 0)  # Proportional to pos_freq
        enemy_outline_color = (int(enemy[3] / 100000 * 255), 0, 0)  # Proportional to neg_freq
        inner_rad = ENEMY_RADIUS / enemy[4]
        if inner_rad <= 5:
            inner_rad = 5
        pygame.draw.circle(screen, enemy_color, enemy[:2], int(inner_rad))
        pygame.draw.circle(screen, enemy_outline_color, enemy[:2], int(ENEMY_RADIUS), 2)
    
    for power_up in power_ups:
        color = (0,200,100)
        rad = 10
        pygame.draw.circle(screen, color, power_up[:2], rad)

    # Draw the inlet and outlet ports
    pygame.draw.rect(screen, BLACK, inlet_port)
    pygame.draw.rect(screen, BLACK, outlet_port)

    # Draw the player circle
    pygame.draw.circle(screen, GREEN, player_pos, PLAYER_RADIUS)

    # Display score, frequency, and voltage
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    frequency_text = font.render(f"Frequency: {frequency}", True, WHITE)
    voltage_text = font.render(f"Voltage: {voltage}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))
    screen.blit(frequency_text, (WIDTH - 150, 40))
    screen.blit(voltage_text, (WIDTH - 150, 70))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Game over screen loop
game_over_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dielectrophoresis, the video game - Game Over")

game_over_running = True
while game_over_running:
    game_over_screen.fill(RED)

    # Display "GAME OVER" and high score
    font_game_over = pygame.font.Font(None, 48)
    game_over_text = font_game_over.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    font_high_score = pygame.font.Font(None, 36)
    high_score_text = font_high_score.render(f"High Score: {score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Draw the "QUIT" button
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 100, 40)
    pygame.draw.rect(game_over_screen, BLUE, quit_button)
    quit_font = pygame.font.Font(None, 24)
    quit_text = quit_font.render("QUIT", True, WHITE)
    quit_rect = quit_text.get_rect(center=quit_button.center)
    game_over_screen.blit(quit_text, quit_rect)

    # Draw the "RESTART" button
    restart_button = pygame.Rect(WIDTH // 2, HEIGHT // 2 + 50, 100, 40)
    pygame.draw.rect(game_over_screen, GREEN, restart_button)
    restart_font = pygame.font.Font(None, 24)
    restart_text = restart_font.render("RESTART", True, WHITE)
    restart_rect = restart_text.get_rect(center=restart_button.center)
    game_over_screen.blit(restart_text, restart_rect)

    # Draw "GAME OVER" and high score texts
    game_over_screen.blit(game_over_text, game_over_rect)
    game_over_screen.blit(high_score_text, high_score_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game_over_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the "QUIT" button is clicked
            if quit_button.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                game_over_running = False

            # Check if the "RESTART" button is clicked
            if restart_button.collidepoint(mouse_x, mouse_y):
                # Reset game state
                score = 0
                voltage = 0
                frequency = 0
                num_enemies = 15
                enemies = []
                for _ in range(num_enemies):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    e_pos_freq = random.randint(0, 99999)
                    e_neg_freq = random.randint(0, 99999)
                    e_voltage = random.randint(1, 19)
                    enemies.append([x, y, e_pos_freq, e_neg_freq, e_voltage])

                game_over_running = False  # Exit the game over screen loop
                title_screen_running = True  # Return to the title page


# Quit the game
pygame.quit()