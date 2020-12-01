import pygame

width,height = 1024, 748
window = pygame.display.set_mode((width,height), pygame.RESIZABLE)

objList = []
scroll = 0

# GENERATE OBJECT LIST FOR DRAWING CUBES
for num in range(75):
    objList.append(num)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            winodw = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = event.w, event.h
        if event.type == pygame.MOUSEBUTTONDOWN:
            print()
    window.fill((0,0,255))

    pygame.draw.rect(window, (255,255,255), (width-30,20,20,height-40))
    pygame.draw.rect(window, (0,0,0), (width-25, scroll+21, 10, 30))

    for obj in objList:
        #margin 16 | box size 32
        pygame.draw.rect(window, (255,0,0), (16+(46*obj), scroll, 32, 32))


    pygame.display.flip()