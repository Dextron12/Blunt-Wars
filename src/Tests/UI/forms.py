import pygame

def text(fc, font, size, msg):
    font = pygame.font.SysFont('Tahoma', size)
    text = font.render(msg, True, fc)
    return text

class EventHandler:

    def __init__(self, w, h):
        pygame.init()

        self.event_list = pygame.event.get()
        self.width, self.height = w, h
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)


        self.pressedKey = []
        self.logEvents = False

    def update(self):
        self.event_list = pygame.event.get()

    def handle(self):
        for event in self.event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.w, event.h
                self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if self.logEvents:
                    if event.key != pygame.K_BACKSPACE or pygame.K_CAPSLOCK or pygame.K_ESCAPE: # BLACKLISTED KEYS FOR RAW TEXT
                        self.pressedKey = list(event.unicode)
                    if event.key == pygame.K_BACKSPACE:
                        self.pressedKey = ['backspace']
        self.update()

    def search(self, eventName): # SEARCH FOR AN EVENT IN THE EVENT QUEUE
        for event in self.event_list:
            if event.type == eventName:
                return True
            else:
                return False



class Form(object):

    def __init__(self, x, y, w, h, message, timerEvent, eventHandler, mode=True, encryption=False):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.encryption = encryption
        self.textOut = []
        self.mode = mode # mode = true |light mode, mode = false | dark mode
        self.activeForm = False
        self.msg = message
        self.activeTimer = False # BOOL TO REPRESEANT IF THE FORM IS IN AN ACTIVE STATE OR NOT
        pygame.time.set_timer(timerEvent, 800)

        self.event = eventHandler # event handler class from external call
        self.timer = timerEvent   # TIMER SWITCH

    def draw(self, surface):
        if self.mode == True:
            pygame.draw.rect(surface, (255,255,255), (self.x,self.y,self.w,self.h)) # BACKGROUND
            pygame.draw.rect(surface, (0,0,0), (self.x,self.y,self.w,self.h), 4) # BORDER

            #DRAW INPUT TO FORM
            if self.encryption == False:
                surface.blit(text((48, 79, 79), 'Arial', self.h//2, ''.join(self.textOut)), (self.x+10, self.y+2))
            else: # ENCRYPT AND DISPLAY MESSAGE
                surface.blit(text((47, 79, 79), 'Arial', self.h//2, "*" * len(''.join(self.textOut))), (self.x+10, self.y+2))

            if self.activeForm == False and self.textOut == []: # DRAW INACTIVE MESSAGE
                surface.blit(text((48, 79, 79), 'Arial', self.h//2, self.msg), (self.x+10, self.y+2))
            

            if self.activeTimer == True:
                pygame.draw.line(surface, (47, 79,79), (self.x+10, self.y+5), (self.x+10, self.y+20), 2) # DRAWS FLASHING CURSOR | MULTIPLY TEXT FEILD BY CHAR LENGTH TO ADD SPACING TO MOVE THE CURSOR ACROSS THE FORM

        elif self.mode == False:
            pygame.draw.rect(surface, (49, 79, 79), (self.x,self.y,self.w,self.h)) # BACKGROUND
            pygame.draw.rect(surface, (37, 49, 49), (self.x,self.y,self.w, self.h), 4) #BORDER

        #DRAW INPUT TO FORM
        if self.encryption == False:
            surface.blit(text((240, 255, 255), 'Arial', self.h//2, ''.join(self.textOut)), (self.x+10, self.y+2))
        else:
            surface.blit(text((240, 255, 255), 'Arial', self.h//2, "*" * len(''.join(self.textOut))), (self.x+10, self.y+2))

        if self.activeForm == False and self.textOut == []:
            surface.blit(text((240,255,255), 'Arial', self.h//2, self.msg), (self.x+10, self.y+2))

        if self.activeTimer == True:
            pygame.draw.line(surface, (240,255,255), (self.x+10, self.y+5), (self.x+10, self.y+20), 2)

        # DO LOGIC
        
        # CHECKS IF FORM ACTIVE
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y: # FORM ACTIVATOR
            if click[0] == 1:
                self.activeForm = True
                self.event.logEvents = True
        else:
            if click[0] == 1:
                self.activeForm = False
                self.event.logEvents = False

        if self.event.logEvents == True and self.event.pressedKey != []:
            if self.event.pressedKey[0] != 'backspace':
                self.textOut.append(self.event.pressedKey[0])
                self.event.pressedKey = []
            elif self.event.pressedKey[0] == 'backspace':
                if self.textOut != []:
                    del self.textOut[-1]
                    self.event.pressedKey = []


        if self.activeForm == True: # CURSOR SWITCH
            if self.event.search(self.timer):
                if self.activeTimer == False:
                    self.activeTimer = True
                elif self.activeTimer == True:
                    self.activeTimer = False


handler = EventHandler(1024, 678)


textForm = Form(10,(handler.height//2)-30, handler.width-20, 30, 'Username', pygame.USEREVENT, handler, False)

while True:
    handler.handle()
    handler.window.fill((0,0,255))

    textForm.draw(handler.window)

    pygame.display.flip()