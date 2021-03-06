import sys
import pygame
import random
import math

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 1000

BLACK = (0, 0, 0)

MAX_VELOCITY = 10
PREDATOR_MAX_VELOCITY = 11

NUM_PREDATOR = 1
NUM_BOIDS = 50

BORDER = 25

class Predator(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Predator, self).__init__()

        self.image = pygame.image.load("img/predator.png").convert()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, prey):
        '''Return the distance from another prey'''

        distX = self.rect.x - prey.rect.x
        distY = self.rect.y - prey.rect.y

        return math.sqrt(distX * distX + distY * distY)

    

    



class Prey(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Prey, self).__init__()

        self.image = pygame.image.load("img/prey.png").convert()
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, prey):
        '''Return the distance from another prey'''

        distX = self.rect.x - prey.rect.x
        distY = self.rect.y - prey.rect.y

        return math.sqrt(distX * distX + distY * distY)

    def move_closer(self, prey_list):
        '''Move closer to a set of prey_list'''

        if len(prey_list) < 1:
            return

        # calculate the average distances from the other prey_list
        avgX = 0
        avgY = 0
        for prey in prey_list:
            if prey.rect.x == self.rect.x and prey.rect.y == self.rect.y:
                continue

            avgX += (self.rect.x - prey.rect.x)
            avgY += (self.rect.y - prey.rect.y)

        avgX /= len(prey_list)
        avgY /= len(prey_list)

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)


    def move_with(self, prey_list):
        '''Move with a set of prey_list'''

        if len(prey_list) < 1:
            return

        # calculate the average velocities of the other prey_list
        avgX = 0
        avgY = 0

        for prey in prey_list:
            avgX += prey.velocityX
            avgY += prey.velocityY

        avgX /= len(prey_list)
        avgY /= len(prey_list)

        # set our velocity towards the others
        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)

    def move_away(self, prey_list, minDistance):
        '''Move away from a set of prey_list. This avoids crowding'''

        if len(prey_list) < 1:
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for prey in prey_list:
            distance = self.distance(prey)

            if  distance < minDistance:
                numClose += 1
                xdiff = (self.rect.x - prey.rect.x)
                ydiff = (self.rect.y - prey.rect.y)

                if xdiff >= 0:
                    xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0:
                    xdiff = -math.sqrt(minDistance) - xdiff

                if ydiff >= 0:
                    ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0:
                    ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff

        if numClose == 0:
            return

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    def update(self):
        '''Perform actual movement based on our velocity'''

        if abs(self.velocityX) > MAX_VELOCITY or abs(self.velocityY) > MAX_VELOCITY:
            scaleFactor = MAX_VELOCITY / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

prey_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

predator = Predator(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
all_sprites_list.add(predator)

for i in range(NUM_BOIDS):
    prey = Prey(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    prey_list.add(prey)
    all_sprites_list.add(prey)


clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    for prey in prey_list:
        closeBoids = []
        for otherBoid in prey_list:
            if otherBoid == prey:
                continue
            distance = prey.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)

        prey.move_closer(closeBoids)
        prey.move_with(closeBoids)
        prey.move_away(closeBoids, 20)

        if prey.rect.x < BORDER and prey.velocityX < 0:
            prey.velocityX = -prey.velocityX * random.random()
        if prey.rect.x > SCREEN_WIDTH - BORDER and prey.velocityX > 0:
            prey.velocityX = -prey.velocityX * random.random()
        if prey.rect.y < BORDER and prey.velocityY < 0:
            prey.velocityY = -prey.velocityY * random.random()
        if prey.rect.y > SCREEN_HEIGHT - BORDER and prey.velocityY > 0:
            prey.velocityY = -prey.velocityY * random.random()

        prey.update()


    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
sys.exit()