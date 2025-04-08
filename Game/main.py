import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40
PLAYER_SPEED = 5

FLOOR_COLOR = (168, 168, 168)
ROOM_WALL_COLORS = {
    1: (146, 77, 191),
    2: (200, 109, 53),
}
DEFAULT_WALL_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 255, 0)
DOOR_COLOR = (100, 100, 100)
KEY_COLOR = (255, 255, 0)
SAFE_COLOR = (80, 80, 80)
TROPHY_COLOR = (0, 128, 255)

UP, DOWN, LEFT, RIGHT = 'up', 'down', 'left', 'right'

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
menu_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 36)

title_text = menu_font.render("The Adventure", True, (0, 255, 0))
start_text = small_font.render("START - A", True, (255, 255, 255))
exit_text = small_font.render("EXIT - B", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

player = pygame.Rect(100, 100, TILE_SIZE, TILE_SIZE)
room_transitions = {
    1: {RIGHT: 2},
    2: {LEFT: 1, RIGHT: 4, UP: 3, DOWN: 5},
    3: {DOWN: 2},
    4: {LEFT: 2},
    5: {UP: 2},
}
current_room = 1
wall_thickness = 20
door_size = 100

key = pygame.Rect(370, 200, TILE_SIZE, TILE_SIZE)
has_key = False
safe_rect = pygame.Rect(350, 400, 100, 60)
safe_open = False
trophy = pygame.Rect(375, 410, TILE_SIZE, TILE_SIZE)
trophy_visible = False
you_won = False

def get_door_rect(direction):
    if direction == UP:
        return pygame.Rect(SCREEN_WIDTH // 2 - door_size // 2, 0, door_size, wall_thickness)
    elif direction == DOWN:
        return pygame.Rect(SCREEN_WIDTH // 2 - door_size // 2, SCREEN_HEIGHT - wall_thickness, door_size, wall_thickness)
    elif direction == LEFT:
        return pygame.Rect(0, SCREEN_HEIGHT // 2 - door_size // 2, wall_thickness, door_size)
    elif direction == RIGHT:
        return pygame.Rect(SCREEN_WIDTH - wall_thickness, SCREEN_HEIGHT // 2 - door_size // 2, wall_thickness, door_size)

def draw_room_and_get_walls(room_id):
    walls = []
    directions = [UP, DOWN, LEFT, RIGHT]
    exits = room_transitions.get(room_id, {})
    wall_color = ROOM_WALL_COLORS.get(room_id, DEFAULT_WALL_COLOR)

    for dir in directions:
        if dir not in exits:
            if dir == UP:
                rect = pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness)
            elif dir == DOWN:
                rect = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness)
            elif dir == LEFT:
                rect = pygame.Rect(0, 0, wall_thickness, SCREEN_HEIGHT)
            elif dir == RIGHT:
                rect = pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT)
            pygame.draw.rect(screen, wall_color, rect)
            walls.append(rect)
        else:
            if dir == UP:
                left = pygame.Rect(0, 0, SCREEN_WIDTH // 2 - door_size // 2, wall_thickness)
                right = pygame.Rect(SCREEN_WIDTH // 2 + door_size // 2, 0, SCREEN_WIDTH // 2 - door_size // 2, wall_thickness)
            elif dir == DOWN:
                left = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH // 2 - door_size // 2, wall_thickness)
                right = pygame.Rect(SCREEN_WIDTH // 2 + door_size // 2, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH // 2 - door_size // 2, wall_thickness)
            elif dir == LEFT:
                left = pygame.Rect(0, 0, wall_thickness, SCREEN_HEIGHT // 2 - door_size // 2)
                right = pygame.Rect(0, SCREEN_HEIGHT // 2 + door_size // 2, wall_thickness, SCREEN_HEIGHT // 2 - door_size // 2)
            elif dir == RIGHT:
                left = pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT // 2 - door_size // 2)
                right = pygame.Rect(SCREEN_WIDTH - wall_thickness, SCREEN_HEIGHT // 2 + door_size // 2, wall_thickness, SCREEN_HEIGHT // 2 - door_size // 2)
            pygame.draw.rect(screen, wall_color, left)
            pygame.draw.rect(screen, wall_color, right)
            walls.extend([left, right])
            pygame.draw.rect(screen, DOOR_COLOR, get_door_rect(dir))
    return walls

def handle_room_transition():
    global current_room
    for direction in room_transitions.get(current_room, {}):
        door_rect = get_door_rect(direction)
        if player.colliderect(door_rect):
            current_room = room_transitions[current_room][direction]
            if direction == UP:
                player.bottom = SCREEN_HEIGHT - wall_thickness - 1
            elif direction == DOWN:
                player.top = wall_thickness + 1
            elif direction == LEFT:
                player.right = SCREEN_WIDTH - wall_thickness - 1
            elif direction == RIGHT:
                player.left = wall_thickness + 1

def handle_wall_collision(walls):
    for wall in walls:
        if player.colliderect(wall):
            if player.right > wall.left and player.left < wall.left:
                player.right = wall.left
            if player.left < wall.right and player.right > wall.right:
                player.left = wall.right
            if player.bottom > wall.top and player.top < wall.top:
                player.bottom = wall.top
            if player.top < wall.bottom and player.bottom > wall.bottom:
                player.top = wall.bottom

def draw():
    screen.fill(FLOOR_COLOR)
    walls = draw_room_and_get_walls(current_room)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    if current_room == 1:
        text = font.render("START", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    elif current_room == 3 and not has_key:
        pygame.draw.rect(screen, KEY_COLOR, key)
    elif current_room == 5:
        pygame.draw.rect(screen, SAFE_COLOR, safe_rect)
        if safe_open:
            pygame.draw.rect(screen, TROPHY_COLOR, trophy)

    return walls

def show_menu():
    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return
                elif event.key == pygame.K_b:
                    pygame.quit()
                    sys.exit()

show_menu()

running = True
while running:
    if you_won:
        screen.fill((0, 0, 0))
        text = font.render("YOU WON!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and current_room == 3 and player.colliderect(key):
                has_key = True
            elif event.key == pygame.K_b and current_room == 5 and player.colliderect(safe_rect) and has_key:
                safe_open = True
                has_key = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]: player.x += PLAYER_SPEED
    if keys[pygame.K_UP]: player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]: player.y += PLAYER_SPEED

    wall_rects = draw()
    handle_wall_collision(wall_rects)
    handle_room_transition()

    if current_room == 5 and safe_open and player.colliderect(trophy):
        you_won = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
