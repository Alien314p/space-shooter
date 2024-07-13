import pygame 

pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT=1280,720
running=True

display_surface=pygame.display.set_mode(WINDOW_WIDTH,WINDOW_HEIGHT)

while running:
    for event in pygame.event.get():
        if event==pygame.QUIT:
            running=False


pygame.quit()


