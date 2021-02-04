import pygame

class Text(object):

    def generic(self, x, y, fg, font, size, msg, surface):
        font = pygame.font.SysFont(font, size)
        text = font.render(msg, True, fg)
        textRect = text.get_rect()
        textRect.center = (x,y)
        surface.blit(text, textRect)

    def bare(self, fg, font, size, msg):
        font = pygame.font.SysFont(font, size)
        text = font.render(msg, True, fg)
        return text

text = Text()

class EventHandler:

    def __init__(self, w, h):
        pygame.init()

        self.event_list = pygame.event.get()
        self.width, self.height = w, h
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)


        self.pressedKey = []
        self.logEvents = False
        self.mouse = pygame.mouse.get_pos()

        self.vUpdate = False # SWITCH FOR OTHER CLASSES TO REFRESH VARS WHEN SCREEN RESIZES

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
                self.vUpdate = True
            if event.type == pygame.KEYDOWN:
                if self.logEvents:
                    if event.key != pygame.K_BACKSPACE or pygame.K_CAPSLOCK or pygame.K_ESCAPE or pygame.K_RETURN: # BLACKLISTED KEYS FOR RAW TEXT
                        self.pressedKey = list(event.unicode)
                    if event.key == pygame.K_BACKSPACE:
                        self.pressedKey = ['backspace']
                    if event.key == pygame.K_RETURN:
                        self.pressedKey = ['return']
        self.update()

    def search(self, eventName): # SEARCH FOR AN EVENT IN THE EVENT QUEUE
        for event in self.event_list:
            if event.type == eventName:
                return True
            else:
                return False


class Form(object):

    def __init__(self, x, y, w, h, message, timerEvent, mode=True, encryption=False, border=True, whFull=False):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.encryption = encryption
        self.textOut = []
        self.mode = mode # mode = true |light mode, mode = false | dark mode
        self.activeForm = False
        self.msg = message
        self.activeTimer = False # BOOL TO REPRESEANT IF THE FORM IS IN AN ACTIVE STATE OR NOT
        self.setBorder = border
        pygame.time.set_timer(timerEvent, 800)

        self.timer = timerEvent   # TIMER SWITCH

        self.usewh = whFull # uses abitary mouse search loop using only the length and width coords

        self.TextObject = None # var to store text output object

    def draw(self, surface, event, drawX=None, drawY=None): # DRAW COORDS FOR WHEN DRAIWWNG FORM TO SURFACE USING SCREEN COORDS TO ACTIVATE MOUSE FAILS IF DRAW COORDS ARENT USED
        if self.mode == True:
            pygame.draw.rect(surface, (255,255,255), (self.x,self.y,self.w,self.h)) # BACKGROUND
            if self.setBorder == True:
                pygame.draw.rect(surface, (0,0,0), (self.x,self.y,self.w,self.h), 4) # BORDER

            #DRAW INPUT TO FORM
            if self.encryption == False:
                self.TextObject = text.bare((48, 79, 79), 'Arial', self.h//2, ''.join(self.textOut))
                surface.blit(self.TextObject, (self.x+10, self.y+2))
            else: # ENCRYPT AND DISPLAY MESSAGE
                self.TextObject = text.bare((47, 79, 79), 'Arial', self.h//2, "*" * len(''.join(self.textOut)))
                surface.blit(self.textObject, (self.x+10, self.y+2))

            if self.activeForm == False and self.textOut == []: # DRAW INACTIVE MESSAGE
                surface.blit(text.bare((48, 79, 79), 'Arial', self.h//2, self.msg), (self.x+10, self.y+2))
            

            if self.activeTimer == True:
                pygame.draw.line(surface, (47, 79,79), (self.x+10, self.y+5), (self.x+10, self.y+20), 2) # DRAWS FLASHING CURSOR | MULTIPLY TEXT FEILD BY CHAR LENGTH TO ADD SPACING TO MOVE THE CURSOR ACROSS THE FORM

        elif self.mode == False:
            pygame.draw.rect(surface, (49, 79, 79), (self.x,self.y,self.w,self.h)) # BACKGROUND
            if self.setBorder == True:
                pygame.draw.rect(surface, (37, 49, 49), (self.x,self.y,self.w, self.h), 4) #BORDER

            #DRAW INPUT TO FORM
            if self.encryption == False:
                self.TextObject = text.bare((240, 255, 255), 'Arial', self.h//2, ''.join(self.textOut))
                surface.blit(self.TextObject, (self.x+10, self.y+2))
            else:
                self.TextObject = text.bare((240, 255, 255), 'Arial', self.h//2, "*" * len(''.join(self.textOut)))
                surface.blit(self.TextObject, (self.x+10, self.y+2))

            if self.activeForm == False and self.textOut == []:
                surface.blit(text.bare((240,255,255), 'Arial', self.h//2, self.msg), (self.x+10, self.y+2))

            if self.activeTimer == True and self.activeForm == True:
                pygame.draw.line(surface, (240,255,255), (self.x+10+self.TextObject.get_size()[0], self.y+5), (self.x+10+self.TextObject.get_size()[0], self.y+20), 2)

        # DO LOGIC

        # CHECKS IF FORM ACTIVE
        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()


        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y: # FORM ACTIVATOR
            if click[0] == 1:
                self.activeForm = True
                event.logEvents = True
        else:
            if click[0] == 1:
                self.activeForm = False
                event.logEvents = False


        if event.logEvents == True and event.pressedKey != []:
            if event.pressedKey[0] != 'backspace':
                if event.pressedKey[0] != 'return':
                    self.textOut.append(event.pressedKey[0])
                    event.pressedKey = []
            elif event.pressedKey[0] == 'backspace':
                if self.textOut != []:
                    del self.textOut[-1]
                    event.pressedKey = []
            elif event.pressedKey[0] == 'return':
                if self.textOut != []:
                    del self.textOut[-1]
                    event.pressedKey = []


        if self.activeForm == True: # CURSOR SWITCH
            if event.search(self.timer):
                if self.activeTimer == False:
                    self.activeTimer = True
                elif self.activeTimer == True:
                    self.activeTimer = False



class Button(object):

    def generic(self, x, y, w, h, bg, fg, tc, msg, event):
        pygame.draw.rect(init.window, bg, (x,y,w,h))
        Text.generic(w//2,h//2, tc, "Arial", h//4, msg)
        if x+w > init.mouse[0] > x and y+h > init.mouse[1] > y:
            if init.click[0] == 1:
                event()

    def border(self, x, y, w, h, bg, fg, tc, msg, bc, borderSize, event, handlerObject):
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(handlerObject.window, bc, (x,y,w,h), borderSize)
        pygame.draw.rect(handlerObject.window, bg, (x,y,w-borderSize,h-borderSize))
        text.generic(w//2,h//2, tc, "Arial", h//4, msg)
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if init.click[0] == 1:
                event()


    def returnClick(self, x, y, w, h, bg, fg, tc, msg, returnIdentifier, handlerObject):
        pygame.draw.rect(handlerObject.window, bg, (x,y,w,h))
        text.generic(w//2,h//2, tc, "Arial", h//4, msg, handlerObject.window)
        if x+w > handlerObject.mouse[0] > x and y+h > handlerObject.mouse[1] > y:
            for event in handlerObject.event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return returnIdentifier
        else:
            returnIdentifier = False
        return returnIdentifier

    def drop(self, x, y, w, h, bg, fg, tc, dropPX, msg, event):
        if x+w > init.mouse[0] > x and y+h > init.mouse[1] > y:
            pygame.draw.rect(init.window, bg, (x,y+dropPX,w,h))
            Text.generic(w//2,(h+dropPX)//2, tc, "Arial", h//4, msg)
            if click[0] == 1:
                event()
        else:
            pygame.draw.rect(init.window, bg, (x,y,w,h))
            Text.generic(w//2,h//2, tc, "Arial", h//4, msg)

class imgButton:

    def __init__(self, fileDir, size):
        try:
            self.img = pygame.image.load(fileDir)
        except: raise Exception("FileNotFound", fileDir)
        self.pressed = False
        self.img = pygame.transform.scale(self.img, (size,size))
        self.w, self.h = size, size
        self.drawBtn = True # ANIMATION SWTICH FOR POPPING AFFECT

    def draw(self, surface, x, y, eventObject):
        mouse = pygame.mouse.get_pos()

        for event in eventObject.event_list:
            if x+self.w > mouse[0] > x and y+self.h > mouse[1] > y:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.pressed == False:
                            self.pressed = True
                        else:
                            self.pressed = False
                        self.drawBtn = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.drawBtn = True
        if self.drawBtn == True:
            surface.blit(self.img, (x,y))

class notifyPopup:

    def __init__(self, w, h, windowTitle, msg):
        self.w, self.h =  w, h
        self.title = windowTitle
        self.msg = msg

        self.display = False # MASTER DISPLAY
        self.btnDisplay = False # BTN ANIMATION SWITCH
        
        self.window = pygame.Surface((self.w, self.h))

    def draw(self, surface, x, y, eventObject):
        if self.display == True:
            self.window.fill((0,255,255))
            pygame.draw.rect(self.window, (0, 139, 139), (0,0, self.w, 30))

            pygame.draw.rect(self.window, (114, 128, 128), ((self.w//2)-40, self.h-40, 80, 30)) # ok btn
            
            self.window.blit(text.bare((0,0,0), "Tahoma", 15, self.title), (2,6)) # title
            self.window.blit(text.bare((0,0,0), 'Tahoma', 15, self.msg), ((self.w//2)-(text.bare((0,0,0), 'Tahoma', 15, self.msg).get_size()[0]//2), (self.h//2)-20)) # msg
            self.window.blit(text.bare((0,0,0), 'Tahoma', 15, 'Ok'), ((self.w//2)-10, self.h-35))

            # LOGIC
            mouse = pygame.mouse.get_pos()

            for event in eventObject.event_list:
                if x+((self.w//2)-40)+80 > mouse[0] > x+((self.w//2)-40) and y+(self.h-10) > mouse[1] > y+(self.h-40): # OK BTN
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.display = False

                # quit btn
                if x+self.w > mouse[0] > x+(self.w-30) and y+30 > mouse[1] > y:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.display = False
                    self.btnDisplay = True
                else:
                    if self.btnDisplay:
                        self.btnDisplay = False

            if self.btnDisplay: # DRAWS BTN ANIMATION
                pygame.draw.rect(self.window, (255,0,0), (self.w-30,0,30,30))

            pygame.draw.line(self.window, (0,0,0), (self.w-28, 2), (self.w-2, 28)) # EXIT BUTN
            pygame.draw.line(self.window, (0,0,0), (self.w-2, 2), (self.w-28, 28))
                        

            surface.blit(self.window, (x, y))

    def update(self, width, height):
        self.w, self.h = width, height
        self.window = pygame.Surface((self.w, self.h))


class formPopup:

    def __init__(self, x, y, w, h, title, msg, timer, formNum, formHeight=30, formOffset=5, formEncryption=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.title = title
        self.msg = msg

        self.timerObj = timer
        
        self.formObj = []
        self.formHeight = formHeight
        self.formNum = formNum
        self.formOffset = formOffset
        self.encryption = formEncryption

        self.display = False
        self.displayExit = False

        self.finishAction = False # only true if user presses ok

        self.formIterator = 0

        #CRETAE SURFACE
        self.window = pygame.Surface((w,h))
        #CREATE FORMOBJ
        if (formNum // formHeight)+self.formOffset < h-70: # CHECKS IF ALL FORMS CAN BE DISPLAYED PROBERLY 
            for i in range(formNum):
                self.formObj.append(Form(self.x+10, self.y+(40+(i*(self.formOffset+30))), self.w-20, 30, self.msg, self.timerObj, False, self.encryption, False)) # GENERATES FORMS AND APPENDS TO FORMOBJECT FOR DRAWING
        else:
            print("Fatal Error: Cannot draw %s forms in this window." % (formNum)) # NOT ALL FORMS CAN FIT IN WINDOW SIZE. PASS ERROR AND DO NOT CREATE FORM

    def draw(self, surface, eventObj):
        if self.display == True:
            self.window.fill((0,255,255))
            pygame.draw.rect(self.window, (0, 139, 139), (0,0, self.w, 30))

            pygame.draw.rect(self.window, (114, 128, 128), ((self.w//2)-40, self.h-40, 80, 30)) # ok btn !!!!!

            self.window.blit(text.bare((0,0,0), 'Tahoma', 15, 'Ok'), ((self.w//2)-10, self.h-35))
            self.window.blit(text.bare((0,0,0), 'Tahoma', 15, self.title), (10, 8))

            mouse = pygame.mouse.get_pos()
            for event in eventObj.event_list:
                if self.x+self.w > mouse[0] > self.x+(self.w-30) and self.y+30 > mouse[1] > self.y:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.display = False
                # USED FOR RED BUTTON ANIMATION
                    self.displayExit = True
                else:
                    self.displayExit = False

                # OK BUTTON
                if self.x+((self.w//2)-40)+80 > mouse[0] > self.x+((self.w//2)-40) and self.y+(self.h-40)+30 > mouse[1] > self.y+(self.h-40):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.display = False
                            self.finishAction = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.formNum == 1:
                            self.display = False
                            self.finishAction = True
                        elif self.formNum <= len(self.formObj):
                            pass # WRIET CHANGE TO NEXT FORM CODE HERE

            
            if self.displayExit == True:
                pygame.draw.rect(self.window, (255,0,0), (self.w-30, 0, 30, 30))

            pygame.draw.line(self.window, (0,0,0), (self.w-28, 2), (self.w-2, 28)) # EXIT BUTN
            pygame.draw.line(self.window, (0,0,0), (self.w-2, 2), (self.w-28, 28))

            surface.blit(self.window, (self.x, self.y))


            for i in range(self.formNum): # DRAW FORMS
                self.formObj[i].draw(surface, eventObj)
            
            

    def update(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.window = pygame.Surface((self.w, self.h))

class dynamicArray:

    def __init__(self, x, y, w, h, scrollHeight, dataObject, searchForm=False, dynamicScroll=True):
        # searchForm = if there should be a search box at teh top
        # dynamicScroll = controls if there should be a scrollbar if required or not
        self.x, self.y, self.w, self.h = x, y, w, h
        self.data = dataObject
        self.drawList = []

        self.maxX = int((w//32)*0.7)
        self.maxY = int((h//32)*0.7)

        if dataObject != None:
            self.dataColumn = len(dataObject) // self.maxX
        else: self.dataColumn = 0
        self.dataRow = 0
        self.scroll = False # different fron dynamic scroll. Dynamic scroll tells script to check if it needs a scrollbar. Scroll is the switch for the scroll bar
        self.scrollH = scrollHeight
        self.scrollp = 0

        # HANDLE DYNAMIC SCROLLING
        if dynamicScroll == True: 
            # Dynamic Scrolling is not specifically enabled. It is only enabled when the size of the data to draw is to large for the area specified
            if self.dataColumn > self.maxX:
                self.scrollSpeed = self.dataColumn*0.7 # GO %70 as fast as how many objects are drawn
                self.scrollY = 0
                self.scroll = True
            else:
                self.scrollSpeed, self.scrollY = 0, 0
                self.scroll = False
        else:
            self.scroll = False

        self.updateRow = True

        # populate drawList with all objects to draw
        if self.data != None:
            for obj in range(len(self.data)):
                self.drawList.append(obj)
        #except TypeError: raise Exception('Invalid data Object')
        
        #---THE SPECIAL SAUCE---
        
        # determine if data does not compleet a full row
        if len(self.drawList) % self.maxX != 0: # if this reutns a num it is the num of objs that dont copmplete the row
            self.dataColumn += 1 # minipulates program into drawing our missing data from a null row
            self.dataRow = self.maxX - (len(self.drawList) % self.maxX)

            #!---THE SECRET INGREIDENT TO THE SAUCE---

            # REMOVE EXTRA DRAWN DataRows. Prevents extra cubes from drawing outside of dynamicArray | Only required for testing mode
            """for i in list(self.drawList):
                if i <= self.dataRow-1:
                    del self.drawList[-1]"""

    def draw(self, surface, eventObject, scale, testMode=False):
        # TestMode = Draws rectangles instead of objects define din the dictionary given to init func

        if self.scroll == True:
            pygame.draw.rect(surface, (128,128,128), (self.x-10, self.y+10, 18, self.scrollH)) # Scroll Gb
            pygame.draw.rect(surface, (0,0,0), (self.x-8, self.y+12+self.scrollp, 14, 60)) # Scroll Bar
        # Draw Dynamic Grid array based on dataObject given
        mouse = pygame.mouse.get_pos()
        # !-- CRITICAL WARNIGN -- Don't add or subtract on posX when drawing incomplete rows. This causes the incomplete rows to draw false data sets off the specified window
        for x in range(self.maxX):
            for y in range(self.dataColumn):
                if y == self.dataColumn-1 and len(self.drawList) % self.maxX != 0: # DRAW INCOMPLETE ROWS IF ANY
                    if testMode == True:
                        pygame.draw.rect(surface, (255, 0, 0), (16+((16+scale)*(x-self.dataRow)), self.y+16+((16+scale)*y)+self.scrollY, scale, scale))
                    else:
                        if type(self.data) == dict:
                            if x-self.dataRow > -1:
                                surface.blit(self.data.get(list(self.data)[y+(x-self.dataRow)]), (16+((scale)*(x-self.dataRow))+self.x, self.y+16+((16+scale)*y)+self.scrollY))

                        if type(self.data) == list:
                            surface.blit(self.data[y+(x-self.dataRow)], (self.x+16+((16+scale)*(x-self.dataRow)), self.y+16+((16+scale)*y)+self.scrollY))
                else:
                    if testMode == True:
                        if self.y-48+((16+scale)*y)+self.scrollY > -0.8:
                            pygame.draw.rect(surface, (255, 0, 0), (self.x+(16+((16+scale)*x)), self.y+16+((16+scale)*y)+self.scrollY, scale, scale))
                        else:
                            #print(self.data)
                            if type(self.data) == dict:
                                surface.blit(pygame.transform.scale(self.data.get(list(self.data)[y+(x-self.dataRow)])), self.x+(16+((self.x+scale)*x), (16+((16+scale)*y)-self.scrollY)))
                            if type(self.data) == list:
                                surface.blit(self.data[y+(x-self.dataRow)], (16+((16+scale)*x), self.x+(16+((16+scale)*y)-self.scrollY)))
                # HANDLE IF USER SELECTS WEAPON TO EDIT
                """if self.x+(16+((16+scale)*x))+32 > mouse[0] > 16+((16+scale)*x):
                    if (self.y+16+((16+scale)*y)+self.scrollY)+74 > mouse[1] > self.y+58+((16+scale)*y)+self.scrollY:
                        if y == self.dataColumn-1 and len(self.drawList) % self.maxX != 0: # HANDLE MOUSE PRESSSES FOR INCOMPLETE ROWS
                            if x < self.maxX-self.dataRow:
                                print(y+x)
                                for event in eventObject.event_list:
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1:
                                            #call form that allows editing of the weapon/defence Unless its click and hold if so move the object to another list
                                            print('Clicked On: %s' % (y+x))"""
                if self.x+(16+((16+scale)*x))+28 > mouse[0] > self.x+(16+((16+scale))*x): # USES APROX VALUES FOR SIZING!!!! | GET TEXTURE SIZE FOR PROPER BUTTON MAPING
                    if self.y+(64+((16+scale)*y)-self.scrollY)+32 > mouse[1] > self.y+64+((16+scale)*y)-self.scrollY:
                        if y == self.dataColumn-1 and len(self.drawList) % self.maxX != 0:
                            if x < self.maxX-self.dataRow:
                                for event in eventObject.event_list:
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        return list(self.data)[y+x]
            # Handle Logic Here


        if self.scroll == True:
            for event in eventObject.event_list:
                if event.type == pygame.MOUSEBUTTONDOWN: # HANDLE SCROLLING EVENTS
                    if event.button == 4:
                        self.scrollY += self.scrollSpeed
                    if event.button == 5:
                        self.scrollY -= self.scrollSpeed

        return None

    def update(self, dataObject):
        self.data = {}
        self.dataColumn = 0
        self.drawList = []
        self.data = dataObject
        if dataObject != None:
            self.dataColumn = len(dataObject) // self.maxX
        else: self.dataColumn = 0
        if self.data != None:
            for obj in range(len(self.data)):
                self.drawList.append(obj)
        if len(self.drawList) % self.maxX != 0: # if this reutns a num it is the num of objs that dont copmplete the row
            self.dataColumn += 1 # minipulates program into drawing our missing data from a null row
            self.dataRow = self.maxX - (len(self.drawList) % self.maxX)

        
class dynamicFormPopup:
            
    def __init__(self, x, y, w, h, formHeight, formInsize, formStackSpace, timerEvent, drawMode=True): # Not intended to update sizing, only to change messages and forms
        self.x, self.y, self.w, self.h = x, y, w , h
        self.formSize = formHeight
        self.formInsize = formInsize # The spacing between the start of the window to the end of the window | exampe, formInsize = 5 means minus 5p  from both sides of form
        self.formSpacing = formStackSpace # the spacing between the forms on the y axis | example, formStackSize = 15, means 15p space between each form form the one ontop. Will check if it cand raw all forms with thsi sapcing

        self.timer = timerEvent
        self.Mode = drawMode

        # define important surfaces and vars here
        self.surface = pygame.Surface((self.w, self.h))
        self.fontObj = pygame.font.SysFont('Tahoma', 15)

        self.Title = None
        self.Messages = []  # msgList = [Ttitle, form1.Inactive, form2.Inactive, *form3*.Inactive] | formCount si the amoutn of forms stacked onto each other | * at the start of the form means this active message should be encrypted
        self.forms = {} # {formName: formObject}

        # Very Unimportant stuff
        self.moveWindow = False
        self.close = False


    def updateForm(self, messageList, formHeight, formInsize, formStackSize):
        if type(messageList) != list:
            raise Exception("Invalid message data")
        self.Title = messageList[0]
        del messageList[0]
        self.Messages = messageList
        self.formInsize = formInsize
        self.formSpacing = formStackSize
        self.formSize = formHeight
        #Generate forms
        for form in range(len(self.Messages)):
            if '*' not in self.Messages[form]:
                #Message wont be encrypted
                #x, y, w, h, message, timerEvent, mode=True, encryption=False, border=True, whFull=False
                formObj = Form(self.x+self.formInsize, self.y+42+self.formInsize+(form*self.formSpacing), self.w-(self.formInsize*2), self.formSize, self.Messages[form], self.timer)
                self.forms[self.Messages[form]] = formObj
            else:
                #Active form message to be encrypted
                formObj = Form(self.x+self.formInsize, self.y+42+self.formInsize+(form*self.formSpacing), self.w-(self.formInsize*2), self.formSize, self.Messages[form].strip('*'), self.timer, True, True)
                self.forms[self.Messages[form].strip('*')] = formObj
                

    def updateText(self, font, fontSize):
        self.fontObj = pygame.font.SysFont(font, fontSize)




    def moveableWindow(self, mouse): # Call in main loop and pass mouseObject to allow user to drag window around
        self.x, self.y = mouse[0], mouse[1]

    def draw(self, window, eventObject): # X, Y ARE SCREEN COORDS!!!!
        self.surface.fill((255,255,255))

        # Draw title and drag menu
        pygame.draw.rect(self.surface, (0, 139, 139), (0, 0, self.w, 42)) # draw menu bg
        surface.blit(self.font.render(self.Title, True, (240, 240, 240)), (15, 8)) # draw title
        #draw cross over x btn
        pygame.draw.line(self.surface, (47, 79, 79), (self.x+(self.y-40), 0), (self.x+(self.y-2), 40), 2) # \
        pygame.draw.line(self.surface, (47, 79, 79), (self.x+(self.y-2), 0), (self.x+(self.y-40), 40), 2) # /



        #Stop drawing here
        window.blit(self.surface, (self.x, self.y))

        # Handle Logic

        # Handle window move and exit btn
        mouse == pygame.mouse.get_pos()
        for event in eventObject.list_events: # Event loop

            if self.x+(self.w-42) > mouse[0] > self.x and self.y+42 > mouse[1] < self.y: # Inside main title area
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.moveWindow = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.moveWindow = False

            if self.x+self.w > mouse[0] > self.x+(self.w-42) and self.y+42 > mouse[1] > self.y: # Inside exit btn
                pygame.draw.rect(self.surface, (200, 0, 0), (self.x+(self.y-42), 0, 42, 42)) # draw red bg
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.close = True
                

                    
        if self.moveWindow == True:
            self.moveableWindow(mouse)

class Switch:

    def __init__(self, x, y, w, h, bg, fg, activefg, surface, eventObj):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.window = surface
        self.handler = eventObj

        #Internal switch stuff
        self.active = False

        self.background = bg
        self.foreground = fg
        self.activeForeground = activefg

    def draw(self):
        pygame.draw.rect(self.window, self.background, (self.x, self.y, self.w, self.h), )
            
#defines relevant objects
button = Button()