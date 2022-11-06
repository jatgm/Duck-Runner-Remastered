import pygame
import sys
from random import randint
import newclient

pygame.init()

screen = pygame.display.set_mode((1024, 786))
pygame.display.set_caption('Duck Runner Remastered')

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    multiplayer = False
    alive = False
    def __init__(self, player_two=False):
        super().__init__()
        
        self.run_sprites = [pygame.image.load("sprites/sprite_1.png").convert_alpha(),
        pygame.image.load("sprites/sprite_2.png").convert_alpha()]
        self.jump_sprite = pygame.image.load("sprites/sprite_0.png").convert_alpha()
        self.dead_sprite = pygame.image.load("sprites/deadscene.png").convert_alpha()
        self.player_two = player_two
        self.image = self.jump_sprite

        if player_two:
            self.rect = self.image.get_rect(midbottom=(300,650))
        else:
            self.rect = self.image.get_rect(midbottom=(100,650))

        self.animation_index = 0
        self.gravity = 0

        self.multiplayer_count = 0
        self.player_two_count = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')

    def player_input(self):
        if not self.player_two:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.rect.bottom >= 650:
                    self.gravity = -23
                    if self.multiplayer and self.client.connected:
                        self.client.sendMsg('jump')
                    self.jump_sound.play()
        else:
            for sprite in player.sprites():
                if sprite.multiplayer:
                    if sprite.client.connected:
                        if sprite.client.player_two_jump:
                            self.gravity = -23
                            sprite.client.player_two_jump = False

    def initiate_multiplayer(self):
        self.client = newclient.Client()
        self.multiplayer = True
        
    def collision(self):
        if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
            self.image = self.dead_sprite
            self.alive = False
            for i in text_group.sprites():
                i.score = 0
            for i in range(3):
                button_group.add(Buttons(i))

    def animation_state(self):
        if self.rect.bottom < 650:
            self.image = self.image
        else:
            if sprite.alive or sprite.multiplayer and sprite.client.start:
                self.animation_index += 0.1
                if self.animation_index >= len(self.run_sprites):
                    self.animation_index = 0
                self.image = self.run_sprites[int(self.animation_index)]
            else:
                self.image = self.jump_sprite

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 650:
            self.rect.bottom = 650

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.collision()                

        for sprite in player.sprites():
            if sprite.multiplayer:
                if self.multiplayer_count == 0:
                    if not self.player_two:
                        if self.client.start:
                            playertwo.add(Player(True))
                            self.multiplayer_count += 1                    
                    if not sprite.client.first:
                        if sprite.player_two_count == 0:
                            if self.player_two:
                                self.rect.midbottom = (100,650)
                            else:
                                self.rect.midbottom = (300,650)
                            self.multiplayer_count+=1

                if not self.player_two:        
                    if not self.client.start:
                        playertwo.empty()
                        if self.player_two_count == 0:
                            self.rect.midbottom = (100,650)
                            self.player_two_count += 1
                        self.multiplayer_count = 0
                        
class Enviroment(pygame.sprite.Sprite):
    def __init__(self, type, index):
        super().__init__()
        self.index = index
        self.type = type
        if type == "ground":
            self.image = pygame.image.load("sprites/ground.png").convert_alpha()
            if index:
                self.rect = self.image.get_rect(topleft=(1200,634))
            else:
                self.rect = self.image.get_rect(topleft=(0,634))
        else:
            self.image = pygame.image.load("sprites/clouds.png").convert_alpha()
            if index:
                self.rect = self.image.get_rect(topleft=(1200,250))
            else:
                self.rect = self.image.get_rect(topleft=(0,250))
    
    def move(self):
        if self.rect.right < 0:
            self.rect.left = 1200

        for sprite in player.sprites():
            if sprite.alive or sprite.multiplayer and sprite.client.start:
                if self.type == "ground":
                    self.rect.x -= 10
            if self.type == "sky":
                self.rect.x -= 1

    def update(self):
        self.move()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,multiplayer=False):
        super().__init__()
        enemy_sprites = [pygame.image.load("sprites/enemy_1.png").convert_alpha(),
        pygame.image.load("sprites/enemy_2.png").convert_alpha(),
        pygame.image.load("sprites/enemy_3.png").convert_alpha()]
        if not multiplayer:
            self.image = enemy_sprites[randint(0, 2)]
            print('fart')
        else:
            self.image = enemy_sprites[int(multiplayer)]
            print(f"Made a {multiplayer}")
        self.rect = self.image.get_rect(bottomleft=(1024,650))

    def move(self):
        if self.rect.right < 0:
            self.kill()        
        self.rect.x -= 10
        
    def update(self):
        self.move()

class Buttons(pygame.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        button_sprites = [pygame.image.load("icons/icons1.png").convert_alpha(),
        pygame.image.load("icons/icons2.png").convert_alpha(),
        pygame.image.load("icons/icons3.png").convert_alpha()]
        self.index = index
        self.button_hover = pygame.image.load("icons/icons0.png").convert_alpha()
        self.image = button_sprites[index]
        self.rect = self.image.get_rect(topleft = (328 + (self.index*128), 355))
        self.count = 0

    def interact(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.button_hover, (self.rect.x+8,self.rect.y+8))
            if pygame.mouse.get_pressed()[0]:
                if self.count == 0:
                    if self.index == 1:
                        for sprite in player.sprites():
                            sprite.alive = True
                        enemy_group.empty()
                        button_group.empty()
                        self.count+=1
                    if self.index == 0:
                        for sprite in player.sprites():
                            sprite.initiate_multiplayer()
                        enemy_group.empty()
                        button_group.empty()
                        self.count+=1

    def update(self):
        self.interact()

class Title(pygame.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        self.flashing_sprites = [pygame.image.load("sprites/startanimation0.png").convert_alpha(),
        pygame.image.load("sprites/startanimation1.png").convert_alpha()]
        self.title_sprite = pygame.image.load("sprites/titlescreen.png").convert_alpha()
        self.index = index
        self.animation_index = 0
        if index:
            self.image = self.flashing_sprites[0]
            self.rect = self.image.get_rect(topleft = ((222, 93)))
        else:
            self.image = self.title_sprite
            self.rect = self.image.get_rect(topleft = ((512,93)))

    def animate(self):
        if self.index:
            self.animation_index += 0.03
            if self.animation_index >= len(self.flashing_sprites):
                self.animation_index = 0
            self.image = self.flashing_sprites[int(self.animation_index)]

    def update(self):
        self.animate()

class Text(pygame.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        self.font = pygame.font.Font("fonts/Unibody8Pro-Regular.otf", 32)
        self.counter = 0
        self.score = 0
        self.high_score = 0
        self.index = index
        if index:
            self.color = (200,200,200)
            self.image = self.font.render(f"00000".zfill(5), True, self.color)
            self.rect = self.image.get_rect(topleft = (512 + 350, 393 - 380))
        else:
            self.color = (150,150,150)
            self.image = self.font.render(f"00000".zfill(5), True, self.color)
            self.rect = self.image.get_rect(topleft = (512 + 200, 393 - 380))
    
    def count(self):
        self.counter += 1
        if self.counter >= 30:
            self.counter = 0
            if self.high_score == self.score:
                self.high_score += 1
            self.score += 1
        if not self.index:
            self.image = self.font.render(f"{self.high_score}".zfill(5), True, self.color)
        else:
            self.image = self.font.render(f"{self.score}".zfill(5), True, self.color)

    def update(self):
        self.count()

playertwo = pygame.sprite.GroupSingle()
player = pygame.sprite.GroupSingle()
player.add(Player())

enviroment_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
title_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

for i in range(2):
    enviroment_group.add(Enviroment('ground', i))
    enviroment_group.add(Enviroment('sky', i))

for i in range(3):
    button_group.add(Buttons(i))

for i in range(2):
    title_group.add(Title(i))

for i in range(2):
    text_group.add(Text(i))

while True:
    for sprite in player.sprites():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if sprite.alive:
                if event.type == enemy_timer:
                    enemy_group.add(Enemy())
                    print("Fortnitebalecnaiga")

        screen.fill((91,91,91))

        player.draw(screen)
        playertwo.draw(screen)

        enviroment_group.draw(screen)

        enemy_group.draw(screen)

        if sprite.alive:
            title_group.update()
            player.update()
            playertwo.update()
            enemy_group.update()
            text_group.draw(screen)
            text_group.update()
        elif sprite.multiplayer:
            player.update()
            playertwo.update()
            enemy_group.update()
            if sprite.client.start:
                for sprite in player.sprites():
                    if sprite.client.spawn != "":
                        enemy_group.add(Enemy(str(sprite.client.spawn)))
                        sprite.client.spawn = ""
            else:
                enemy_group.empty()
        else:
            button_group.update() # Update before draw
            button_group.draw(screen)
            title_group.draw(screen)
            title_group.update()

    enviroment_group.update()

    pygame.display.update()
    clock.tick(60)