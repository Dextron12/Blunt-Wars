import pygame

width, height = 1024, 640

window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

menu = pygame.Surface((int(width-20),int(height-30)))

# initiate | load objects into list or dict
loadedObj = []
for obj in range(17):
    loadedObj.append(obj)

maxX, maxY = 0, 0
dataColumn = 0

maxX = int(((menu.get_size()[0]//2)//32)*0.7)
maxY = int(((menu.get_size()[1]-16)//32)*0.7)
dataColumn = len(loadedObj) // maxX
dataRow = 0
updateRow = True

if dataColumn > maxY:
    scrollH = menu.get_size()[1] - 20
    scrollSpeed = int(maxY*0.95)*2
    scrollY = 0
    scroll = True
else:
    scroll = False
    scrollSpeed, scrollY = 0, 0


while True:
    window.fill((0, 0, 255))
    menu.fill((49, 79, 79))   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            menu = pygame.Surface((int(event.w-20), int(height-30)))
            maxX = int(((menu.get_size()[0]//2)//32)*0.7)
            maxY = int(((menu.get_size()[1]-16)//32)*0.7)
            dataColumn = len(loadedObj) // maxX
        if event.type == pygame.MOUSEBUTTONDOWN:
            if scroll == True:
                if event.button == 4:
                    if scrollY != 0:
                        scrollY -= scrollSpeed
                if event.button == 5:
                    if scrollY+76 < scrollH:
                        scrollY += scrollSpeed


    if scroll == True:
        pygame.draw.rect(menu, (128, 128, 128), (0, 10, 16, scrollH)) # Scroll Bg
        pygame.draw.rect(menu, (0, 0, 0), (1, 12+scrollY, 14, 60)) # Scroll bar

    pygame.draw.line(menu, (255,255,255), (menu.get_size()[0]//2, 0), (menu.get_size()[0]//2, menu.get_size()[1]), 2)

    if len(loadedObj) % maxX != 0: # whatever this returns is the number of items that dont fill a whole row
        if updateRow == True:
            dataColumn += 1
            dataRow =  maxX - len(loadedObj) % maxX
            updateRow = False
    for x in range(maxX):
        for y in range(dataColumn):
            if y == dataColumn-1 and len(loadedObj) % maxX != 0:
                pygame.draw.rect(window, (255, 0, 0), (16+(48*(x-dataRow)), 16+(48*y)-scrollY, 32, 32))
            else:
                pygame.draw.rect(window, (255, 0, 0), (16+(48*x), 16+(48*y)-scrollY, 32, 32))
    #window.blit(menu, (10, 10))        
    pygame.display.flip()

    scrollSpeed = (dataColumn//4)*0.15