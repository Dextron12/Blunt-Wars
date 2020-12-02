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
            if event.button == 4 and scroll > 0:
                print("Scroll up: %s" % ((height-40)//len(objList)))
            if event.button == 5 and scroll < height-40:
                print("scroll down: %s" % ((height-20)//len(objList)))
                
        window.fill((0,0,255))

    pygame.draw.rect(window, (255,255,255), (width-30,20,20,height-40))
    pygame.draw.rect(window, (0,0,0), (width-25, scroll+21, 10, 30))

    """for obj in objList:
        #margin 16 | box size 32
        pygame.draw.rect(window, (255,0,0), (16+(46*obj), scroll, 32, 32))"""

    # FIND FORMULA TO SEE HOW MANY RECTS CAN FIT ON X SCREEN
    # FIND FORMULA TO SEE HOW MANY RECTS CAN FIT ON Y SCREEN
    # RUN ROW AND COLUMN NUMBERS INOT FOR LOOP BELOW 
    # THIS CREATES A DYNAMICALLY RANGED GRID THAT RELIES ON A LIST OR DICT TO DRAW THE ITEMS

    # X FORMULA
    TotalRow = int((width//32)*0.65) # SUCCESS
    # Y FORMULA
    column = int((height//32)*0.65)

    row = TotalRow-(column//len(objList))-(0.55*TotalRow))

    while row != TotalRow:
        row += 1

    for x in range(9):
        for y in range(8):
            pygame.draw.rect(window, (255,0,0), (16+(48*x), 16+(48*y), 32, 32))


    pygame.display.flip()