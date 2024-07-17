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
        self.speed=500

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

        recentkeys=pygame.key.get_just_pressed()
        if recentkeys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites,laser_sprites),laser_surf,(self.rect.midtop[0],self.rect.midtop[1]+7))
            self.can_shoot=False
            self.last_shoot_time=pygame.time.get_ticks()

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
        self.rect=self.image.get_frect(center=pos)
    
    def update(self,dt):
        self.rect.centery+= 100 * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()



class Laser(pygame.sprite.Sprite):
    def __init__(self, groups,surf,pos):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)
    
    def update(self,dt):
        self.rect.centery-= 400 * dt
        # self.check_collision()

        if self.rect.bottom < 0:
            self.kill()
    
    def check_collision(self):
        collision = pygame.sprite.spritecollide(self,meteor_sprites,True)
        if collision:
            self.kill()

def collisions():
    collision = pygame.sprite.spritecollide(player,meteor_sprites,True)
    if collision:
        return False
    
    for laser in laser_sprites:
        laserxmeteor=pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if laserxmeteor:
            laser.kill()




#importing
star_surface=pygame.image.load(jo('images','star.png')).convert_alpha()
meteor_surf=pygame.image.load(jo('images','meteor.png')).convert_alpha()
laser_surf=pygame.image.load(jo('images','laser.png')).convert_alpha()
font=pygame.font.Font('',35)


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






while running:
    dt=clock.tick()/1000

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==meteor_event:
            print('meteor')
            x,y= randint(0,WINDOW_WIDTH),randint(-300,-100)
            Meteor((all_sprites,meteor_sprites),meteor_surf,(x,y))

    #update
    all_sprites.update(dt)
    collisions()
   

    #draw 
    display_surface.fill((22, 8, 51))
    
    all_sprites.draw(display_surface)
    

    

    
    pygame.display.update()

pygame.quit()


