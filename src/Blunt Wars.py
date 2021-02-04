import pygame, os, random

from Scripts import PygUI as ui
from ast import literal_eval
from datetime import datetime

BASE_DIR = os.getcwd()
BASE_DIR = BASE_DIR + '\\'

handler = ui.EventHandler(1024, 648)

class Auth:

    def __init__(self):
        self.User = 'Guest'
        self.logged = False

auth = Auth()

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
        self.CountryWeapons = {} # NAME: {weaponName: surface, weaponName: surface} # A DICT THAT STORES ALL COUNTRIES WITH ASSOCIATED WEAPONS
        self.Weapons = weapons.weaponObj # A copy of the global weapons dict for map editing ONLY!!

        # LOAD ALL WEAPON OBJECTS
        weapons.load_all(BASE_DIR + '\\src\\Resources\\Objects\\Weapon')

        # Define UI Apps
        pygame.time.set_timer(pygame.USEREVENT, 800)
        self.searchFeild = ui.formPopup(handler.width//3, (handler.height//2)-80, handler.width//3, 160, "Load Map File", "Enter File name to load into map", pygame.USEREVENT, 1)
        self.saveMap = ui.formPopup(handler.width//3, (handler.height//2)-60, handler.width//3, 120, 'Save Map', 'Name of Map', pygame.USEREVENT, 1)

        # Map Editor stuff
        self.mapObjects = {} # Name: [Surface, posX, posY]
        self.selectedObj = None # SELECTED SRUFACE: (posX, posY) 
        self.selectedWeapon = None # Name of weapon | USED AS A RETURN METHOD IF WEAPON PRESSED IN EDITOR
        self.select = False
        self.move = False

        self.updateMove = False

        self.availableWeaponArray = ui.dynamicArray(self.weaponsGUI.get_size()[0]//2, 80, self.weaponsGUI.get_size()[0]+(self.weaponsGUI.get_size()[0]//2)+10, self.weaponsGUI.get_size()[0]+(self.weaponsGUI.get_size()[0]//2)-90, self.weaponsGUI.get_size()[1]-10, self.Weapons)
        self.addedWeaponArray = ui.dynamicArray(10, 80, self.weaponsGUI.get_size()[0]//2, self.weaponsGUI.get_size()[1]-10,self.weaponsGUI.get_size()[1]-10, self.CountryWeapons.get(self.selectedObj))


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

        selector = self.availableWeaponArray.draw(self.weaponsGUI, handler, 32)
        if selector != None:
            self.selectedWeapon = selector
        selector = self.addedWeaponArray.draw(self.weaponsGUI, handler, 32)
        if selector != None:
            self.selectedWeapon = selector

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

        # Handle weapon editor button events and movement
        if self.selectedWeapon in self.Weapons:
            if mouse[0] < self.weaponsGUI.get_size()[0]//2:
                for event in handler.event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.selectedObj not in self.CountryWeapons:
                                self.CountryWeapons[self.selectedObj] = {self.selectedWeapon: self.Weapons[self.selectedWeapon]}
                            else:
                                self.CountryWeapons[self.selectedObj][self.selectedWeapon] = self.Weapons[self.selectedWeapon]
                            # remove weaponObject from self.Weapons
                            self.Weapons.pop(self.selectedWeapon)
                            #Update Dynamic Array's. Required updtating to change how many items are being drawn
                            self.availableWeaponArray.update(self.Weapons)
                            self.addedWeaponArray.update(self.CountryWeapons[self.selectedObj]) # UPDATES ARRAY WITH DICT FROM COUNTRY
                            #Clear selected weapon Object
                            self.selectedWeapon = None
        if self.CountryWeapons != {}:
            if self.selectedWeapon in self.CountryWeapons[self.selectedObj]:
                if mouse[0] > self.weaponsGUI.get_size()[0]//2:
                    for event in handler.event_list:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.Weapons[self.selectedWeapon] = self.CountryWeapons[self.selectedObj][self.selectedWeapon]
                                # remove weapon object from self.CountryWeapons
                                self.CountryWeapons[self.selectedObj].pop(self.selectedWeapon)
                                # Update Array's
                                self.availableWeaponArray.update(self.Weapons)
                                self.addedWeaponArray.update(self.CountryWeapons[self.selectedObj])
                                #Clear selected weapon
                                self.selectedWeapon = None
        if self.selectedWeapon != None:
            for event in handler.event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print('pressed enter')


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
            if self.saveMap.display == True:
                self.writeSave()
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
            if self.saveBtn.pressed == True:
                self.saveMap.display = True
                self.saveBtn.pressed = False



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
            # Country Weapons

        # CHECK  IF OFFENSIV EOF DEFENSIVE DATA CHANGED IF SO ADD NEW DATA
        '''if auth.logged == True:
            # need to get name of saved file
            user = auth.User
            time = datetime.now()
            if time.hour < 12:
                saveTime = '%s-%s-%s, %sam:%s' %s (time.day, time.month, time.year, time.hour, time.minute)# Time standard!! dd--mm--yy, hour:minute
            else: #convert time 12 hour time from 24 hour time
                saveTime = '%s-%s-%s, %spm:%s' %s (time.day, time.month, time.year, time.hour-12, time.minute)
            self.mapSize
            self.mapObjects
            self.CountryWeapons'''
        self.saveMap.draw(handler.window, handler)

        # LOGIC

        if ''.join(self.saveMap.formObj[0].textOut) != '' and self.saveMap.finishAction == True:
            if os.path.isdir(BASE_DIR + 'src\\Resources\\SavedMaps\\') == False: # Map folder exists
                os.mkdir(BASE_DIR + 'src\\Resources\\SavedMaps\\')
            fileName = ''.join(self.saveMap.formObj[0].textOut)
            # CHECK IF FILENAME IS TAKEN
            if os.path.isfile(BASE_DIR + 'src\\Resources\\SavedMaps\\%s.dat' % (fileName)) == False: # file name not in use
                # Begin save data dump
                if auth.logged == True:
                    time = datetime.now()
                    if time.hour < 12:
                        savedTime = '%s-%s-%s, (%s:%sam)' % (time.day, time.month, time.year, time.hour, time.minute)
                    else:
                        savedTime = '%s-%s-%s, (%s:%spm)' % (time.day, time.month, time.year, time.hour-12, time.minute)
                    mapData = {} # {CountryName: [posX, posY]}
                    for i in self.mapObjects:
                        mapData[i] = [self.mapObjects[i][1], self.mapObjects[i][2]]
                    weapons = {}# {CountryName: [weapon1, weapon2]}
                    for name in self.CountryWeapons:
                        for i in self.CountryWeapons[name]:
                            if name in weapons:
                                weapons[name].append(i)
                            else:
                                weapons[name] = []
                                weapons[name].append(i)
                    self.saveMap.finishAction = False
                    self.saveMap.formObj[0].textOut = ''

                    #Write allocated data
                    with open(BASE_DIR + 'src\\Resources\\SavedMaps\\%s.dat' % (fileName), 'w') as f:
                        f.write('%s\n%s\n%s\n%s\n%s\n%s\n' % (fileName, savedTime, auth.User, self.mapSize, mapData, weapons))
            else:
                print('%s is currently used as a map name' % fileName)

class Menu:
    def __init__(self):
        pygame.time.set_timer(pygame.USEREVENT, 800)

        self.memos = []
        self.memoMsg = None
        self.popMsg = False
        self.globalSettings = {"Dark Mode": False, "Child Mode": False, "Global Multiplayer Servers": True, "Keep Logged": False}
        self.keySettings = {"up": "w", "down": "s", "left": "a", "right": "d", "left_click": "btn1", "right_click": "btn2", "pause": "escape"}

        #Menu Swicthes
        self.HelpSwitch = False
        self.SettingsSwitch = False
        #load game msgs from file
        if os.path.isfile(BASE_DIR + "src\\Resources\\memo.dat"):
            with open(BASE_DIR + "src\\Resources\\memo.dat", 'r') as f:
                data = f.read()
            self.memos = data.split('\n')
        else:
            print("Error loading memos. Consider updating the game!")
            pygame.quit()

    def settings(self):
        #Declare Button switches
        Switch1 = ui.Switch(10, 80, 60, 30, (0, 191, 255), (105, 105, 105), (255,255,255), handler.window, handler)
        while self.SettingsSwitch:
            handler.handle()
            handler.window.fill((105, 105, 105))
            pygame.draw.rect(handler.window, (0, 191, 255), (0, handler.height-42, handler.width, 42))

            handler.window.blit(ui.text.bare((0,0,0), 'Tahoma', 24, 'Settings'), ((handler.width//2)-48, 32))
            pygame.draw.line(handler.window, (211, 211, 211), (0, 68), (handler.width, 68))

            # Control Settings

            #Draw Switches
            Switch1.draw()
            


            pygame.display.flip()

            #handle logic
            for event in handler.event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.SettingsSwitch = False


    def help(self):
        while self.HelpSwitch:
            handler.handle()
            handler.window.fill((105, 105, 105))
            pygame.draw.rect(handler.window, (0, 191, 255), (0, handler.height-42, handler.width, 42))

            handler.window.blit(ui.text.bare((0,0,0), 'Tahoma', 24, 'Help'), ((handler.width//2)-42, 32))
            pygame.draw.line(handler.window, (211, 211, 211), (0, 68), (handler.width, 68))

            pygame.display.flip()

            # handle Logic
            for event in handler.event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.HelpSwitch = False

    def draw(self):
        pygame.display.set_caption('Blunt Wars - Menu')
        self.memoMsg = random.choice(self.memos)
        #create a random rotation for random memo
        randomRotation = random.randrange(35, 95)
        while True:
            handler.handle()
            handler.window.fill((105, 105, 105))
            pygame.draw.rect(handler.window, (0, 191, 255), (0, handler.height-42, handler.width, 42))

            
            #display memos with pooping effect
            if self.memos != []:
                if self.popMsg:
                    text = ui.text.bare((0, 0, 0), 'Arial', 18, self.memoMsg)
                else:
                    text = ui.text.bare((0, 0, 0), 'Arial', 14, self.memoMsg)

                handler.window.blit(text, ( ((handler.width//2)-(text.get_rect()[0]//2)), 55))

            handler.window.blit(ui.text.bare((0,0,0), 'Tahoma', 24, 'Blunt Wars'), ((handler.width//2)-84, 32)) # header

            # Draw menu buttons
            pygame.draw.rect(handler.window, (211, 211, 211), (20, 85, (handler.width-50)//2, 30)) # Singleplayer
            pygame.draw.rect(handler.window, (211, 211, 211), (30+(handler.width-50)//2, 85, (handler.width-50)//2, 30)) # Multiplayer
            pygame.draw.rect(handler.window, (211, 211, 211), (20, 125, (handler.width-50)//2, 30)) # Sandbox
            pygame.draw.rect(handler.window, (211, 211, 211), (30+(handler.width-50)//2, 125, (handler.width-50)//2, 30)) # Settings
            pygame.draw.rect(handler.window, (211, 211, 211), (20, 165, handler.width-40, 30)) # help

            # Draw text onto btns
            handler.window.blit(ui.text.bare((47, 79, 79), 'Arial', 16, 'Singleplayer'), ((handler.width-50)//4, 88))
            handler.window.blit(ui.text.bare((47, 79, 79), 'Arial', 16, 'Multiplayer'), ( ((30+(handler.width-50)//2)+((handler.width-50)//4)), 88 ))
            handler.window.blit(ui.text.bare((47, 79, 79), 'Arial', 16, 'Sandbox'), ((handler.width-50)//4, 128))
            handler.window.blit(ui.text.bare((47, 79, 79), 'Arial', 16, 'Settings'), ( ((30+(handler.width-50)//2)+((handler.width-50)//4)), 128 ))
            handler.window.blit(ui.text.bare((47, 79, 79), 'Arial', 16, 'Help'), ((handler.width-40)//2, 168))




            pygame.display.flip()

            # Handle logic

            # Check for timer
            if handler.search(pygame.USEREVENT):
                if self.popMsg == False:
                    self.popMsg = True
                else:
                    self.popMsg = False

            mouse = pygame.mouse.get_pos()
            for event in handler.event_list:
                if 20+(handler.width-50)//2 > mouse[0] > 20 and 115 > mouse[1] > 85:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print("Clicked singleplayer")
                if (30+(handler.width-50)//2)+(handler.width-50)//2 > mouse[0] > 20+(handler.width-50)//2 and 115 > mouse[1] > 85:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print("Clicked Multiplayer")
                if 20+(handler.width-50)//2 > mouse[0] > 20 and 155 > mouse[1] > 125:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print('Clicked Sandbox')
                if (30+(handler.width-50)//2)+(handler.width-50)//2 > mouse[0] > 20+(handler.width-50)//2 and 155 > mouse[1] > 125:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.SettingsSwitch = True
                        self.settings()
                if handler.width-20 > mouse[0] > 20 and 195 > mouse[1] > 165:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.HelpSwitch = True
                            self.help()

            pygame.display.flip()
                

# GAME MODES

class Singleplayer:

    def __init__(self):
        pass

    def ask_mode(self):
        while True:
            handler.handle()

            handler.window.fill((105, 105, 105))
            pygame.draw.rect(handler.window, (0, 191, 255), (0, handler.height-42, handler.width, 42))
            #available modes
            """
            1. Country V Country # A country warfare gomemode
            2. World War # A general war where all country are fighting opposing alliance
            3. Controlled Wars # gamemode where you control the type of war from normal to a bio break out
            4. Scuffed Pervertion # Old Country V Country
            5. Select User defined map
            """


            handler.window.fill(())
"""
class Multiplayer:

    def __init__(self):
        pass

class Sandbox:

    def __init__(self):
        pass
"""

menu = Menu()
menu.draw()
#editor = Editor(0, 42, handler.width, handler.height)
#editor.draw()