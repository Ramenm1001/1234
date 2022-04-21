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
        pygame.draw.rect(win, (255, 0, 0), self.rect)


class A(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = [0, 255, 0]
        group.add(self)

    def update(self):
        pygame.draw.rect(win, self.color, self.rect)


player = Player(500, 500)
bots = pygame.sprite.Group()

A(100, 150, bots)
A(200, 150, bots)
A(300, 250, bots)

run = True
while run:
    pygame.time.delay(20)
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            run = False
    win.fill((0,0,0))
    player.update()
    bots.update()
    if pygame.sprite.spritecollideany(player, bots):
        pygame.sprite.spritecollideany(player, bots).color[1] -= 1
        pygame.sprite.spritecollideany(player, bots).color[0] += 1
        player.color[0] -= 1
        player.color[1] += 1
        if pygame.sprite.spritecollideany(player, bots).color[1] == 0:
            pygame.sprite.spritecollideany(player, bots).kill()
            A(300, 250, bots)
    pygame.display.update()
pygame.quit()