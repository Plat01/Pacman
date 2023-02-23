import pygame
import random

# initialize Pygame
pygame.init()

# set up the display
width, height = 560, 620
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# define background colors
black = (0, 0, 0)

# Load the background image
background = pygame.image.load("assets/back.jpg")

# Resize the background image to match the game window size
background = pygame.transform.scale(background, (width, height))


class Ghost(pygame.sprite.Sprite):
    def __init__(self, size=40, speed=2):
        super().__init__()
        self._sprite = pygame.transform.scale(pygame.image.load(f'assets/blue_ghost.png'), (size, size))
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - size)
        self.rect.y = random.randrange(height - size)
        self.speed = speed
        self._time = 0
        self._dir_x = 0
        self._dir_y = 0

    def update(self):
        if not self._time:
            self._time = fps * 5
            self._dir_x = random.randrange(-1, 2)
            self._dir_y = random.randrange(-1, 2)
        if self.rect.left <= 0 or self.rect.right >= width:
            self._dir_x = - self._dir_x
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self._dir_y = - self._dir_y
        self.rect.x += self._dir_x * self.speed
        self.rect.y += self._dir_y * self.speed
        self._time -= 1

        self.image.blit(self._sprite, (0, 0))


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x=width / 2, y=height / 2, speed=5, size=60, mouth=0, facing="r"):
        super().__init__()
        self._imgs = []
        for i in range(4):
            self._imgs.append(pygame.transform.scale(pygame.image.load(f'assets/{i + 1}.png'), (size, size)))
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self._mouth_counter = mouth
        self._facing = facing

    def update(self):
        # Move Pacman
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._facing = "l"
            self.rect.x -= self.speed
            if self.rect.left <= 0:
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self._facing = "r"
            self.rect.x += self.speed
            if self.rect.right >= width:
                self.rect.right = width
        if keys[pygame.K_UP]:
            self._facing = "u"
            self.rect.y -= self.speed
            if self.rect.top <= 0:
                self.rect.top = 0
        if keys[pygame.K_DOWN]:
            self._facing = "d"
            self.rect.y += self.speed
            if self.rect.bottom >= height:
                self.rect.bottom = height

        # Open and close Pacman's mouth
        self._mouth_counter = (self._mouth_counter + 0.25) % len(self._imgs)

        self.image.fill(pygame.SRCALPHA)  # fill with transparent color
        if self._facing == 'r':
            self.image.blit(self._imgs[int(self._mouth_counter)], (0, 0))
        elif self._facing == 'l':
            self.image.blit(pygame.transform.flip(self._imgs[int(self._mouth_counter)], True, False), (0, 0))
        elif self._facing == 'u':
            self.image.blit(pygame.transform.rotate(self._imgs[int(self._mouth_counter)], 90), (0, 0))
        elif self._facing == 'd':
            self.image.blit(pygame.transform.rotate(self._imgs[int(self._mouth_counter)], -90), (0, 0))

    # method to check collision
    def collision(self, other: Ghost) -> bool:
        return self.rect.colliderect(other.rect)


if __name__ == '__main__':
    # create a Pacman object
    pacman = Pacman()

    # create a sprite group
    pcmn_sprite = pygame.sprite.Group()
    ghosts_sprites = pygame.sprite.Group()

    # add Pacman to the sprite group
    pcmn_sprite.add(pacman)

    # set up the game loop
    clock = pygame.time.Clock()
    fps = 40
    score = 0
    running = True
    while running:
        #  set cadre fps
        clock.tick(fps)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not ghosts_sprites:
            for _ in range(4):
                ghosts_sprites.add(Ghost())

        for ghost in ghosts_sprites:
            if pacman.collision(ghost):
                ghosts_sprites.remove(ghost)
                score += 1

        # update sprites
        pcmn_sprite.update()
        ghosts_sprites.update()

        # draw sprites on the display surface
        screen.blit(background, (0, 0))
        pcmn_sprite.draw(screen)
        ghosts_sprites.draw(screen)

        # update the display
        pygame.display.update()

    pygame.quit()
