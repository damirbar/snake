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

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Snake:

    def __init__(self, loc):
        self.__links = [loc]
        self.ate_food = False

    @property
    def head_loc(self):
        return self.__links[0]

    @head_loc.setter
    def head_loc(self, loc):
        # num_links = len(self.__links)
        # for i in range(num_links - 1):
            # self.__links[num_links - i - 2] = self.__links[num_links - i - 1]
            # self.__links[i] = self.__links[i]
        if not self.ate_food:
            self.__links.pop()
        else:
            self.ate_food = False
        self.__links.insert(0, loc)

    def add_link(self, loc):
        # self.__links.append(loc)
        self.ate_food = True

    @property
    def links(self):
        return self.__links



class SnakeGame:

    def __init__(self, snake_speed=30):
        # Initialize the game window
        pygame.init()
        self.disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.update()
        pygame.display.set_caption("Snake Game")
        self.snake = Snake(Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.clock          = pygame.time.Clock()
        self.snake_speed    = snake_speed
        self.food_location  = self.generate_random_location()
        self.keep_playing   = True
        self.snake_is_dead  = False
        self.direction      = None

    @staticmethod
    def generate_random_location():
        return Location(
            round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
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
                    if evt.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                        self.direction = pygame.K_LEFT
                        location_modify = Location(-SNAKE_BLOCK_SIZE, 0)
                    if evt.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                        self.direction = pygame.K_RIGHT
                        location_modify = Location(SNAKE_BLOCK_SIZE, 0)
                    if evt.key == pygame.K_UP and self.direction != pygame.K_DOWN:
                        self.direction = pygame.K_UP
                        location_modify = Location(0, -SNAKE_BLOCK_SIZE)
                    if evt.key == pygame.K_DOWN and self.direction != pygame.K_UP:
                        self.direction = pygame.K_DOWN
                        location_modify = Location(0, SNAKE_BLOCK_SIZE)


            if self.snake.head_loc == self.food_location:
                print("Yum")
                self.snake.add_link(self.snake.head_loc)
                self.food_location = self.generate_random_location()

            # Update the snake's location
            self.snake.head_loc = self.snake.head_loc + location_modify
            # print(self.snake.set_head_loc)

            if self.is_out_of_bounds(self.snake.head_loc) or self.snake.head_loc in self.snake.links[1:]:
                print(f"Score: {len(self.snake.links)}")
                print(f"Links: {[loc for loc in self.snake.links]}")
                self.handle_snake_is_dead()
            else:
                self.disp.fill(Colors.black)
                pygame.draw.rect(self.disp, Colors.red,
                                 [self.food_location.x, self.food_location.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

                for link in self.snake.links:
                    pygame.draw.rect(self.disp, Colors.green,
                                 [link.x, link.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

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