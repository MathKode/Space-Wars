import pygame
import random
pygame.init()
#Color :
black = (0,0,0)
white = (255,255,255)
green = (64, 181, 81)
bleu = (3, 229, 208)
yellow = (240, 233, 11)
orange = (240, 136, 11)
red = (212, 45, 45)
# -----

screen = pygame.display.set_mode((600,800))
pygame.display.set_caption("Space Wars")

clock = pygame.time.Clock()
FPS = 55

class PLAY_button:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('graph/play.png')
        self.image = pygame.transform.scale(self.image,(80,80))
    def afficher(self,screen):
        screen.blit(self.image,(self.x,self.y))
class TUTO_button:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('graph/tuto.png')
        self.image = pygame.transform.scale(self.image,(80,80))
    def afficher(self,screen):
        screen.blit(self.image,(self.x,self.y))
class SELECTEUR:
    def __init__(self,x,y):
        self.rect1 = pygame.Rect(x,y,15,10)
        self.rect2 = pygame.Rect(x+15,y,5,10)
    def move(self,v):
        self.rect1.y += v
        self.rect2.y += v
    def afficher(self,screen):
        pygame.draw.rect(screen,(212, 45, 45),self.rect1)
        pygame.draw.rect(screen,(240, 233, 11),self.rect2)


class PLAYER:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.live_enemi_1 = 10
        self.live_enemi_2 = 25
        self.live_player = 100
        self.attack = 5 
        self.tire_ls = []
        self.bonus = []
        self.enemi_ls = []
        self.velocity = 8
        self.score = 0
        self.image = pygame.image.load('graph/player.png')
        self.image = pygame.transform.scale(self.image,(80,80))
    def move(self,direction):
        self.x += direction*self.velocity #direction is 1 or -1
        if self.x < 5 or self.x > 515 :
            self.x += direction*self.velocity*-1
        for tire in self.tire_ls :
            tire.move()
            if tire.rect.y < 0 :
                self.tire_ls.remove(tire)
        for tire in self.tire_ls :
            for enemi in self.enemi_ls:
                self.Touche(enemi,tire)
        for enemi in self.enemi_ls:
            enemi.move()
            self.Touche3(player,enemi) 
            if enemi.y > 800 :
                if enemi.name == "graph/en2.png" :
                    self.live_player -= 15
                else :
                    self.live_player -= 10
                self.enemi_ls.remove(enemi)
    def shot(self):
        self.tire_ls.append(SHOT(self.x+35,self.y,self.attack))
    def life_en1(self,new):
        self.live_enemi_1 = new
    def life_en2(self,new):
        self.live_enemi_2 = new
    def shot_power(self,new):
        self.attack = new
    def new_bonus(self):
        self.bonus.append(BONUS(random.randint(0,540),3))
    def new_en2(self):
        self.enemi_ls.append(ENEMI(random.randint(0,520),3,self.live_enemi_2,80,'graph/en2.png',70))
    def new_en(self):
        self.enemi_ls.append(ENEMI(random.randint(0,520),3,self.live_enemi_1,70,'graph/en1.png',50)) # dernier a 20
    def new_en2_maxlife(self):
        self.enemi_ls.append(ENEMI(random.randint(0,250),2,self.live_enemi_2 + self.attack*4,90,'graph/en2.png',80))
    def Touche(self,enemi,shot):
        #Permet de dire s ils sont en contact
        #print(shot.rect.topright,enemi.y+70)
        if shot.rect.topright[1] < enemi.y + enemi.largeur and  shot.rect.topright[1] > enemi.y - 30:
            if shot.rect.topright[0] > enemi.x and shot.rect.topright[0] < enemi.x + enemi.largeur :
                #print('touché')
                enemi.shoter(self.attack)
                try :
                    self.tire_ls.remove(shot)
                except :
                     print('er')
                if enemi.life <= 0 :
                    if enemi.name == 'graph/en2.png' :
                        #print('en2')
                        self.score += 2
                    else :
                        self.score += 1
                    self.enemi_ls.remove(enemi)
    def Touche2(self,player,bonus):
        if player.y < bonus.y + 70 and  player.y > bonus.y - 30:
            if player.x > bonus.x - 80 and player.x < bonus.x + 30:
                #print('tBONUS 2')
                player.shot_power(player.attack + 5)
                self.bonus.remove(bonus)
    def Touche3(self,player,enemi):
        if player.y < enemi.y :
            if enemi.x > player.x - enemi.largeur and enemi.x < player.x + enemi.largeur:
                print('BOOM')
                if enemi.name == "graph/en2.png" :
                    self.live_player -= 15
                else :
                    self.live_player -= 10
                self.enemi_ls.remove(enemi)
    def afficher(self,screen):
        screen.blit(self.image,(self.x,self.y))
        BAR_LIVE(self.live_player,100,self.x-9,self.y+80,80,4,screen)
        for i in self.tire_ls: 
            i.afficher(screen)
        for i in self.enemi_ls:
            i.afficher(screen)
            BAR_LIVE(i.life,i.life_totale,i.x,i.y,i.bar_vie_largeur,4,screen)
        for i in self.bonus :
            i.move(3)
            self.Touche2(player,i) 
            i.afficher(screen)
            if i.y > 800 :
                self.bonus.remove(i)
class SHOT:
    def __init__(self,x,y,attack):
        self.velocity = 10
        self.attack = attack
        self.rect = pygame.Rect(x,y,6,17)
    def move(self):
        self.rect.y -= self.velocity
    def afficher(self,screen):
        pygame.draw.rect(screen,(64, 181, 81),self.rect)
class ENEMI:
    def __init__(self,x,velocity,life,taille,name,bar_de_vie_largeur):
        self.x = x
        self.name = name
        self.largeur = taille
        self.y = 0
        self.bar_vie_largeur = bar_de_vie_largeur
        self.life = life
        self.life_totale = life
        self.velocity = velocity
        self.image = pygame.image.load(name)
        self.image = pygame.transform.scale(self.image,(taille,taille))
        self.image = pygame.transform.rotate(self.image,180)
    def move(self):
        self.y += self.velocity
    def shoter(self,under):
        self.life -= under
    def afficher(self,screen):
        screen.blit(self.image,(self.x,self.y))
class BAR_LIVE:
    def __init__(self,vie,vie_totale,x,y,weight,height,ecran):
        fréquence = int(vie / vie_totale * 100) # ex : 10/20 = 0,5
        x += 9
        self.vert = (64, 181, 81) 
        self.red = (212, 45, 45)
        self.pixel_vert = int(weight*fréquence/100) # ex : 30*0,5 = 15 il y a 15 pixel vert
        self.pixel_rouge = weight - self.pixel_vert
        self.rect_vert = pygame.Rect(x,y,self.pixel_vert,height)
        self.rect_red = pygame.Rect(x+self.pixel_vert,y,self.pixel_rouge,height)
        pygame.draw.rect(ecran,self.vert,self.rect_vert)
        pygame.draw.rect(ecran,self.red,self.rect_red)
class BONUS:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('graph/bonus.png')
        self.image = pygame.transform.scale(self.image,(50,50))
    def move(self,vitesse):
        self.y += vitesse
    def afficher(self,screen):
        screen.blit(self.image,(self.x,self.y))

Game_loop = True
ECRAN = 0
choosen_but = 0
touche_appuyée = 0
v = 0
tour = 1
tir = 0
score = 0
music = 1

play_but = PLAY_button(280,300)
tuto_but = TUTO_button(280,350)
selecteur = SELECTEUR(240,338)
player = PLAYER(130,710)

pygame.mixer.music.load("SpaceWars.mp3")
pygame.mixer.music.play(-1)

while Game_loop :
    if ECRAN == 0 :
        tour = 1
        nb_enemi = 1
        spon = 0
        spon_total = 120
        tir = 0
        touche_appuyée = 0
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                Game_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if choosen_but == 0 :
                        selecteur.move(50)
                        choosen_but = 1
                if event.key == pygame.K_UP:
                    if choosen_but == 1 :
                        selecteur.move(-50)
                        choosen_but = 0
                if event.key == pygame.K_RIGHT:
                    if choosen_but == 0 :
                        ECRAN = 1
                        player = PLAYER(130,710)
                    else :
                        ECRAN = 2
                if event.key == pygame.K_m :
                    if music == 1 :
                        music = 0
                        pygame.mixer.music.pause()
                    else :
                        music = 1
                        pygame.mixer.music.unpause()
        myfont = pygame.font.SysFont("Menlo", 50)
        texte = myfont.render("Space WARS", 1, yellow)
        screen.blit(texte, (180, 220))

        play_but.afficher(screen)
        tuto_but.afficher(screen)
        selecteur.afficher(screen)
    if ECRAN == 1 :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                Game_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    v = 1
                    touche_appuyée += 1
                if event.key == pygame.K_LEFT:
                    v = -1
                    touche_appuyée += 1
                if event.key == pygame.K_SPACE:
                    if tir == 0 :
                        player.shot()
                if event.key == pygame.K_UP or event.key == pygame.K_a:
                    tir = 1
                if event.key == pygame.K_m :
                    if music == 1 :
                        music = 0
                        pygame.mixer.music.pause()
                    else :
                        music = 1
                        pygame.mixer.music.unpause()
            if event.type == pygame.KEYUP:
                if nb_enemi > -1 :
                    if event.key == pygame.K_RIGHT:
                        touche_appuyée -= 1
                    if event.key == pygame.K_LEFT:
                        touche_appuyée -= 1
                if event.key == pygame.K_UP or event.key == pygame.K_a :
                    tir = 0
        if tir == 1 and tour%11 == 0 :
            player.shot()
        if touche_appuyée == -1 :
            v = 0  
        if nb_enemi % 10 == 0 :
            nb_enemi += 1
            player.life_en1(player.live_enemi_1 + 5)
        if nb_enemi % 13 == 0 : #25
            nb_enemi += 1
            print("BONUS")
            player.life_en2(player.live_enemi_2 + 5)
            player.new_bonus()
            spon -= 10
        if nb_enemi % 5 == 0 :
            nb_enemi += 1
            player.new_en2()
        if tour == 100 : #220
            tour = 1
            player.new_en()
            nb_enemi += 1
        if spon == spon_total:
            spon = 0
            player.new_en()
            spon_total -= 5
        if spon_total <= 50 :
            spon_total = 120
            player.new_en2_maxlife()
        
        if player.live_player <= 0 :
            print("END")
            ECRAN = 0

        
        player.move(v)
        player.afficher(screen)
    if ECRAN == 2 :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                Game_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    ECRAN = 0
                if event.key == pygame.K_m :
                    if music == 1 :
                        music = 0
                        pygame.mixer.music.pause()
                    else :
                        music = 1
                        pygame.mixer.music.unpause()
        myfont = pygame.font.SysFont("Arial", 20)
        texte = myfont.render("Use arrows to deplace your space boat :", 1, white)
        screen.blit(texte, (0, 100))
        image = pygame.image.load('graph/arrow.png')
        image = pygame.transform.scale(image,(80,80))
        screen.blit(image,(200,250))
        texte = myfont.render("Use Up arrow, a or space to shoot : ", 1, white)
        screen.blit(texte, (0, 400))
        image = pygame.image.load('graph/space.png')    
        image = pygame.transform.scale(image,(80,80))
        screen.blit(image,(200,550))
        texte = myfont.render("Press m to mute ", 1, white)
        screen.blit(texte, (0, 700))
        texte = myfont.render("Press z to return... ", 1, orange)
        screen.blit(texte, (0, 750))

    #fixer le nombre de fps
    clock.tick(FPS)

    #montre le score
    myfont = pygame.font.SysFont("Arial", 20)
    texte = myfont.render(f"Score : {player.score}", 1, white)
    screen.blit(texte, (0, 0))
    myfont = pygame.font.SysFont("Arial", 20)
    texte = myfont.render(f"Degat : {player.attack}", 1, white)
    screen.blit(texte, (250, 0))

    pygame.display.flip()
    screen.fill(black)     
    tour += 1   
    spon += 1
pygame.quit()
quit()