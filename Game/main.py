import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Adventure")

font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 36)

title_text = font.render("The Adventure", True, (0, 255, 0))
start_text = small_font.render("START - A", True, (255, 255, 255))
exit_text = small_font.render("EXIT - B", True, (255, 255, 255))

title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
start_rect = start_text.get_rect(center=(width // 2, height // 2 + 50))
exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 100))

background_color = (0, 0, 0)
show_text = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                background_color = (255, 255, 255)
                show_text = False
                # here game code
            elif event.key == pygame.K_b:
                running = False

    screen.fill(background_color)

    if show_text:
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(exit_text, exit_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
