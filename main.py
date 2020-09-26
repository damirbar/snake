import pygame

# Initialize the game window
pygame.init()
dis = pygame.display.set_mode((800, 600))
pygame.display.update()
pygame.display.set_caption("Snake Game")

# Colors
class Colors:
    red   = (255,0,0)
    green = (0,255,0)
    blue  = (0,0,255)
    white = (255,255,255)
    black = (0,0,0)

x_loc, y_loc = 300, 300
x_modify, y_modify = 0, 0

clock = pygame.time.Clock()

keep_playing = True
while keep_playing:
    for evt in pygame.event.get():
        print(evt)

        # If the user attempts to close the game window
        if evt.type == pygame.QUIT:
            keep_playing = False

        # If the user pressed a key
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_LEFT:
                x_modify = -10
                y_modify = 0
            if evt.key == pygame.K_RIGHT:
                x_modify = 10
                y_modify = 0
            if evt.key == pygame.K_UP:
                x_modify = 0
                y_modify = -10
            if evt.key == pygame.K_DOWN:
                x_modify = 0
                y_modify = 10


    x_loc += x_modify
    y_loc += y_modify
    dis.fill(Colors.black)
    pygame.draw.rect(dis, Colors.green, [x_loc, y_loc, 10, 10])
    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()

