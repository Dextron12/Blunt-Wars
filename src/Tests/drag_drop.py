import pygame


width, height = 1024, 764
window = pygame.display.set_mode((width,height), pygame.RESIZABLE)

# SURFACES DICT HOLDS PSO OF ALL ADDED SURFACES. uSE KEY FROM ACTUAL MAP DICT FOR KEYS
surfacePos = {}


surfacePos['Australia'] = (64,64)
surfacePos['Canada'] = (704,571)

selected = None
click = 0
#oldMouse = 0

while True:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = event.w, event.h
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = 1
        if event.type == pygame.MOUSEBUTTONUP:
            click = 0
            selected = None
    window.fill((0,0,255))

    for surface in surfacePos:
        pygame.draw.rect(window, (255,0,0), (surfacePos[surface][0], surfacePos[surface][1], 64, 64))

        if surfacePos[surface][0]+64 > mouse[0] > surfacePos[surface][0] and surfacePos[surface][1]+64 > mouse[1] > surfacePos[surface][1]:
            if click == 1:
                selected = surface
    
    if selected != None:
        #if oldMouse != mouse:
        surfacePos[selected] = mouse[0]-32, mouse[1]-32

    pygame.display.flip()
    #oldMouse = mouse