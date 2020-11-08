import pygame, os
from ast import literal_eval

pygame.init()

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
            if '.png' in file:
                loaded_texture = pygame.image.load(self.BASE_DIR + '/Resources/Maps/%s' % (file))
                loaded_texture = pygame.transform.scale(loaded_texture, (16,16))
                self.Textures[file.strip('.png')] = loaded_texture

    def draw_map(self):
        for texture in self.Textures:
            greeter.window.blit(self.Textures[texture], (self.TextureData[texture]))

    """def scale_texture(self, texture):
        #width,height = texture.get_size()
        pygame.transform.scale(texture, (int(greeter.Width/4),int(greeter.Height/4)))
        return texture"""

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
        self.viewLib = False
        self.scroll = [0,0]
        self.png = pygame.image.load(world.BASE_DIR + "/Resources/Icons/pictureIco.png")
        self.png = pygame.transform.scale(self.png, (86,82))

    def text(self, fc, msg, size, font, x, y, surf):
        font = pygame.font.SysFont(font, size)
        text = font.render(msg, True, fc)
        textRect = text.get_rect()
        textRect.center = (x,y)
        surf.blit(text, textRect)

    def imageBtn(self, x, y, image, action):
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        w,h = image.get_size()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1:
                #editor.imageBtnClick[action] = True # IN FUNCTION EVENT DO FUNCTION THEN CLOSE true STATEMENT AFTER FUNCTION
                return True
        greeter.window.blit(image, (x,y))

    def scrollBar(self, x, y, w, h):
        pygame.draw.rect(greeter.window, (105,105,105), (x,y,w,h))
        pygame.draw.rect(greeter.window, (47, 79,79), (x+3, y+self.scroll[1], w-6, 85)) # SCROLL BAR

    def LibViewer(self, fileDir, fileSearch): # MUST CALL IN A LOOP
        if self.viewLib:
            searchDir = []
            searchDir = os.listdir()
            for selectedFile in searchDir:
                if selectedFile not in self.fileList:
                    self.fileList.append(selectedFile)
            pygame.draw.rect(greeter.window, (47,79,79), (60,60,greeter.Width-120,greeter.Height-120)) # DRAW BACK DROP
            pygame.draw.rect(greeter.window, (169,169,169), (62,88,greeter.Width-124,greeter.Height-150)) # EXPLOERER PANE
            pygame.draw.rect(greeter.window, (169,169,169), (greeter.Width-86,62,24,24)) # EXIT BUTTON
            # DRAW CROSS ON EXIT BUTTON
            pygame.draw.line(greeter.window, (0,0,0), (greeter.Width-86,62), (greeter.Width-64,82), 2)
            pygame.draw.line(greeter.window, (0,0,0), (greeter.Width-62,62), (greeter.Width-86,82), 2)
            # DRAW SCROLL BAR
            self.scrollBar(greeter.Width-78, 90, 15, greeter.Height-153)

            mouse,click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
            if greeter.Width-62 > mouse[0] > greeter.Width-86 and 86 > mouse[1] > 62:
                if click[0] == 1:
                    self.viewLib = False


            for file in range(len(self.fileList)):
                if self.fileList[file][-4:] ==  ".png":
                    print(self.fileList, file)
                    self.fileList[file] = self.fileList[file].strip('.png')
                if file == 0:
                    greeter.window.blit(self.png, (65,90+self.scroll[1]))
                    self.text((0,0,0), self.fileList[file], 16, 'Arial', 74, 172+self.scroll[1], greeter.window)
                    print(self.fileList[file])
                else:
                    greeter.window.blit(self.png, (65+(98*file), 90+self.scroll[1]))

class WeaponEditor(object):

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        self.Weapons = {}
        self.countryWeapons = {} # country: [weapons]

        #name = [weaponObject, weaponType, usage, xp, definition]

        # LOAD DEFENSE AND OFFENCE WEAPONS THEN LABEL AND SORT THEM
        for weaponObj in os.listdir(self.BASE_DIR + "//Resources//Objects//Weapons//Defence//"):
            try:
                weaponObjName = weaponObj.strip('.png')
                weaponObj = pygame.image.load(self.BASE_DIR + "//Resources//Objects//Weapons//Defence//%s.png" % (weaponObjName))
                self.Weapons[weaponObjName] = [weaponObj, 'defense', None, None, None]
            except:
                print("%s isn't a PNG file. Ignoring!" % (weaponObj))
        for weaponObj in os.listdir(self.BASE_DIR + "//Resources//Objects//Weapons//Offence//"):
            try:
                weaponObjName = weaponObj.strip(".png")
                weaponObj = pygame.image.load(self.BASE_DIR + "//Reources//Objects//Weapons//Defence//%s.png" % (weaponObjName))
                self.Weapons[weaponObjName] = [weaponObj, 'offence', None, None, None]
            except:
                print("%s isn't a PNG file. Ignoring!" % (weaponObj))
        if os.path.isfile(self.BASE_DIR + "//Resources//Objects//Weapons//Defence//defense.dat"):
            with open(self.BASE_DIR + "//Resources//Objects//Weapons//Defence//defense.dat", 'r') as f:
                data = f.read()
                # FILE STRUCTURE
                # name = [usage, xp, definition]
                # name = [usage, xp, definition]
                # name = [usage, xp, definition]
                # etc...

        if os.path.isfile(self.BASE_DIR + "//Resources//Objects//Weapons//Offence//offence.dat"):
            with open(self.BASE_DIR + "//Resources//Objects//Weapons//Offence//offence.dat", 'r') as f:
                data = f.read()
                data = data.split("\n")
            for weaponObj in data:
                weaponName = weaponObj.split("=")[0]
                weaponData = weaponObj.split("=")[1]
                weaponData = literal_eval(weaponData)
                self.Weapons[weaponName][2] = weaponData[0]
                self.Weapons[weaponName][3] = weaponData[1]
                self.Weapons[weaponName][4] = weaponData[2]
            


            

        
            

    def weaponEditorGUI(self, window, selectedObj):
        menu = pygame.Surface((greeter.Width-20, greeter.Height-20), pygame.SRCALPHA, 32)
        menu.fill((245, 255, 240))
        pygame.draw.rect(menu, (0,0,0), (0,0,greeter.Width-20,greeter.Height-20), 2)
        pygame.draw.line(menu, (0,0,0), ((greeter.Width-20)//2, 0), ((greeter.Width-20)/2,greeter.Height-20))
        gui.text((47, 79, 79), "Available Weapons", 18, "Arial", 15, 10, menu)
        gui.text((47, 79, 79), "Added Weapons", 18, "Arial", (greeter.Width-30)//2, 10, menu)
        pygame.draw.line(menu, (0,0,0), (0,50), (greeter.Width-20,50), 2)
        window.blit(menu, (10,10))

        menuPos = {}

        # DISPLAY ALL WEPAONS SELECTED BYT THE COUNTRY
        for weapon in range(len(self.countryWeapons)):
            menuPos[self.countryWeapons[weapon]] = (32+(10*weapon, 210)) # SETS POSITION OF WEAPON TILES FOR SELECTING PURPOSES | CREATE Y VALUE FORMULA THAT MOVES DOWN EVERY SAY 15 TILED WEAPONS

        for weapon in menuPos:
            menu.blit(self.Weapons[weapon][0], (menuPos[weapon])) 

class mapEditor(object):

    def __init__(self):
        self.edit = True
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        self.saveBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/save.png')
        self.loadBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/load.png')
        self.addBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/add.png')
        self.removeBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/remove.png')
        self.selectBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/cursor.png')
        self.moveBtn = pygame.image.load(self.BASE_DIR + '/Resources/Buttons/move.png')
        self.imgBtnClick = {'saveBtn': False, 'loadBtn': False, 'addBtn': False, 'removeBtn': False, 'selectBtn': False, 'moveBtn': False}
        self.loadedTextures = {}
        self.TexturePos = {}
        self.selectedObj = None


    def draw(self):
        pygame.draw.rect(greeter.window, (211,211,211), (0,0,greeter.Width,52))
        #greeter.window.blit(self.saveBtn, (5,8))
        gui.imageBtn(5,8, self.saveBtn, 'saveBtn')
        gui.imageBtn(42,8, self.loadBtn, "loadBtn")
        pygame.draw.line(greeter.window, (47,79,79), (76,0), (76,52), 2)
        if gui.imageBtn(80,1, self.addBtn, 'addBtn'):
            self.imgBtnClick['addBtn'] = True
            gui.viewLib = True
        gui.imageBtn(140, 1, self.removeBtn, 'removeBtn')
        pygame.draw.line(greeter.window, (0,0,0), (192,0), (192,52), 2)
        if gui.imageBtn(194, 10, self.selectBtn, 'selectBtn'):
            self.imgBtnClick['selectBtn'] = True
        if gui.imageBtn(228, 10, self.moveBtn, 'moveBtn'):
            self.imgBtnClick['moveBtn'] = True

        # DRAW ANY LOADED TEXTURE POSITIONS TO MAP
        for texture in self.TexturePos:
            greeter.window.blit(self.loadedTextures[texture], (self.TexturePos[texture]))

            # CHECK IF USER HAS SELECTED TEXTURE WHEN SELECTING TOOL ACTIVE
            if self.imgBtnClick['selectBtn'] == True:
                mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
                cWidth, cHeight = self.loadedTextures[texture].get_size()
                
                if self.TexturePos[texture][0]+cWidth > mouse[0] > self.TexturePos[texture][0] and self.TexturePos[texture][1]+cHeight > mouse[1] > self.TexturePos[texture][1]:
                    if click[0] == 1:
                        self.selectedObj = texture


        if self.selectedObj != None:
            if self.TexturePos[self.selectedObj][0]+self.loadedTextures[self.selectedObj].get_size()[0] < pygame.mouse.get_pos()[0] < self.TexturePos[self.selectedObj][0] and self.TexturePos[self.selectedObj][1]+self.loadedTextures[self.selectedObj].get_size()[1] < pygame.mouse.get_pos()[1] < self.TexturePos[self.selectedObj]:
                # USER'S MOUSE IS OUTSIDE OF SELECTED OBJECT
                print("outside of selected obj")
                if pygame.mouse.get_presssed()[0] == 1:
                    self.selectedObj = None

            textureX, textureY = self.TexturePos[self.selectedObj][0], self.TexturePos[self.selectedObj][1]
            textureW, textureH = self.loadedTextures[self.selectedObj].get_size()[0], self.loadedTextures[self.selectedObj].get_size()[1]
            pygame.draw.rect(greeter.window, (255,0,0), (textureX, textureY, textureW, textureH), 4)


    def editor(self):
        while self.edit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    greeter.Width, greeter.Height = event.w, event.h
                    greeter.window = pygame.display.set_mode((greeter.Width, greeter.Height), pygame.RESIZABLE)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if gui.scroll[1] > 0:
                            gui.scroll[1] -= 25
                    elif event.button == 5:
                        if gui.scroll[1] < greeter.Height-263:
                            gui.scroll[1] += 25
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.selectedObj != None:
                            self.imgBtnClick['moveBtn'] = None
                            self.imgBtnClick['selectBtn'] = None
            greeter.window.fill((0,0,255))

            self.draw()

            if self.imgBtnClick['addBtn']:
                #gui.LibViewer(self.BASE_DIR + '/Resources/Maps/', 'png')
                # ALPHA PURPOSES ONLY!!!
                fileName = input("File to load in Map Dir: ")
                try:
                    texture = pygame.image.load(self.BASE_DIR + '/Resources/Maps/%s.png' % (fileName))
                    self.loadedTextures[fileName] = texture
                    texture = pygame.transform.scale(texture, (32,36))
                    self.TexturePos[fileName] = (texture.get_size()[0], texture.get_size()[1])
                    self.imgBtnClick['addBtn'] = False
                except:
                    print("Failed to load texture: %s.png" % (fileName))

            if self.imgBtnClick['moveBtn'] == True and self.selectedObj != None:
                mouse = pygame.mouse.get_pos()
                self.TexturePos[self.selectedObj] = mouse



            pygame.display.flip()


                

world = World()
gui = GUI()
editor = mapEditor()

editor.editor()