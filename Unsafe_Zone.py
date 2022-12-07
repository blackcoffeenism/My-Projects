from itertools import cycle
import random
import sys

import os
import pygame
from pygame.locals import *

import heapq

import sqlite3
fps = 30


ScreenWidth = 1280
ScreenHeight = 720
CovidGapSize = 75
BaseY = ScreenHeight * 0.79
Img,Sfx,Hitmasks = {},{},{}
bg_num = 0

conn = sqlite3.connect('scores.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS scores(score_list INTEGER, top INTEGER)")
conn.commit()
if cursor.execute("SELECT score_list FROM scores")== None:
    score_list = []
    top = []
    cursor.execute("INSERT INTO scores(score_list,top)VALUES (?,?)",(score_list,top))
    conn.commit()
    

Players = (
    # red box
    (
        'assets/sprites/p1.png',
        'assets/sprites/p2.png',
        'assets/sprites/p3.png',
    ),
    # blue box
    (
        'assets/sprites/p1.png',
        'assets/sprites/p2.png',
        'assets/sprites/p3.png',
    ),
    # yellow box
    (
        'assets/sprites/p1.png',
        'assets/sprites/p2.png',
        'assets/sprites/p3.png',
    ),
)

# list of backgrounds
Backgrounds = (
    'assets/sprites/paris-bg.jpg',
    'assets/sprites/rome.jpg',
    'assets/sprites/haliwud.jpg',
    'assets/sprites/mountain.jpg',
    'assets/sprites/great wall.jpg',
    'assets/sprites/hands.jpg',
    'assets/sprites/japan.jpg',
    'assets/sprites/newyork.jpg',
)

# list of pipes
Covid = (
    'assets/sprites/covid1.png',
    'assets/sprites/covid1.png',
)

Tips = (
    'assets/sprites/tips1.png',
    'assets/sprites/tips2.png',
    'assets/sprites/tips3.png',
    'assets/sprites/tips4.png',
    'assets/sprites/tips5.png',
    'assets/sprites/tips6.png',
    'assets/sprites/tips7.png',
    'assets/sprites/fact1.png',
    'assets/sprites/fact2.png',
    'assets/sprites/fact3.png',
    'assets/sprites/fact4.png',
)
try:
    xrange
except NameError:
    xrange = range

class MainScreen:
    def main():
        global SCREEN, FPSCLOCK,count
        os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        # Fullscreen scaled output
        SCREEN = pygame.display.set_mode((ScreenWidth, ScreenHeight),FULLSCREEN)
        pygame.display.set_caption('Avoid Covid')
        

        # numbers sprites for score display
        Img['numbers'] = (pygame.image.load('assets/sprites/0.png').convert_alpha(), pygame.image.load('assets/sprites/1.png').convert_alpha(), pygame.image.load('assets/sprites/2.png').convert_alpha(), pygame.image.load('assets/sprites/3.png').convert_alpha(), pygame.image.load('assets/sprites/4.png').convert_alpha(), pygame.image.load('assets/sprites/5.png').convert_alpha(), pygame.image.load('assets/sprites/6.png').convert_alpha(), pygame.image.load('assets/sprites/7.png').convert_alpha(), pygame.image.load('assets/sprites/8.png').convert_alpha(), pygame.image.load('assets/sprites/9.png').convert_alpha())

        # game over sprite
        Img['gameover'] = pygame.image.load('assets/sprites/game over.png').convert_alpha()
        # message sprite for welcome screen
        Img['message'] = pygame.image.load('assets/sprites/getready.png').convert_alpha()
        # base (ground) sprite
        Img['base'] = pygame.image.load('assets/sprites/road.png').convert_alpha()
        # Tips and facts sprite about covid
        

        # sounds
        soundExt = '.ogg'

        Sfx['die'] = pygame.mixer.Sound('assets/audio/nani' + soundExt)
        Sfx['hit'] = pygame.mixer.Sound('assets/audio/nani' + soundExt)
        Sfx['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
        Sfx['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)
        Sfx['bg'] = pygame.mixer.Sound('assets/audio/bg_music' + soundExt)

        Sfx['bg'].play(-1)
        
        while True:

            # select random background sprites
            
            randBg = random.randint(0, len(Backgrounds) - 1)
            Img['background'] = pygame.image.load(Backgrounds[randBg]).convert()
            Img['background'] = pygame.transform.scale(Img['background'],(ScreenWidth,600))

            # select random player sprites
            randPlayer = random.randint(0, len(Players) - 1)
            Img['player'] = (
                pygame.image.load(Players[randPlayer][0]).convert_alpha(),
                pygame.image.load(Players[randPlayer][1]).convert_alpha(),
                pygame.image.load(Players[randPlayer][2]).convert_alpha(),
            )

            # select random pipe sprites
            covindex = random.randint(0, len(Covid) - 1)
            Img['covid'] = (
                pygame.transform.flip(pygame.image.load(Covid[covindex]).convert_alpha(), False, True),
                pygame.image.load(Covid[covindex]).convert_alpha())
            

            # hismask for pipes
            Hitmasks['covid'] = (
                MainProcess.getHitmask(Img['covid'][0]),
                MainProcess.getHitmask(Img['covid'][1]),
            )

            # hitmask for player
            Hitmasks['player'] = (
                MainProcess.getHitmask(Img['player'][0]),
                MainProcess.getHitmask(Img['player'][1]),
                MainProcess.getHitmask(Img['player'][2]),
            )
            
            
            MainScreen.Lobby()
            count += 1   
            movementInfo = MainScreen.showWelcomeAnimation()
            crashInfo = MainProcess.mainGame(movementInfo)
            MainProcess.showGameOverScreen(crashInfo)
            
            
            
    def Lobby():
        btns.buttons()
        pygame.display.update()
        
    def recent():
        global count
        
        Img['back'] = pygame.image.load('assets/sprites/bg.jpg').convert()
        Img['back'] = pygame.transform.scale(Img['back'],(ScreenWidth,ScreenHeight))
        Img['recent'] = pygame.image.load('assets/sprites/recentscores.png').convert_alpha()
        
        while True:
            
            if count >0:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                        return False
            else:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                SCREEN.blit(Img['back'],(0,0))
                SCREEN.blit(Img['recent'],(int((ScreenWidth - Img['recent'].get_width()) / 2),int(ScreenHeight * 0.12)+50))
                interval = 0
                rcount = 0
                for score in score_list:
                    if rcount<5:
                        MainProcess.showScore(score,200+interval)
                        interval+=50
                        rcount+=1
                btns.back_button()
                pygame.display.update()
                FPSCLOCK.tick(fps)

    def top3():
        global count
        
        Img['back'] = pygame.image.load('assets/sprites/bg.jpg').convert()
        Img['back'] = pygame.transform.scale(Img['back'],(ScreenWidth, ScreenHeight))
        Img['top'] = pygame.image.load('assets/sprites/top3.png').convert_alpha()
        
        while True:
            
            if count >0:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                        return False
            else:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                SCREEN.blit(Img['back'],(0,0))
                SCREEN.blit(Img['top'],(int((ScreenWidth - Img['top'].get_width()) / 2),int(ScreenHeight * 0.12)+50))
                

                best = []
                while top:
                    heapq._heapify_max(top)
                    if top[0] in best:
                        heapq.heappop(top)
                    else:
                        best.append(top[0])
                        heapq.heappop(top)
                interval = 0
                rcount = 0
                for score in best:
                    if rcount<3:
                        MainProcess.showScore(score,200+interval)
                        top.append(score)
                        interval += 50
                        rcount +=1
                    else:
                        top.append(score)
                 
                btns.back_button()
                pygame.display.update()
                FPSCLOCK.tick(fps)
        
        
    def showWelcomeAnimation():
        global count
        count += 1
        
        """Shows welcome screen animation of flappy box"""
        # index of player to blit on screen
        playerIndex = 0
        playerIndexGen = cycle([0, 1, 2, 1])
        # iterator used to change playerIndex after every 5th iteration
        loopIter = 0

        playerx = int(ScreenWidth * 0.2)
        playery = int((ScreenHeight - Img['player'][0].get_height()) / 2)

        messagex = int((ScreenWidth - Img['message'].get_width()) / 2)
        messagey = int(ScreenHeight * 0.12)

        basex = 1200
        # amount by which base can maximum shift to left
        
        baseShift = Img['base'].get_width() - Img['background'].get_width()

        # player shm for up-down motion on welcome screen
        playerShmVals = {'val': 0, 'dir': 1}

        Img['high'] = pygame.image.load('assets/sprites/highscore.png').convert_alpha()
        Img['black'] = pygame.image.load('assets/sprites/black.jpg').convert()
        high = top
        heapq._heapify_max(high)
        if high == []:
            highscore = 0
        else:
            highscore = high[0]

            
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                    # make first flap sound and return values for mainGame
                    count+=1
                    Sfx['wing'].play()
                    return {
                        'playery': playery + playerShmVals['val'],
                        'basex': basex,
                        'playerIndexGen': playerIndexGen,
                    }

            # adjust playery, playerIndex, basex
            if (loopIter + 1) % 5 == 0:
                playerIndex = next(playerIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 4) % baseShift)
            MainProcess.playerShm(playerShmVals)
            font = pygame.font.SysFont('Constantia', 18)
            white = (255,255,255)
            black = (0,0,0)
            text = font.render('[Click space bar to play]',False,white)

            Img['base'] = pygame.transform.scale(Img['base'],(3560, 720-568))
            Img['black'] = pygame.transform.scale(Img['black'],(1280, 360))
            
            # draw sprites
            
            SCREEN.blit(Img['background'], (0,0))
            SCREEN.blit(Img['black'],(0,-360))
            SCREEN.blit(Img['black'],(0,720))
                
            SCREEN.blit(Img['base'],(0,568))
            SCREEN.blit(Img['player'][playerIndex], (playerx, playery + playerShmVals['val']))
            SCREEN.blit(Img['message'], (messagex, messagey))
            SCREEN.blit(Img['high'],(int((ScreenWidth - Img['high'].get_width()) / 2),int(ScreenHeight * 0.12)+150))
            SCREEN.blit(text,(int((ScreenWidth - text.get_width())/2),int(ScreenHeight * 0.12)+600))
            MainProcess.showScore(highscore,300)
            
            btns.back_button()
            pygame.display.update()
            FPSCLOCK.tick(fps)

class MainProcess:
    def mainGame(movementInfo):
        Sfx['intro'] = pygame.mixer.Sound('assets/audio/intro.ogg')
        SCREEN.blit(Img['background'], (0,0))
        
        Sfx['intro'].play()
        
        score = playerIndex = loopIter = 0
        playerIndexGen = movementInfo['playerIndexGen']
        playerx, playery = int(ScreenWidth * 0.2), movementInfo['playery']

        basex = movementInfo['basex']
        baseShift = Img['base'].get_width() - Img['background'].get_width()

        # get 2 new pipes to add to upperPipes lowerPipes list
        newcov1 = MainProcess.getRandomCovid()
        newcov2 = MainProcess.getRandomCovid()

        # list of upper pipes
        upperCovid = [
            {
                'x': ScreenWidth + 10,
                'y': newcov1[0]['y']
            },
            {
                'x': ScreenWidth + 10 + (ScreenWidth / 4),
                'y': newcov2[0]['y']
            },
            {
                'x': ScreenWidth + 650,
                'y': newcov1[0]['y']
            },
            {
                'x': ScreenWidth + 650 + (ScreenWidth / 4),
                'y': newcov2[0]['y']
            },
        ]

        # list of lowerpipe
        lowerCovid = [
            {
                'x': ScreenWidth + 10,
                'y': newcov1[1]['y']
            },
            {
                'x': ScreenWidth + 10 + (ScreenWidth / 4),
                'y': newcov2[1]['y']
            },
            {
                'x': ScreenWidth + 650,
                'y': newcov1[1]['y']
            },
            {
                'x': ScreenWidth + 650 + (ScreenWidth / 4),
                'y': newcov2[1]['y']
            },
        ]
                

        covVelX = -5

        # player velocity, max velocity, downward accleration, accleration on flap
        playerVelY = -9  # player's velocity along Y, default same as playerFlapped
        playerMaxVelY = 10  # max vel along Y, max descend speed
        playerMinVelY = -8  # min vel along Y, max ascend speed
        playerAccY = 1  # players downward accleration
        playerRot = 45  # player's rotation
        playerVelRot = 3  # angular speed
        playerRotThr = 20  # rotation threshold
        playerFlapAcc = -9  # players speed on flapping
        playerFlapped = False  # True when player flaps

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                    if playery > -2 * Img['player'][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        Sfx['wing'].play()



            # check for crash here
            crashTest = MainProcess.checkCrash({'x': playerx, 'y': playery, 'index': playerIndex}, upperCovid, lowerCovid)
            if crashTest[0]:
                return {'y': playery, 'groundCrash': crashTest[1], 'basex': basex, 'upperCovid': upperCovid, 'lowerCovid': lowerCovid, 'score': score, 'playerVelY': playerVelY, 'playerRot': playerRot}

            # check for score
            playerMidPos = playerx + Img['player'][0].get_width() / 2
            for covid in upperCovid:
                covMidPos = covid['x'] + Img['covid'][0].get_width() / 2
                if covMidPos <= playerMidPos < covMidPos + 5:
                    score += 1
                    Sfx['point'].play()

            # playerIndex basex change
            if (loopIter + 1) % 3 == 0:
                playerIndex = next(playerIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 100) % baseShift)

            # rotate the player
            if playerRot > -90:
                playerRot -= playerVelRot

            # player's movement
            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False

                # more rotation to cover the threshold (calculated in visible rotation)
                playerRot = 45

            playerHeight = Img['player'][playerIndex].get_height()
            playery += min(playerVelY, BaseY - playery - playerHeight)

            # move pipes to left
            for ucov, lcov in zip(upperCovid, lowerCovid):
                ucov['x'] += covVelX
                lcov['x'] += covVelX

            # add new pipe when first pipe is about to touch left of screen
            if len(upperCovid) > 0 and 0 < upperCovid[0]['x'] <6 :
                newCovid = MainProcess.getRandomCovid()
                upperCovid.append(newCovid[0])
                lowerCovid.append(newCovid[1])

            # remove first pipe if its out of the screen
            if len(upperCovid) > 0 and upperCovid[0]['x'] < -Img['covid'][0].get_width():
                upperCovid.pop(0)
                lowerCovid.pop(0)

            # draw sprites
            SCREEN.blit(Img['background'], (0, 0))

            for ucov, lcov in zip(upperCovid, lowerCovid):
                SCREEN.blit(Img['covid'][0], (ucov['x'], ucov['y']))
                SCREEN.blit(Img['covid'][1], (lcov['x'], lcov['y']))

            SCREEN.blit(Img['base'], (basex, BaseY))
            # print score so player overlaps the score
            MainProcess.showScore(score,50)

            # Player rotation has a threshold
            visibleRot = playerRotThr
            if playerRot <= playerRotThr:
                visibleRot = playerRot

            playerSurface = pygame.transform.rotate(Img['player'][playerIndex], visibleRot)
            SCREEN.blit(playerSurface, (playerx, playery))

            pygame.display.update()
            FPSCLOCK.tick(fps)
    def loop():
        
        # numbers sprites for score display
        Img['numbers'] = (pygame.image.load('assets/sprites/0.png').convert_alpha(), pygame.image.load('assets/sprites/1.png').convert_alpha(), pygame.image.load('assets/sprites/2.png').convert_alpha(), pygame.image.load('assets/sprites/3.png').convert_alpha(), pygame.image.load('assets/sprites/4.png').convert_alpha(), pygame.image.load('assets/sprites/5.png').convert_alpha(), pygame.image.load('assets/sprites/6.png').convert_alpha(), pygame.image.load('assets/sprites/7.png').convert_alpha(), pygame.image.load('assets/sprites/8.png').convert_alpha(), pygame.image.load('assets/sprites/9.png').convert_alpha())

        # game over sprite
        Img['gameover'] = pygame.image.load('assets/sprites/game over.png').convert_alpha()
        # message sprite for welcome screen
        Img['message'] = pygame.image.load('assets/sprites/getready.png').convert_alpha()
        # base (ground) sprite
        Img['base'] = pygame.image.load('assets/sprites/road.png').convert_alpha()
        # Tips and facts sprite about covid
        

        # sounds
        soundExt = '.ogg'

        Sfx['die'] = pygame.mixer.Sound('assets/audio/nani' + soundExt)
        Sfx['hit'] = pygame.mixer.Sound('assets/audio/nani' + soundExt)
        Sfx['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
        Sfx['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)
        Sfx['bg'] = pygame.mixer.Sound('assets/audio/bg_music' + soundExt)

        while True:
            # select random background sprites
            randBg = random.randint(0, len(Backgrounds) - 1)
            Img['background'] = pygame.image.load(Backgrounds[randBg]).convert()
            Img['background'] = pygame.transform.scale(Img['background'],(ScreenWidth,600))

            # select random player sprites
            randPlayer = random.randint(0, len(Players) - 1)
            Img['player'] = (
                pygame.image.load(Players[randPlayer][0]).convert_alpha(),
                pygame.image.load(Players[randPlayer][1]).convert_alpha(),
                pygame.image.load(Players[randPlayer][2]).convert_alpha(),
            )

            # select random pipe sprites
            covindex = random.randint(0, len(Covid) - 1)
            Img['covid'] = (
                pygame.transform.flip(pygame.image.load(Covid[covindex]).convert_alpha(), False, True),
                pygame.image.load(Covid[covindex]).convert_alpha())
            

            # hismask for pipes
            Hitmasks['covid'] = (
                MainProcess.getHitmask(Img['covid'][0]),
                MainProcess.getHitmask(Img['covid'][1]),
            )

            # hitmask for player
            Hitmasks['player'] = (
                MainProcess.getHitmask(Img['player'][0]),
                MainProcess.getHitmask(Img['player'][1]),
                MainProcess.getHitmask(Img['player'][2]),
            )
            
              
            return False

        return MainScreen.showWelcomeAnimation()


    def showGameOverScreen(crashInfo):
        """crashes the player down ans shows gameover image"""
        score = crashInfo['score']
        playerx = ScreenWidth * 0.2
        playery = crashInfo['y']
        playerHeight = Img['player'][0].get_height()
        playerVelY = crashInfo['playerVelY']
        playerAccY = 2
        playerRot = crashInfo['playerRot']
        playerVelRot = 7
        Scores.score_list(score)

        basex = crashInfo['basex']

        upperCovid, lowerCovid = crashInfo['upperCovid'], crashInfo['lowerCovid']

        # play hit and die sounds
        Sfx['hit'].play()
        if not crashInfo['groundCrash']:
            Sfx['die'].play()
        Img['tips'] = pygame.image.load(Tips[random.randint(0,len(Tips)-1)]).convert()
        Img['tips'] = pygame.transform.scale(Img['tips'],(500,300))
        font = pygame.font.SysFont('Constantia', 18)
        white = (255,255,255)
        black = (0,0,0)
        text = font.render('[Click space bar to continue]',False,white)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                    if playery + playerHeight >= BaseY - 1:
                        
                        return MainProcess.loop()
                    

            # player y shift
            if playery + playerHeight < BaseY - 1:
                playery += min(playerVelY, BaseY - playery - playerHeight)

            # player velocity change
            if playerVelY < 15:
                playerVelY += playerAccY

            # rotate only when it's a pipe crash
            if not crashInfo['groundCrash']:
                if playerRot > -90:
                    playerRot -= playerVelRot

            # draw sprites
            SCREEN.blit(Img['background'], (0, 0))

            for ucov, lcov in zip(upperCovid, lowerCovid):
                SCREEN.blit(Img['covid'][0], (ucov['x'], ucov['y']))
                SCREEN.blit(Img['covid'][1], (lcov['x'], lcov['y']))

            SCREEN.blit(Img['base'], (0, 568))
            MainProcess.showScore(score,50)

            playerSurface = pygame.transform.rotate(Img['player'][1], playerRot)
            SCREEN.blit(playerSurface, (playerx, playery))
            SCREEN.blit(Img['gameover'], (int((ScreenWidth - Img['gameover'].get_width()) / 2),int(ScreenHeight * 0.12)+50))
            SCREEN.blit(Img['tips'],(int((ScreenWidth - Img['tips'].get_width()) / 2),int(ScreenHeight * 0.12)+100))
            SCREEN.blit(text,(int((ScreenWidth - text.get_width())/2),int(ScreenHeight * 0.12)+600))
            
            FPSCLOCK.tick(fps)
            pygame.display.update()

    def playerShm(playerShm):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(playerShm['val']) == 8:
            playerShm['dir'] *= -1

        if playerShm['dir'] == 1:
            playerShm['val'] += 1
        else:
            playerShm['val'] -= 1

    def getRandomCovid():
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(BaseY * 0.6 - CovidGapSize))
        gapY += int(BaseY * 0.2)
        covHeight = Img['covid'][0].get_height()
        covX = ScreenWidth + 1
        
        return [
            {
                'x': covX,
                'y': gapY - covHeight
            },  # upper pipe
            {
                'x': covX,
                'y': gapY + CovidGapSize
            },  # lower pipe
        ]

    def showScore(score,height):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += Img['numbers'][digit].get_width()

        

        Xoffset = (ScreenWidth - totalWidth) / 2

        for digit in scoreDigits:
            SCREEN.blit(Img['numbers'][digit], (Xoffset, height))
            Xoffset += Img['numbers'][digit].get_width()

    def checkCrash(player, upperCovid, lowerCovid):
        """returns True if player collders with base or pipes."""
        pi = player['index']
        player['w'] = Img['player'][0].get_width()
        player['h'] = Img['player'][0].get_height()

        # if player crashes into ground
        if player['y'] + player['h'] >= BaseY :
            return [True, True]
        else:

            playerRect = pygame.Rect(player['x'], player['y'], player['w']-10, player['h']-12)
            covW = Img['covid'][0].get_width()-15
            covH = Img['covid'][0].get_height()-12

            for ucov, lcov in zip(upperCovid, lowerCovid):
                # upper and lower pipe rects
                ucovRect = pygame.Rect(ucov['x'], ucov['y'], covW, covH)
                lcovRect = pygame.Rect(lcov['x'], lcov['y'], covW, covH)

                # player and upper/lower pipe hitmasks
                pHitMask = Hitmasks['player'][pi]
                uHitmask = Hitmasks['covid'][0]
                lHitmask = Hitmasks['covid'][1]

                # if player collided with upipe or lpipe
                uCollide = MainProcess.pixelCollision(playerRect, ucovRect, pHitMask, uHitmask)
                lCollide = MainProcess.pixelCollision(playerRect, lcovRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    return [True, False]

        return [False, False]

    def pixelCollision(rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in xrange(rect.width):
            for y in xrange(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False

    def getHitmask(image):
        """returns a hitmask using an image's alpha."""
        mask = []
        for x in xrange(image.get_width()):
            mask.append([])
            for y in xrange(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

clicked = False

class Button:
    button_col = (25,190,225)
    hover_col = (75,225,255)
    click_col = (50,150,255)
    text_col = (225,255,255)


    def __init__(self,x,y,text,width,height):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.height = height

    def draw_btn(self):
        global clicked
        action = False

        
        #mouse position
        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x,self.y,self.width,self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(SCREEN, self.click_col, button_rect)
                
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True

            else:
                pygame.draw.rect(SCREEN,self.hover_col, button_rect)
        else:
            pygame.draw.rect(SCREEN, self.button_col, button_rect)
            
        font = pygame.font.SysFont('Constantia', 25)
        white = (255,255,255)
        black = (0,0,0)

        pygame.draw.line(SCREEN,white,(self.x,self.y),(self.x + self.width,self.y),2)
        pygame.draw.line(SCREEN,white,(self.x,self.y),(self.x, self.y + self.height),2)
        pygame.draw.line(SCREEN,black,(self.x,self.y + self.height),(self.x + self.width,self.y + self.height),2)
        pygame.draw.line(SCREEN,black,(self.x + self.width, self.y),(self.x + self.width,self.y + self.height),2)
        

        text_img = font.render(self.text,True,self.text_col)
        text_len = text_img.get_width()
        SCREEN.blit(text_img,(self.x + int(self.width/2) - int(text_len/2),self.y+5))
        return action

class btns:
    def buttons():
        global count
        round_played = str(len(score_list))
        if count > 0:
            return MainScreen.showWelcomeAnimation()
        elif count == 0:
            
            Img['bg'] = pygame.image.load('assets/sprites/bg.jpg').convert_alpha()
            Img['bg'] = pygame.transform.scale(Img['bg'],(ScreenWidth,ScreenHeight))
            Img['title'] = pygame.image.load('assets/sprites/title.png').convert_alpha()
            Img['title'] = pygame.transform.scale(Img['title'],(500,100))
            font = pygame.font.SysFont('timesnewroman', 18)
            white = (255,255,255)
            black = (0,0,0)
            text = font.render(('Rounds Played ' + round_played),False,white)


            
            recent = Button(170,500,'Recent Scores',300,40)
            top = Button(810,500,'Top 3 Scores',300,40)
            play = Button(490,400,'Play',300,40)
            how = Button(1130,50,'?',50,25)
            empty = Button(0,0,'',0,0)
            
            run = True
            while run:
                SCREEN.blit(Img['bg'],(0,0))
                SCREEN.blit(Img['title'],(int((ScreenWidth - Img['title'].get_width()) / 2),int(ScreenHeight * 0.12)+100))
                SCREEN.blit(text,(int((ScreenWidth - text.get_width())/2),int(ScreenHeight * 0.12)+600))
                if recent.draw_btn():
                        
                    MainScreen.recent()
                    run = False
                    
                elif top.draw_btn():
                    MainScreen.top3()
                    run = False

                
                elif how.draw_btn():
                    a = 0
                    Tutorial.how(a)
                    run = False
                    
                elif play.draw_btn():
                    MainScreen.showWelcomeAnimation()
                    run = False

                else:
                    run = True
                    
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                pygame.display.update()


    def back_button():
        global count
        back = Button(490,600,'Return to Lobby',300,40)
        
        if back.draw_btn():
            count = 0
            MainScreen.Lobby()      

class Tutorial:
    def how(a):
        global count

        Img['how'] = [pygame.image.load('assets/sprites/howtoplay1.jpg').convert(),
                      pygame.image.load('assets/sprites/howtoplay2.jpg').convert(),
                      pygame.image.load('assets/sprites/howtoplay3.jpg').convert(),
                      ]
        
        
        Img['bg1'] = pygame.image.load('assets/sprites/bg.jpg').convert()
        Img['bg1'] = pygame.transform.scale(Img['bg1'],(ScreenWidth,ScreenHeight))
        
        font = pygame.font.SysFont('arial', 20)
        white = (255,255,255)
        black = (0,0,0)
        text = [font.render(('To play tap the [space bar], [arrow up] or [left mouse key] to move. Avoid covid-19 obstacle by passing through its gap or spaces'),False,white),
                font.render(('To view 5 recent scores, Go to lobby and look for recent scores button'),False,white),
                font.render(('To view your top 3 scores, Go to lobby and look for top 3 score button'),False,white),
                ]

        
        while True:
            
            if count >0:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                        return True
            else:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                SCREEN.blit(Img['bg1'],(0,0))
                SCREEN.blit(Img['how'][a],(int((ScreenWidth - Img['how'][a].get_width()) / 2),int(ScreenHeight * 0.12)+50))
                SCREEN.blit(text[a],(int((ScreenWidth - text[a].get_width())/2),int(ScreenHeight * 0.12)+400))
                next_how = Button(1130,ScreenHeight/2,'Next',60,40)
                back_how = Button(150,ScreenHeight/2,'Back',60,40)
                if a < 2:
                    if next_how.draw_btn():
                        
                        return Tutorial.how(a+1)
                    
                if a > 0:
                    if back_how.draw_btn():
                        
                        return Tutorial.how(a-1)
       
                btns.back_button()
                pygame.display.update()
                FPSCLOCK.tick(fps)

class Scores:
    def score_list(score):
        global score_list
        score_list.insert(0,score)
        top.append(score)
        Update.database(score)

class Update:
    def database(score):
        score = str(score)
        cursor.execute("INSERT INTO scores(score_list)VALUES ('{}');".format(score))
        conn.commit()
        cursor.execute("INSERT INTO scores(top)VALUES ('{}');".format(score))
        conn.commit()
                
   
cursor.execute("SELECT score_list FROM scores")          
scores =cursor.fetchall()
score_list = []
if not(scores==[]):
    for score in scores:
        score = str(score)
        score = score.replace("(","")
        score = score.replace(")","")
        score = score.replace(",","")
        if score != 'None':
            score_list.append(int(score))
else:
    score_list = []
    
conn.commit()
cursor.execute("SELECT top FROM scores")
tops = cursor.fetchall()
top = []
if not(tops==[]):
    for score in tops:
        score = str(score)
        score = score.replace("(","")
        score = score.replace(")","")
        score = score.replace(",","")
        if score != 'None':
            top.append(int(score))
else:
    top = []
conn.commit()

count = 0
MainScreen.main()

