import pygame


pygame.time.set_timer(pygame.USEREVENT+1, 1000)

def display_cursor(e):
    print(e.type)
    if e.type == pygame.USEREVENT+1:
        print("This should print when USERVENT is in the event queue")

class EventHandler:

    def __init__(self, w, h):
        pygame.init()

        self.event_list = pygame.event.get()
        self.width, self.height = w, h
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)


        self.pressed_keys = None
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
                    self.pressedKey = event.unicode
        self.update()

    def search(self, eventName): # SEARCH FOR AN EVENT IN THE EVENT QUEUE
        for event in self.event_list:
            if event.type == eventName:
                return True
            else:
                return False

handler = EventHandler(1024, 648)

while True:
    handler.handle()
    handler.window.fill((0,0,255))
    
    if handler.search(pygame.USEREVENT+1):
        print("found event")
    pygame.display.flip()



