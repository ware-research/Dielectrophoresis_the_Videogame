import pygame
import random
import numpy as np
import json
from cryptography.fernet import Fernet

'''
---------------- DEV NOTES -----------------
Delete "scores.json" before compiling
Include "bacteria.

TO DO: 
- shorten power up text pause
- more power ups

Changelog (Since V2.0):
- added "ghost mode" powerup
- added "add power ups" power
'''

#Load the player image
player_image = pygame.image.load("bacteria.png")

key = b'3uU5-dVsUnh9UK99Jukly9HVgjF7vO9Q8Wk08BqyYag='

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

# Encrypt and decrypt functions
def encrypt(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

def decrypt(cipher_text, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text

# Save and load scores
def save_scores(scores):
    global key
    encrypted_data = encrypt(json.dumps(scores), key)
    with open("scores.json", "wb") as file:
        file.write(encrypted_data)

def load_scores():
    global key
    try:
        with open("scores.json", "rb") as file:
            encrypted_data = file.read()
            decrypted_data = decrypt(encrypted_data, key)
            return json.loads(decrypted_data)
    except FileNotFoundError:
        default_scores = [{"score": 0} for _ in range(5)]
        save_scores(default_scores)
        return default_scores

def display_text(text, color, screen):
    
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
            running = False

        pygame.display.update()

def apply_powerup(screen):
    power_id = random.randint(1,7)
    global temperature, enemies

    if power_id == 1:# Heat
        display_text("HEATING!", RED, screen)
        temperature += 7
        return temperature
    
    if power_id == 2:# Cool
        display_text("COOLING!", GREEN, screen)
        if temperature > 0:
            temperature -= 7
            return temperature
        
    if power_id == 3:#Push off
        display_text("Push Off!", RED, screen)
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
        display_text("MACROPHAGE!", GREEN, screen)
        global num_enemies, score
        n = 0
        if len(enemies) > score:
            for enemy in enemies:
                    if n < 10:
                        enemies.remove(enemy)
                        n += 1
            num_enemies -= 10
        return num_enemies
    
    if power_id == 5: #random player speed
        display_text("SPEED CHANGE!", RED, screen)
        global PLAYER_SPEED
        PLAYER_SPEED = random.randint(1,10)
        return PLAYER_SPEED
    
    if power_id == 6: #ghost mode
        global ghost_mode_active
        ghost_mode_active = not ghost_mode_active
        if ghost_mode_active == True:
            display_text("Ghost Mode Activated!", RED, screen)
        if ghost_mode_active == False:
            display_text("Ghost Mode Off!", GREEN, screen)

    if power_id == 7: #bonus power ups
        global power_up_num
        bonus = random.randint(1,5)
        power_up_num += bonus
        display_text(f"+ {bonus} power ups!", GREEN, screen)
    
    if power_id == 8: #RUN!
        global run_mode_active
        run_mode_active = not run_mode_active
        if run_mode_active == True:
            display_text("RUN!!!", RED, screen)
        if run_mode_active == False:
            display_text("run mode off", GREEN, screen)

    
def initialize_game():
    global ghost_mode_active, PLAYER_SPEED, ENEMY_SPEED, enemies, power_up_num, power_ups, temperature, score, voltage, temperature, frequency, run_mode_active

    ghost_mode_active = False
    run_mode_active = False

    PLAYER_SPEED = 5
    ENEMY_SPEED = 1
    enemies = []
    power_up_num = 0
    power_ups = []
    temperature = 20

    score = 0
    voltage = 10
    frequency = 10000
    
def title_screen_loop():
    global WIDTH, HEIGHT, BLUE, WHITE, GREEN
    title_screen_running = True
    title_screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_x, mouse_y):
                    title_screen_running = False

def game_loop():
    global game_over, player_image, electrodes, WIDTH, HEIGHT, BLUE, WHITE, GREEN, PLAYER_SPEED, voltage, frequency, score, num_enemies, enemies, power_up_num, power_ups, temperature
    
    game_over = False

    initialize_game()
    
    # Create the player circle
    player_pos = [15, HEIGHT // 2 + 15]

    # Create the inlet and outlet ports
    inlet_port = pygame.Rect(0, HEIGHT // 2, 30, 30)
    outlet_port = pygame.Rect(WIDTH - 30, HEIGHT // 2, 30, 30)

    # Create the electrode circles
    num_electrodes = 7
    electrodes = []
    for _ in range(num_electrodes):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        electrodes.append([x, y])
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dielectrophoresis, the video game")
    clock = pygame.time.Clock()

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
        if keys[pygame.K_8]:
            num_enemies = 0
            power_up_num = 100

        # Teleport the player if they reach the outlet port
        if player_pos[0] > (WIDTH - 30) and player_pos[1] > (HEIGHT // 2) - 30 and player_pos[1] < (HEIGHT // 2) + 30:
            player_pos[0] = -PLAYER_RADIUS

            voltage = 10
            frequency = 10000

            score += 1

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
            if power_up_num > 101:
                power_up_num = 15

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
            enemy[0] += direction * ENEMY_SPEED * temperature /20
            direction = random.choice([-1, 1])
            enemy[1] += direction * ENEMY_SPEED * temperature /20

            # Keep the enemy circles within the game window
            if enemy[0] < 0:
                enemy[0] = 0
            if enemy[0] > WIDTH - 0:
                enemy[0] = WIDTH - 0

            if enemy[1] < 0:
                enemy[1] = 0
            if enemy[1] > HEIGHT:
                enemy[1] = HEIGHT

            #Safety Buffer
            midline = HEIGHT/2
            if enemy[0] < 150 and enemy[1] < midline + 100 and enemy[1] > midline - 100 and player_pos[0] < 45:
                enemy[0] = WIDTH
                enemy[1] = midline

        # Check for collisions with the electrode circles
        for electrode in electrodes:
            distance = ((player_pos[0] - electrode[0]) ** 2 + (player_pos[1] - electrode[1]) ** 2) ** 0.5
            if distance < ELECTRODE_RADIUS:
                player_pos[0] += int((electrode[0] - player_pos[0]) / 100)
                player_pos[1] += int((electrode[1] - player_pos[1]) / 100)

        # Check for collisions with the enemy circles
        for enemy in enemies:
            distance = ((player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2) ** 0.5
            if distance < enemy[4] + 9:
                game_over = True

        for power_up in power_ups:
            distance = ((player_pos[0] - power_up[0]) ** 2 + (player_pos[1] - power_up[1]) ** 2) ** 0.5
            if distance < 20:
                apply_powerup(screen)
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
        '''
                    add this
                                       if np.abs(frequency-enemy[2])<np.abs(frequency-enemy[3]): #and np.abs(frequency-enemy[3])<50000:
                        distance = (((enemy_x - player_pos[0]) ** 2) + ((enemy_y - player_pos[1]) ** 2)) ** 0.5
                        
                        dx = (player_pos[0] - enemy_x) / distance
                        dy = (player_pos[1] - enemy_y) / distance

                        enemy[0] += dx/20 * voltage * score * TEMPERATURE/20
                        enemy[1] += dy/20 * voltage * score * TEMPERATURE/20
                    break
                end add this
        '''             

        # Clear the screen
        screen.fill(BLUE)

        # Draw the electrode circles
        for electrode in electrodes:
            pygame.draw.circle(screen, GREY, electrode, ELECTRODE_RADIUS)

        # Draw the enemy circles
        for enemy in enemies:
            if ghost_mode_active == False:
                enemy_color = (int(enemy[2] / 100000 * 255), 0, 0)  # Proportional to pos_freq
                enemy_outline_color = (int(enemy[3] / 100000 * 255), 0, 0)  # Proportional to neg_freq
            elif ghost_mode_active == True:
                enemy_color = (0, 110, 190)  # Proportional to pos_freq
                enemy_outline_color = (0, 105, 195)  # Proportional to neg_freq
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

        # Draw the player image
        screen.blit(player_image, (int(player_pos[0] - (3*PLAYER_RADIUS)), int(player_pos[1] - (3*PLAYER_RADIUS))))


        # Display score, frequency, and voltage
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {score}", True, WHITE)
        frequency_text = font.render(f"Frequency: {int(frequency)}", True, WHITE)
        voltage_text = font.render(f"Voltage: {int(voltage)}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))
        screen.blit(frequency_text, (WIDTH - 150, 40))
        screen.blit(voltage_text, (WIDTH - 150, 70))

        pygame.display.flip()
        clock.tick(60)  

def game_over_loop():
    global WIDTH, HEIGHT, RED, WHITE, BLUE, GREEN, game_over_running, game_over_screen, score
    
    game_over_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dielectrophoresis, the video game - Game Over")
    
    game_over_running = True
    while game_over_running:
        game_over_screen.fill(RED)

        font_game_over = pygame.font.Font(None, 48)
        game_over_text = font_game_over.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        font_high_score = pygame.font.Font(None, 36)

        all_scores = sorted(load_scores(), key=lambda x: x["score"], reverse=True)
        
        font_game_over = pygame.font.Font(None, 48)
        game_over_text = font_game_over.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        font_score = pygame.font.Font(None, 36)
        current_score_text = font_score.render(f"Score: {score}", True, WHITE)
        current_score_rect = current_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))

        font_high_score = pygame.font.Font(None, 36)
        highest_score = max(all_scores, key=lambda x: x["score"])["score"]
        high_score_text = font_high_score.render(f"High Score: {highest_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 100, 40)
        pygame.draw.rect(game_over_screen, BLUE, quit_button)
        quit_font = pygame.font.Font(None, 24)
        quit_text = quit_font.render("QUIT", True, WHITE)
        quit_rect = quit_text.get_rect(center=quit_button.center)
        game_over_screen.blit(quit_text, quit_rect)

        restart_button = pygame.Rect(WIDTH // 2, HEIGHT // 2 + 100, 100, 40)
        pygame.draw.rect(game_over_screen, GREEN, restart_button)
        restart_font = pygame.font.Font(None, 24)
        restart_text = restart_font.render("RESTART", True, WHITE)
        restart_rect = restart_text.get_rect(center=restart_button.center)
        game_over_screen.blit(restart_text, restart_rect)

        game_over_screen.blit(game_over_text, game_over_rect)
        game_over_screen.blit(current_score_text, current_score_rect)
        game_over_screen.blit(high_score_text, high_score_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                all_scores.append({"score": score})
                save_scores(all_scores)
                game_over_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if quit_button.collidepoint(mouse_x, mouse_y):
                    game_over_running = False
                    pygame.quit()
                    return True

                if restart_button.collidepoint(mouse_x, mouse_y):
                    all_scores.append({"score": score})
                    save_scores(all_scores)

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

                    game_over_running = False 

        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 100, 40)
        pygame.draw.rect(game_over_screen, BLUE, quit_button)
        quit_font = pygame.font.Font(None, 24)
        quit_text = quit_font.render("QUIT", True, WHITE)
        quit_rect = quit_text.get_rect(center=quit_button.center)
        game_over_screen.blit(quit_text, quit_rect)

        restart_button = pygame.Rect(WIDTH // 2, HEIGHT // 2 + 100, 100, 40)
        pygame.draw.rect(game_over_screen, GREEN, restart_button)
        restart_font = pygame.font.Font(None, 24)
        restart_text = restart_font.render("RESTART", True, WHITE)
        restart_rect = restart_text.get_rect(center=restart_button.center)
        game_over_screen.blit(restart_text, restart_rect)

def main():
    pygame.init()

    num_electrodes = 7
    electrodes = []
    for _ in range(num_electrodes):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        electrodes.append([x, y])

    num_enemies = 15
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        e_pos_freq = random.randint(0, 99999)
        e_neg_freq = random.randint(0, 99999)
        e_voltage = random.randint(1, 19)
        enemies.append([x, y, e_pos_freq, e_neg_freq, e_voltage])

    while True:
        title_screen_loop()
        game_loop()
        quit = game_over_loop()
        if quit == True:
            break

if __name__ == "__main__":
    main()

