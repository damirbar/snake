import random

import os
import pygame


# Constants
SNAKE_BLOCK_SIZE      = 10
SCREEN_HEIGHT         = 600
SCREEN_WIDTH          = 800
LOSE_QUIT             = 1
LOSE_REPLAY           = 2
FONT_SIZE             = 25
SNAKE_HIGH_SCORE_PATH = './.snake_high_score'

# Colors
class Colors:
    red        = (255,0,0)
    green      = (0,255,0)
    dark_green = (0,200,0)
    blue       = (0,0,255)
    white      = (255,255,255)
    black      = (0,0,0)


class Location:

    def __init__(self, x=0, y=0):
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
        if not self.ate_food:
            self.__links.pop()
        else:
            self.ate_food = False
        self.__links.insert(0, loc)

    def add_link(self):
        self.ate_food = True

    @property
    def links(self):
        return self.__links



class SnakeGame:

    def __init__(self, snake_speed=30):
        self.disp                 = None
        self.init_display()

        self.snake                = Snake(Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.clock                = pygame.time.Clock()
        self.snake_speed          = snake_speed
        self.food_location        = self.generate_random_location()
        self.keep_playing         = True
        self.is_snake_dead        = False
        self.direction            = None
        self.is_direction_changed = False
        self.location_modify      = None
        self.score_font           = pygame.font.SysFont("calibri", FONT_SIZE)
        self.font_style           = pygame.font.SysFont("bahnschrift", FONT_SIZE)
        self.high_score           = self.read_high_score()

    def read_high_score(self):
        if os.path.exists(SNAKE_HIGH_SCORE_PATH):
            with open(SNAKE_HIGH_SCORE_PATH) as score_file:
                try:
                    return int(score_file.read())
                except:
                    return 0

    def update_high_score(self):
        with open(SNAKE_HIGH_SCORE_PATH, 'w') as score_file:
            score_file.write(str(self.high_score))

    def restart(self):
        self.snake = Snake(Location(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
        self.food_location = self.generate_random_location()
        self.keep_playing = True
        self.is_snake_dead = False
        self.direction = None
        self.is_direction_changed = False
        self.location_modify = None

    def init_display(self):
        pygame.init()
        self.disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.update()
        pygame.display.set_caption("Snake Game")

    @staticmethod
    def generate_random_location():
        return Location(
            round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        )

    @staticmethod
    def is_out_of_bounds(loc):
        if loc.x < 0 or loc.y < 0 or loc.x > SCREEN_WIDTH-1 or loc.y > SCREEN_HEIGHT-1:
            return True

    def score_counter(self):
        value = self.score_font.render(f"Score: {len(self.snake.links)}", True, Colors.white)
        self.disp.blit(value, [10,10])

        if self.high_score is not None:
            value = self.score_font.render(f"High Score: {self.high_score}", True, Colors.white)
            self.disp.blit(value, [10, 37])

    def should_continue_playing(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_c:
                return LOSE_REPLAY
            else:
                return LOSE_QUIT
        if evt.type == pygame.QUIT:
            return LOSE_QUIT

    def handle_play_event(self, evt):
        # If the user attempts to close the game window
        if evt.type == pygame.QUIT:
            self.keep_playing = False
            exit(0)

        # If the user pressed a key
        if evt.type == pygame.KEYDOWN and not self.is_direction_changed:
            if evt.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                self.direction = pygame.K_LEFT
                self.is_direction_changed = True
                self.location_modify = Location(-SNAKE_BLOCK_SIZE, 0)
            if evt.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                self.direction = pygame.K_RIGHT
                self.is_direction_changed = True
                self.location_modify = Location(SNAKE_BLOCK_SIZE, 0)
            if evt.key == pygame.K_UP and self.direction != pygame.K_DOWN:
                self.direction = pygame.K_UP
                self.is_direction_changed = True
                self.location_modify = Location(0, -SNAKE_BLOCK_SIZE)
            if evt.key == pygame.K_DOWN and self.direction != pygame.K_UP:
                self.direction = pygame.K_DOWN
                self.is_direction_changed = True
                self.location_modify = Location(0, SNAKE_BLOCK_SIZE)

    def prompt(self, msg, color):
        lines = msg.splitlines()
        for i, line in enumerate(lines):
            prompt_line = self.font_style.render(line, True, color)
            self.disp.blit(prompt_line, [SCREEN_WIDTH/6, SCREEN_HEIGHT/3 + (FONT_SIZE*i + 2)])

    def game_loop(self):
        self.location_modify = Location()

        while self.keep_playing and not self.is_snake_dead:
            self.is_direction_changed = False

            for evt in pygame.event.get():
                self.handle_play_event(evt)


            if self.snake.head_loc == self.food_location:
                self.snake.add_link()
                self.food_location = self.generate_random_location()

            # Update the snake's location
            self.snake.head_loc = self.snake.head_loc + self.location_modify

            if self.is_out_of_bounds(self.snake.head_loc) or self.snake.head_loc in self.snake.links[1:]:
                print(f"Score: {len(self.snake.links)}")
                self.is_snake_dead = True

                if self.high_score is None or len(self.snake.links) > self.high_score:
                    self.high_score = len(self.snake.links)
                    self.update_high_score()
            else:
                self.disp.fill(Colors.black)
                pygame.draw.rect(self.disp, Colors.red,
                                 [self.food_location.x, self.food_location.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

                pygame.draw.rect(self.disp, Colors.dark_green,
                             [self.snake.links[0].x, self.snake.links[0].y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
                for link in self.snake.links[1:]:
                    pygame.draw.rect(self.disp, Colors.green,
                                 [link.x, link.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

                self.score_counter()
                pygame.display.update()

                # Refresh rate according to the selected snake speed
                self.clock.tick(self.snake_speed)



def play_game(game):
    while True:
        game.game_loop()

        if game.is_snake_dead:
            game.prompt("Play another round?\nC - continue\nAny other key to quit", Colors.red)
            game.score_counter()
            pygame.display.update()

            user_res = None

            while user_res is None:
                for evt in pygame.event.get():
                    user_res = game.should_continue_playing(evt)

            if user_res == LOSE_REPLAY:
                game.restart()
            else:
                pygame.quit()
                exit(0)

def main():
    game = SnakeGame()
    play_game(game)



if __name__ == '__main__':
    main()