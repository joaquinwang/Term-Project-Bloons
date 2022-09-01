#Term Project 
# Bloons Tower Defense

from cmu_112_graphics import *
import math
import random

class Monkey():
    def __init__(self, cx, cy, r, image, fireSpeed, projectileSpeed, cost):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.image = image
        #self.fireType = fireType
        self.projectileSpeed = projectileSpeed
        self.fireSpeed = fireSpeed
        self.cost = cost

class Balloon():
    def __init__(self, cx, cy, r, speed, i, color, xMove, yMove):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.speed = speed
        self.i = i
        self.color = color
        self.xMove = xMove
        self.yMove =  yMove
        self.counter = self.speed * 10


class Projectile():
    def __init__(self, cx, cy, r, color, ix, iy, c, target):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.color = color
        self.ix = ix
        self.iy = iy
        self.c = c
        self.target = target

def appStarted(app):

    app.mode = "startScreenMode"
    
    app.health = 100
    app.rows = 15
    app.cols = 15
    app.margin = 30 
    app.selection = [] # (row, col) of selection, [] for none
    app.gold = 1000 
    app.status = "drawingMap"
    app.circleRadius = 10
    app.projectile = []
    getStartTile(app)
    randomMap(app)
    app.balloonAlgorith = 0

    app.dartMonkeyCounter = 0
    app.caveMonkeyCounter = 0
    app.wizardMonkeyCounter = 0
    app.squirtMonkeyCounter = 0
    app.doubleGunMonkeyCounter = 0

    app.currentMonkey = None
    app.monkeyClicked = False
    app.currentlyFiring = { "dartMonkey": False,
                            "caveMonkey": False,
                            "wizardMonkey": False,
                            "squirtMonkey": False,
                            "doubleGunMonkey": False  }


    app.gameOver = False
    
    app.counter = 0
    app.redCounter = 0
    app.blueCounter = 0
    app.blackCounter = 0

    app.timerDelay = 100
    app.monkeyClassList = []

    #Balloon 
    app.balloons = []

    #URL for Loadscreen and Monkeys are from the internet. The websites are also
    #the URLs. This means that this images of load screen and monkeys were not
    #created by me but I found them online and used them. Below are 6 URLs and
    # websites from where I got them are:
    # https://bloons.fandom.com/wiki/Bloons_TD_5_Console
    # https://bloons.fandom.com/wiki/Dart_Monkey
    # https://bloons.fandom.com/wiki/Cave_Monkey
    # https://bloons.fandom.com/wiki/Wizard_Monkey
    # https://bloons.fandom.com/wiki/Towers
    # https://bloons.fandom.com/wiki/Double_Gun

    #Load Screen Image
    url0 = ("https://static.wikia.nocookie.net/b__/images/5/5d/Bloons-td-5-switch-hero.jpg/revision/latest?cb=20210107232029&path-prefix=bloons")
    app.screenImage = app.loadImage(url0)
    app.screenImage1 = app.scaleImage(app.screenImage, 7/9)

    #First Monkey
    app.dartMonkeys = False
    url = ('https://static.wikia.nocookie.net/b__/images/b/b2/000-DartMonkey.png/revision/latest?cb=20190522014750&path-prefix=bloons')
    app.image = app.loadImage(url)
    app.image1 = app.scaleImage(app.image, 1/8)
    app.image1_2 = app.scaleImage(app.image1, 1/2)

    #Second Monkey
    app.caveMonkeys = False
    url2 = ('https://static.wikia.nocookie.net/b__/images/9/9b/Cave_Monkey.png/revision/latest?cb=20200411230945&path-prefix=bloons')
    app.image2 = app.loadImage(url2)
    app.image2_1 = app.scaleImage(app.image2, 1/9)
    app.image2_2 = app.scaleImage(app.image2_1, 1/2)

    #Third Monkey
    app.wizardMonkeys = False
    url3 = ('https://static.wikia.nocookie.net/b__/images/9/99/000-WizardMonkey.png/revision/latest?cb=20190522015102&path-prefix=bloons')
    app.image3 = app.loadImage(url3)
    app.image3_1 = app.scaleImage(app.image3, 1/8)
    app.image3_2 = app.scaleImage(app.image3_1, 1/2)

    #Fourth Monkey
    app.squirtMonkeys = False
    url4 = ('https://static.wikia.nocookie.net/b__/images/1/1f/BTD6_Glue_Gunner.png/revision/latest?cb=20180616145926&path-prefix=bloons')
    app.image4 = app.loadImage(url4)
    app.image4_1 = app.scaleImage(app.image4, 1/4)
    app.image4_2 = app.scaleImage(app.image4_1, 1/2)

    #Fifth Monkey
    app.doubleGunMonkeys = False
    url5 = ('https://static.wikia.nocookie.net/b__/images/a/ac/003-EngineerMonkey.png/revision/latest?cb=20190921173801&path-prefix=bloons')
    app.image5 = app.loadImage(url5)
    app.image5_1 = app.scaleImage(app.image5, 1/9)
    app.image5_2 = app.scaleImage(app.image5_1, 1/2)

    app.imagesDict = {  "dartMonkey": app.image1_2,
                        "caveMonkey": app.image2_2,
                        "wizardMonkey": app.image3_2,
                        "squirtMonkey": app.image4_2,
                        "doubleGunMonkey": app.image5_2  }
    
   
def drawImageWithSizeBelowIt(self, canvas, image, cx, cy, cost):
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(image))
    imageWidth, imageHeight = image.size
    canvas.create_text(cx, cy - imageHeight + 50,
                    text = cost, font='Arial 17 bold', fill='black')

def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):
    # aka "viewToModel"
    if (not pointInGrid(app, x, y)):
        pass
    gridWidth  = app.width - 8*app.margin
    gridHeight = app.height - 6*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 8*app.margin
    gridHeight = app.height - 6*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def inBoard(app, x,y):
    if ((app.width - 8*app.margin + app.margin > x > app.margin) and 
        (app.height - 6*app.margin + app.margin > y > app.margin)):
        return True
    else: return False

def gameMode_keyPressed(app, event):
    if app.status == "drawingMap" and event.key == "r":
        app.selection = []
        getStartTile(app)
        randomMap(app)
    if app.status == "drawingMap" and event.key == "s":
        app.selection = []
    

def gameMode_mousePressed(app, event):
    (row, col) = getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if inBoard(app, event.x, event.y):
        if app.status == "drawingMap":
            if (row, col) in app.selection:
                app.selection.remove((row, col))
            else:
                app.selection += [(row, col)]

    if app.status == "drawingMap" and (290 <= event.x <= 424) and (743 <= event.y <= 800) :
        app.status = "creatingMonkey"

    elif app.status == "creatingMonkey" and (event.x > 740 and app.margin < event.y < 715):
        app.monkeyClicked = True
        if event.x > 740 and app.margin < event.y < 155:
            if app.gold >= 100:
                app.dartMonkeys = True
                app.gold -= 100
            else: 
                pass

        elif event.x > 740 and 170 < event.y < 295:
            if app.gold >= 200:
                app.caveMonkeys = True 
                app.gold -= 200
            else:
                pass

        elif event.x > 740 and 310 < event.y < 450:
            if app.gold >= 300:
                app.wizardMonkeys = True
                app.gold -= 300
            else:
                pass

        elif event.x > 740 and 460 < event.y < 585:
            if app.gold >= 400:
                app.squirtMonkeys = True
                app.gold -= 400
            else:
                pass

        elif event.x > 740 and 600 < event.y < 715:
            if app.gold >= 500:
                app.doubleGunMonkeys = True
                app.gold -= 500
            else: 
                pass
        

    #Monkey is clicked, check if next click is on board, and place it.
    elif app.monkeyClicked == True and inBoard(app, event.x, event.y):
        x0,y0,x1,y1 = getCellBounds(app, row, col)
        if app.dartMonkeys:
            app.monkeyClassList += [Monkey(event.x, event.y, 2, app.image1_2, 20, 3, 200)]
            app.dartMonkeys = False

        elif app.caveMonkeys:
            app.monkeyClassList += [Monkey(event.x, event.y, 3, app.image2_2, 30, 200, 300)]
            app.caveMonkeys = False

        elif app.wizardMonkeys:
            app.monkeyClassList += [Monkey(event.x, event.y, 3, app.image3_2, 20, 200, 400)]
            app.wizardMonkeys = False

        elif app.squirtMonkeys:
            app.monkeyClassList += [Monkey(event.x, event.y, 17, app.image4_2, 50, 200, 500)]
            app.squirtMonkeys = False
            
        elif app.doubleGunMonkeys:
            app.monkeyClassList += [Monkey(event.x, event.y, 2, app.image5_2, 10, 200, 600)]
            app.doubleGunMonkeys = False
        app.monkeyClicked = False

def gameMode_mouseDragged(app, event):
    (row, col) = getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if app.status == "drawingMap":
        if (row, col) not in app.selection:
            app.selection += [(row, col)]
    

def drawBoardwithMonkeys(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill="silver", outline = "black")                      
    # draw grid of cells
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            fill = "wheat" if ((row, col) in app.selection) else "olivedrab"
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "olivedrab")
    drawImageWithSizeBelowIt(app, canvas, app.image1, 800, 100, "100 Gold")
    drawImageWithSizeBelowIt(app, canvas, app.image2_1, 800, 240, "200 Gold")
    drawImageWithSizeBelowIt(app, canvas, app.image3_1, 800, 390, "300 Gold")
    drawImageWithSizeBelowIt(app, canvas, app.image4_1, 800, 530, "400 Gold")
    drawImageWithSizeBelowIt(app, canvas, app.image5_1, 800, 660, "500 Gold")

    for monkey in app.monkeyClassList:
        x0, y0 = monkey.cx, monkey.cy
        row, col = getCell(app, x0, y0)
        x1,y1,x2,y2 = getCellBounds(app, row, col)
        if getCell(app, x1 ,y1) in app.selection:
            pass
        else:
            canvas.create_image(x1 + app.margin ,y1 + app.margin/2, image=ImageTk.PhotoImage(monkey.image))

def drawHealthBox(app, canvas):
    canvas.create_rectangle(30, 730, 250 ,814, fill = "ivory")
    if app.health <= 30:
        canvas.create_text(140, 772, font = "Helvetica 22 bold", 
                             text = ("Health:", app.health), fill = "red")
    else: 
        canvas.create_text(140, 772, font = "Helvetica 22 bold", 
                             text = ("Health:", app.health))

def drawStartPauseForfeitButtons(app, canvas):
    canvas.create_rectangle(290, 743, 424 ,800, fill = "beige")
    canvas.create_rectangle(424, 743, 558 ,800, fill = "beige")
    canvas.create_rectangle(558, 743, 692 ,800, fill = "beige")
    canvas.create_rectangle(742, 726, 852, 813, fill = "beige")

    canvas.create_text(357, 771, font = "Helvetica 22 bold", 
                             text = ("Start"), fill = "green")
    canvas.create_text(491, 771, font = "Helvetica 20 bold", 
                             text = ("To Pause\nClick Ctrl-p"), fill = "gold")
    canvas.create_text(625, 771, font = "Helvetica 20 bold", 
                             text = ("To Forfeit\nClick Ctrl-q"), fill = "red")
    canvas.create_text(797, 771, font = "Helvetica 16 bold", 
                             text = ("Gold:", app.gold), fill = "royalblue")

def isComplete(app):
    if len(app.selection) ==0:
        return False
    lastRow, lastCol = app.selection[-1]
    return (len(app.selection) >= 24 and (lastRow>= 14 or lastRow<=0 or lastCol >= 14 or lastCol <=0))
        
def getNextStep(app, startRow, startCol):
    moves = [   [(startRow+1, startCol), (startRow+2, startCol), (startRow+3, startCol)], 
                [(startRow-1, startCol), (startRow-2, startCol), (startRow-3, startCol)], 
                [(startRow, startCol+1), (startRow, startCol+2), (startRow, startCol+3)],
                [(startRow, startCol-1), (startRow, startCol-2), (startRow, startCol-3)] ]
    random.shuffle(moves)
    return moves


def randomMap(app):
    if isComplete(app):
        return True
    startRow, startCol = app.selection[-1]
    nextStep = getNextStep(app, startRow, startCol)
    for move in nextStep:
        if isValid(app, move):
            app.selection += move
            if randomMap(app):
                return True
            app.selection = app.selection[:-3]
            if len(app.selection) % 3 == 1:
                app.selection.pop()
            elif  len(app.selection) % 3 == 2:
                app.selection = app.selection[:-2]
    return False


def isValid(app, move):
    for (row, col) in move:
        if ((row, col) in app.selection):
            return False
        elif len(app.selection)<= 21 and (row < 0 or row >14 or col < 0 or col > 14):
            return False
    return True


def getStartTile(app):
    startRow = random.randint(0,14)
    if startRow == 0 or startRow == 14:
        startCol = random.randrange(0,15,14)
    else:
        startCol = random.randrange(0,15,14)

    if not ((startRow ==0 and startCol ==0) or (startRow ==0 and startCol ==14) 
        or (startRow ==14 and startCol ==0) or (startRow ==14 and startCol ==14)):
        app.selection += [(startRow, startCol)]
        if findUpDownLeftRight(startRow, startCol) == "down":
            app.selection.extend([(startRow+1, startCol), (startRow+2, startCol)])
        elif findUpDownLeftRight(startRow, startCol) == "up":
            app.selection.extend([(startRow-1, startCol), (startRow-2, startCol)])
        elif findUpDownLeftRight(startRow, startCol) == "right":
            app.selection.extend([(startRow, startCol+1), (startRow, startCol+2)])
        elif findUpDownLeftRight(startRow, startCol) == "left":
            app.selection.extend([(startRow, startCol-1), (startRow, startCol-2)])
    else:
        getStartTile(app)
    
                
def findUpDownLeftRight(row, col):
    if row == 0 and (col >0 and col < 14):
        return "down"
    elif row == 14 and (col >0 and col < 14):
        return "up"
    elif (row>0 and row<14) and col ==0:
        return "right"
    elif (row>0 and row<14) and col == 14:
        return "left"

        

def gameMode_timerFired(app): 
    app.currentlyFiring = { "dartMonkey": False,
                            "caveMonkey": False,
                            "wizardMonkey": False,
                            "squirtMonkey": False,
                            "doubleGunMonkey": False  }
    if app.gameOver == False:
        #Projectile location
        for p in app.projectile:
            if p.c == 0:
                if p.target in app.balloons:
                    app.balloons.remove(p.target)
                    app.gold += 20
                app.projectile.remove(p)
            p.c -= .5
            p.cx += p.ix
            p.cy += p.iy

        app.counter += 1
        app.redCounter += 1
        app.blueCounter += 1
        app.blackCounter += 1
        app.balloonAlgorith += 1

        if app.counter == 10:
            app.counter = 0
        if app.redCounter == 10:
            app.redCounter = 0
        if app.blueCounter == 7:
            app.blueCounter = 0
        if app.blackCounter == 5:
            app.blackCounter = 0
        if (app.counter == 0 or app.redCounter == 0 or app.blueCounter == 0 or app.blackCounter == 0) and app.status== "creatingMonkey":
            spawnBalloon(app)
            for balloon in app.balloons:
                if (balloon.color == "red" and app.redCounter == 0) \
                    or (balloon.color == "blue" and app.blueCounter == 0) \
                    or (balloon.color == "black" and app.blackCounter == 0):
                    # total health lowering
                    if balloon.i + 1 == len(app.selection):
                        app.balloons.remove(balloon)
                        app.health -= 7
                        if app.health <= 0:
                            app.health = 0
                            if app.health == 0:
                                app.gameOver = True
                    #moving balloon on the path
                    else:
                        (x1, y1) = app.selection[balloon.i + 1]
                        (x0, y0) = app.selection[balloon.i]
                        balloon.cx = x0
                        balloon.cy = y0
                        #x movement
                        if x0 > x1:
                            balloon.xMove = -1
                        elif x0 == x1:
                            balloon.xMove = 0
                        else:
                            balloon.xMove = 1
                        if y0 > y1:
                            balloon.yMove = -1
                        elif y0 == y1:
                            balloon.yMove = 0
                        else:
                            balloon.yMove = 1
                        balloon.i = balloon.i + 1

        app.dartMonkeyCounter += 1
        app.caveMonkeyCounter += 1
        app.wizardMonkeyCounter += 1
        app.squirtMonkeyCounter += 1
        app.doubleGunMonkeyCounter += 1

        if app.dartMonkeyCounter == 20:
            app.dartMonkeyCounter = 0
            app.currentlyFiring["dartMonkey"] = True
        
        if app.caveMonkeyCounter == 30:
            app.caveMonkeyCounter = 0
            app.currentlyFiring["caveMonkey"] = True

        if app.wizardMonkeyCounter == 20:
            app.wizardMonkeyCounter = 0
            app.currentlyFiring["wizardMonkey"] = True

        if app.squirtMonkeyCounter == 50:
            app.squirtMonkeyCounter = 0
            app.currentlyFiring["squirtMonkey"] = True

        if app.doubleGunMonkeyCounter == 10:
            app.doubleGunMonkeyCounter = 0
            app.currentlyFiring["doubleGunMonkey"] = True

    fireMonkey(app)
        
        
#Interaction and Dart Throwing
def fireMonkey(app):
    currentImages = []
    for m in app.currentlyFiring:
        b = app.currentlyFiring[m]
        if b:
            currentImages.append(app.imagesDict[m])
    for monkey in app.monkeyClassList:
        if monkey.image in currentImages:
            t = findTargetBalloon(app, monkey)
            if t == None:
                return 
            else:
                throwDart(app, monkey, t)

def findTargetBalloon(app, monkey):
    for balloon in app.balloons:
        bx = balloon.cx
        by = balloon.cy 
        (monkeyRow, monkeyCol) = getCell(app, monkey.cx, monkey.cy)
        d = math.sqrt((bx - monkeyRow)**2 + (by - monkeyCol)**2)
        if d < monkey.r:
            return balloon
    return None

def throwDart(app, monkey, t):
    bx = t.cx
    by = t.cy
    (monkeyRow, monkeyCol) = getCell(app, monkey.cx, monkey.cy)
    dx = abs(monkeyRow - bx)
    dy = abs(monkeyCol - by)
    
    if (dy == 0):
        iy = monkey.projectileSpeed
        ix = 0
        c = dx
    elif (dx == 0):
        iy = 0
        ix = -1 * monkey.projectileSpeed
        c = dy
    else:
        x = math.atan(dx/dy)
        if (by < monkeyCol): 
            x += math.pi
        distance = math.sqrt(((dx)**2 + (dy)**2))
        c = distance//monkey.projectileSpeed
        ix = monkey.projectileSpeed * math.cos(x)
        iy = monkey.projectileSpeed * math.sin(x)
    
    app.projectile.append(Projectile(monkey.cx, monkey.cy, 7, "black", ix, iy, c,t))

        
def drawDarts(app, canvas):
    for p in app.projectile:
        canvas.create_oval(p.cx - p.r , p.cy - p.r, p.cx + p.r, p.cy + p.r, fill = p.color)
    
   
def spawnBalloon(app):
    if app.status == "creatingMonkey" and app.counter == 0:
        (x,y) = app.selection[0]

        randomNum = random.randint(0,9)

        if 0 <= app.balloonAlgorith <= 40:
            if 0 <= randomNum <= 4: 
                balloon = Balloon(x, y, 10, 1, 0, "red", 0, 0)
            elif 5 <= randomNum <= 8:
                balloon = Balloon(x, y, 10, 1.5, 0, "blue", 0, 0)
            elif randomNum == 9:
                balloon = Balloon(x, y, 10, 2, 0, "black", 0, 0)
            app.balloons += [balloon]

        elif  41<= app.balloonAlgorith <= 80:
            if 0 <= randomNum <= 3: 
                balloon = Balloon(x, y, 10, 1, 0, "red", 0, 0)
            elif 4 <= randomNum <= 6:
                balloon = Balloon(x, y, 10, 1.5, 0, "blue", 0, 0)
            elif 7 <= randomNum <= 9:
                balloon = Balloon(x, y, 10, 2, 0, "black", 0, 0)
            app.balloons += [balloon]
        
        elif  app.balloonAlgorith >= 81: 
            if 0 <= randomNum <= 2: 
                balloon = Balloon(x, y, 10, 1, 0, "red", 0, 0)
            elif 3 <= randomNum <= 5:
                balloon = Balloon(x, y, 10, 1.5, 0, "blue", 0, 0)
            elif 6 <= randomNum <= 9:
                balloon = Balloon(x, y, 10, 2, 0, "black", 0, 0)
            app.balloons += [balloon]
        

def drawBalloon(app, canvas):
    for balloon in app.balloons:
        (x0, y0, x1, y1) = getCellBounds(app, balloon.cx, balloon.cy)
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        if balloon.color == "red":
            xOffset = balloon.xMove * ((app.redCounter + 1)/10) * 44
            yOffset = balloon.yMove * ((app.redCounter + 1)/10) * 48
        elif balloon.color == "blue":
            xOffset = balloon.xMove * ((app.blueCounter + 1)/7) * 44
            yOffset = balloon.yMove * ((app.blueCounter + 1)/7) * 48
        elif balloon.color == "black":
            xOffset = balloon.xMove * ((app.blackCounter + 1)/5) * 44
            yOffset = balloon.yMove * ((app.blackCounter + 1)/5) * 48

        canvas.create_oval(
            cx - balloon.r + yOffset,
            cy - balloon.r + xOffset,
            cx + balloon.r + yOffset, 
            cy + balloon.r + xOffset, 
            fill = balloon.color)
        
def drawGameOver(app, canvas):
    if app.gameOver:

        canvas.create_rectangle(0, 375, 900, 525, fill = "white")
        canvas.create_text(app.height//2, app.width//2, font = "Helvetica 50 bold", 
                             text = ("Game Over"))


def startScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2 + 15 , app.height/2, image=ImageTk.PhotoImage(app.screenImage1))
    canvas.create_rectangle(300, 640, 600, 730, fill = "lightblue")
    canvas.create_rectangle(360, 750, 540, 820, fill = "lightblue")
    canvas.create_text(450, 685, font = "Helvetica 20 bold", 
                             text = ("Press Any Key To Start Game"))
    canvas.create_text(450, 785, font = "Helvetica 12 bold", 
                             text = ("Press 'I' Key For Instructions"))                          


def startScreenMode_keyPressed(app, event):
    if event.key == "i":
        app.mode = "helpMode"
    else:
        app.mode = 'gameMode'


def helpMode_redrawAll(app, canvas):
    margin = 28
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "deepskyblue")
    canvas.create_rectangle(140, 110, 740, 725, fill = "skyblue", width = "7")
    canvas.create_text(440, 110 + margin, font = "Helvetica 30 bold", 
                             text = ("Instructions"))
    canvas.create_text(220 + margin, 220 + margin, font = "Helvetica 24 bold", 
                             text = ("How To Play:"))
    canvas.create_text(400 + margin, 400 + margin, font = "Helvetica 16 bold", 
                             text = ("- Maps / Paths where balloons travel on are automatically created\n- To generate a new random path press 'R' key \n- To create a map yourself by dragging mouse, press 'S' Key\n- Click 'Start' button at the bottom and balloons will generate \n- Place a monkey by clicking on the monkey, and then position\n on board. If the position is legal, a monkey will be placed\n- No monkey can be placed on the balloons path\n- Monkeys are placed if gold is enough, displayed at bottom right\n- For every balloon popped, the gold is increased which can be used\n to buy more monkeys and added to board\n- Monkeys have different costs and different abilities\n- Dart Monkey: Cost -> 200 Gold, Range -> 2 Tiles, Speed -> Medium\n- Cave Monkey: Cost -> 300 Gold, Range -> 3 Tiles, Speed -> Medium\n- Wizard Monkey: Cost -> 400 Gold, Range -> 3 Tiles, Speed -> Fast\n- Squirt Monkey: Cost -> 500 Gold, Range -> Anywhere, Speed -> Slow\n- Double Gun Monkey: Cost -> 600 Gold, Range -> 2, Speed -> Very Fast"))

def helpMode_keyPressed(app, event):
    app.mode = "startScreenMode"

def gameMode_redrawAll(app, canvas):
    drawBoardwithMonkeys(app, canvas)
    drawHealthBox(app, canvas)
    drawStartPauseForfeitButtons(app, canvas)
    drawBalloon(app, canvas)
    drawGameOver(app, canvas)
    drawDarts(app,canvas)

runApp(width = 900, height = 900)