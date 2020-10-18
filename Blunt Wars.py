import pygame, os

class Greeter(object):
    Width, Height = 1024, 768
    window = pygame.display.set_mode((Width,Height), pygame.RESIZABLE)
    pygame.display.set_caption("Blunt Wars")


    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    self.Width, self.Height = event.w, event.h
                    #print(event.w, event.h)
                    #print(self.Width)
                    world.update_map()
                    self.window = pygame.display.set_mode((self.Width, self.Height), pygame.RESIZABLE)
            
            self.window.fill((0,0,255))

            world.draw_map()

            pygame.display.flip()

greeter = Greeter()

# OBJECT CLASSES

class World(object):

    def __init__(self):
        self.Textures, self.TextureData = {}, {}
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        self.load_texture()
        self.update_map()

    def load_texture(self):
        for file in os.listdir(self.BASE_DIR + '/Resources/Maps/'):
            print(file)
            if '.png' in file:
                loaded_texture = pygame.image.load(self.BASE_DIR + '/Resources/Maps/%s' % (file))
                loaded_texture = pygame.transform.scale(loaded_texture, (greeter.Width//4,greeter.Height//4))
                self.Textures[file.strip('.png')] = loaded_texture

    def draw_map(self):
        for texture in self.Textures:
            greeter.window.blit(self.Textures[texture], (self.TextureData[texture]))

    def scale_texture(self, texture):
        width,height = texture.get_size()
        pygame.transform.scale(texture, (int(greeter.Width/4),int(greeter.Height/4)))
        return texture

    def update_map(self):
        for texture in self.Textures:
            width,height = self.Textures[texture].get_size()
            # SET OFFSET FOR EACH MAP FROM SCALING COORDS 
            if texture == 'Australia':
                self.TextureData[texture] = ((greeter.Width-width), greeter.Height-height)
            else:
                self.TextureData[texture] = (0,0)

class GUI(object):

    def __init__(self):
        self.fileList = []

    def imageBtn(self, x, y, image, action):
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        w,h = image.get_size()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1:
                #editor.imageBtnClick[action] = True # IN FUNCTION EVENT DO FUNCTION THEN CLOSE true STATEMENT AFTER FUNCTION
                return True
        greeter.window.blit(image, (x,y))

    def LibViewer(self, fileDir, fileSearch): # MUST CALL IN A LOOP
        for file in os.listdir(fileDir):
            self.fileList = file
        pygame.draw.rect(greeter.window, (47,79,79), (60,60,greeter.Width-120,greeter.Height-120)) # DRAW BACK DROP
        pygame.draw.rect(greeter.window, (169,169,169), (62,88,greeter.Width-124,greeter.Height-150)) # EXPLOERER PANE
        pygame.draw.rect(greeter.window, (169,169,169), (greeter.Width-86,62,24,24)) # EXIT BUTTON
        # DRAW CROSS ON EXIT BUTTON
        pygame.draw.line(greeter.window, (0,0,0), (greeter.Width-86,62), (greeter.Width-64,82), 2)



class mapEditor(object):

    def __init__(self):
        self.edit = True
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        self.saveBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/save.png')
        self.loadBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/load.png')
        self.addBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/add.png')
        self.removeBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/remove.png')
        self.imgBtnClick = {'saveBtn': False, 'loadBtn': False, 'addBtn': False, 'removeBtn': False}

    def draw(self):
        pygame.draw.rect(greeter.window, (211,211,211), (0,0,greeter.Width,52))
        #greeter.window.blit(self.saveBtn, (5,8))
        gui.imageBtn(5,8, self.saveBtn, 'saveBtn')
        gui.imageBtn(42,8, self.loadBtn, "loadBtn")
        pygame.draw.line(greeter.window, (47,79,79), (76,0), (76,52), 2)
        if gui.imageBtn(80,1, self.addBtn, 'addBtn'):
            self.imgBtnClick['addBtn'] = True
        gui.imageBtn(140, 1, self.removeBtn, 'removeBtn')

    def editor(self):
        while self.edit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    greeter.Width, greeter.Height = event.w, event.h
                    greeter.window = pygame.display.set_mode((greeter.Width, greeter.Height), pygame.RESIZABLE)
            greeter.window.fill((0,0,255))

            self.draw()

            if self.imgBtnClick['addBtn']:
                gui.LibViewer(self.BASE_DIR + '/Resources/Maps/', 'png')

            pygame.display.flip()


                

world = World()
gui = GUI()
editor = mapEditor()

editor.editor()