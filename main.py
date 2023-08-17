import pygame
from random import randint

pygame.init()

win_width, win_height = 700, 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Космічний шутер")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

FPS = 60
enemy_wait = 50
miss = 0
score = 0
game_over = False
restart_game = False
clock = pygame.time.Clock()
level_width = 700
max_score = 0
game_over_color = (250, 0, 0)
pygame.mixer_music.load("space.ogg")
pygame.mixer_music.set_volume(0.05)
pygame.mixer_music.play(-1)
bullet_sound = pygame.mixer.Sound("laser_shoot.mp3")
bullet_sound.set_volume(0.05)
sad_sound = pygame.mixer.Sound("Game_over.mp3")
sad_sound.set_volume(0.05)
menu_sound = pygame.mixer.Sound("menu_sound.mp3")
menu_sound.set_volume(0.05)
knopca_sound = pygame.mixer.Sound("knopca_sound.mp3")
knopca_sound.set_volume(0.5)

background = pygame.image.load("galaxy.png")
background = pygame.transform.scale(background, (win_width, win_height))
bullet_img = pygame.image.load("bullet.png")
heart_img = pygame.image.load("heart.png")

game = True
finish = False

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        self.speed = speed
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, w, h, image, speed, hp):
        super().__init__(x, y, w, h, image, speed)
        self.hp = hp
        hearts = []
        h = 650
        for i in range(self.hp):
            h = GameSprite(x, 0, 20, 20, heart_img, 0)
            hearts.append(h)
            x -= 22
        self.hearts = hearts

    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
            if self.rect.x <= level_width - self.rect.width:
                self.rect.x += self.speed
        if k[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx - 10, self.rect.y, 20, 30, bullet_img, 5)
        bullet_sound.play()

enemies_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        enemies_group.add(self)
        self.direction = 1
        self.move_counter = 0

    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            enemies_group.remove(self)
            miss += 1
        current_x = self.rect.x
        self.rect.x += self.speed * self.direction
        if self.rect.right >= win_width or self.rect.left <= 0:
            self.rect.x = current_x
            self.direction *= -1
        self.move_counter += 1
        if self.move_counter == 30:
            self.direction *= -1
            self.move_counter = 0

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed,):
        super().__init__(x, y, w, h, image, speed)
        bullet_group.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            bullet_group.remove(self)

font1 = pygame.font.SysFont("Arial", 25)
font2 = pygame.font.SysFont("Arial", 35)
player_img = pygame.image.load("rocket.png")
player1 = Player(320, 400, 50, 100, player_img, 5, 3)
enemy_img = pygame.image.load("ufo.png")

try:
    with open("hit.txt", "r") as file:
        max_score = int(file.read())
except FileNotFoundError:
    file = open("hit.txt", "x")
    file.close()
except ValueError:
    pass

def show_menu():
    menu = True
    play_button_rect = pygame.Rect(win_width // 2 - 100, win_height // 2 - 50, 200, 50)
    quit_button_rect = pygame.Rect(win_width // 2 - 100, win_height // 2 + 50, 200, 50)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button_rect.collidepoint(event.pos):
                        menu = False
                        knopca_sound.play()
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        quit()

        window.blit(pygame.image.load("menu_background.png"), (0, 0))
        pygame.draw.rect(window, (255, 255, 255), play_button_rect)
        pygame.draw.rect(window, (255, 255, 255), quit_button_rect)

        font = pygame.font.SysFont("Arial", 30)
        play_text = font.render("Грати", True, (0, 0, 0))
        quit_text = font.render("Вийти", True, (0, 0, 0))

        window.blit(play_text, (win_width // 2 - 35, win_height // 2 - 40))
        window.blit(quit_text, (win_width // 2 - 30, win_height // 2 + 60))

        pygame.display.update()
        clock.tick(FPS)

show_menu()

while game:
    if enemy_wait == 0:
        enemy = Enemy(randint(0, win_width - 50), 20, 50, 40, enemy_img, randint(2, 4))
        enemy_wait = randint(70, 150)
    else:
        enemy_wait -= 1

    window.blit(background, (0, 0))
    miss_lb = font1.render("Пропущено: " + str(miss), True, (250, 0, 0))
    window.blit(miss_lb, (10, 30))
    score_txt = font1.render("Вбито: " + str(score), True, (0, 250, 0))
    window.blit(score_txt, (10, 60))

    if not game_over:
        enemies_group.draw(window)
        enemies_group.update()
        bullet_group.draw(window)
        bullet_group.update()
        for h in player1.hearts:
            h.paint()
        player1.move()
        player1.paint()

        if pygame.sprite.groupcollide(enemies_group, bullet_group, True, True):
            score += 1

        if pygame.sprite.spritecollide(player1, enemies_group, True):
            player1.hp -= 1
            if len(player1.hearts) > 0:
                heart_to_remove = player1.hearts.pop()

        if player1.hp <= 0 or miss >= 3:
            miss += 1
            game_over = True
            if score > max_score:
                max_score = score
                with open("hit.txt", "w") as file:
                    file.write(str(max_score))
                new_record = True
            else:
                new_record = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player1.shoot()

    if game_over:
        window.fill(game_over_color)
        game_over_label = font2.render("Game Over", True, (0, 0, 0))
        if new_record:
            record_label = font1.render("Новий рекорд: " + str(max_score), True, (0, 0, 0))
        else:
            record_label = font1.render("Рекорд: " + str(max_score), True, (0, 0, 0))
        restart_label = font1.render("Натисни Enter щоб почати гру знов", True, (0, 0, 0))
        window.blit(game_over_label, (win_width // 2 - 100, win_height // 2 - 50))
        window.blit(record_label, (win_width // 2 - 75, win_height // 2 + 10))
        window.blit(restart_label, (win_width // 2 - 170, win_height // 2 + 50))
        pygame.mixer.music.stop()
        sad_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart_game = True
                elif event.key == pygame.K_ESCAPE:
                    game = False

    if restart_game:
        sad_sound.stop()
        pygame.mixer.music.play(-1)
        enemies_group.empty()
        bullet_group.empty()
        player1.hp = 3
        player1.hearts = []
        x = 320
        for i in range(player1.hp):
            h = GameSprite(x, 0, 20, 20, heart_img, 0)
            player1.hearts.append(h)
            x -= 22
        player1.rect.x = 320
        player1.rect.y = 400
        miss = 0
        score = 0
        game_over = False
        restart_game = False

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()