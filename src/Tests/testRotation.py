import pygame, random

pygame.init()

width, height = 1024, 684
window = pygame.display.set_mode((width, height))

def Text(fg, font, size, msg):
    font = pygame.font.SysFont(font, size)
    text = font.render(msg, True, fg)
    return text

randomAngle = random.randint(15, 45)
scale = False
while True:
    text = Text((149, 0, 0), "Tahoma", 16, "Too Blunt!")
    text = pygame.transform.rotate(text, -randomAngle)
    pygame.time.set_timer(pygame.USEREVENT, 800)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.USEREVENT:
            print("event call")
            if scale == False:
                scale = True
            else: scale = False
        
    window.fill((0,0,255))

    if scale == True:
        text = Text((149, 0, 0), "Tahoma", 8, "Too Blunt!")
    else:
        text = Text((149, 0, 0), "Tahoma", 160, "Too Blunt!")
    text = pygame.transform.rotate(text, -randomAngle)

    window.blit(text, (width//2, 80))

    pygame.display.flip()