import pygame

pygame.init()

width,height = 1024, 684
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

def text(fc, font, size, msg):
    font = pygame.font.SysFont('Tahoma', size)
    text = font.render(msg, True, fc)
    return text




class Notify(object):

    def __init__(self, w, h, title, msg, mode='notify'):
        self.width, self.height = w, h
        self.popupSurface = pygame.Surface((self.width//3, 160))
        self. mode = mode
        self.title = title
        self.msg = msg
        self.xOffest = self.width  - (self.width//3)*2
        self.yOffset = (self.height//2)-60
        self.close = False

    def draw(self):
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        self.popupSurface.fill((0,255,255))
        pygame.draw.rect(self.popupSurface, (0,139, 139), (0,0,self.width//3,30)) # TOP BAR

        pygame.draw.line(self.popupSurface, (0,0,0), ((self.width//3)-9.5, 7.5), ((self.width//3)-16, 23.5))
        pygame.draw.line(self.popupSurface, (0,0,0), ((self.width//3)-16, 7.5), ((self.width//3)-9.5, 23.5)) ######

        pygame.draw.rect(self.popupSurface, (128,128,128), ((self.popupSurface.get_size()[0]//2)-30, self.popupSurface.get_size()[1]-45, 80, 30)) # OK BUTTON bg
        pygame.draw.rect(self.popupSurface, (149, 149, 149), ((self.popupSurface.get_size()[0]//2)-28, self.popupSurface.get_size()[1]-44, 77, 28)) # OK BUTTON fg
        self.popupSurface.blit(text((0,0,0), 'Tahoma', 11, 'Ok'), ((self.popupSurface.get_size()[0]//2), self.popupSurface.get_size()[1]-35))

        self.popupSurface.blit(text((0,0,0), 'Tahoma', 14, self.title), (5, 5)) # display title
        self.popupSurface.blit(text((0,0,0), 'Tahoma', 12, self.msg), ((self.popupSurface.get_rect()[0]//2)+120, 60)) # display message


        if (self.xOffest+(self.popupSurface.get_size()[0]//2)-30)+80 > mouse[0] > self.xOffest+(self.popupSurface.get_size()[0]//2)-30: # ok btn
            if (self.yOffset+self.popupSurface.get_size()[1]-45)+30 > mouse[1] > self.yOffset+self.popupSurface.get_size()[1]-45:
                if click[0] == 1:
                    self.close = True

        if self.popupSurface.get_size()[0] > mouse[0] > self.popupSurface.get_size()[0]-32 and self.yOffset+30 > mouse[1] > self.yOffset:
            print("over x btn")
        
        

        window.blit(self.popupSurface, (self.width//3, (self.height//2)-60))
        
                


noTouch = Notify(width, height, "Error", "Don't Touch Me Keys!")

while True:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.VIDEORESIZE)
            width, height = event.w, event.h
            noTouch = Notify(width, height, "Error", "Don't Touch Me Keys!")
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    window.fill((41,49,49))

    if noTouch.close == False:
        noTouch.draw()
    pygame.display.flip()
        