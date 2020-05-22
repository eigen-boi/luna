"""
Created on Sun Apr  7 20:21:22 2019
@author: Aidan
"""
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import math
import secrets
import sys
import os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

number_of_levels = 2

PINK = (255,200,200)
coll = (255, 255, 255) 
displaywidth = 1152
displayheight = 648
floor = 440
volume = 1
wn = pygame.display.set_mode((displaywidth, displayheight))
pygame.display.set_caption('luna')

game_folder = os.path.dirname(__file__)
textures = os.path.join(game_folder, "textures")
audio = os.path.join(game_folder, "audio")

walkright = pygame.image.load(os.path.join(textures, "R12.png")).convert_alpha()
walkleft = pygame.image.load(os.path.join(textures, "L12.png")).convert_alpha()
leftcrouch = pygame.image.load(os.path.join(textures, "sql2.png")).convert_alpha()
rightcrouch = pygame.image.load(os.path.join(textures, "sqr2.png")).convert_alpha()
crouch = pygame.image.load(os.path.join(textures, "sq2.png")).convert_alpha()
lookup = pygame.image.load(os.path.join(textures, "up2.png")).convert_alpha()
screm = [pygame.image.load(os.path.join(textures, "1.png")).convert_alpha(), pygame.image.load(os.path.join(textures, "2.png")).convert_alpha(), 
         pygame.image.load(os.path.join(textures, "3.png")).convert_alpha(), pygame.image.load(os.path.join(textures, "4.png")).convert_alpha(), 
         pygame.image.load(os.path.join(textures, "5.png")).convert_alpha(), pygame.image.load(os.path.join(textures, "6.png")).convert_alpha(),
         pygame.image.load(os.path.join(textures, "7.png")).convert_alpha(), pygame.image.load(os.path.join(textures, "8.png")).convert_alpha(), 
         pygame.image.load(os.path.join(textures, "9.png")).convert_alpha(), pygame.image.load(os.path.join(textures, "10.png")).convert_alpha()]
bg1 = pygame.image.load(os.path.join(textures, "bg2.png")).convert_alpha()
bg2 = pygame.image.load(os.path.join(textures, "bg345.png")).convert_alpha()
introbg = pygame.image.load(os.path.join(textures, "slide.png")).convert_alpha()
pausescreen = pygame.image.load(os.path.join(textures, "pause.png")).convert_alpha()
char = pygame.image.load(os.path.join(textures, "default2.png")).convert_alpha()
turnip_front = pygame.image.load(os.path.join(textures, "radish4.png")).convert_alpha()
turnip_left = pygame.image.load(os.path.join(textures, "radishl3.png")).convert_alpha()
turnip_right = pygame.image.load(os.path.join(textures, "radishr3.png")).convert_alpha()
icon = pygame.image.load(os.path.join(textures, "icon.png")).convert_alpha()
orbtex = pygame.image.load(os.path.join(textures, "orb3.png")).convert_alpha()
darkorbtex = pygame.image.load(os.path.join(textures, "orb4.png")).convert_alpha()
#songs = ['audio/KylaAlfredo.m4a', 'audio/SportsResort.wav', 'audio/froth.m4a', 'audio/Homecoming.wav'] 
songs = [os.path.join(audio, "KylaAlfredo.m4a"), os.path.join(audio, "SportsResort.wav"), os.path.join(audio, "froth.m4a"), os.path.join(audio, "Homecoming.wav")]
pygame.mixer.pre_init(buffer=128)
pygame.mixer.init()
pygame.init()
scream = pygame.mixer.Sound(os.path.join(audio, "screm3.WAV"))
bounc = pygame.mixer.Sound(os.path.join(audio, "Bo.WAV"))
ear = pygame.mixer.Sound(os.path.join(audio, "boom.WAV"))
wall = [pygame.mixer.Sound(os.path.join(audio, "wall1.WAV")), 
        pygame.mixer.Sound(os.path.join(audio, "wall2.WAV"))]
hit = [pygame.mixer.Sound(os.path.join(audio, "hit1.WAV")), 
       pygame.mixer.Sound(os.path.join(audio, "hit2.WAV")),
       pygame.mixer.Sound(os.path.join(audio, "hit3.WAV")),
       pygame.mixer.Sound(os.path.join(audio, "hit4.WAV")),
       pygame.mixer.Sound(os.path.join(audio, "hit5.WAV"))]
pop = pygame.mixer.Sound(os.path.join(audio, "pop2.WAV"))
clock = pygame.time.Clock()

 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        width = 37
        height = 35
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.leftc = False
        self.rightc = False
        self.c = False
        self.up = False
        self.screme = False
        self.holdit = 0
        self.isj=False
        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        #self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.level = None
        
    def draw(self,wn):
        if self.holdit>=10:
            self.holdit = 0
        if self.left:
            wn.blit(walkleft, self.rect)
        elif self.right:
            wn.blit(walkright, self.rect)
        elif self.screme:
            wn.blit(screm[self.holdit], self.rect)
            self.holdit += 1
        elif self.leftc:
            wn.blit(leftcrouch, self.rect)
        elif self.rightc:
            wn.blit(rightcrouch, self.rect)
        elif self.c:
            wn.blit(crouch, self.rect)
        elif self.up:
            wn.blit(lookup, self.rect)
        else:
            wn.blit(char, self.rect)  

    def jump(self):
        self.isj = True
        while self.isj:
            self.rect.y += 1
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 1
            if len(platform_hit_list) > 0 or self.rect.bottom >= floor:
                self.vely = -19
                bounc.play()
            # wait here
            self.isj=False


    def update(self): # move 
        self.gravity()
        self.rect.x += self.velx
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.velx > 0:
                self.stop()
                self.rect.right = block.rect.left
            elif self.velx < 0:
                self.stop()
                self.rect.left = block.rect.right
           # self.velx = -self.velx
            self.velx = 0

        self.rect.y += self.vely
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # reset position based on the top/bottom of the object
            if self.vely > 0 and self.vely < 18:
                self.rect.bottom = block.rect.top
                self.vely = 0
            elif self.vely>=18:
                self.rect.bottom = block.rect.top
                if self.isj == False:
                    self.vely = -7
                else:
                    self.vely = -19
                #self.vely = -7
            elif self.vely < 0:
                self.rect.top = block.rect.bottom
                self.vely = 0
            #self.vely = 0

    def gravity(self):
        if self.vely == 0:
            self.vely = 0.1
        else:
            self.vely += 0.9
        # see if on ground 
        if self.rect.y >= floor and self.vely >= 0:
            if self.vely <= 20:
                self.vely = 0
                self.rect.y = floor 
            if self.vely >= 20 and self.vely < 30:
                if self.isj == False:
                    self.vely = -6
                else:
                    self.vely = 0
                self.rect.y = floor
                bounc.play()
            if self.vely >= 30:
                scream.play()
                bounc.play()
                if self.isj == False:
                    self.vely = -10
                else:
                    self.vely = 0
                self.rect.y = floor
        elif self.rect.y == 10 and self.vely <=0 :
            ear.play()
            self.vely = -35
            scream.play()
            
    def go_left(self):
        self.right=False
        self.velx = -6
    def go_right(self):
        self.left=False
        self.velx = 6
    def stop(self):
        self.left=False
        self.right=False
        self.leftc = False
        self.rightc = False
        self.up = False
        self.velx = 0
        
        

class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        width = 37
        height = 37
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.isj=False
        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        #self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.level = None
        
    def draw(self,wn):
        if self.left:
            wn.blit(turnip_left, self.rect)
        elif self.right:
            wn.blit(turnip_right, self.rect)
        else:
            wn.blit(turnip_front, self.rect)  

    def jump(self):
        self.isj = True
        while self.isj:
            # next three lines check for collision (is jump allowed)
            self.rect.y += 1
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 1
            if len(platform_hit_list) > 0 or self.rect.bottom >= floor:
                self.vely = -19
                bounc.play()
            # wait here
            self.isj=False

    def update(self): # move 
        self.gravity()
        self.rect.x += self.velx
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.velx > 0:
                self.stop()
                self.rect.right = block.rect.left
            elif self.velx < 0:
                self.stop()
                self.rect.left = block.rect.right
           # self.velx = -self.velx
            self.velx = 0

        self.rect.y += self.vely
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # reset position based on the top/bottom of the object
            if self.vely > 0 and self.vely < 18:
                self.rect.bottom = block.rect.top
                self.vely = 0
            elif self.vely>=18:
                self.rect.bottom = block.rect.top
                if self.isj == False:
                    self.vely = -7
                else:
                    self.vely = -19
                #self.vely = -7
            elif self.vely < 0:
                self.rect.top = block.rect.bottom
                self.vely = 0
            #self.vely = 0

    def gravity(self):
        if self.vely == 0:
            self.vely = 0.1
        else:
            self.vely += 1
        # see if on ground 
        if self.rect.y >= floor and self.vely >= 0:
            if self.vely <= 20:
                self.vely = 0
                self.rect.y = floor 
            if self.vely >= 20 and self.vely < 30:
                if self.isj == False:
                    self.vely = -6
                else:
                    self.vely = 0
                self.rect.y = floor
                bounc.play()
            if self.vely >= 30:
                bounc.play()
                if self.isj == False:
                    self.vely = -10
                else:
                    self.vely = 0
                self.rect.y = floor
        elif self.rect.top <= 50 and self.rect.top > 0 and self.vely <=0 :
            ear.play()
            self.vely = -35
            scream.play()
            
    def go_left(self):
        self.right=False
        self.velx = -7
    def go_right(self):
        self.left=False
        self.velx = 7
    def stop(self):
        self.left=False
        self.right=False
        self.velx = 0


# ---------------------------------------------------------------
BOB = pygame.USEREVENT
i = 1
velx = 0
poss = 180
possy = 265
pygame.time.set_timer(BOB, 300)
class Orb(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()

        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()

        self.rect = self.image.get_rect()

        self.vely = 0
        self.level = None

    def update(self): # move 

        self.vely = i
        self.rect.y = possy
        self.rect.y += self.vely
        self.rect.x = poss

    def draw(self,wn):
        if current_level_no == 2:
            wn.blit(orbtex, self.rect)
        elif current_level_no == 1:
            wn.blit(darkorbtex, self.rect)

 
# ---------------------------------------------------------------

def new_song(): # how does this work? idk
    global songs 
    songs = songs[1:] + [songs[0]]
    pygame.mixer.music.load(songs[0])
    pygame.mixer.music.play()
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

class Pause(object):

    def __init__(self):
        self.paused = pygame.mixer.music.get_busy()

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
        if not self.paused:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    
def text_format(message, textFont, textSize, textColor): # why is the text ugly? idk
    pygame.font.init()
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText
    
def main_menu():
    menu=True
    selected = False
    while menu:
        pygame.init()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    selected=True
                elif event.key==pygame.K_ESCAPE or event.key==pygame.K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                if event.key==pygame.K_RETURN:
                    if selected==True:
                        menu = False

        title = text_format("luna", 'freesansbold.ttf', 75, (0,0,0))
        # Main Menu UI
        wn.blit(introbg, (0,0))
        prompt = text_format("press enter to play", 'freesansbold.ttf', 45, (0, 0, 0))
        # Main Menu Text
        wn.blit(prompt, (displaywidth*0.6, displayheight/2))
        wn.blit(title, (displaywidth*0.74, displayheight/4))
        pygame.display.update()
        pygame.display.set_caption("luna")
        
def set_players():
    menu=True
    selected = False
    global two_player
    while menu:
        pygame.init()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE or event.key==pygame.K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                if event.key==pygame.K_1:
                    two_player = False
                    menu = False
                elif event.key==pygame.K_2:
                    two_player = True
                    menu = False
        if selected == True:
            title = text_format("Play!", 'freesansbold.ttf', 75, (0,0,0))
        else:
            title = text_format("luna", 'freesansbold.ttf', 75, (0,0,0))
        # Main Menu UI
       # print('two_player 2', two_player)
        wn.blit(introbg, (0,0))
        prompt = text_format("press 1 for single player, or 2 for two player", 'freesansbold.ttf', 20, (0, 0, 0))
        # Main Menu Text
        wn.blit(prompt, (displaywidth*0.6, displayheight/2))
        wn.blit(title, (displaywidth*0.74, displayheight/4))
        pygame.display.update()
        pygame.display.set_caption("luna")
#print('two_player 3', two_player)
def pause_menu():
    menu=True
    selected = False
    pygame.init()
    global two_player
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    selected=True
                elif event.key==pygame.K_ESCAPE or event.key==pygame.K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                if event.key==pygame.K_RETURN:
                    if selected==True:
                        menu = False
                if event.key==pygame.K_1:
                    two_player = False
                    menu = False
                elif event.key==pygame.K_2:
                    two_player = True
                    menu = False
        if selected == True:
            title = text_format("Play!", 'freesansbold.ttf', 75, (0,0,0))
        else:
            title = text_format("luna", 'freesansbold.ttf', 75, (0,0,0))
        # Main Menu UI
        wn.blit(pausescreen, (0,0))
        prompt = text_format("press enter to resume", 'freesansbold.ttf', 35, (0, 0, 0))
        prompt2 = text_format("press 1 for single player", 'freesansbold.ttf', 25, (0, 0, 0))
        prompt3 = text_format("press 2 for two player", 'freesansbold.ttf', 25, (0, 0, 0))
        # Main Menu Text
        wn.blit(prompt, (displaywidth*0.6, displayheight/2))
        wn.blit(prompt2, (displaywidth*0.7, 2*displayheight/3))
        wn.blit(prompt3, (displaywidth*0.73, 0.71*displayheight))
        wn.blit(title, (displaywidth*0.74, displayheight/4))
        pygame.display.update()
        pygame.display.set_caption("luna")

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        #self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
 
class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.friend_list = pygame.sprite.Group()
        self.player = player
        self.active_sprite_list = pygame.sprite.Group()
        # Background image
        #self.background = None
    # Update everything on this level
    def update(self):
        self.platform_list.update()
        self.friend_list.update()
    def draw(self, wn):
        if current_level_no == 1:
            bg = bg1
        elif current_level_no == 2:
            bg = bg2
        #draw this level
        # draw background
        wn.blit(bg, (0, 0))
        # draw sprite lists 
        self.platform_list.draw(wn)
        self.friend_list.draw(wn)
# platforms 
class Level_01(Level):
    pygame.display.set_icon(icon)
    def __init__(self, player):
        # parent constructor?
        Level.__init__(self, player)
        level = [[100, 32, 526, 342],
                 [100, 32, 142, 300],
                 [100, 32, 910, 300],
                 [100, 32, 334, 200],
                 [100, 32, 718, 200]]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        luna = Player(340, floor, 64, 64)
        turnip = Player2(748, floor, 64, 64)
        fleftorb = Orb(20, 20, 180, 265)   
        
        self.friend_list.add(fleftorb)
        self.active_sprite_list.add(luna)
        self.active_sprite_list.add(turnip)
        
class Level_02(Level):
    pygame.display.set_icon(icon)
    bg = pygame.image.load(os.path.join(textures, "bg345.png")).convert_alpha()
    def __init__(self, player):
        # parent constructor?
        Level.__init__(self, player)
        level = [[160, 32, 112, 342],
                 [160, 32, 880, 342],
                 [100, 32, 142, 200],
                 [100, 32, 910, 200],
                 [100, 32, 526, 200]]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        luna = Player(340, floor, 64, 64)
        fleftorb = Orb(20, 20, 180, 265)  
        turnip = Player2(748, floor, 64, 64)
        
        self.friend_list.add(fleftorb)
        self.active_sprite_list.add(luna)
        self.active_sprite_list.add(turnip)
        
current_level_no = 0       
choose_pause = False
def main():
    global two_player
    global current_level_no
    global choose_pause
    pygame.display.set_caption("luna")
    PAUSE = Pause()
    luna = Player(340, floor, 64, 64)
    fleftorb = Orb(20, 20, 180, 265)
    turnip = Player2(748, floor, 64, 64)
    
    # create levels
    level_list = []
    level_list.append(Level_01(luna))
    level_list.append(Level_01(fleftorb))
    level_list.append(Level_02(luna))
    level_list.append(Level_02(fleftorb))
    if two_player:
        level_list.append(Level_01(turnip))
        level_list.append(Level_02(turnip))
    
    # set current level
    current_level_no += 1
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    luna.level = current_level
    fleftorb.level = current_level
    turnip.level = current_level
    active_sprite_list.add(turnip)
        
    luna.rect.x = 340
    luna.rect.y = floor
    fleftorb.rect.x = 180
    fleftorb.rect.y = 265
    turnip.rect.x = 748
    turnip.rect.y = floor
    active_sprite_list.add(luna)
    active_sprite_list.add(fleftorb)

    new_song()
    #main_menu()
    run = True
    iii = 0
    points = 0
    clock = pygame.time.Clock()
    compliments = ["outstanding! you're an expert on being cool!", 
            "I can't believe it! You've practically beat the game!",
            "wow, you're good", "you will continue to inspire for generations to come!",
            "where did you learn to get so many points?", 
            "great job!", "I'm so proud of you!", 
            "I love what you've done with the place", 
            "uh oh, your gamer score is too high to calculate!", 
            "do you have the wifi password?", "god, what an ingenious point system",
            '"you will die"', "don't look now, but I think whoever is playing this game is the best",
            "sometimes, you just gotta get it", "it just be that way sometimes", 
            "wasps have physically manifested in my mouth", 
            "you'll never read all of these if that's what you're trying to do...",
            "one of us has to pretend", "Each minor problem like a grain of sand, each night I inherit the desert.",
            "it's just such a HIGH SCORE", "oh right, we're playing a game. I forgot",
            "maybe one day", "who are you?", "who am I?",
            "lets play truth or dare. I dare you to be the best ever - oh wait, you already are!",
            "a moment is a slice of eternity", "you look familiar, do you have your own cereal?",
            "My greatest weapon is knowledge. And laser beam eyes.",
            "why must all the hoops be on fire?", "A snake with hands, but I have your gloves!",
            "We fat all creatures else for us, and we fat ourselves for maggots",
            "little known fact, steel wool comes from robot sheep",
            "Death: the final succ", "nitrogen isn't real", "my mind is like a well oiled Eagle",
            "the eary bird gets the worm - the early worm is eaten", 
            "every second you're not running, I'm only getting closer",
            "I survived because the fire inside me burned brighter than the fire around me",
            "you cannot kill me in a way that matters", "technology's just nature we taught to do cool tricks", 
            "are you putting a curse on me?", "I'd eat your slice",
            "that really stirs my noodles", "people don't understand how many bats there are", "well thumb me green", 
            "this is where they create their power", 
            "my sonar has been up for days", "We exist because the jellyfish wills it so. WHY ELSE?",
            "you are welcome here... the earth does not shrink away from your footsteps",
            "guillotines often backfired, leaving the victims head even more firmly attached",
            "sloths aren't lazy, they're saving their energy. Today, that energy is released.",
            "when you die, you go to the mii plaza", "I swear I can hear the plants whispering", "hnggg", "what are you looking at"]
    # -------- main loop --------
    while run:
        
        distance = math.sqrt((luna.rect.x - fleftorb.rect.x)**2 + (luna.rect.y - fleftorb.rect.y)**2)
        distance2 = math.sqrt((turnip.rect.x - fleftorb.rect.x)**2 + (turnip.rect.y - fleftorb.rect.y)**2)
        distance3 = math.sqrt((turnip.rect.x - luna.rect.x)**2 + (turnip.rect.y - luna.rect.y)**2)
        global i
        global volume
        global possy
        length = int(len(compliments))
        spoints = str(points)
        disp_point = text_format("points:", 'freesansbold.ttf', 35, (0, 0, 0))
        if distance3 < 20 and two_player:
            hit_now = secrets.choice(hit)
            hit_now.play()
            if turnip.velx == 0 and turnip.vely == 0:
                luna.vely = -12
            else:
                luna.velx = 3.5*turnip.velx + luna.velx
                luna.vely = 2*turnip.vely 
        if distance < 32 or distance2 < 32 and two_player:
            points += 1
            pop.play()
            global poss
            if poss == 180:
                poss = secrets.choice([948, 372, 756])
            elif poss == 948:
                poss = secrets.choice([180, 372, 756])
            elif poss == 372:
                poss = secrets.choice([180, 948, 756])
            elif poss == 756:
                poss = secrets.choice([180, 372, 948])
            possy = secrets.choice([10, 20, 30, 40, 60, 70, 80, 90, 100, 
                                    110, 120, 130, 140, 150, 160, 170, 180,
                                    230, 240, 250, 260, 270, 280,
                                    330, 350, 360, 370, 380, 390, 400, 410, 420,
                                    430])
            if length>0 and points>=7:
                iii = secrets.choice(range(length))
                soup = compliments.pop(iii) 

        if length <= 0:
            disp_points = text_format(spoints, 'freesansbold.ttf', 35, (0, 0, 0))
            if points == 69:
                disp_points = text_format("696969696969696969696969696969696969696969696969696969696969696969696969", 'freesansbold.ttf', 25, (0, 0, 0))
            if points == 100:
                disp_points = text_format("100 points? I get it, you're a hardcore gamer... no need to flex so hard!", 'freesansbold.ttf', 25, (0, 0, 0))
        else:
            if points > 5 and points < 7:
                disp_points = text_format("so many", 'freesansbold.ttf', 35, (0, 0, 0))
            elif points <= 5:
                disp_points = text_format(spoints, 'freesansbold.ttf', 35, (0, 0, 0))
            elif points == 42:
                disp_points = text_format("420 - I mean 42... my bad", 'freesansbold.ttf', 35, (0, 0, 0))
            elif points % 10 == 0:
                disp_points = text_format(spoints, 'freesansbold.ttf', 35, (0, 0, 0))
            else:
                disp_points = text_format(soup, 'freesansbold.ttf', 25, (0, 0, 0))

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            clock.tick(60)
            if event.type == BOB:
                i=i*-1
            if event.type == pygame.QUIT or keys[pygame.K_BACKSPACE]:
                run = False
            if event.type == SONG_END:
                new_song()
                
            if keys[pygame.K_a]:
                luna.go_left()
                if keys[pygame.K_LSHIFT]:
                    luna.left = False
                    luna.leftc = True
                    luna.rightc = False
                else:
                    luna.left = True
                    luna.leftc = False
            elif keys[pygame.K_d]:
                luna.go_right()
                if keys[pygame.K_LSHIFT]:
                    luna.right = False
                    luna.rightc = True
                    luna.leftc = False
                else:
                    luna.right = True
                    luna.rightc = False
                    
            if keys[pygame.K_LEFT]:
                turnip.go_left()
                turnip.left = True
            elif keys[pygame.K_RIGHT]:
                turnip.go_right()
                turnip.right = True

            if keys[pygame.K_SPACE]:
                luna.jump()
            if keys[pygame.K_UP]:
                turnip.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and luna.velx < 0:
                    luna.stop()
                if event.key == pygame.K_d and luna.velx > 0:
                    luna.stop()
                if event.key == pygame.K_LEFT and turnip.velx < 0:
                    turnip.stop()
                if event.key == pygame.K_RIGHT and turnip.velx > 0:
                    turnip.stop()
                
                
            if keys[pygame.K_ESCAPE] or keys[pygame.K_s] or keys[pygame.K_BACKSPACE]:
                scream.play()
                luna.left = False
                luna.right = False
                
            if keys[pygame.K_ESCAPE]:
                if choose_pause == False:
                    PAUSE.toggle()
                pause_menu()
                if choose_pause == False:
                    PAUSE.toggle()
            
            if keys[pygame.K_i]:
                choose_pause = not choose_pause
                PAUSE.toggle()

            if points == 70:
                if current_level_no < number_of_levels: # number of levels so don't break
                    main()
                else:
                    current_level_no = 0
                    main()

            else:
                luna.screme = False
                luna.c = False
                luna.up = False
                if keys[pygame.K_LSHIFT]:
                    luna.c = True
                if keys[pygame.K_w]:
                    luna.up = True
                if keys[pygame.K_s]:
                    luna.screme = True

        # update the players
        active_sprite_list.update()
 
        # update items in the level
        current_level.update()
 
        if luna.rect.right > displaywidth:
            if luna.velx > 24:
                wall_now = secrets.choice(wall)
                wall_now.play()
            luna.velx = 0
            luna.stop()
            luna.rect.right = displaywidth
        if turnip.rect.right > displaywidth:
            turnip.rect.right = displaywidth
 
        if luna.rect.left < 0:
            if luna.velx < -24:
                wall_now = secrets.choice(wall)
                wall_now.play()
            luna.velx = 0
            luna.stop()
            luna.rect.left = 0
        if turnip.rect.left < 0:
            turnip.rect.left = 0
 
        # CODE TO DRAW BELOW THIS 
        current_level.draw(wn)
        wn.blit(disp_points, (150, 24))
        wn.blit(disp_point, (24, 24))
        active_sprite_list.draw(wn)
        fleftorb.draw(wn)
        luna.draw(wn)
        if two_player:
            turnip.draw(wn)
        # CODE TO DRAW ABOVE THIS 
 
        clock.tick(60)
 
        pygame.display.update()

    pygame.quit()

main_menu()
set_players()
main()