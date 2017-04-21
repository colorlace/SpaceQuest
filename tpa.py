from Tkinter import *
from math import *
import random

#FALLING OBJECT CLASSES#########################################################
class Asteroid(object):
    def __init__(self,c_width,asteroidSpeedList):
        self.r = random.randint(5,20) #random size
        self.cy = -20 #start above screen
        self.cx = random.randint(0, c_width) #random x on canvas width
        i = random.randint(0,len(asteroidSpeedList)-1)
        self.yVelocity = asteroidSpeedList[i]
        self.fill = "saddlebrown"

class Bullet(object):
    def __init__(self,startX,startY,xDir,color):
        self.cx = startX
        self.cy = startY
        self.height = 10
        self.width = 4
        self.outline = color
        self.fill = color

class EnemyBullet(Bullet):
    def __init__(self,startX,startY,xDir,color):
        super(EnemyBullet,self).__init__(startX,startY,xDir,color)
        self.xDir = xDir

class Explosion(object):
    def __init__(self, cx, cy, fill1="firebrick",fill2="orange",fill3="yellow"):
        self.cx = cx
        self.cy = cy
        self.r1,self.r2,self.r3 = 1,1,1
        self.fill1 = fill1
        self.fill2 = fill2
        self.fill3 = fill3

class Title(object):
    def __init__(self,c_width,c_height,currentLevel):
        self.cx = c_width/2
        self.cy = c_height/2
        self.font, self.size, self.typeface = "Helvetica", 62, "bold"
        
class GameOver(Title):
    def __init__(self,c_width,c_height,currentLevel):
        super(GameOver,self).__init__(c_width,c_height)
        self.text = ("Game Over")
        self.fill = "red"
        
class LevelingUpTitle(Title):
    def __init__(self,c_width,c_height,currentLevel):
        super(LevelingUpTitle,self).__init__(c_width,c_height,currentLevel)
        self.text = ("Level %d" % currentLevel)
        self.fill = "green"

class BossLevel(Title):
    def __init__(self,c_width,c_height,currentLevel):
        super(BossLevel,self).__init__(c_width,c_height,currentLevel)
        self.text = "ALERT: \n incoming threat"
        self.fill = "red"
        self.size = 45

class BossLevelText(Title):
    def __init__(self,c_width,c_height,currentLevel):
        super(BossLevelText,self).__init__(c_width,c_height,currentLevel)
        self.text = "The earthlings have caught up to you. \n Destroy or be destroyed!"
        self.fill = 'white'
        self.size = 15

class EnemyShip(object):
    def __init__(self,c_width,c_height,comingFromLeft):
        self.width = 60
        self.height = 40
        self.cy = random.randint(c_height/9, c_height/2)
        if not comingFromLeft:
            self.cx = c_width + self.width/2
        elif comingFromLeft:
            self.cx = 0 - self.width/2
        self.x1, self.x2 = (self.cx-self.width/2), (self.cx+self.width/2)
        self.y1, self.y2 = (self.cy-self.height/2), (self.cy+self.height/2)

class USA(EnemyShip):
    def __init__(self,c_width, c_height,comingFromLeft):
        super(USA,self).__init__(c_width, c_height, comingFromLeft)
        self.fill1 = "blue"  
        
class PowerUp(object):
    def __init__(self,c_width):
        self.r = 10
        self.cy = -20
        self.cx = random.randint(0, c_width)
     
class SpeedUp(PowerUp):
    def __init__(self,c_width):
        super(SpeedUp,self).__init__(c_width)
        self.fill = "firebrick"

class Shield(PowerUp):
    def __init__(self,c_width):
        super(Shield,self).__init__(c_width)
        self.fill = "cyan"

class Lazer(PowerUp):
    def __init__(self,c_width):
        super(Lazer,self).__init__(c_width)
        self.fill = "limegreen"

class WarpDrive(PowerUp):
    def __init__(self,c_width):
        super(WarpDrive,self).__init__(c_width)
        self.fill = "gold"
        self.cy = 150
        self.cx = c_width/2
    


#SPACEQUEST!!!!!!
class SpaceQuest(object):

#MODEL##########################################################################

    def init(self):
    
        self.timer = 0
        self.score = 0
        self.isOutro = False
        self.isTitle = False
        self.prologue = """\t \tYou are Commander Smegmar of planet
                           Fluxunonchradliztdergrad piloting your
                           universe-famous spaceship, the SS Tiny
                           Triangle. On a joy ride through the
                           cosmos, your ship began to break down...
                           You had no choice but to execute a crash
                           landing on planet Earth (inhabited by the
                           friendly-looking humanpeople) to seek assistance
                           from your fellow living beings. Unfortunately,
                           you have slimy tentacly things sticking out
                           of your face (just like all Fluxunonch-
                           radliztdergradonians), so when you approached
                           the humanpeople in your time of need, they
                           said 'Ew, ew, ew!', 'It looks weird.', and
                           'KILL IT!'. Subsequently, the jerk
                           earthlings stole your warp drive and tried
                           to kill you. Luckily, you escaped by the skin
                           of your slimy tentacly things, but it looks
                           like you're all alone in this..."""
        self.epilogue ="""\t \tWith the jerk earthlings that tried to kill
                           you forever in your dust. You, Commander
                           Grandinstorf of planet Tripteminininiosis are free
                           to roam the stars in your spaceship, the SS
                           Tiny Triangle, at lightspeed... alone... in
                           this..."""
        self.instructions = """\t \tFly throught the asteroid belt!
                               Avoid asteroids. Pick and use power
                               ups for points. Space to shoot lazer,
                               if lazer power up is found! Press R
                               to restart at anytime."""
        self.isInstructions = False
        self.miniShipR = 6
        self.miniShipX = self.c_width+self.miniShipR
        self.miniShipY = 3*self.c_height/4
        self.prologueY = self.c_height + 300
        self.epilogueY = self.c_height + 50
        self.mainTitle = "SPACEQUEST!"
        self.subTitle = "to the stars and beyond"
        self.bossLevelTimer = 0
        self.isBossLevel = False
        self.bossLevelTitle = None
        self.bossLevelText = None
        self.usaShip = None
        self.enemyHitsLeft = 10
        self.enemyBulletList = []

        self.isWinSequence = False
        self.comingFromLeft = False
        self.waitPeriod = False
        self.giveMeABreak =False

        self.isWarpDriveText=False
        self.warpDrive = None
        
        self.isGameOver = False
     
        self.livesLeft = 3
        #init player position
        self.pr = 20 #pr = player radius
        self.px, self.py = self.c_width/2, 9*self.c_height/10 #c_width == canvas width
        self.xVelocity = 0 #nosideways movement yet
        self.yVelocity = 0 #no upwards movement yet
        self.maxVelocity = 5
        self.acceleration = 1

        #initialize player colors (will be modified when power ups are acquired)
        self.playerFill = "turquoise"
        self.playerOutline = "honeydew"
        self.playerOutlineWidth = 1

        #intialize the beautiful background stars
        self.starList = [[random.randint(0,self.c_width),random.randint(0,self.c_height)] for i in xrange(100)]

        #initialize empty asteroid list cause none on screen
        self.asteroidList = []
        self.asteroidFrequency1, self.asteroidFrequency2, self.asteroidFrequency3 = 10,7,4
        self.asteroidFrequency = self.asteroidFrequency1
        self.asteroidSpeedList1,self.asteroidSpeedList2,self.asteroidSpeedList3=[3],[3,4,6],[3,4,6,7,8,9,10]
        self.asteroidSpeedList = [3]
        
        self.fallingPowerUp = Shield(self.c_width)
        self.gottenPowerUp = None #no acquired powerups yet!
        self.bulletList = []
        self.explosionList = []

        self.explosionMaxRadius = 32
        self.explosionExpansionRate = 8

        self.collisionSequenceUnderway = False
        self.speedUpCounter = 0

        self.transitioning = False
        self.currentLevel = 0
        self.levelingUpTitle =  LevelingUpTitle(self.c_width,self.c_height,self.currentLevel)
        self.commenceTransitionalPeriod()
        self.intro()

#VIEW###########################################################################

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawTheVoid()
        self.drawStars()
        self.drawScore()
        self.drawLivesLeft()
        if not self.isIntro and not self.isOutro:
            if self.isWarpDriveText: self.drawWarpDriveText()
            if self.warpDrive != None: self.drawWarpDrive()
            if type(self.gottenPowerUp) == Shield: self.drawShield()
            if self.isGameOver == False:
                if self.usaShip != None: self.drawEnemyShip()
                self.drawPlayer()
                self.drawAsteroids()
                if self.fallingPowerUp != None: self.drawPowerUp()
                if self.bulletList != None: self.drawBullets()
                if self.enemyBulletList !=  None: self.drawEnemyBullets()
            elif self.isGameOver == True:
                self.drawGameOver()
            if self.explosionList != []: self.drawExplosion()
            if self.levelingUpTitle != None: self.drawLevelingUp()
            if self.bossLevelTitle != None: self.drawBossLevelTitle()
            elif self.bossLevelText != None: self.drawBossLevelText()
            if self.isInstructions:
                self.drawInstructions()
        elif self.isIntro:
            self.drawMiniShip()
            self.drawPrologue()
        elif self.isOutro:
            self.drawMiniShip()
            self.drawEpilogue()
        if self.isTitle == True: self.drawTitle()
             
    def drawTheVoid(self): #just black
        self.canvas.create_rectangle(0,0,self.c_width, self.c_height, fill="black")

    def drawStars(self):
        for star in self.starList:
            x1, y1 = star[0], star[1]
            x2, y2 = x1+4, y1+4
            self.canvas.create_rectangle(x1,y1,x2,y2,fill="white")
    def drawScore(self):
        cx, cy = self.c_width-30, self.c_height-30
        score = "%d" % self.score
        fill = "red"
        font = "Helvetica 12 bold"
        self.canvas.create_text(cx,cy,text=score,fill=fill, font=font)
        
    def drawLivesLeft(self):
        cxList = [10, 30, 50]
        cy, r = self.c_height -20, 7
        for cx in cxList[:self.livesLeft]:
            self.canvas.create_polygon(cx,cy-r, cx+r,cy+r, cx,cy, cx-r,cy+r, fill="turquoise")

    def drawPrologue(self):
        x,y = self.c_width/3, self.prologueY
        self.canvas.create_text(x,y,text=self.prologue,fill='white',font="Helvetica 15 bold")
    def drawTitle(self):
        x,y = self.c_width/2,self.c_height/2
        self.canvas.create_text(x,y,text=self.mainTitle,fill="green",font="Helvetica 40 bold")
        self.canvas.create_text(x,y+60,text=self.subTitle,fill="green",font="Helvetica 10 bold")

    def drawInstructions(self):
        text = self.instructions
        x,y = self.c_width/2, 3*self.c_height/4
        self.canvas.create_text(x,y,text=text,fill="white",font="Helvetica 10 bold")

    def drawMiniShip(self):
        px,py,pr = self.miniShipX,self.miniShipY,self.miniShipR
        self.canvas.create_polygon(px-pr,py, px+pr,py-pr, px,py, px+pr,py+pr, fill="turquoise", outline="honeydew",width=1)

    def drawEpilogue(self):
        x,y = self.c_width/3, self.epilogueY
        self.canvas.create_text(x,y,text=self.epilogue,fill='white',font="Helvetica 15 bold")
    
    def drawWarpDriveText(self):
        cx,cy1 = self.c_width/2, self.c_height/2
        cy2 = cy1 + 20
        font = "Helvetica 16 bold"
        text1, text2 = "threat eliminated", "retrieve your warp drive"
        self.canvas.create_text(cx,cy1,text=text1,fill="white",font=font)
        self.canvas.create_text(cx,cy2,text=text2,fill="white",font=font)
        
    def drawWarpDrive(self):
        cx,cy,r,fill = self.warpDrive.cx,self.warpDrive.cy,self.warpDrive.r,self.warpDrive.fill
        self.canvas.create_oval(cx-r,cy-r, cx+r,cy+r, fill=fill, outline="honeydew", width=4)
        
    def drawShield(self):
        pr = self.pr
        px, py = self.px, self.py
        self.canvas.create_oval(px-pr,py-pr,px+pr,py+pr, outline="white", fill="blue")
        
    def drawPlayer(self):
        pr = self.pr
        px, py = self.px, self.py
        self.canvas.create_polygon(px,py-pr, px+pr,py+pr, px,py, px-pr,py+pr,fill=self.playerFill, outline=self.playerOutline, width=self.playerOutlineWidth)

    def drawAsteroids(self):
        for asteroid in self.asteroidList:
            cx, cy, r = asteroid.cx, asteroid.cy, asteroid.r
            self.canvas.create_oval(cx-r,cy-r, cx+r,cy+r, fill="saddlebrown")

    def drawPowerUp(self):
        cx,cy,r,fill = self.fallingPowerUp.cx,self.fallingPowerUp.cy,self.fallingPowerUp.r,self.fallingPowerUp.fill
        self.canvas.create_oval(cx-r,cy-r, cx+r,cy+r, fill=fill, outline="honeydew", width=4)

    def drawBullets(self):
        for bullet in self.bulletList:
            x1,x2 = bullet.cx-(bullet.width/2), bullet.cx+(bullet.width/2)
            y1,y2 = bullet.cy-(bullet.height/2), bullet.cy+(bullet.height/2)
            fill = bullet.fill
            self.canvas.create_rectangle(x1,y1,x2,y2,fill=fill)

    def drawEnemyBullets(self):
        for enemyBullet in self.enemyBulletList:
            x1,x2 = enemyBullet.cx-(enemyBullet.width/2), enemyBullet.cx+(enemyBullet.width/2)
            y1,y2 = enemyBullet.cy-(enemyBullet.height/2), enemyBullet.cy+(enemyBullet.height/2)
            fill = enemyBullet.fill
            self.canvas.create_oval(x1,y1,x1+8,y1+8,fill=fill)
            
    def drawExplosion(self):
        for explosion in self.explosionList:
            cx, cy = explosion.cx, explosion.cy
            r1,r2,r3 = explosion.r1, explosion.r2, explosion.r3
            fill1,fill2,fill3 = explosion.fill1,explosion.fill2,explosion.fill3
            self.canvas.create_oval(cx-r1,cy-r1, cx+r1,cy+r1,fill=fill1)
            self.canvas.create_oval(cx-r2,cy-r2, cx+r2,cy+r2,fill=fill2)
            self.canvas.create_oval(cx-r3,cy-r3, cx+r3,cy+r3,fill=fill3)

    def drawBossLevelTitle(self):
            text = self.bossLevelTitle.text
            fill = self.bossLevelTitle.fill
            cx,cy = self.bossLevelTitle.cx, self.bossLevelTitle.cy
            font,size,typeface=self.bossLevelTitle.font,self.bossLevelTitle.size,self.bossLevelTitle.typeface
            self.canvas.create_text(cx,cy,text=text, fill=fill,font="%s %d %s" % (font,size,typeface))

    def drawBossLevelText(self):
        text = self.bossLevelText.text
        fill = self.bossLevelText.fill
        cx,cy = self.bossLevelText.cx, self.bossLevelText.cy
        font,size = self.bossLevelText.font,self.bossLevelText.size
        self.canvas.create_text(cx,cy, text=text, fill=fill, font="%s %d" % (font,size))

    def drawEnemyShip(self):
        
        cx,cy = self.usaShip.cx, self.usaShip.cy
        width, height = self.usaShip.width, self.usaShip.height
        x1, x2 = (cx-width/2), (cx+width/2)
        y1, y2 = (cy-height/2), (cy+height/2)

        if self.comingFromLeft:
            x1,x2 = x2,x1
        self.canvas.create_rectangle(x1,y1, x2,y2, fill = "white")
        self.canvas.create_rectangle(x1,y1, cx,cy,fill='blue')
        self.canvas.create_rectangle(cx,y1, x2,y1+height/6,fill="red")
        self.canvas.create_rectangle(cx,y1+height/3, x2,y1+height/2,fill="red")
        self.canvas.create_rectangle(x1,y1+4*height/6, x2,y1+5*height/6,fill="red")
        
        if not self.comingFromLeft:
            self.canvas.create_polygon(x1-width/2,cy, x1,y1, x1,y2, fill="darkslategray")
            self.canvas.create_polygon(x2-width/2,y2, x2,y2, x2,y2+height/3,fill="darkslategray")
            self.canvas.create_polygon(x2-width/2,y1, x2,y1, x2,y1-height/3,fill="darkslategray")
        elif self.comingFromLeft:
            self.canvas.create_polygon(x1+width/2,cy, x1,y1, x1,y2, fill="darkslategray")
            self.canvas.create_polygon(x2+width/2,y2, x2,y2, x2,y2+height/3,fill="darkslategray")
            self.canvas.create_polygon(x2+width/2,y1, x2,y1, x2,y1-height/3,fill="darkslategray")

    def drawGameOver(self):
        cx, cy = self.c_width/2, self.c_height/2
        text = "GAME OVER"
        font, size, typeface = "Helvetica", 72, "bold"
        fill = "red"
        text2 = "r for restart"
        self.canvas.create_text(cx,cy,text=text,fill=fill,font="%s %d %s" %(font,size,typeface))
        self.canvas.create_text(cx,cy+50,text=text2,fill=fill,font="%s %d" % (font,24))
        
    def drawLevelingUp(self):
        text = self.levelingUpTitle.text
        cx, cy = self.levelingUpTitle.cx, self.levelingUpTitle.cy
        fill = self.levelingUpTitle.fill
        font, size, typeface = self.levelingUpTitle.font, self.levelingUpTitle.size, self.levelingUpTitle.typeface
        self.canvas.create_text(cx,cy, text=text, fill=fill, font="%s %d %s" %(font,size,typeface))
            
    
#CONTROLLER#####################################################################
    def mousePressed(self, event):
        self.enemyHitsLeft -=8

    def keyPressed(self, event):
        if self.collisionSequenceUnderway == False and self.isGameOver == False:
            if (event.keysym=="Left"):    
                if self.xVelocity > -self.maxVelocity:
                    self.xVelocity -= self.acceleration
            elif (event.keysym=="Right"):
                if self.xVelocity < self.maxVelocity:
                    self.xVelocity += self.acceleration
            elif (event.keysym=="Up"):
                if self.yVelocity > -self.maxVelocity and self.py-self.pr > 0:
                    self.yVelocity -= self.acceleration
            elif (event.keysym=="Down"):
                if self.yVelocity < self.maxVelocity and self.py+self.pr < self.c_height:
                    self.yVelocity += self.acceleration
            elif (event.keysym=="space"):
                if type(self.gottenPowerUp) == Lazer:
                    self.fireBullet()
            elif (event.char=="l"):
                self.commenceTransitionalPeriod()
        if (event.char=="r"):
            self.init()
        if self.isIntro == True:
            if (event.char=="s"):
                self.isIntro =False
                
          
        self.redrawAll()
 
    def timerFired(self):
        if self.isIntro:
            self.prologueY -= 3
            if self.prologueY <= -200:
                self.miniShipX -= 11
                self.createTitle()
        elif self.isOutro:
            self.epilogueY -= 5
            self.miniShipX -= 1
            if self.epilogueY <= -50:
                self.createTitle()
        else:
            self.timer += 1#increment timer
            if not self.isGameOver and self.asteroidList != []:
                self.score += 1
            if not self.isIntro and not self.isOutro:
                self.moveStarsDown()

            
            #count off 1 minute for levelUp
            if self.timer >= 420 and not self.isBossLevel and not self.isWinSequence and not self.isIntro and not self.isOutro:
                self.commenceTransitionalPeriod()
            
            #count off 15 seconds for the SpeedUp power up
            if type(self.gottenPowerUp) == SpeedUp:
                self.speedUpCounter += 1
                self.score += 2

            #increment bossTimer if isBossLevel
            if self.isBossLevel == True:
                self.bossLevelTimer +=1
                self.score += 2
            
            self.setShipParameters()#depeding on powerups, ship will differ

            self.setAsteroidParameters() #depending on level, asteroids will differ
        
            self.movePlayer()
            #check player movement for left/right transport

            self.createInstructions()
            
            #add asteroid every x seconds depending on current level
            if self.timer % self.asteroidFrequency == 0 and self.transitioning == False:
                self.asteroidList += [Asteroid(self.c_width,self.asteroidSpeedList)]    
            self.moveAsteroidsDown()


            #move enemy ship if it exists
            if self.usaShip != None:
                self.moveEnemyShip()
            
            #fire 3 bullets one in ten timerFireds (roughly 1 per second)
            if random.randint(0,20) == 0 and self.usaShip != None and self.giveMeABreak == False and self.isGameOver==False:
                self.fireEnemyBullet("red")

            self.moveEnemyBulletsDown()
           
            #add random PowerUp every 20 seconds on non-bosslevel
            #add bullets every 10 seconds on bosslevel
            if not self.isBossLevel and not self.isWinSequence:
                if self.timer % 200 == 0:
                    powerUps = [SpeedUp(self.c_width), Shield(self.c_width), Lazer(self.c_width)]
                    i = random.randint(0,2)
                    self.fallingPowerUp = powerUps[i]
            elif self.isBossLevel:
                if self.fallingPowerUp == None:
                    self.fallingPowerUp = Lazer(self.c_width)
            if self.fallingPowerUp != None: self.movePowerUpDown()

            #explosions!
            if self.explosionList != []:
                self.expandExplosion()
        
            #bullets!
            if self.bulletList != None: self.moveBulletsUp()

            #level up if transition period is on and all asteroids are off map!
            if self.transitioning == True and self.asteroidList == []:
                self.levelUp()
        self.redrawAll()
        
        def f():
            self.timerFired()
        delay = 100
        self.canvas.after(delay,f)

    def moveStarsDown(self):
        for star in self.starList:
            star[1] += 1
            if star[1] > self.c_height:
                star[1] = 0

    def setShipParameters(self):
        #Lazer!
        if type(self.gottenPowerUp) == Lazer:
            self.playerOutline = "DarkGreen"
            self.playerOutlineWidth = 3

        else:
            self.playerOutline = "honeydew"
            self.playerOutlineWidth = 1
        if self.isBossLevel:
            self.maxVelocity = 10
            self.acceleration = 2
        #Speed Up!
        if type(self.gottenPowerUp) == SpeedUp:
            self.maxVelocity = 10
            self.acceleration = 2
            self.playerFill = "red"
            #blink the last 2 seconds of powerUp
            blinkingTimes = [140,142,144,146]
            if self.speedUpCounter in blinkingTimes:
                if (blinkingTimes.index(self.speedUpCounter)%2)==0:
                    self.playerFill = "turquoise"
                else: self.playerFill = "red"
            if self.speedUpCounter >= 150:
                self.losePowerUp()
        else:
            self.maxVelocity = 5
            self.acceleration = 1
            self.playerFill = "turquoise"

        if type(self.gottenPowerUp) == Shield:
            if self.shieldHitsLeft == 0:
                self.losePowerUp()

    def setAsteroidParameters(self):
        asteroidSpeedLists=[self.asteroidSpeedList1,self.asteroidSpeedList2,self.asteroidSpeedList3]
        asteroidFrequencies=[self.asteroidFrequency1,self.asteroidFrequency2,self.asteroidFrequency3]
        if self.currentLevel <= 3:
            i = self.currentLevel-1
            self.asteroidSpeedList = asteroidSpeedLists[i]
            self.asteroidFrequency = asteroidFrequencies[i]
        elif self.isBossLevel:
            self.asteroidSpeedList = [3]
            self.asteroidFrequency = self.asteroidFrequency2

    def moveAsteroidsDown(self):
        for asteroid in self.asteroidList:
            asteroid.cy += asteroid.yVelocity
            #collision=lose life if not shield powerup unlocked
            #also 
            if self.isAsteroidCollision(asteroid) and self.isGameOver == False:
                if type(self.gottenPowerUp) != Shield and not self.giveMeABreak:
                    self.loseLife()
                    self.asteroidList.remove(asteroid)
                    self.asteroidCollisionSequence()
                elif type(self.gottenPowerUp) == Shield:
                    self.score += 50
                    self.shieldCollisionSequence(asteroid)
            if asteroid.cy - asteroid.r >= self.c_height:#remove when  off screen
                self.asteroidList.remove(asteroid)

    def movePowerUpDown(self):
        self.fallingPowerUp.cy += 8
        if self.isPowerUpCollision():
            self.score += 75
            self.getPowerUp()
            self.fallingPowerUp = None
        elif (self.fallingPowerUp.cy - self.fallingPowerUp.r >= self.c_height):
            self.fallingPowerUp = None

    def moveBulletsUp(self):
        for bullet in self.bulletList:
            if bullet.cy+(bullet.height/2) <= 0:
                try: self.bulletList.remove(bullet)
                except: pass
            for asteroid in self.asteroidList:
                if self.isBulletCollision(bullet,asteroid):
                    self.bulletCollisionSequence(bullet,asteroid)
            if self.usaShip != None:
                if self.isBulletEnemyCollision(bullet):
                    self.bulletEnemyCollisionSequence(bullet)
            bullet.cy -= 30

    def movePlayer(self):
        py1, py2 = self.py-self.pr, self.py+self.pr

        self.px += self.xVelocity
        self.py += self.yVelocity

        if self.yVelocity < 0 and py1 <= 0:
            self.yVelocity = 0
        elif self.yVelocity > 0 and py2 >= self.c_height:
            self.yVelocity = 0
        if self.xVelocity < 0 and self.px <= 0:
            self.px = self.c_width-1
        elif self.xVelocity > 0 and self.px >= self.c_width:
            self.px = 1
        if self.warpDrive != None:
            if self.isWarpDriveCollision():
                self.outro()

    def isWarpDriveCollision(self):
        wdx1, wdx2 = self.warpDrive.cx-self.warpDrive.r, self.warpDrive.cx+self.warpDrive.r
        wdy1, wdy2 = self.warpDrive.cy-self.warpDrive.r, self.warpDrive.cy+self.warpDrive.r
        px1, px2 = self.px-self.pr, self.px+self.pr
        py1, py2 = self.py-self.pr, self.py+self.pr
        for xCoor in xrange(wdx1, wdx2):
            if xCoor in xrange(px1, px2):
                for yCoor in xrange(wdy1, wdy2):
                    if yCoor in xrange(py1, py2):
                        return True
        return False 
     
    def isAsteroidCollision(self,asteroid):
        px,py,pr = self.px,self.py,self.pr
        cx,cy,r = asteroid.cx, asteroid.cy,asteroid.r
        for xCoor in xrange(cx-r, cx+r):
            if xCoor in xrange(px-pr, px+pr):
                self.explosionX = xCoor
                for yCoor in xrange(cy-r, cy+r):
                    if yCoor in xrange(py-pr, py+pr):
                        self.explosionY = yCoor
                        return True
        return False

    def isPowerUpCollision(self):
        px,py,pr = self.px,self.py,self.pr
        cx,cy,r = self.fallingPowerUp.cx, self.fallingPowerUp.cy, self.fallingPowerUp.r
        for xCoor in xrange(cx-r, cx+r):
            if xCoor in xrange(px-pr, px+pr):
                for yCoor in xrange(cy-r, cy+r):
                    if yCoor in xrange(py-pr, py+pr):
                        return True
        return False

    def isBulletCollision(self,bullet,asteroid):
        #bullet x1,x2,y1,y2
        bx1,bx2 = bullet.cx-(bullet.width/2), bullet.cx+(bullet.width/2)
        by1,by2 = bullet.cy-(bullet.height/2), bullet.cy+(bullet.height/2)
        #asteroid x and y and r
        ax, ay, r = asteroid.cx, asteroid.cy,asteroid.r
        for xCoor in xrange(bx1,bx2):
            if xCoor in xrange(ax-r, ax+r):
                self.bulletExplosionX = xCoor
                for yCoor in xrange(by1,by2):
                    if yCoor in xrange(ay-r,ay+r):
                        self.bulletExplosionY = yCoor
                        return True
        return False

    def isBulletEnemyCollision(self, bullet):
        bx1,bx2 = bullet.cx-(bullet.width/2), bullet.cx+(bullet.width/2)
        by1,by2 = bullet.cy-(bullet.height/2), bullet.cy+(bullet.height/2)
        ex,ey = self.usaShip.cx, self.usaShip.cy
        width, height = self.usaShip.width, self.usaShip.height
        ex1, ex2 = ex-width/2, ex+width/2
        ey1, ey2 = ey-height/2, ey+height/2
        for xCoor in xrange(bx1,bx2):
            if xCoor in xrange(ex1, ex2):
                self.bulletExplosionX = xCoor
                for yCoor in xrange(by1,by2):
                    if yCoor in xrange(ey1,ey2):
                        self.bulletExplosionY = yCoor
                        return True
        return False

    def isEnemyBulletCollision(self,enemyBullet):
        bx1 = enemyBullet.cx-(enemyBullet.width/2)
        by1 = enemyBullet.cy-(enemyBullet.height/2)
        bx2,by2 = bx1+8, by1+8
        px,py,pr = self.px,self.py,self.pr
        for xCoor in xrange(bx1,bx2):
            if xCoor in xrange(px-pr, px+pr):
                self.enemyBulletExplosionX = xCoor
                for yCoor in xrange(by1,by2):
                    if yCoor in xrange(py-pr,py+pr):
                        self.enemyBulletExplosionY = yCoor
                        return True
        return False
    
    def isEnemyBulletAsteroidCollision(self,enemyBullet,asteroid):
        eBX1 = enemyBullet.cx-enemyBullet.width/2
        eBX2 = enemyBullet.cx+enemyBullet.width/2
        eBY1 = enemyBullet.cy-enemyBullet.height/2
        eBY2 = enemyBullet.cy+enemyBullet.height/2
        ax, ay, r = asteroid.cx, asteroid.cy,asteroid.r
        for xCoor in xrange(eBX1,eBX2):
            if xCoor in xrange(ax-r, ax+r):
                self.enemyBulletAsteroidExplosionX = xCoor
                for yCoor in xrange(eBY1, eBY2):
                    if yCoor in xrange(ay-r, ay+r):
                        self.enemyBulletAsteroidExplosionY = yCoor
                        return True
        return False

    def enemyBulletAsteroidCollisionSequence(self,enemyBullet,asteroid):
        self.explosionList += [Explosion(self.enemyBulletAsteroidExplosionX,self.enemyBulletAsteroidExplosionY,"red","white","blue")]
        self.asteroidList.remove(asteroid)
        self.enemyBulletList.remove(enemyBullet)
        
    def asteroidCollisionSequence(self):
        self.collisionSequenceUnderway = True
        self.explosionList += [Explosion(self.explosionX,self.explosionY)]
        
        self.losePowerUp()
        self.xVelocity, self.yVelocity = 0,0
        self.asteroidSpeedList = [0]
        self.asteroidFrequency = 99999999

    def shieldCollisionSequence(self,asteroid):
        cx,cy = self.explosionX, self.explosionY
        self.explosionList += [Explosion(cx,cy)]
        def f():
            try: self.asteroidList.remove(asteroid)
            except: pass
            self.shieldHitsLeft -= 1
        delay = 300
        self.canvas.after(delay,f)
        
    def bulletCollisionSequence(self,bullet,asteroid):
        self.asteroidList.remove(asteroid)
        self.score += 25
        try: self.bulletList.remove(bullet)
        except: pass
        cx,cy = self.bulletExplosionX,self.bulletExplosionY
        self.explosionList += [Explosion(cx,cy)]

    def bulletEnemyCollisionSequence(self,bullet):
        self.enemyHitsLeft -= 1
        self.score += 50
        try: self.bulletList.remove(bullet)
        except: pass
        if self.enemyHitsLeft <= 0:
            self.explosionMaxRadius =400
            self.explosionExpansionRate = 16
            self.enemyDie()
        cx,cy = self.bulletExplosionX,self.bulletExplosionY
        self.explosionList += [Explosion(cx,cy)]

    def enemyBulletCollisionSequence(self):
        self.enemyBulletList = []
        cx,cy = self.enemyBulletExplosionX, self.enemyBulletExplosionY
        self.explosionList += [Explosion(cx,cy,"red","white","blue")]
        
    def expandExplosion(self):
        maxR = self.explosionMaxRadius
        exR = self.explosionExpansionRate
        for explosion in self.explosionList:
            if explosion.r1 < maxR:
                explosion.r1 += exR
            if explosion.r1 >= maxR/2 and explosion.r2 < maxR:
                    explosion.r2 += exR
            if explosion.r2 >= maxR/2 and explosion.r3 < maxR:
                explosion.r3 += exR
            if explosion.r3 >= maxR:
                self.explosionList.remove(explosion)

    def getPowerUp(self):
        self.gottenPowerUp = self.fallingPowerUp
        if type(self.gottenPowerUp) == Lazer:
            self.bulletsLeft = 10
        elif type(self.gottenPowerUp) == SpeedUp:
            self.speedUpCounter = 0
        elif type(self.gottenPowerUp)== Shield:
            self.shieldHitsLeft = 4
            
    def losePowerUp(self):
        self.gottenPowerUp = None
    
    def fireBullet(self):
        self.bulletList += [Bullet(self.px,self.py-self.pr,None, "DarkGreen")]
        self.bulletsLeft -= 1
        if self.bulletsLeft <= 0:
            self.losePowerUp()

    def fireEnemyBullet(self,color):
        if not self.comingFromLeft: shipNoseX = (self.usaShip.cx-self.usaShip.width)
        elif self.comingFromLeft: shipNoseX = (self.usaShip.cx+self.usaShip.width)
        shipNoseY = self.usaShip.cy
        self.enemyBulletList += [EnemyBullet(shipNoseX,shipNoseY,self.px,color)]
        def f():
            if self.usaShip!=None: self.enemyBulletList += [EnemyBullet(shipNoseX,shipNoseY,self.px,"white")]
        def g():
            if self.usaShip!=None: self.enemyBulletList += [EnemyBullet(shipNoseX,shipNoseY,self.px,"blue")]
        delay=100
        self.canvas.after(delay,f)
        self.canvas.after(delay*2,g)

    def moveEnemyBulletsDown(self):
        for enemyBullet in self.enemyBulletList:
            enemyBullet.cy += 20
            if enemyBullet.cx < enemyBullet.xDir: enemyBullet.cx +=10
            elif enemyBullet.cx > enemyBullet.xDir: enemyBullet.cx -= 10
            for asteroid in self.asteroidList:
                if self.isEnemyBulletAsteroidCollision(enemyBullet,asteroid):
                    self.enemyBulletAsteroidCollisionSequence(enemyBullet,asteroid)
            if self.isEnemyBulletCollision(enemyBullet) and not self.giveMeABreak:
                self.enemyBulletCollisionSequence()
                self.loseLife()
            
    def loseLife(self):
        self.livesLeft -= 1
        self.score -= 200
        self.giveMeABreak = True
        if self.livesLeft < 0:
            self.gameOver()
        def f():
            self.resetLevel()
        def g():
            self.giveMeABreak = False
        delay = 600
        self.canvas.after(delay,f)
        self.canvas.after(delay*5,g)

    def startBossLevel(self):
        self.isBossLevel = True
        self.levelingUpTitle = None
        
        self.asteroidFrequency = 10
        self.asteroidSpeedList = self.asteroidSpeedList1
        self.bossLevelTitle = BossLevel(self.c_width,self.c_height, "boss")

        def f():
            self.bossLevelTitle = None
            self.bossLevelText = BossLevelText(self.c_width,self.c_height,"boss")
        def g():
            self.bossLevelText = None
            self.spawnEnemy()
        delay = 3000
        self.canvas.after(delay,f)
        self.canvas.after(delay*2,g)

    def spawnEnemy(self):
        self.usaShip = USA(self.c_width, self.c_height, self.comingFromLeft)

    def moveEnemyShip(self):
        if self.comingFromLeft == False and self.usaShip != None:
            self.usaShip.cx -= 10
            if self.usaShip.cx+self.usaShip.width/2 <= 0:
                self.usaShip = None
                self.comingFromLeft = True
                self.startWaitPeriod()
        elif self.comingFromLeft == True and self.usaShip != None:
            self.usaShip.cx += 10
            if self.usaShip.cx-self.usaShip.width/2 >= self.c_width:
                self.usaShip = None
                self.comingFromLeft = False
                self.startWaitPeriod()
                
    def enemyDie(self):

        self.isBossLevel = False
        self.usaShip = None
        self.winSequence()
        

    def winSequence(self):
        self.giveMeABreak = True
        self.isWinSequence = True
        self.asteroidList = []
        self.asteroidFrequency = 9999999999999
        self.yVelocity,self.xVelocity = 0,0
        def f():
            self.spawnWarpDrive()
            self.writeWarpDriveText()
        delay = 3000
        self.canvas.after(delay,f)

    def spawnWarpDrive(self):
        self.warpDrive = WarpDrive(self.c_width)

    def writeWarpDriveText(self):
        self.isWarpDriveText = True
        
    def startWaitPeriod(self):
        def f():
            self.usaShip = EnemyShip(self.c_width,self.c_height,self.comingFromLeft)
        delay = random.randint(500,1800)
        self.canvas.after(delay,f)
        
    def resetLevel(self):
        self.collisionSequenceUnderway = False
        self.transitioning = False

        #ship reset
        self.px, self.py = self.c_width/2, 9*self.c_height/10
        self.acceleration = 1

        self.fallingPowerUp = None

    def levelUp(self):

        self.timer = 0
        self.transitioning = False
        self.currentLevel += 1
        if self.currentLevel > 3 and not self.isGameOver:
            self.startBossLevel()
        elif self.currentLevel <= 3:
            self.levelingUpTitle = LevelingUpTitle(self.c_width, self.c_height,self.currentLevel)
        def f():
            self.levelingUpTitle = None
        delay = 3000
        self.canvas.after(delay,f)
        
    def commenceTransitionalPeriod(self):
        self.transitioning = True
        
    def gameOver(self):       
        self.isGameOver = True
        self.livesLeft = 0
        self.isBossLevel = False

    def outro(self):
        self.isOutro = True
        self.miniShipX = self.c_width+self.miniShipR
        
    def intro(self):
        self.isIntro = True

    def createTitle(self):
        self.isTitle=True
        def f():
            self.isIntro = False
            self.isOutro = False
            self.isTitle=False
        delay = 7000
        self.canvas.after(delay,f)
    def createInstructions(self):
        if self.timer <= 100 and self.currentLevel == 1:
            self.isInstructions  =True
        else: self.isInstructions =False

############################################   
#RUN########################################
#####        ###   ###   ###         ##   ##
#####   ########   ###   ###   ###   ##   ##
#####   ########   ###   ###   ###   #######
#####   ########         ###   ###   ##   ##
############################################
                                             
    def run(self, c_width=600, c_height=600):
        #creating root & canvas
        root = Tk()
        self.c_width, self.c_height = c_width, c_height
        self.canvas = Canvas(root, width=c_width, height=c_height)
        self.canvas.pack()
     
        #root
        root.resizable(width=0, height=0)
        root.bind("<Button-1>", lambda event: self.mousePressed(event))
        root.bind("<Key>", lambda event: self.keyPressed(event))
     
        #init and timerFired
        self.init()
        self.timerFired()
        root.mainloop()

SpaceQuest().run()





