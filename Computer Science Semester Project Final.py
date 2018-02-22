import Draw
import random
import math

#Added method intersects and distance to HW module Rectangle
import Rectangle
    
# global dictionary and lists to remember the state of the board    
saveBuildings = [[] for j in range(10)]
saveWindows = {}
saveMonkey = []

#re-draws the gameboard, if no parameters given, then chooses a new board
def drawBoard(bananaX =0, bananaY=0):
    global saveBuildings
    global saveWindows
    global saveMonkey  
    LIME = Draw.color(174, 255, 0)   
    colors = [Draw.CYAN, Draw.ORANGE, LIME, Draw.PINK, Draw.VIOLET]
    windowColor = [Draw.WHITE, Draw.GRAY]
    buildingNumber = 10
    buildingWidth = 100
    buildingHeight = 400
    buildingYNumbers = []
    #Draws buildings
    for i in range(buildingNumber):
        if saveBuildings[i] == []:
            colorChoice = random.choice(colors)
            buildingY = random.randint (200, 500)
            buildingYNumbers += [buildingY]
            saveBuildings[i] = [buildingY, colorChoice]            
        else:
            colorChoice = saveBuildings[i][1]
            buildingY = saveBuildings[i][0]
            buildingYNumbers += [buildingY]
        Draw.setColor(colorChoice)
        Draw.filledRect((i*buildingWidth), buildingY, buildingWidth, \
        buildingHeight)
        Draw.setColor(Draw.BLACK)
        Draw.rect((i*buildingWidth), buildingY, buildingWidth, buildingHeight)        
        # Draws Windows
        nextWindow = 0
        nextLine = 0
        centerWindows = 5
        for k in range(22):    
            for j in range(5):
                if (k, j) not in saveWindows:
                    colorChoiceWindow = random.choice(windowColor)
                    saveWindows[(k, j)] = colorChoiceWindow                    
                    
                else:
                    colorChoiceWindow = saveWindows[(k, j)]
                Draw.setColor(colorChoiceWindow)
                Draw.filledRect((i*buildingWidth)+centerWindows+nextWindow, \
                buildingY+centerWindows+nextLine, 10, 10)
                nextWindow = j*20
                
            nextLine = 20*k 
    
    #Draws Monkeys
    computerMonkeyChooser, computerBananaX, computerBananaY, computerMonkeyArea\
        = drawMonkeyBanana("computer", buildingWidth, buildingYNumbers, bananaX, \
        bananaY) 
    userMonkeyChooser, userBananaX, userBananaY, userMonkeyArea = \
        drawMonkeyBanana("user", buildingWidth, buildingYNumbers, bananaX, bananaY) 
    
    
    saveMonkey = [computerMonkeyChooser, userMonkeyChooser]
    
    #draws the sun
    sun(500, 25)    
    
    return userBananaX, userBananaY, computerBananaX, computerBananaY, \
           userMonkeyArea, computerMonkeyArea   

#draws the monkey and banana for both user and computer
def drawMonkeyBanana(case, buildingWidth, buildingYNumbers, bananaX, bananaY): 
    global saveMonkey
    
    monkeyHeight = 96
    monkeyWidth = 80
    bananaOffSetX = 40
    bananaOffSetY = 35 
    
    #draws computer monkey on one of the last 3 buildings randomly
    if case == "computer":
        if saveMonkey == []:
            #choose new monkey position
            monkeyChooser = random.randint(7, 9)
        else:
            #restore previous monkey position
            monkeyChooser = saveMonkey[0]
            
    #draws user monkey on one of the first 3 buildings randomly    
    else:
        if saveMonkey == []:
            #choose new monkey position
            monkeyChooser = random.randint(0, 2)
        else:  
            #restore previous monkey position
            monkeyChooser = saveMonkey[1]
    
    # draw the banana y coordinate based on the new monkey position
    if bananaX == 0:
        bananaX = monkeyChooser*buildingWidth + bananaOffSetX
    #else: keep bananaX, don't change banana position
    
    # draw the banana y coordinate based on the new monkey position
    if bananaY == 0:
        bananaY = buildingYNumbers[monkeyChooser] - monkeyHeight + bananaOffSetY
    #else: keep bananaX, don't change banana position 
                
    #compute the coordinates of the monkey
    monkeyX = monkeyChooser*buildingWidth
    monkeyY = buildingYNumbers[monkeyChooser] - monkeyHeight
    
    #creates area of monkey using Rectangle.py
    monkeyArea = Rectangle.Rectangle(monkeyX+10, monkeyY, monkeyWidth, \
        monkeyHeight)
    
    #draws monkeys and bananas
    banana(bananaX, bananaY)
    monkey(monkeyX, monkeyY)
   
    return monkeyChooser, bananaX, bananaY, monkeyArea
    
# rotate points in a shape
def _rotatePoint(x, y, angle):
    r = math.sqrt(x*x + y*y)
    theta = math.atan2(y, x)
    
    theta += angle
    newx = math.cos(theta) * r
    newy = math.sin(theta) * r
    
    return newx, newy

# draw a filled partial oval
def filledPartialOval(x, y, wide, high, degStart, degEnd, rot):
    coords = []
    rot = math.radians(rot)
    
    for angle in range(degStart, degEnd+1, 1):
        rad = math.radians(angle)
        newx = math.cos(rad) * wide/2
        newy = math.sin(rad) * high/2

        newx, newy = _rotatePoint(newx, newy, rot)
        coords += [x+newx, y-newy]
        
    Draw.filledPolygon(coords)

#defines a banana shape
def banana(x, y):
    
    #draws the banana body in yellow
    Draw.setColor(Draw.YELLOW)
    filledPartialOval(x, y, 50, 100, 200, 300, -30)   
    
    #draws the banana top in brown
    BROWN = Draw.color(130, 82, 1)
    Draw.setColor(BROWN)
    bananaTop = (x-29, y+3, x-27, y+3, x-26, y+7, x-30, y+7)
    Draw.filledPolygon(bananaTop)
    
#defines a monkey shape
def monkey(x, y):
    #set custom color brown
    BROWN = Draw.color(130, 82, 1)
    Draw.setColor(BROWN)
    
    #draws the monkey's arms
    Draw.filledOval(15+x, 35+y, 22, 30)
    Draw.filledOval(61+x, 35+y, 22, 30)
    
    #draws the monkey's body
    Draw.filledRect(33+x, 33+y, 33, 33)
    Draw.filledRect(27+x, 35+y, 6, 7)
    Draw.filledRect(66+x, 35+y, 6, 7)
    
    #draws the monkey's legs
    Draw.filledOval(31+x, 60+y, 36, 35)
    
    #draws the monkey's head
    Draw.filledRect(43+x, 27+y, 14, 6)
    Draw.filledRect(38+x, 12+y, 23, 15)
    
    #defines the shape of the monkey
    Draw.setColor(Draw.BLUE)
    Draw.filledOval(20+x, 42+y, 14, 20)
    Draw.filledOval(64+x, 42+y, 14, 20)
    Draw.filledOval(39+x, 64+y, 20, 26)
    Draw.filledRect(33+x, 87+y, 33, 9)
    Draw.filledRect(33+x, 87+y, 33, 9)
    Draw.filledRect(27+x, 57+y, 6, 9)
    Draw.filledRect(66+x, 57+y, 6, 9)
    
    #draws the monkey's torso
    Draw.setColor(BROWN)
    Draw.filledRect(33+x, 33+y, 33, 33)
    
    #draws the monkey's eyes and eyebrows
    Draw.setColor(Draw.BLACK)
    Draw.filledRect(41+x, 15+y, 17, 2)
    Draw.filledRect(41+x, 19+y, 7, 3)
    Draw.filledRect(51+x, 19+y, 7, 3)

#draws explosion on the monkey that was hit
def monkeyHit(Type, userBananaX, userBananaY, computerBananaX, computerBananaY,\
              computerScore, userScore, inputVelocity, angle, originalUserMonkey,\
              originalComputerMonkey):
    
    #redraw the board for each frame
    Draw.clear()
    scoreBoard(computerScore, userScore)
    userInput(inputVelocity, angle) 
    
    #if the computer monkey was hit
    if Type == "user":
        drawBoard(computerBananaX, computerBananaY) 
        drawBoard(userBananaX, userBananaY)
        
        #draws explosion
        Draw.setColor(Draw.BLUE)
        Draw.filledOval(originalComputerMonkey.getX()-50,\
                        originalComputerMonkey.getY()-50, 200, 200)
        Draw.setColor(Draw.RED)
        Draw.filledOval(originalComputerMonkey.getX(),\
                        originalComputerMonkey.getY(), 100, 100)
    
    #if the user monkey was hit
    elif Type == "computer":        
        drawBoard(userBananaX, userBananaY)
        drawBoard(computerBananaX, computerBananaY)
        
        #draws explosion
        Draw.setColor(Draw.BLUE)
        Draw.filledOval(originalUserMonkey.getX()-50,\
                        originalUserMonkey.getY()-50, 200, 200)
        Draw.setColor(Draw.RED)
        Draw.filledOval(originalUserMonkey.getX(),\
                        originalUserMonkey.getY(), 100, 100)
        
    Draw.show(2000)  

#defines a sun shape
def sun(x, y):
    #Draw.setColor(Draw.ORANGE)
    #triangle = (1,1,1,1)
    #Draw.filledPolygon(triangle)
    
    #draws the sun body
    Draw.setColor(Draw.YELLOW)
    Draw.filledOval(x, y, 30, 30)
    
    #draws the sun's eyes and mouth
    Draw.setColor(Draw.BLUE)
    Draw.filledOval(x+6, y+7, 6, 5)
    Draw.filledOval(x+18, y+7, 6, 5)
    Draw.filledOval(x+7, y+15, 16, 10)
    
    #defines the sun's mouth
    Draw.setColor(Draw.YELLOW)
    Draw.filledRect(x+7, y+15, 17, 5)

#defines the score board in the upper right hand corner    
def scoreBoard(computerScore = 0, userScore = 0):
    Draw.setColor(Draw.BLACK)
    Draw.string("User Score: %s" %userScore, 850, 25)
    Draw.string("Computer Score: %s" %computerScore, 850, 50)
    
#defines the user input area in the upper left hand corner 
def userInput(inputVelocity, angle):
    Draw.setColor(Draw.BLACK)
    Draw.string("Velocity: %s" %inputVelocity, 25, 50)
    Draw.string("Angle: %s" %angle, 25, 25)
    
    return (inputVelocity, angle)

#Displays the winner message
def end(computerScore, userScore):
    if computerScore >= 3:
        winner = "Computer"
        
    elif userScore >= 3:
        winner = "User"  
        
    #draws the game over text with appropriate winner
    Draw.setColor(Draw.BLACK)
    Draw.string("Game Over! %s Wins!" %winner, 200, 25)    

#tells the user if there is a problem with input data
def problem():
    
    #displays the error message
    Draw.setColor(Draw.BLACK)
    Draw.string("Please input a value from 1 to 90 for Velocity and Angle."\
                , 25, 75)
    
#throws the user banana, needs to know complete state of monkeys and bananas for user and computer
def userThrow(inputVelocity, angle, userBananaX, userBananaY, \
    computerBananaX, computerBananaY, computerMonkey, originalUBX, originalUBY, originalUserMonkey, \
    originalCBX, originalCBY, originalComputerMonkey, userScore, computerScore,\
    computerTurn, vdone, adone, computerAngleHigh, computerAngleLow):
        
    #sets the boundaries of the game board
    lowerBorder = 600
    rightBorder = 1100
    
    #variables determining the direction of the throw unit vector
    c = 1
    k = 1
    
    #time step variable
    gameTime = 0
    
    #creates an arbitrary area for user banana
    userBanana = Rectangle.Rectangle(0, 0, 30, 45)
    
    #game is still in play
    gameOver = False
    
    #continue updating position of banana until banana intersects monkey or
    #travels out of bounds
    while (userBananaY <= lowerBorder and userBananaX <= rightBorder) and \
          (not userBanana.intersects(computerMonkey)):
        
        #update time intervals of throw
        gameTime += 0.1
        
        #reverses direction of banana when it exceeds maximum height
        if userBananaY <= 0:
            k = -1  
            
        #initialize throw and update position according to displacment formula
        userBananaX = userBananaX + c * (inputVelocity * gameTime * \
            math.cos(math.radians(angle)))
        userBananaY = userBananaY - k * (inputVelocity * gameTime * \
            math.sin(math.radians(angle)))
        
        #contiunes redrawing the board with each position of the banana
        Draw.clear()
        scoreBoard(computerScore, userScore)
        userInput(inputVelocity, angle) 
        drawBoard(computerBananaX, computerBananaY) 
        drawBoard(userBananaX, userBananaY)
        Draw.show(40)
        
        #creates area of userBanana using Rectangle.py with last position of 
        #userBanana
        userBanana = Rectangle.Rectangle(userBananaX-33, userBananaY+3, 30, 45)
    
    #checks to see if user banana hits computer monkey and updates the score
    if userBanana.intersects(computerMonkey):
        userScore += 1
        
        #displays exploading monkey
        monkeyHit("user", userBananaX, userBananaY, \
            computerBananaX, computerBananaY, computerScore, userScore, \
            inputVelocity, angle, originalUserMonkey, originalComputerMonkey)
        
        #checks if the game is over
        if userScore >= 3 or computerScore >= 3:
            
            #redraws the final state of the board with monkey explosion
            Draw.clear()
            scoreBoard(computerScore, userScore)
            userInput(inputVelocity, angle)
            drawBoard(userBananaX, userBananaY)
            drawBoard(computerBananaX, computerBananaY)
            monkeyHit("user", userBananaX, userBananaY, \
                computerBananaX, computerBananaY, computerScore, userScore, \
                inputVelocity, angle, originalUserMonkey, originalComputerMonkey)
            
            #displays the winner of the game
            end(computerScore, userScore)
            Draw.show(2000)
            
            #ends the game
            gameOver = True
        
        #start new round if game not over and monkey hit
        (inputVelocity, angle, vdone, adone, originalUBX, originalUBY, \
        originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey, computerAngleHigh, computerAngleLow)\
            = newRound(computerScore, userScore, inputVelocity, angle, vdone, adone, computerAngleHigh, computerAngleLow)
        
        #restore banana position for new throw
        (userBananaX, userBananaY, userMonkey, computerBananaX, computerBananaY, \
         computerMonkey) = restoreBananaPosition(originalUBX, originalUBY, \
        originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey) 
        
    #contiune with new throw for same round
    else:
        #sets the computer's turn
        computerTurn = True
        
        #not time for new round
        timeForNewRound = False
    
    #pass game state to the caller
    return userBananaX, userBananaY, computerBananaX, computerBananaY, computerMonkey, \
           originalUBX, originalUBY, originalUserMonkey, \
           originalCBX, originalCBY, originalComputerMonkey, userScore, computerTurn, inputVelocity, \
           angle, vdone, adone, gameOver, computerAngleHigh, computerAngleLow

#throws the computer banana, needs to know complete state of monkeys and bananas for user and computer
def computerThrow(computerVelocity, computerAngle, inputVelocity, \
    angle, computerBananaX, computerBananaY, userBananaX, userBananaY, \
    userMonkey, originalUBX, originalUBY, originalUserMonkey, \
    originalCBX, originalCBY, originalComputerMonkey,\
    userScore, computerScore, vdone, adone, computerAngleHigh, computerAngleLow):

    #sets the boundaries of the game board
    lowerBorder = 600
    leftBorder = -20
    
    #variables determining the direction of the throw unit vector
    c = -1
    k = 1
    
    #time step variable
    gameTime = 0 
    
    #creates an arbitrary area for computer banana
    computerBanana = Rectangle.Rectangle(0, 0, 30, 45)
    
    #initialize distance to maximum value
    minDistance = 10000000000
    
    #determines the new round
    timeForNewRound = True
    
    #game is still in play
    gameOver = False
    
    #continue updating position of banana until banana intersects monkey or
    #travels out of bounds    
    while (int(computerBananaY) <= lowerBorder and int(computerBananaX) >= \
        leftBorder) and (not computerBanana.intersects(userMonkey)):
        
        #update time intervals of throw
        gameTime += 0.1
        
        #reverses direction of banana when it exceeds maximum height
        if computerBananaY <= 0:
            k = -1
            
        #initialize throw and update position according to displacment formula    
        computerBananaX = computerBananaX + c * (computerVelocity * gameTime * \
            math.cos(math.radians((computerAngleHigh + computerAngleLow)/2)))
        computerBananaY = computerBananaY - k * (computerVelocity * gameTime * \
            math.sin(math.radians((computerAngleHigh + computerAngleLow)/2)))
        
        #contiunes redrawing the board with each position of the banana
        Draw.clear()
        scoreBoard(computerScore, userScore)
        userInput(inputVelocity, angle)
        drawBoard(userBananaX, userBananaY)
        drawBoard(computerBananaX, computerBananaY)
        Draw.show(40)
        
        #creates area of computerBanana using Rectangle.py with last position of 
        #computerBanana     
        computerBanana = Rectangle.Rectangle(computerBananaX-33, \
                                                 computerBananaY+3, 30, 45)
        
        #Computer Strategy
        #Computes the distance from computerbanana to usermonkey
        distance = computerBanana.distance(userMonkey)
        
        #Finds the minimum distance from computerbanana to usermonkey
        if distance < minDistance:
            minDistance = distance
            closestComputerBananaX = computerBananaX

    #Binary Search on last computer angle
    computerAngle = (computerAngleHigh + computerAngleLow)/2
    
    #determine under or over throw based on closest x position of banana
    #using Rectangle.py method for center of monkey area x coordinate
    if closestComputerBananaX < userMonkey.getCenterX():
        #Banana over thrown-increase angle
        computerAngleLow = computerAngle
    else:
        #Banana under thrown-decrease angle
        computerAngleHigh = computerAngle
    
    #checks to see if computer banana hits user monkey and updates the score
    if computerBanana.intersects(userMonkey):
        computerScore += 1 
        
        #displays exploading monkey
        monkeyHit("computer", userBananaX, userBananaY, \
            computerBananaX, computerBananaY, computerScore, userScore, \
            inputVelocity, angle, originalUserMonkey, originalComputerMonkey)
        
        #checks if the game is over
        if userScore >= 3 or computerScore >= 3:
            
            #redraws the final state of the board with monkey explosion
            Draw.clear()
            scoreBoard(computerScore, userScore)
            userInput(inputVelocity, angle)
            drawBoard(userBananaX, userBananaY)
            drawBoard(computerBananaX, computerBananaY)
            monkeyHit("computer", userBananaX, userBananaY, \
                computerBananaX, computerBananaY, computerScore, userScore, \
                inputVelocity, angle, originalUserMonkey, originalComputerMonkey)
            
            #displays the winner of the game
            end(computerScore, userScore)
            Draw.show(2000)            
            
            #ends the game
            gameOver = True        
        
        #start new round if game not over and monkey hit
        (inputVelocity, angle, vdone, adone, originalUBX, originalUBY, \
        originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey, computerAngleHigh, computerAngleLow)\
            = newRound(computerScore, userScore, inputVelocity, angle, vdone, adone, computerAngleHigh, computerAngleLow)
        
        #restore banana position for new throw
        (userBananaX, userBananaY, userMonkey, computerBananaX, computerBananaY, \
         computerMonkey) = restoreBananaPosition(originalUBX, originalUBY, \
        originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey)
        
    #contiune with new throw for same round    
    else:
        #not time for new round
        timeForNewRound = False   
    
    #pass game state to the caller
    return userBananaX, userBananaY, userMonkey, computerBananaX, \
           computerBananaY, originalUBX, originalUBY, originalUserMonkey, \
           originalCBX, originalCBY, originalComputerMonkey,\
           computerScore, inputVelocity, \
           angle, vdone, adone, timeForNewRound, gameOver, computerAngleHigh, computerAngleLow, computerAngle 

#Save starting position of banana and monkey when board is created, so during 
#continue round monkey will start from the same place
def saveBananaPosition(userBananaX, userBananaY, userMonkey, computerBananaX, \
                       computerBananaY, computerMonkey):
   
    (originalUBX, originalUBY, originalUserMonkey, originalCBX, originalCBY, \
     originalComputerMonkey) = (userBananaX, userBananaY, userMonkey, computerBananaX, \
                       computerBananaY, computerMonkey)
    
    return (originalUBX, originalUBY, originalUserMonkey, originalCBX, originalCBY, \
     originalComputerMonkey)

#Restore position of banana for next throw so that banana originates from monkey
#and not final position of last throw
def restoreBananaPosition(originalUBX, originalUBY, originalUserMonkey, \
                          originalCBX, originalCBY, originalComputerMonkey):
    
    (userBananaX, userBananaY, userMonkey, computerBananaX, computerBananaY, \
     computerMonkey) = (originalUBX, originalUBY, originalUserMonkey, \
                        originalCBX, originalCBY, originalComputerMonkey)
    
    return (userBananaX, userBananaY, userMonkey, computerBananaX, computerBananaY, \
     computerMonkey)

#resets all the parameters for a new throw
def continueRound(computerScore, userScore, inputVelocity, angle, originalUBX, \
                  originalUBY, originalUserMonkey, originalCBX, originalCBY, \
                  originalComputerMonkey):
    
    #Restore position of banana for next throw so that banana originates from monkey
    #and not final position of last throw
    (userBananaX, userBananaY, userMonkey, computerBananaX, computerBananaY, \
     computerMonkey) = restoreBananaPosition(originalUBX, originalUBY, \
        originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey)  
    
    #clears the inputs for user banana angle and velocity
    inputVelocity = ""
    angle = "" 
    
    #redraws the saved board with the initial banana positions
    Draw.clear()
    drawBoard()
    Draw.setBackground(Draw.BLUE)
    scoreBoard(computerScore, userScore)
    userInput(inputVelocity, angle)
    drawBoard()
    
    #pass game state to the caller
    return (inputVelocity, angle, userBananaX, userBananaY, userMonkey, \
            computerBananaX, computerBananaY, computerMonkey)

#redraws the board and saves it for a new round
def newRound(computerScore, userScore, inputVelocity, angle, vdone, adone, \
             computerAngleHigh, computerAngleLow):
    
    global saveBuildings
    global saveWindows
    global saveMonkey
    
    #clears the current saved board
    saveBuildings = [[] for j in range(10)]
    saveWindows = {}
    saveMonkey = []
    
    #clears the inputs for user banana angle and velocity
    inputVelocity = ""
    angle = "" 
    
    #allows the user to type new inputs
    adone = False
    vdone = False 
    
    #resets the computer strategy for each new round
    computerAngleHigh = 90
    computerAngleLow = 0      
    
    #picks a new board
    Draw.clear()
    Draw.setBackground(Draw.BLUE)
    scoreBoard(computerScore, userScore)
    userInput(inputVelocity, angle)
    userBananaX, userBananaY, computerBananaX, computerBananaY, userMonkey, \
        computerMonkey = drawBoard()
    
    #Save starting position of banana and monkey when board is created, so during 
    #continue round monkey will start from the same place    
    (originalUBX, originalUBY, originalUserMonkey, originalCBX, originalCBY, \
     originalComputerMonkey) = saveBananaPosition\
        (userBananaX, userBananaY, userMonkey, computerBananaX, \
         computerBananaY, computerMonkey)       
    
    #pass game state to the caller
    return (inputVelocity, angle, vdone, adone, originalUBX, originalUBY, \
        originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey, \
        computerAngleHigh, computerAngleLow)

#creates the instructions page
def startPage():
    
    #the game has not begun
    gameStart = False
    
    #if the game didn't start yet
    while not gameStart:
        
        #check for mouse clicks and set the x and y mouse values to variables
        if Draw.mousePressed():
            newX = Draw.mouseX()
            newY = Draw.mouseY()
            
            #check if the user has clicked the start button
            if  (newX >= 415 and newX <= 445) or (newY >= 500 and newX <= 570):
                gameStart = True
                
        #redraws the board with every mouse click
        Draw.clear()
        Draw.setFontSize(45)
        Draw.setColor(Draw.BLACK)
        Draw.string("Welcome to Monkey Banana!", 95, 25)  
        
        #fun decorations for the start page
        for i in range(1, 25, 2):
            banana(50, 25 * i)
            
        monkey(650, 490)
        monkey(750, 490)
        
        #draws the game instructions
        Draw.setFontSize(15)
        Draw.setColor(Draw.BLACK)
        Draw.string("Instructions:\n\n Object: The object of the game is to hit the computer monkey on the right three times using your \n banana which is found in the user monkey's hand on the left. The banana follows a trajectory of \n displacement according to the velocity and angle you enter.\n\n To play: When prompted in the upper left-hand corner for angle or velocity, type any number \n between 1 and 90. You may change your answer by using the backspace key. However, once \n the enter key is pressed you cannot change your angle or velocity value until the next prompt. \n Once you have pressed enter for the second time, indicating you are finished typing velocity, \n the monkey will launch the banana. When your throw is finished, the computer will launch its \n banana at your user monkey. \n\n Score: When the user banana hits the computer monkey or when the computer banana hits the user \n monkey the correct side will earn one point shown on the scoreboard in the upper right-hand corner. \n The game is over when either side reaches 3 hits. \n\n Click start to begin!", 100, 100)        
        
        #draws the start button
        Draw.setColor(Draw.ORANGE)
        Draw.filledRect(415, 500, 130, 70)
        
        #draws the start text
        Draw.setFontSize(25)
        Draw.setColor(Draw.BLACK)
        Draw.string("Start!", 440, 515)        
        
        Draw.show() 
        
    return gameStart

#main function defined for each game played     
def main():
    
    #draws the canvas and sets background color
    Draw.setCanvasSize(1000, 600) 
    Draw.setBackground(Draw.BLUE)
   
    #Start page
    gameStart = startPage()
    
    #sets the font size back to the correct size
    Draw.setFontSize(12)
    
    #when the game starts
    if gameStart:    
        
        #draws the scoreboard and user input area
        Draw.clear()
        scoreBoard()
        userInput("","")
        Draw.show()
        
        #draws the initial board and returns initial positions of monkey and banana
        userBananaX, userBananaY, computerBananaX, computerBananaY, userMonkey, \
            computerMonkey = drawBoard()
        
        #Save starting position of banana and monkey when board is created, so during 
        #continue round monkey will start from the same place  
        (originalUBX, originalUBY, originalUserMonkey, originalCBX, originalCBY, \
         originalComputerMonkey) = saveBananaPosition\
            (userBananaX, userBananaY, userMonkey, computerBananaX, \
             computerBananaY, computerMonkey)
        
        #sets the initial angle and velocity for the user
        inputVelocity = ""
        angle = ""
        
        #start user typing
        adone = False
        vdone = False
        
        #the game is not over
        gameOver = False
        
        #it is not the computer turn
        computerTurn = False
        
        #the initial score for user and computer is 0
        userScore = 0
        computerScore = 0  
        
        #the initial values for the computer angle and velocity
        computerVelocity = 20
        computerAngle = 45 
        computerAngleHigh = 90
        computerAngleLow = 0      
        
        #forever, until a game is over, are we done yet?
        while not gameOver:
            #if the next key has been typed
            if Draw.hasNextKeyTyped():
                
                #set that key to variable key
                key = Draw.nextKeyTyped()
                
                #if the enter key has been typed
                if key == "Return":
                    
                    #if the user is done typing check the values of angle
                    if not adone:
                        #check the values of angle
                        #if empty set to 0
                        if angle == "":
                            angle = "0" 
                            
                        #the user is done typing the angle
                        adone = True
                    
                    #if the user is done typing the angle and the velocity
                    elif adone and not vdone:
                        #check the values of velocity
                        #if empty set to 0                        
                        if inputVelocity == "":
                            inputVelocity = "0"
                            
                        #the user is done typing the velocity
                        vdone = True
                        
                    #if both values are entered and the function is ready to initialize
                    if vdone and adone:
                        
                        #check the range of the input for angle and velocity
                        #if the values for angle and velocity are out of range
                        if int(angle) == 0 or int(inputVelocity) == 0 or \
                           int(angle) > 90 or int(inputVelocity) > 90:
                            
                            #clear the canvas
                            Draw.clear()
                            
                            #restart user typing
                            adone = False
                            vdone = False
                            
                            #clears the inputs for user banana angle and velocity
                            inputVelocity = ""
                            angle = "" 
                            
                            #redraws the board with the error message
                            Draw.setBackground(Draw.BLUE)              
                            scoreBoard(computerScore, userScore)
                            userInput(inputVelocity, angle) 
                            
                            #error message
                            problem()
                            
                            drawBoard()
                            Draw.show(2000)
                        
                        #if the user angle and velocity are in range
                        else:
                            #Restore position of banana for next throw so that banana originates from monkey
                            #and not final position of last throw                            
                            (userBananaX, userBananaY, userMonkey, computerBananaX, computerBananaY, \
                              computerMonkey) = restoreBananaPosition(originalUBX, originalUBY, \
                              originalUserMonkey, originalCBX, originalCBY, originalComputerMonkey)
                            
                            #Completes the user throw, checks for new rounds,
                            #continuing rounds, banana intersection, ends game,
                            #switches to computer turn
                            #updates the game state
                            (userBananaX, userBananaY, computerBananaX,\
                             computerBananaY, computerMonkey, \
                            originalUBX, originalUBY, originalUserMonkey, \
                               originalCBX, originalCBY, originalComputerMonkey,\
                               userScore, computerTurn, inputVelocity, angle, vdone,\
                               adone, gameOver, \
                               computerAngleHigh, computerAngleLow) = userThrow\
                                (int(inputVelocity), int(angle), userBananaX, \
                                 userBananaY, computerBananaX, computerBananaY, \
                                 computerMonkey, originalUBX, originalUBY,\
                                 originalUserMonkey, \
                                 originalCBX, originalCBY, originalComputerMonkey,\
                                 userScore, computerScore, computerTurn, \
                                 vdone, adone, computerAngleHigh, computerAngleLow)
                            
                #if the user is not finished typing the angle
                elif not adone:
                    #if the key typed was backspace
                    if key == "BackSpace":
                        #slice the last character off of the string angle
                        angle = angle[:-1] 
                        
                    #if the key is not a digit
                    elif not key.isdigit():
                       #don't allow the key to be added to the string
                        pass
                    
                    #if the key is a digit
                    else: 
                        #add the last key typed to the string angle
                        angle += key
                        
                #if the user is finished typing the angle but not the velocity   
                else: 
                    #if the key typed was backspace
                    if key == "BackSpace":
                        #slice the last character off of the string velocity
                        inputVelocity = inputVelocity[:-1] 
                        
                    #if the key is not a digit    
                    elif not key.isdigit():
                        #don't allow the key to be added to the string
                        pass
                    
                    #if the key is a digit
                    else:
                        #add the last key typed to the string velocity
                        inputVelocity += key                       
                        
                #Redraws the board after every key typed
                Draw.clear()
                Draw.setBackground(Draw.BLUE)              
                scoreBoard(computerScore, userScore)
                userInput(inputVelocity, angle) 
                drawBoard()
                Draw.show()
                
            # when it is the computer's turn
            elif computerTurn:
                
                #Completes the computer throw, checks for new rounds,
                #continuing rounds, banana intersection, ends game,
                #computes the computer strategy
                #updates the game state               
                (userBananaX, userBananaY, userMonkey, computerBananaX, \
                    computerBananaY, originalUBX, originalUBY, originalUserMonkey, \
                    originalCBX, originalCBY, originalComputerMonkey,\
                    computerScore, inputVelocity, \
                    angle, vdone, adone, timeForNewRound, gameOver, computerAngleHigh, \
                    computerAngleLow, computerAngle) = computerThrow(computerVelocity, \
                    computerAngle, inputVelocity, angle, computerBananaX, computerBananaY, \
                    userBananaX, userBananaY, userMonkey, originalUBX, originalUBY,\
                    originalUserMonkey, \
                    originalCBX, originalCBY, originalComputerMonkey, userScore,\
                    computerScore, \
                    vdone, adone, computerAngleHigh, computerAngleLow) 
                       
                #after the computer's turn 
                computerTurn = False
                
                #when computerBanana finishes throwing and no intersection let 
                #user try again, continues the round          
                if  not timeForNewRound:
                    (inputVelocity, angle, userBananaX, userBananaY, userMonkey, \
                     computerBananaX, computerBananaY, computerMonkey) = \
                        continueRound(computerScore, userScore, inputVelocity, \
                           angle, originalUBX, originalUBY, originalUserMonkey, \
                           originalCBX, originalCBY, originalComputerMonkey)
                    
                #restart user typing  
                adone = False
                vdone = False                        
      
main()
