import pygame
import random
import csv
from data import *

# init pygame
pygame.init()
clock = pygame.time.Clock()

# init display
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen = pygame.display.set_mode((800, 640), pygame.DOUBLEBUF)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# map variables
level = 1
ROWS = 16
COLS = 160

# game variables
moving_left = False
moving_right = False
attack = False
jump = False
coins = 0
screen_scroll = 0
bg_scroll = 0

# define groups
# enemy_group = []
# object_group = pygame.sprite.Group()
# interactive_group = pygame.sprite.Group()
# sword_interactive_group = pygame.sprite.Group()

# load level
world_data = load_level(level, ROWS, COLS)
world = World(world_data)
obstacle_group, decoration_group = world.read_data()
enemy_group, object_group, interactive_group, sword_interactive_group = world.read_json()


# temp - spawn units
player = Player(48, 176)
health_bar = HealthBar(10, 10, player.health, player.health)
chest = Object(832, 184, 16, 1, 'chest', True, True)
door = Object(2492, 72, 24, 1, 'door')

# vase = Object(200, 84, 16, 1, 'vase', True, True)
# sword_interactive_group.add(vase)
# coin = Object(300, 84, 8, 1, 'coin', True, True, True)
# health1 = Object(400, 84, 8, 1, 'apple')
# health2 = Object(450, 80, 8, 1, 'health')
# torch = Object(100, 240, 8, 1, 'torch', True)

interactive_group.add(chest)
object_group.add(chest, door)

# enemy = Enemy('mushroom', 150, 100)
# enemy_group.append(enemy)
# enemy = Enemy('slime', 170, 100)
# enemy_group.append(enemy)
# enemy = Enemy('worm', 200, 100)
# enemy_group.append(enemy)
# enemy = Enemy('goblin', 230, 100)
# enemy_group.append(enemy)

run = True


while run:
    draw_bg(display, bg_scroll)
    # clock
    clock.tick(FPS)
    pygame.display.set_caption(f'MyGame - {round(clock.get_fps(), 2)} fps')

    # update groups
    object_group.update(screen_scroll)
    object_group.draw(display)

    for sprite in obstacle_group:
        sprite.update(screen_scroll)
        if -16 < sprite.rect.x < DISPLAY_WIDTH:
            sprite.draw(display, bg_scroll)
    for sprite in decoration_group:
        sprite.update(screen_scroll)
        if -16 < sprite.rect.x < DISPLAY_WIDTH:
            sprite.draw(display, bg_scroll)

    # update player
    player.draw(display)
    player.update()
    health_bar.draw(display, player.health)

    # update enemies
    for enemy in enemy_group:
        if -16 < enemy.rect.x < DISPLAY_WIDTH:
            if not enemy.dead:
                if enemy.alive and player.alive:
                    enemy.ai(obstacle_group)
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
                enemy.update(screen_scroll)
                enemy.draw(display, bg_scroll)
        else:
            enemy.rect.x -= screen_scroll

    # update player actions
    if player.alive:
        # controls and animations
        if attack and not player.attack and not player.in_air:
            player.update_action(0)
            sword = Sword(player)
            player.attack = True
        if player.attack:
            sword.update(enemy_group)
            sword.draw(display)
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
        screen_scroll = player.move(moving_left, moving_right, obstacle_group, bg_scroll)
        bg_scroll += screen_scroll

        # check collide to interactive objects
        if player.rect.colliderect(door) and player.key:
            print('You win!')
            run = False
        for sprite in pygame.sprite.spritecollide(player, interactive_group, False):
            if sprite.interactive:
                sprite.update_action(1)
            if sprite.type == 'chest':
                sprite.rect.y = sprite.y - 2
                player.key = True
            elif sprite.type == 'coin':
                sprite.rect.y = sprite.y - 20
                coins += 1
            elif sprite.type == 'apple':
                player.health += 10
                sprite.kill()
            elif sprite.type == 'health':
                player.health += 35
                sprite.kill()

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

    # update screen
    screen.blit(pygame.transform.scale(display, (800, 640)), (0, 0))
    pygame.display.update()

pygame.quit()
