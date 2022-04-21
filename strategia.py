import random
import pygame
pygame.init()

win = pygame.display.set_mode((1024, 768))

class Players():
    def __init__(self):
        self.x = random.randint(300,700)
        self.y = random.randint(200,500)
        self.go_x = self.x
        self.go_y = self.y
        self.color = (random.randint(64,192),random.randint(64,192),random.randint(64,192))
        self.size = 50
        self.selecket = False

    def selecked(self, x, y):
        if self.x < x < self.x + self.size and self.y < y < self.y + self.size and self.selecket == False:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 1, 1)
            self.selecket = True
            return True
        elif self.x < x < self.x + self.size and self.y < y < self.y + self.size and self.selecket == True:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 1, 1)
            self.selecket = False
            return False

    def update(self):
        if self.selecket == False:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 1, 1)

    def move(self):
        if self.x >= 7 and self.y >= 7:
            if self.x > self.go_x: self.x -= 7
            if self.x < self.go_x: self.x += 7
            if self.y > self.go_y: self.y -= 7
            if self.y < self.go_y: self.y += 7
        else: self.x = self.y = 7

any_selecked = False
players = []
run = True
while run:
    pygame.time.delay(100)
    win.fill((255,255,255))
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed() # (0, 0, 0)
    x, y = pygame.mouse.get_pos()
    if mouse[0]:
        for i in players:
            if any_selecked == False:
                if i.selecked(x, y) == True: any_selecked = True
            elif any_selecked == True and i.selecket == True:
                if i.selecked(x, y) == False: any_selecked = False
            if i.selecket == True and any_selecked == True:
                i.go_x = x
                i.go_y = y
    for i in players:
        if i.selecket == True and any_selecked == True:
            i.move()
        i.update()
    if mouse[2]:
        players.append(Players())
    pygame.display.update()
pygame.quit()