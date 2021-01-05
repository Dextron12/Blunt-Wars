import pygame, os

from Scripts import PygUI as ui
from ast import literal_eval

BASE_DIR = os.getcwd()
BASE_DIR = BASE_DIR + '\\'

handler = ui.EventHandler(1024, 648)

class Auth:

    def __init__(self):
        self.User = 'Guest'
        self.logged = False

class Weapons:

    def __init__(self):
        self.weaponObj = {} # NAME: SURFACE
        self.offensive = {} # NAME: [DAMAGE, USAGE, IMMUNITY] | IMMUNITY IS EITHER None or [CountryNmae, CountryName]
        self.defensive = {} # NAME: [Protection, Usage, defenceStat, IndustryStat] # Protection: how much protection thsi provides you | defenceStat how much more defence you have. More defence means less damage and less attacks
        # IndustryStat: A Statistic of how well a countries industry is performing. Can make country a super power

    def load_all(self, dir): # function to load all weapon images for generic game modes use loadMap_weapons function to load weapons for individual maps
        for file in os.listdir(dir):
            if '.png' in file:
                #load the image
                self.weaponObj[file.split('.png')[0]] = pygame.image.load(dir + '\\%s' % (file)) 
                # IF IMAGE REQUIRES SCALING DO NOT SCALE THE IMAGE DIRECTLY
        if 'Defensive.weaponExtension' not in os.listdir(dir) or "Offensive.weaponExtension" not in os.listdir(dir):
            # CREATE EMPTY FILES FOR EDITOR TO FILL
            with open(dir + '\\Offensive.weaponExtension', 'w') as f:
                f.write(' ')
            with open(dir + '\\Defensive.weaponExtension', 'w') as f:
                f.write(' ')
        else:
            with open(dir + '\\Offensive.weaponExtension', 'r') as f:
                data = f.read()
            data = data.split('\n')
            for obj in data:
                print(data) 
            with open(dir + '\\Defensive.weaponExtension', 'r') as f:
                data = f.read()
            data = data.split('\n')
            for obj in data:
                print(obj)

    def loadMap_weapons(self, mapName):
        print("I am not complete")

weapons = Weapons()
# use weapons.load_all() to laod generic weapons or loadMap_weapons to load map specific weapons
                

class Editor:
    
    def __init__(self, mapX, mapY, mapW, mapH):
        self.mapSize = [mapX, mapY, mapW, mapH]

        # DEFINE UI OBJECTS HERE
        self.loadBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\save.png', 32)
        self.saveBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\load.png', 32)
        self.addBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\add.png', 38)
        self.remBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\remove.png', 38)
        self.selBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\cursor.png', 32)
        self.movBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\move.png', 32)
        self.wepBtn = ui.imgButton(BASE_DIR + 'src\\Resources\\Buttons\\weapons.png', 32)

        # WEAPON EDITOR GUI VARIABLES
        self.weaponsGUI = pygame.Surface((self.mapSize[2]-20, self.mapSize[3]-72))
        self.openWepEditor = False
        self.privWeapons = [] # A list of map specific weapons can be toggled in editor

        # LOAD ALL WEAPON OBJECTS
        weapons.load_all(BASE_DIR + '\\src\\Resources\\Objects\\Weapon')

        # Define UI Apps
        pygame.time.set_timer(pygame.USEREVENT, 800)
        self.searchFeild = ui.formPopup(handler.width//3, (handler.height//2)-80, handler.width//3, 160, "Load Map File", "Enter File name to load into map", pygame.USEREVENT, 1)

        self.addedWeaponArray = ui.dynamicArray(10, 80, self.weaponsGUI.get_size()[0]+(self.weaponsGUI.get_size()[0]//2)+10, self.weaponsGUI.get_size()[0]+(self.weaponsGUI.get_size()[0]//2)-90, self.weaponsGUI.get_size()[1]-10, weapons.weaponObj)

        # Map Editor stuff
        self.mapObjects = {} # Name: [Surface, posX, posY]
        self.selectedObj = None # SELECTED SRUFACE: (posX, posY) 
        self.select = False
        self.move = False

        self.updateMove = False


    def weaponEditor(self, x, y):
        self.weaponsGUI.fill((255,255,255))
        sizeX, sizeY = self.weaponsGUI.get_size()[0], self.weaponsGUI.get_size()[1]

        pygame.draw.rect(self.weaponsGUI, (49, 79, 79), (0,0,sizeX,30)) # window panel
        pygame.draw.line(self.weaponsGUI, (49, 79, 79), (int(sizeX//2), 30), (int(sizeX//2), sizeY), 2)
        pygame.draw.line(self.weaponsGUI, (49, 79, 79), (0, 65), (sizeX, 65), 2)

        # DRAW TEXT
        self.weaponsGUI.blit(ui.text.bare((240, 240, 240), 'Tahoma', 15, 'Edit Weapons For %s' % (self.selectedObj)), (5,8)) # TITLE
        self.weaponsGUI.blit(ui.text.bare((49, 79, 79), 'Tahoma', 18, 'Added Weapons'), (int(sizeX//4)-42, 42))
        self.weaponsGUI.blit(ui.text.bare((49, 79, 79), 'Tahoma', 18, "Available Weapons"), ((sizeX//2)+(int(sizeX//4)-42), 42))

        self.addedWeaponArray.draw(self.weaponsGUI, handler)


        # LOGIC
        mouse = pygame.mouse.get_pos()
        for event in handler.event_list:
            if event.type == pygame.VIDEORESIZE:
                self.weaponsGUI = pygame.Surface((event.w-20, event.h-72))

        if x+sizeX > mouse[0] > x+(sizeX-30) and (y+42)+30 > mouse[1] > y+42:
            pygame.draw.rect(self.weaponsGUI, (255, 0, 0), (sizeX-30, 0, 30, 30))
            for event in handler.event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.openWepEditor = False

        # DRAW EXIT BUTTON
        pygame.draw.line(self.weaponsGUI, (0,0,0), (sizeX-28, 0), (sizeX, 28), 2)
        pygame.draw.line(self.weaponsGUI, (0,0,0), (sizeX, 0), (sizeX-28, 28), 2)


        handler.window.blit(self.weaponsGUI, (x, y+42))



    def draw(self):
        while True:
            handler.handle()
            handler.window.fill((0,0,255))

            pygame.draw.rect(handler.window, (255,255,255), (0,0,handler.width,42)) # EDITOR MENU

            self.loadBtn.draw(handler.window, 2,2, handler)
            self.saveBtn.draw(handler.window, 34, 2, handler)
            pygame.draw.line(handler.window, (47, 79, 79), (68,0), (68,41), 2)

            self.addBtn.draw(handler.window, 70, 2, handler)
            self.remBtn.draw(handler.window, 108, 2, handler)
            pygame.draw.line(handler.window, (47, 79, 79), (150,0), (150,41), 2)

            self.selBtn.draw(handler.window, 152, 2, handler)
            self.movBtn.draw(handler.window, 186, 2, handler)
            self.wepBtn.draw(handler.window, 220, 2, handler)

            self.searchFeild.draw(handler.window, handler)

            for obj in self.mapObjects:
                #handler.window.blit(obj, (self.mapObjects[obj][0], self.mapObjects[obj][1]+42))
                handler.window.blit(self.mapObjects.get(obj)[0], (self.mapObjects[obj][1], self.mapObjects[obj][2]))

            if self.selectedObj != None: # DRAW SELECTED OBJ BORDER
                pygame.draw.rect(handler.window, (255,0,0), (self.mapObjects[self.selectedObj][1], self.mapObjects[self.selectedObj][2], self.mapObjects[self.selectedObj][0].get_size()[0], self.mapObjects[self.selectedObj][0].get_size()[1]), 2)
            
            if self.openWepEditor == True:
                self.weaponEditor(10, 10)
            # END DRAWING
            # DRAW MAP ADJUSTABLE MAP BORDERS
            #pygame.draw.line(handler.window, (0,0,0), (self.mapSize[0], self.mapSize[1]), (self.mapSize[0], self.mapSize[1]+self.mapSize[3]), 16) # mapX
            #pygame.draw.line(handler.window, (0,0,0), (self.mapSize[0]+self.mapSize[2], self.mapSize[1]), (self.mapSize[0]+self.mapSize[2], self.mapSize[3]), 16) # mapW
            #pygame.draw.line(handler.window, (0,0,0), (self.mapSize[0], self.mapSize[1]), (self.mapSize[0]+self.mapSize[2], self.mapSize[1]), 16) # mapY
            pygame.display.flip()

            # UPDATE LOGIC
            if handler.vUpdate == True:
                #self.errMsg.update(handler.width//3, 160)
                self.searchFeild.update(handler.width//3, (handler.height//2)-80, handler.width//3, 160)
                handler.vUpdate = False

            # BUTTON EVENTS
            if self.addBtn.pressed == True:
                self.searchFeild.display = True
                self.addBtn.pressed = False
            if self.selBtn.pressed == True:
                self.select = True
                self.selBtn.pressed = False
            if self.movBtn.pressed == True:
                self.move = True
                self.movBtn.pressed = False
            if self.remBtn.pressed == True:
                if self.selectedObj != None:
                    del self.mapObjects[self.selectedObj]
                    self.selectedObj = None
                self.remBtn.pressed = False
            if self.wepBtn.pressed == True:
                if self.selectedObj != None:
                    self.openWepEditor = True
                    self.wepBtn.pressed = False



            # LOGIC
            if ''.join(self.searchFeild.formObj[0].textOut) != '' and self.searchFeild.finishAction == True: # LOGIC FOR LOADING MAP OBJECTS
                # GET USER INPUT AND CHECK IF FILE EXSISTS THEN LOAD
                if os.path.isfile(BASE_DIR + 'src\\Resources\\Maps\\%s.png' % (''.join(self.searchFeild.formObj[0].textOut))):
                    #self.mapObjects[pygame.image.load(BASE_DIR + 'src\\Resources\\Maps\\%s.png' % (''.join(self.searchFeild.formObj[0].textOut)))] = (0,0)
                    self.mapObjects[''.join(self.searchFeild.formObj[0].textOut)] = [pygame.image.load(BASE_DIR + 'src\\Resources\\Maps\\%s.png' % (''.join(self.searchFeild.formObj[0].textOut))), 0, 42]
                else:
                    print("Couldn't load %s" % (''.join(self.searchFeild.formObj[0].textOut)))
                self.searchFeild.finishAction = False

            if self.select == True: # SELECT BTN ACTIVE
                mouse = pygame.mouse.get_pos()
                for obj in self.mapObjects:
                    if (self.mapObjects[obj][1]*32)+self.mapObjects[obj][0].get_size()[0] > mouse[0] > self.mapObjects[obj][1] and ((self.mapObjects[obj][2])+42)+self.mapObjects[obj][0].get_size()[1] > mouse[1] > (self.mapObjects[obj][2])+42:
                        for event in handler.event_list:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    if self.selectedObj != obj:
                                        self.selectedObj = obj
                                        self.select = False
                                    else:
                                        # unselect selected object
                                        self.selectedObj = None
                                        self.select = False
            if self.move == True:
                if self.selectedObj != None:
                    mouse = pygame.mouse.get_pos()
                    for event in handler.event_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.updateMove = True
                        if self.updateMove == True:
                            if event.type == pygame.MOUSEMOTION:
                                self.mapObjects[self.selectedObj] = [self.mapObjects[self.selectedObj][0], mouse[0], mouse[1]]
                            if event.type == pygame.MOUSEBUTTONUP:
                                if event.button == 1:
                                    self.updateMove = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    self.updateMove = False

    def writeSave(self):

        # !- mainSave.dat \\Resources\\SavedMaps\\
            # Name
            # Date/Time
            # User Saved By
            # mapSize
            # mapObjects
            # weaponObjects
            # privObjects

            # !- Possible Problems -!
            # Cannot get directtory of mapObject
            # Cannot get directory of WeaponObject

        # CHECK  IF OFFENSIV EOF DEFENSIVE DATA CHANGED IF SO ADD NEW DATA
        pass





            


"""class Menu:
    
    def __init__(self):
        pass

# GAME MODES

class Singleplayer:

    def __init__(self):
        pass

class Multiplayer:

    def __init__(self):
        pass

class Sandbox:

    def __init__(self):
        pass
"""
auth = Auth()
auth.logged = True

editor = Editor(0, 42, handler.width, handler.height)
editor.draw()