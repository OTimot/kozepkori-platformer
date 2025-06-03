import pygame
import sys

# Inicializálás
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Középkori Fantasy Platformer")
clock = pygame.time.Clock()
FPS = 60

# Képbetöltő függvény

def load_and_scale(filename, size):
    img = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(img, size)

# Képek betöltése
player_img = load_and_scale("lovag.png", (64, 64))
player_attack_imgs = [
    load_and_scale("lovag_tamadas1.png", (64, 64)),
    load_and_scale("lovag_tamadas2.png", (64, 64)),
    load_and_scale("lovag_tamadas3.png", (64, 64))
]

enemy_img = load_and_scale("sarkany_uj.png", (64, 64))
ground_img = load_and_scale("platform.png", (128, 32))
background_img = load_and_scale("hatter.png", (WIDTH, HEIGHT))
treasure_img = load_and_scale("lada.png", (64, 64))

# Játékos osztály
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5

        self.rect.x += dx

        # Gravitáció
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Ütközés a platformmal
        self.on_ground = False
        for ground in ground_group:
            if self.rect.colliderect(ground.rect):
                if self.vel_y > 0:
                    self.rect.bottom = ground.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Támadás logika (F gomb)
        if keys[pygame.K_f]:
            self.attacking = True
        else:
            self.attacking = False
            self.attack_frame = 0
            self.attack_timer = 0

        if self.attacking:
            self.attack_timer += 1
            if self.attack_timer >= 5:
                self.attack_timer = 0
                self.attack_frame = (self.attack_frame + 1) % len(player_attack_imgs)
            self.image = player_attack_imgs[self.attack_frame]
        else:
            self.image = player_img

# Ellenség osztály (mozog)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * 2
        if abs(self.rect.x - self.start_x) >= 100:
            self.direction *= -1

# Platform osztály
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ground_img
        self.rect = self.image.get_rect(topleft=(x, y))

# Kincsesláda osztály
class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = treasure_img
        self.rect = self.image.get_rect(topleft=(x, y))

# Sprite csoportok
player = Player(100, 400)
player_group = pygame.sprite.GroupSingle(player)

enemy_group = pygame.sprite.Group()
enemy_group.add(Enemy(500, 468))

ground_group = pygame.sprite.Group()
for i in range(0, WIDTH, 128):
    ground_group.add(Ground(i, 532))

treasure_group = pygame.sprite.Group()
treasure_group.add(Treasure(700, 468))

# Fő játékhurok
running = True
while running:
    clock.tick(FPS)
    screen.blit(background_img, (0, 0))

    # Frissítések
    player_group.update()
    enemy_group.update()

    # Ütközések kezelése
    for enemy in enemy_group:
        if player.rect.colliderect(enemy.rect):
            if player.attacking:
                enemy.kill()
            else:
                print("Sebződtél!")

    for treasure in treasure_group:
        if player.rect.colliderect(treasure.rect):
            treasure.kill()
            player.score += 1
            print(f"Pontszám: {player.score}")

    # Kirajzolás
    ground_group.draw(screen)
    treasure_group.draw(screen)
    enemy_group.draw(screen)
    player_group.draw(screen)

    # Kilépés esemény
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()
