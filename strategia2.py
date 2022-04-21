import pygame
import random
pygame.init()

win = pygame.display.set_mode((1024, 768))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = [255, 0, 0]
        self.rect = pygame.Rect(x, y, 50, 50)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect = self.rect.move(-5, 0)
        if keys[pygame.K_d]:
            self.rect = self.rect.move(5, 0)
        if keys[pygame.K_w]:
            self.rect = self.rect.move(0, -5)
        if keys[pygame.K_s]:
            self.rect = self.rect.move(0, 5)

    def update(self):
        self.move()
        pygame.draw.rect(win, self.color, self.rect)


class Entites(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = [0, 255, 0]
        group.add(self)

    def update(self):
        pygame.draw.rect(win, self.color, self.rect)


class Heal(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = [0, 255, 255]
        group.add(self)

    def update(self):
        pygame.draw.rect(win, self.color, self.rect)


player = Player(500, 500)
bots = pygame.sprite.Group()
heals = pygame.sprite.Group()

Entites(100, 150, bots)
Entites(200, 150, bots)
Entites(300, 250, bots)

Heal(random.randint(50, 950), random.randint(50, 550), heals)
Heal(random.randint(50, 950), random.randint(50, 550), heals)
Heal(random.randint(50, 950), random.randint(50, 550), heals)


run = True
while run:
    pygame.time.delay(20)
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            run = False
    win.fill((0,0,0))
    player.update()
    bots.update()
    heals.update()
    if pygame.sprite.spritecollideany(player, bots):
        pygame.sprite.spritecollideany(player, bots).color[1] -= 3
        pygame.sprite.spritecollideany(player, bots).color[0] += 3
        player.color[0] -= 1
        player.color[1] += 1
        if player.color[0] == 0: pygame.quit()
        if pygame.sprite.spritecollideany(player, bots).color[1] == 0:
            pygame.sprite.spritecollideany(player, bots).kill()
            Entites(random.randint(50, 950), random.randint(50, 550), bots)
    if pygame.sprite.spritecollideany(player, heals):
        pygame.sprite.spritecollideany(player, heals).kill()
        if player.color[0] >= 175: player.color[0] = 255
        else: player.color[0] += 75
        if player.color[1] <= 75: player.color[1] = 0
        else: player.color[1] -= 75
        Heal(random.randint(50, 950), random.randint(50, 550), heals)
    pygame.display.update()
pygame.quit()