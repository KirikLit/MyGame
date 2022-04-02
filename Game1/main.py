import pygame
import random
from data import *

# init pygame
pygame.init()
clock = pygame.time.Clock()

# init screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# game variables
moving_left = False
moving_right = False
attack = False
jump = False

# define groups
enemy_group = []
object_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()
interactive_group = pygame.sprite.Group()
sword_interactive_group = pygame.sprite.Group()

# temp - spawn units
player = Player(300, 100)
health_bar = HealthBar(10, 10, player.health, player.health)

chest = Object(700, 280, 16, 2.5, 'chest', True, True)
chest_group.add(chest)
vase = Object(200, 260, 16, 2.5, 'vase', True, True)
sword_interactive_group.add(vase)
door = Object(0, 240, 24, 2.5, 'door')
torch = Object(100, 240, 8, 2.5, 'torch', True)
object_group.add(torch, chest, vase, door)

enemy = Enemy('mushroom', 500, 100)
enemy_group.append(enemy)
enemy = Enemy('slime', 400, 100)
enemy_group.append(enemy)
enemy = Enemy('worm', 600, 100)
enemy_group.append(enemy)
enemy = Enemy('goblin', 100, 100)
enemy_group.append(enemy)

run = True
while run:
    draw_bg(screen)
    # clock
    clock.tick(FPS)
    pygame.display.set_caption(f'MyGame - {round(clock.get_fps(), 2)} fps')

    # update groups
    object_group.update()
    object_group.draw(screen)

    # update player
    player.draw(screen)
    player.update()
    health_bar.draw(screen, player.health)

    # update enemies
    for enemy in enemy_group:
        if not enemy.dead:
            if enemy.alive and player.alive:
                enemy.ai()
            elif not player.alive and enemy.alive:
                enemy.idling = True
                enemy.update_action(0)
            # check collide with player
            if enemy.enemy_type == 'goblin' and \
                    player.rect.colliderect(enemy.rect.x - 8, enemy.rect.y, enemy.rect.width + 16, enemy.rect.height) and \
                    direction(player, enemy) and player.alive and enemy.alive:
                player.hit(enemy_config[enemy.enemy_type]['damage'])
                enemy.update_action(4)
                enemy.idling = True
            elif player.rect.colliderect(enemy.rect) and enemy.alive and enemy.enemy_type != 'goblin':
                # hit player
                player.hit(enemy_config[enemy.enemy_type]['damage'])
            enemy.update()
            enemy.draw(screen)

    # update player actions
    if player.alive:
        # controls and animations
        if attack and not player.attack and not player.in_air:
            player.update_action(0)
            sword = Sword(player)
            player.attack = True
        if player.attack:
            sword.update(enemy_group)
            sword.draw(screen)
            for sprite in pygame.sprite.spritecollide(sword, sword_interactive_group, False):
                sprite.update_action(1)
            if sword.anim():
                sword.kill()
                player.update_action(0)
                player.attack = False
        elif player.in_air:
            if player.vel_y >= 0:
                player.update_action(3)
            else:
                player.update_action(2)
        elif jump:
            player.jump = True
        elif player.after_jump:
            player.update_action(8)
        elif moving_left or moving_right:
            player.update_action(1)   # 1 - run
        else:
            player.update_action(0)
        # move player
        player.move(moving_left, moving_right)

        # check collide to interactive objects
        if pygame.sprite.spritecollide(player, chest_group, False):
            chest.update_action(1)
            chest.rect.y = chest.y - 5
            player.key = True
        elif player.rect.colliderect(door) and player.key:
            print('You win!')
            run = False
        for sprite in pygame.sprite.spritecollide(player, interactive_group, False):
            sprite.update_action(1)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive and not player.in_air and not player.attack:
                jump = True
            if event.key == pygame.K_f:
                attack = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # Button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_f:
                attack = False
            if event.key == pygame.K_SPACE:
                jump = False

    pygame.display.update()


pygame.quit()
