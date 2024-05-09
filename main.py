import pygame
import random

pygame.init()
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]

def reset():
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()
    return snake_pixel.copy()

def is_out_of_bounds():
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 \
        or snake_pixel.left < 0 or snake_pixel.right > square_width

def show_message(message):
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(square_width // 2, square_width // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02}:{seconds:02}"

snake_pixel = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1

target = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
target.center = generate_starting_position()

start_time = pygame.time.get_ticks()  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    if is_out_of_bounds():
        show_message("Try again! Press any key to restart")
        pygame.time.wait(1000)  
        snake_length = 1
        target.center = generate_starting_position()
        snake_pixel.center = generate_starting_position()
        snake = [snake_pixel.copy()]
        start_time = pygame.time.get_ticks()  
        pygame.event.clear()  
        pygame.event.wait()   
        continue

    if snake_pixel.center == target.center:
        target.center = generate_starting_position()
        snake_length += 1
        snake.append(snake_pixel.copy())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake_direction = (0, - pixel_width)
    if keys[pygame.K_s]:
        snake_direction = (0, pixel_width)
    if keys[pygame.K_a]:
        snake_direction = (- pixel_width, 0)
    if keys[pygame.K_d]:
        snake_direction = (pixel_width, 0)

    for snake_part in snake:
        pygame.draw.rect(screen, "green", snake_part)

    pygame.draw.rect(screen, "red", target)

    snake_pixel.move_ip(snake_direction)
    snake.append(snake_pixel.copy())
    snake = snake[-snake_length:]

    elapsed_time = pygame.time.get_ticks() - start_time  
    elapsed_time_seconds = elapsed_time // 1000  
    time_text = font.render("Time: " + format_time(elapsed_time_seconds), True, (255, 255, 255))
    screen.blit(time_text, (10, 10))  

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
