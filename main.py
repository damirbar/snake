import random

import pygame


# Constants
SNAKE_BLOCK_SIZE = 10
SCREEN_HEIGHT    = 600
SCREEN_WIDTH     = 800

# Colors
class Colors:
    red   = (255,0,0)
    green = (0,255,0)
    blue  = (0,0,255)
    white = (255,255,255)
    black = (0,0,0)


class Location:

    def __init__(self, x, y):
        self.__x, self.__y = x, y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    def __add__(self, other):
        return Location(self.__x + other.x, self.__y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Snake:

    def __init__(self, loc):
        self.__loc = loc
        self.__len = 0

    @property
    def loc(self):
        return self.__loc

    @loc.setter
    def loc(self, loc):
        self.__loc = loc

    def add_link(self):
        self.__len += 1

    @property
    def len(self):
        return self.__len


class SnakeGame:

    def __init__(self, snake_speed=30):
        # Initialize the game window
        pygame.init()
        self.disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.update()
        pygame.display.set_caption("Snake Game")
        self.snake_location = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.clock          = pygame.time.Clock()
        self.snake_speed    = snake_speed
        self.food_location  = self.generate_random_location()
        self.keep_playing   = True
        self.snake_is_dead  = False

    @staticmethod
    def generate_random_location():
        return Location(
            round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / 10.0) * 10.0,
            round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / 10.0) * 10.0
        )

    @staticmethod
    def is_out_of_bounds(loc):
        if loc.x < 0 or loc.y < 0 or loc.x > SCREEN_WIDTH or loc.y > SCREEN_HEIGHT:
            return True

    def handle_snake_is_dead(self):
        exit(0)
        pass

    def game_loop(self):
        location_modify = Location(0, 0)

        while self.keep_playing and not self.snake_is_dead:
            for evt in pygame.event.get():
                print(evt)

                # If the user attempts to close the game window
                if evt.type == pygame.QUIT:
                    self.keep_playing = False

                # If the user pressed a key
                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_LEFT:
                        location_modify = Location(-SNAKE_BLOCK_SIZE, 0)
                    if evt.key == pygame.K_RIGHT:
                        location_modify = Location(SNAKE_BLOCK_SIZE, 0)
                    if evt.key == pygame.K_UP:
                        location_modify = Location(0, -SNAKE_BLOCK_SIZE)
                    if evt.key == pygame.K_DOWN:
                        location_modify = Location(0, SNAKE_BLOCK_SIZE)

            if self.snake_location == self.food_location:
                print("Yum")
                self.food_location = self.generate_random_location()

            # Update the snake's location
            self.snake_location = self.snake_location + location_modify

            if self.is_out_of_bounds(self.snake_location):
                self.handle_snake_is_dead()
            else:
                self.disp.fill(Colors.black)
                pygame.draw.rect(self.disp, Colors.red,
                                 [self.food_location.x, self.food_location.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
                pygame.draw.rect(self.disp, Colors.green,
                                 [self.snake_location.x, self.snake_location.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

                pygame.display.update()

                # Refresh rate according to the selected snake speed
                self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()


def main():
    game = SnakeGame()
    game.game_loop()

if __name__ == '__main__':
    main()