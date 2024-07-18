import pygame 
from os.path import join as jo
from random import randint

pygame.init()
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720
running=True
clock=pygame.time.Clock()

#icon and name
icon=pygame.image.load('images/player.png')
icon=pygame.transform.scale(icon,(32,32))
pygame.display.set_icon(icon)
display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('shooter')


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image=pygame.transform.scale_by((pygame.image.load(jo('images','pixelp.png')).convert_alpha()),(0.4,0.4))
        self.rect=self.image.get_frect(center=(WINDOW_HEIGHT/2,WINDOW_WIDTH/2))
        self.direction=pygame.Vector2(0,0)
        self.speed=600
        self.mask=pygame.mask.from_surface(self.image)

        #laser cooldown
        self.can_shoot=True
        self.last_shoot_time=0
        self.shoot_duration=200

    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.last_shoot_time >= self.shoot_duration:
                self.can_shoot=True
                
    def update(self,dt):
        keys=pygame.key.get_pressed()
        self.direction.x= int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y=int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction=self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        if self.rect.left > WINDOW_WIDTH:
            self.rect.right=0
        if self.rect.right <0:
            self.rect.left=WINDOW_WIDTH

        if self.rect.centery > WINDOW_HEIGHT:
            self.rect.centery=WINDOW_HEIGHT
        if self.rect.centery<0:
            self.rect.centery=0



        recentkeys=pygame.key.get_just_pressed()
        if recentkeys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites,laser_sprites),laser_surf,(self.rect.midtop[0],self.rect.midtop[1]+7))
            self.can_shoot=False
            self.last_shoot_time=pygame.time.get_ticks()
            laser_sound.play( )

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups,surf,pos) -> None:
        super().__init__(groups)
        self.image=surf
        self.originalsurf=surf
        self.rect=self.image.get_frect(center=pos)
        self.mask=pygame.mask.from_surface(self.image)
        self.rotation=0
        self.rotatespeed=randint(50,80)
        self.movespeed=randint(80,150)

    
    def update(self,dt):
        self.rect.centery+= self.movespeed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        #rotation
        self.rotation+=self.rotatespeed*dt
        self.image=pygame.transform.rotozoom(self.originalsurf,self.rotation,1)
        self.rect=self.image.get_frect(center=self.rect.center)

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups,surf,pos):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)
        self.mask=pygame.mask.from_surface(self.image)

    
    def update(self,dt):
        self.rect.centery-= 400 * dt
        # self.check_collision()

        if self.rect.bottom < 0:
            self.kill()
    
    def check_collision(self):
        collision = pygame.sprite.spritecollide(self,meteor_sprites,True)
        if collision:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, groups,frames,pos):
        super().__init__(groups)
        self.frames=frames
        self.image=frames[0]
        self.rect=self.image.get_frect(center=pos)
        self.frame_index=0

    def update(self,dt):

        self.frame_index+=20*dt
        if self.frame_index < 21:
            self.image= self.frames[int(self.frame_index) % 21]
        else:
            self.kill()


def display_score(score):
    text_surf=font.render(str(score),True,(240,240,240))
    text_rect=text_surf.get_frect(midtop=(WINDOW_WIDTH/2,10))
    display_surface.blit(text_surf,text_rect)
    # pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(40,30),5,5)

def display_lives(lives):
    # print('in display',lives)
    lives_surf=font.render(str(lives),True,(240,240,240))
    lives_rect=lives_surf.get_frect(center=(50,20))
    display_surface.blit(lives_surf,lives_rect)

def check_game_over():
    if lives<=0:
        return True
    else:
        return False

#importing
star_surface=pygame.image.load(jo('images','star.png')).convert_alpha()
# meteor_surf=pygame.transform.scale_by((pygame.image.load(jo('images','meteorp.png')).convert_alpha()),(0.6,0.6))
laser_surf=pygame.transform.scale_by((pygame.image.load(jo('images','laserp.png')).convert_alpha()),(0.15,0.15))

meteor_surf=pygame.image.load(jo('images','meteor.png')).convert_alpha()
# laser_surf=pygame.image.load(jo('images','laserp.png')).convert_alpha()

font=pygame.font.Font('font/font2.ttf',40)
col_frames=[pygame.image.load(jo('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound=pygame.mixer.Sound(jo('audio','laser2.mp3'))
laser_sound.set_volume(0.25)

explosion_sound=pygame.mixer.Sound(jo('audio','explosion2.mp3'))
explosion_sound.set_volume(0.3)

damage_sound=pygame.mixer.Sound(jo('audio','damage.ogg'))
damage_sound.set_volume(0.5)

game_music=pygame.mixer.Sound(jo('audio','game_music.wav'))
game_music.set_volume(0.1)




#sprites
all_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()
for i in range(20):
    Star(all_sprites,star_surface)
player=Player(all_sprites)


#costum events
meteor_event=pygame.event.custom_type()
pygame.time.set_timer(meteor_event,2000)


#variables
meteor_bounce_score=0
lives=3


# game_music.play()
while running:
    dt=clock.tick()/1000
    score=pygame.time.get_ticks()//100
    score+=meteor_bounce_score

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==meteor_event:
            print('meteor')
            x,y= randint(0,WINDOW_WIDTH),randint(-300,-100)
            Meteor((all_sprites,meteor_sprites),meteor_surf,(x,y))

    #update
    all_sprites.update(dt)

    #collision setting
    collision = pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask)
    if collision:
        damage_sound.play()
        lives-=1
    
    for laser in laser_sprites:
        laserxmeteor=pygame.sprite.spritecollide(laser,meteor_sprites,True,pygame.sprite.collide_mask)
        if laserxmeteor:
            laser.kill()
            Explosion(all_sprites,col_frames,laser.rect.midtop)
            explosion_sound.play()
            meteor_bounce_score+=20

    #draw 
    display_surface.fill((22, 8, 51))
    all_sprites.draw(display_surface)
    display_score(score)
    display_lives(lives)

    if check_game_over():
        print('game over')
        break


    pygame.display.update()

pygame.quit()




#todo:
# 1.pause button 
# 2.menu
# 3.record save

#next game ✔
