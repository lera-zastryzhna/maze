import pygame
#from pygame import display, event, transform, image, time, QUIT, mixer, KEYDOWN, K_ESCAPE, sprite, key, K_w, K_s, K_a, \
    #K_d, K_r
from pygame.surface import Surface
from pygame import *

pygame.init()
mixer.init()
info = display.Info()

game = True

HEIGHT = info.current_h
WIDTH = info.current_w

fps = 60
clock = time.Clock()

window = display.set_mode((WIDTH, HEIGHT))
back = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))
mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (HEIGHT // 10, HEIGHT // 10))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.hp = 3

    def update_pos(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < HEIGHT - HEIGHT // 10:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > -5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < WIDTH - HEIGHT // 10:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = "left"

    def update_pos(self):
        if self.rect.x <= WIDTH - WIDTH // 4:
            self.direction = "right"
        if self.rect.x >= WIDTH - WIDTH // 10:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, width, height):
        super().__init__()
        self.color = (102, 219, 106)
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y


    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



player = Player('hero.png', WIDTH // 15, HEIGHT - HEIGHT // 5, HEIGHT // 110)

monster = Enemy('cyborg.png', WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 3, HEIGHT // 110)

treasure = GameSprite('treasure.png', WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 5, 3)

wall_width = HEIGHT // 80


wall_top = Wall(WIDTH // 20, HEIGHT // 20, WIDTH // 1.1, wall_width)
wall_bot = Wall(WIDTH // 20, HEIGHT - HEIGHT // 20, WIDTH // 1.1, wall_width)

wall_1 = Wall(WIDTH // 6, HEIGHT // 5, wall_width, HEIGHT - HEIGHT // 4)
wall_2 = Wall(WIDTH // 4, HEIGHT // 20, wall_width, HEIGHT - HEIGHT // 4)
wall_3 = Wall(WIDTH // 3, HEIGHT // 5, wall_width, HEIGHT - HEIGHT // 4)
wall_4 = Wall(WIDTH // 2.4, HEIGHT // 20, wall_width, HEIGHT - HEIGHT // 4)
wall_5 = Wall(WIDTH // 2, HEIGHT // 5, wall_width, HEIGHT - HEIGHT // 4)
wall_6 = Wall(WIDTH - WIDTH // 6, HEIGHT // 5, wall_width, HEIGHT - HEIGHT // 4)
wall_7 = Wall(WIDTH - WIDTH // 4, HEIGHT // 20, wall_width, HEIGHT - HEIGHT // 4)
wall_8 = Wall(WIDTH - WIDTH // 3, HEIGHT // 5, wall_width, HEIGHT - HEIGHT // 4)
wall_9 = Wall(WIDTH - WIDTH // 2.4, HEIGHT // 20, wall_width, HEIGHT - HEIGHT // 4)

font = font.Font(None, HEIGHT // 5)

win = font.render("YOU WIN!", True, (196, 246, 114))
lose = font.render("YOU LOSE!", True, (250, 100, 114))

finish = False

def is_collide_wall():
    return (sprite.collide_rect(player, wall_top) or
            sprite.collide_rect(player, wall_bot) or
            sprite.collide_rect(player, wall_1) or
            sprite.collide_rect(player, wall_2) or
            sprite.collide_rect(player, wall_3) or
            sprite.collide_rect(player, wall_4) or
            sprite.collide_rect(player, wall_5) or
            sprite.collide_rect(player, wall_6) or
            sprite.collide_rect(player, wall_7) or
            sprite.collide_rect(player, wall_8) or
            sprite.collide_rect(player, wall_9))

def is_lose():
    return  sprite.collide_rect(player, monster) or player.hp <= 0

def draw_all():
    window.blit(back, (0, 0))

    wall_top.draw_wall()
    wall_bot.draw_wall()
    wall_1.draw_wall()
    wall_2.draw_wall()
    wall_3.draw_wall()
    wall_4.draw_wall()
    wall_5.draw_wall()
    wall_6.draw_wall()
    wall_7.draw_wall()
    wall_8.draw_wall()
    wall_9.draw_wall()

    player.reset()
    monster.reset()
    treasure.reset()

last_x = player.rect.x
last_y = player.rect.y

wait = 0

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            if e.key == K_r:
                finish = False
                player.hp = 3
                player.rect.x = WIDTH // 15
                player.rect.y = HEIGHT - HEIGHT // 5

    if not finish:
        if wait <= 0 and not is_collide_wall():
            last_x = player.rect.x
            last_y = player.rect.y
            wait = 5
        else:
            wait -= 1

        if is_collide_wall():
            kick.play()
            player.hp -= 1
            player.rect.x = last_x
            player.rect.y = last_y

        draw_all()


        player.update_pos()
        monster.update_pos()

        if sprite.collide_rect(player, treasure):
            money.play()
            window.blit(win, (WIDTH // 3, HEIGHT // 2.5))
            finish = True

        if is_lose():

            window.blit(lose, (WIDTH // 3, HEIGHT // 2.5))
            finish = True


    display.update()
    clock.tick(fps)
