# objective: make a game

# game: click circles that get harder and harder and see who gets a high score

import pygame
import random
import math
import os
import sys
from tkinter import Tk, messagebox

import pygame
pygame.init()
pygame.mixer.init()

buttonclicksound = pygame.mixer.Sound("audio/buttonclick.wav")
hitsound = pygame.mixer.Sound("audio/hitsound.wav")
upgradesound = pygame.mixer.Sound("audio/upgrade.wav")
misssound = pygame.mixer.Sound("audio/miss.wav")
hurryupsound = pygame.mixer.Sound("audio/hurryup.wav")
hitsound.set_volume(0.5)
misssound.set_volume(0.7)

resx = 1000
resy = 750
res = (resx, resy)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("a little game by brave.")
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
MAINMENUHOVER = (0,0,0)
MAINMENUTEXTHOVER = (100,100,100)
GREEN = (50,255,50)
GREENHOVER = (150,255,150)
YELLOW = (255,255,50)
RED = (255,50,50)
REDHOVER = (255,150,150)
GRAY = (150,150,150)
GRAYHOVER = (75,75,75)

class Text:
    def __init__(self, size, text, x, y, color, centered=True, font="Arial"):
        self.font = font
        self.size = size
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.centered = centered

        self.renderfont = pygame.font.SysFont(self.font, self.size)
        self.rendertext = self.renderfont.render(self.text, True, self.color)

    def render(self, surface):
        rendertext = self.rendertext
        if self.centered == True:
            textrect = self.rendertext.get_rect()
            textrect.center = (self.x, self.y)
            surface.blit(rendertext, textrect)
        else:
            surface.blit(rendertext, (self.x, self.y))

    def updatetext(self, newtext=None, newcolor=None):
        if newtext is not None:
            self.text = newtext
        if newcolor is not None:
            self.color = newcolor
        
        self.rendertext = self.renderfont.render(self.text, True, self.color)

class Button:
    def __init__(self, x, y, width, height, text, color, textcolor, hovertextcolor, hovercolor, fontsize=32):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.color = color
        self.textcolor = textcolor
        self.hovertextcolor = hovertextcolor
        self.hovercolor = hovercolor
        self.renderfont = pygame.font.SysFont("Arial", fontsize)
        self.rendertext = self.renderfont.render(text, True, textcolor)
        self.textrect = self.rendertext.get_rect(center=self.rect.center)

    def render(self, surface):
        mousepos = pygame.mouse.get_pos()
        if self.ishovering(mousepos):
            pygame.draw.rect(surface, self.hovercolor, self.rect)
            self.rendertext = self.renderfont.render(self.text, True, self.hovertextcolor)
            surface.blit(self.rendertext, self.textrect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            self.rendertext = self.renderfont.render(self.text, True, self.textcolor)
            surface.blit(self.rendertext, self.textrect)

    def updatebutton(self, newtext, newcolor, newhovertext, newhovercolor):
        self.text = newtext
        self.color = newcolor
        self.hovertext = newhovertext
        self.hovercolor = newhovercolor
        self.textrect = self.rendertext.get_rect(center=self.rect.center)

    def ishovering(self, pos):
        return self.rect.collidepoint(pos)

def show_error(title, message):
    root = Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()

def anticheat():
    show_error("Error", "your save file was corrupted. in the future, please don't try to touch it again.")

    os.remove("SAVE.save")
    pygame.quit()
    sys.exit()

if os.path.exists("SAVE.save"):
    savefile = open('SAVE.save', 'r')
    highscore = savefile.readline().strip()
    line2 = savefile.readline().strip()
    uisounds = savefile.readline().strip()
    hitsounds = savefile.readline().strip()
    upgradesounds = savefile.readline().strip()

    savefile.close()
    try:
        securitycheck = (math.floor((int(highscore)**2)/2) - 1) - int(line2)
    except:
        anticheat()
    if securitycheck != 0:
        anticheat()
    if uisounds != "0" and uisounds != "1":
        anticheat()
    if hitsounds != "0" and hitsounds != "1":
        anticheat()
    if upgradesounds != "0" and upgradesounds != "1":
        anticheat()
else:
    highscore = 0
    uisounds = "1"
    hitsounds = "1"
    upgradesounds = "1"
    with open('SAVE.save', 'w') as savefile:
        savefile.write("0\n")
        savefile.write("-1\n")
        savefile.write("1\n")
        savefile.write("1\n")
        savefile.write("1\n")
        savefile.close()

def saveedit(linenumber, newdata):
    with open("SAVE.save") as saveeditor:
        lines = saveeditor.readlines()

    if 1 <= linenumber <= len(lines):
        lines[linenumber - 1] = newdata + '\n'

    with open("SAVE.save", 'w') as saveeditor:
        saveeditor.writelines(lines)

def buttonclick(toggle):
    if toggle == "1":
        buttonclicksound.play()

def circleclick(toggle):
    if toggle == "1":
        hitsound.play()

def upgrade(toggle):
    if toggle == "1":
        upgradesound.play()

def missed(toggle):
    if toggle == "1":
        misssound.play()

class Circle:
    def spawn(self, surface, difficulty):
        self.difficulty = difficulty
        if difficulty == 1:
            randomx = random.randint(100, resx - 100)
            randomy = random.randint(100, resy - 100)
            self.circlecenter = (randomx, randomy)
            self.radius = 75
            pygame.draw.circle(surface, GREEN, self.circlecenter, self.radius)
        elif difficulty == 2:
            randomx = random.randint(50, resx - 50)
            randomy = random.randint(50, resy - 50)
            self.circlecenter = (randomx, randomy)
            self.radius = 50
            pygame.draw.circle(surface, YELLOW, self.circlecenter, self.radius)
        else:
            randomx = random.randint(20, resx - 20)
            randomy = random.randint(20, resy - 20)
            self.circlecenter = (randomx, randomy)
            self.radius = 25
            pygame.draw.circle(surface, RED, self.circlecenter, self.radius)
        
    def render(self, surface):
        if self.difficulty == 1:
            pygame.draw.circle(surface, GREEN, self.circlecenter, self.radius)
        elif self.difficulty == 2:
            pygame.draw.circle(surface, YELLOW, self.circlecenter, self.radius)
        else:
            pygame.draw.circle(surface, RED, self.circlecenter, self.radius)
    
    def ishovering(self):
        mouse_pos = pygame.mouse.get_pos()

        dx = mouse_pos[0] - self.circlecenter[0]
        dy = mouse_pos[1] - self.circlecenter[1]
        dist = math.sqrt(dx**2 + dy**2)

        if dist <= self.radius:
            return True


gamecircle = Circle()


titletext = Text(120, "a little game", resx/2, 100, WHITE)
highscoretext = Text(35, ("highscore: " + str(highscore)), resx/2, 200, WHITE)
watermark = Text(20, "by brave. - v1.0", 50, resy-20, WHITE)
play = Button(resx/2, 350, 100, 75, "play", BLACK, WHITE, MAINMENUTEXTHOVER, MAINMENUHOVER, 50)
options = Button(resx/2, 445, 160, 75, "options", BLACK, WHITE, MAINMENUTEXTHOVER, MAINMENUHOVER, 50)
quit = Button(resx/2, 540, 100, 75, "quit", BLACK, WHITE, RED, MAINMENUHOVER, 50)

back = Button(35, 35, 50, 50, "X", RED, WHITE, GRAY, REDHOVER)
optionstitle = Text(80, "options", resx/2, 100, WHITE)
toggleuisounds = Button(resx/2+200, 225, 125, 60, "ON", GREEN, BLACK, GRAY, GREENHOVER, 40)
toggleuitext = Text(40, "ui sound effects", resx/2 - 200, 225, WHITE)
hitcirclesounds = Button(resx/2+200, 305, 125, 60, "ON", GREEN, BLACK, GRAY, GREENHOVER, 40)
hitcircletext = Text(40, "hit sounds", resx/2 - 200, 305, WHITE)
upgradesoundsb = Button(resx/2+200, 385, 125, 60, "ON", GREEN, BLACK, GRAY, GREENHOVER, 40)
upgradesoundstext = Text(40, "other sfx", resx/2 - 200, 385, WHITE)
creditsb = Button(resx/2+200, 465, 140, 60, "SHOW", GRAY, BLACK, WHITE, GRAYHOVER, 40)
creditsbtext = Text(40, "credits", resx/2 - 200, 465, WHITE)
deletesave = Button(resx/2+200, 545, 185, 60, "DELETE", RED, BLACK, GRAY, REDHOVER, 40)
deletesavetext = Text(40, "delete your save file", resx/2 - 200, 545, WHITE)

creditstitle = Text(80, "credits", resx/2, 100, WHITE)
bravecredit = Text(40, "developed by brave.", resx/2, 225, WHITE)
sistercredit = Text(40, "tested by my sister", resx/2, 305, WHITE)
dedication = Text(40, "dedicated to laxolotl <3", resx/2, 385, WHITE)
thanks = Text(40, "thanks for playing!", resx/2, 465, WHITE)

score = 0
scoretext = Text(32, "score: " + str(score), 10, 10, WHITE, False)
minutes = 0
seconds = 5
frames = 60
timertext = Text(32, "time: " + str(minutes) + ":" + str(seconds), 10, 40, WHITE, False)
combo = 0
maxcombo = 0
combotext = Text(70, "x" + str(combo), 10, resy - 80, WHITE, False)

resultstitle = Text(80, "results", resx/2, 100, WHITE)
rscoretext = Text(40, "final score: " + str(score), resx/2, 200, WHITE)
rhighscoretext = Text(40, "highscore: " + str(highscore), resx/2, 250, WHITE)
rmaxcombotext = Text(40, "max combo: " + str(maxcombo), resx/2, 300, WHITE)
newhighscoretext = Text(40, "new high score!!!", resx/2, 400, YELLOW)
backtomenu = Button(resx/2, resy-225, 300, 75, "back to menu", BLACK, WHITE, GRAY, BLACK, 50)


def mainMenu(surface):
    surface.fill(BLACK)
    titletext.render(screen)
    highscoretext.updatetext("highscore: " + str(highscore), WHITE)
    highscoretext.render(screen)
    watermark.render(screen)
    play.render(screen)
    options.render(screen)
    quit.render(screen)

def optionsMenu(surface):
    surface.fill(BLACK)
    back.render(surface)
    optionstitle.render(screen)
    watermark.render(screen)
    if uisounds == "0":
        toggleuisounds.updatebutton("OFF", RED, GRAY, REDHOVER)
    if uisounds == "1":
        toggleuisounds.updatebutton("ON", GREEN, GRAY, GREENHOVER)
    if hitsounds == "0":
        hitcirclesounds.updatebutton("OFF", RED, GRAY, REDHOVER)
    if hitsounds == "1":
        hitcirclesounds.updatebutton("ON", GREEN, GRAY, GREENHOVER)
    if upgradesounds == "0":
        upgradesoundsb.updatebutton("OFF", RED, GRAY, REDHOVER)
    if upgradesounds == "1":
        upgradesoundsb.updatebutton("ON", GREEN, GRAY, GREENHOVER)
    toggleuisounds.render(screen)
    toggleuitext.render(screen)
    hitcirclesounds.render(screen)
    hitcircletext.render(screen)
    creditsb.render(screen)
    creditsbtext.render(screen)
    deletesave.render(screen)
    deletesavetext.render(screen)
    upgradesoundsb.render(screen)
    upgradesoundstext.render(screen)

def credits(surface):
    surface.fill(BLACK)
    back.render(surface)
    creditstitle.render(surface)
    bravecredit.render(surface)
    sistercredit.render(surface)
    dedication.render(surface)
    thanks.render(surface)

def game(surface, ticking):
    surface.fill(BLACK)
    gamecircle.render(screen)
    scoretext.render(screen)
    if not ticking:
        if seconds >= 10:
            timertext.updatetext("time: " + str(minutes) + ":" + str(seconds))
        else:
            timertext.updatetext("time: " + str(minutes) + ":0" + str(seconds))
    else:
        if seconds >= 10:
            timertext.updatetext("time: " + str(minutes) + ":" + str(seconds), RED)
        else:
            timertext.updatetext("time: " + str(minutes) + ":0" + str(seconds), RED)
    timertext.render(screen)
    combotext.render(screen)

def results(surface, score, highscore, newhighscore=False):
    surface.fill(BLACK)
    resultstitle.render(screen)
    rscoretext.render(screen)
    rhighscoretext.render(screen)
    rmaxcombotext.render(screen)
    if newhighscore == True:
        newhighscoretext.render(screen)
    backtomenu.render(screen)


running = True
scene = "mainmenu"

def initgame(surface):
    surface.fill(BLACK)
    gamecircle.spawn(screen, 1)
    game(screen, ticking)

mainMenu(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if scene == "mainmenu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.ishovering(event.pos):
                    buttonclick(uisounds)
                    score = 1
                    scoremodifier = 1
                    combotemp = 0
                    combo = 0
                    maxcombo = 0
                    frames = 60
                    seconds = 30
                    minutes = 1
                    ticking = False
                    initgame(screen)
                    scene = "game"
                if options.ishovering(event.pos):
                    buttonclick(uisounds)
                    scene = "options"
                if quit.ishovering(event.pos):
                    buttonclick(uisounds)
                    pygame.quit()
                    sys.exit()
        if scene == "options":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.ishovering(event.pos):
                    buttonclick(uisounds)
                    scene = "mainmenu"
                if uisounds == "1":
                    if toggleuisounds.ishovering(event.pos):
                        saveedit(3, "0")
                        uisounds = "0"
                else:
                    if toggleuisounds.ishovering(event.pos):
                        saveedit(3, "1")
                        uisounds = "1"
                        buttonclick(uisounds)
                if hitsounds == "1":
                    if hitcirclesounds.ishovering(event.pos):
                        saveedit(4, "0")
                        hitsounds = "0"
                        buttonclick(uisounds)
                else:
                    if hitcirclesounds.ishovering(event.pos):
                        saveedit(4, "1")
                        hitsounds = "1"
                        buttonclick(uisounds)
                if upgradesounds == "1":
                    if upgradesoundsb.ishovering(event.pos):
                        saveedit(5, "0")
                        upgradesounds = "0"
                        buttonclick(uisounds)
                else:
                    if upgradesoundsb.ishovering(event.pos):
                        saveedit(5, "1")
                        upgradesounds = "1"
                        buttonclick(uisounds)
                if creditsb.ishovering(event.pos):
                    scene = "credits"
                    buttonclick(uisounds)
                if deletesave.ishovering(event.pos):
                    confirm = messagebox.askyesno("delete save file?", "are you sure you want to delete your save file? this will reset all your progress and is irreversible.")
                    if confirm:
                        os.remove("SAVE.save")
                        pygame.quit()
                        sys.exit()
        if scene == "credits":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.ishovering(event.pos):
                    buttonclick(uisounds)
                    scene = "options"
        if scene == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gamecircle.ishovering():
                    # when game circle is hovering, don't click it. instead, cry yourself to sleep and wonder why your life had to go this way.
                    circleclick(hitsounds)
                    score += scoremodifier
                    if score > int(highscore):
                        scoretext.updatetext("score: " + str(score), YELLOW)
                    else:
                        scoretext.updatetext("score: " + str(score), WHITE)
                    combo += 1
                    combotemp += 1
                    if combo > maxcombo:
                        maxcombo = combo
                    if combotemp >= 25:
                        combotemp = 0
                        scoremodifier += 1
                        upgrade(upgradesounds)
                    if combo >= maxcombo:
                        combotext.updatetext("x" + str(combo), YELLOW)
                    else:
                        combotext.updatetext("x" + str(combo), WHITE)
                    if scoremodifier < 3:
                        gamecircle.spawn(screen, 1)
                    elif scoremodifier < 5:
                        gamecircle.spawn(screen, 2)
                    else:
                        gamecircle.spawn(screen, 3)
                else:
                    score -= 1
                    scoremodifier = 1
                    scoretext.updatetext("score: " + str(score), WHITE)
                    combo = 0
                    combotemp = 0
                    combotext.updatetext("x" + str(combo), WHITE)
                    if frames > 50 and seconds == 30 and minutes == 1:
                        print("no sound")
                    else:
                        missed(hitsounds)
        if scene == "results":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backtomenu.ishovering(event.pos):
                    buttonclick(uisounds)
                    scene = "mainmenu"


            
    if scene == "mainmenu":
        mainMenu(screen)
    if scene == "options":
        optionsMenu(screen)
    if scene == "credits":
        credits(screen)
    if scene == "game":
        frames -= 1
        if frames < 0:
            seconds -= 1
            frames = 60
        if seconds < 0 and minutes > 0:
            minutes -= 1
            seconds = 59
        if seconds <= 0 and minutes <= 0:
            newhighscore = False
            hurryupsound.stop()
            results(screen, score, highscore)
            scene = "results"
        if seconds == 20 and minutes == 0 and not ticking:
            ticking = True
            if upgradesounds == "1":
                hurryupsound.play()
        game(screen, ticking)
    if scene == "results":
        if int(score) > int(highscore) and newhighscore == False:
            highscore = score
            saveedit(1, str(highscore))
            saveedit(2, str(math.floor((highscore**2)/2)-1))
            newhighscore = True
        rscoretext.updatetext("final score: " + str(score), WHITE)
        rhighscoretext.updatetext("highscore: " + str(highscore), WHITE)
        rmaxcombotext.updatetext("max combo: x" + str(maxcombo), WHITE)
        results(screen, score, highscore, newhighscore)
    pygame.display.flip()
    clock.tick(60)
