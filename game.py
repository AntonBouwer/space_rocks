# space_rocks/game.py
import pygame
from models import Rock, Spaceship
from utils import load_sprite, print_text


class SpaceRocks:
    NUM_ROCKS = 6

    def __init__(self):
        # Initialize pygame and set the title
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        self.bullets = []

        self.ship = Spaceship((400, 300), self.bullets)

        self.rocks = [
            Rock.create_random(self.screen, self.ship.position)
            for _ in range(self.NUM_ROCKS)
        ]

    def main_loop(self):
        while True:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.ship.alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ship.shoot()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            pygame.quit()
            exit()

        if self.ship.alive:
            if is_key_pressed[pygame.K_RIGHT]:
                self.ship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.ship.rotate(clockwise=False)
            elif is_key_pressed[pygame.K_UP]:
                self.ship.accelerate()

    @property
    def game_objects(self):
        return (
            [*self.rocks, *self.bullets, self.ship]
            if self.ship.alive
            else [*self.rocks, *self.bullets]
        )

    def _game_logic(self):
        for obj in self.game_objects:
            obj.move(self.screen)

        rect = self.screen.get_rect()
        for bullet in self.bullets[:]:
            if not rect.collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for rock in self.rocks[:]:
                if rock.collides_with(bullet):
                    self.rocks += rock.split()
                    self.rocks.remove(rock)
                    self.bullets.remove(bullet)
                    break

        if self.ship.alive:
            if not self.rocks:
                self.message = "WINNER!"
            else:
                for rock in self.rocks[:]:
                    if rock.collides_with(self.ship):
                        self.rocks.remove(rock)
                        self.ship.alive = False
                        self.message = "You lost!"
                        break

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for obj in self.game_objects:
            obj.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(30)
