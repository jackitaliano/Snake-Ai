from codecs import xmlcharrefreplace_errors
from this import s
import pygame
import random
from enum import Enum
from typing import NamedTuple

CLOCK = pygame.time.Clock()
FPS = 10
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Point(NamedTuple):
    x: int
    y: int


# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20


def get_food(display_w, display_h):
    return DrawablePoint(random.randint(
        0, (display_w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE, random.randint(
        0, (display_h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE)


class DrawablePoint(Point):
    def draw(self, display):
        pygame.draw.rect(display, RED, pygame.Rect(
            self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


class Snake:
    def __init__(self, starting_x: int, starting_y: int):
        self.direction = Direction.RIGHT

        self.head = Point(starting_x, starting_y)
        self.body = [self.head,
                     Point(self.head.x-BLOCK_SIZE, self.head.y),
                     Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

    def move(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def draw(self, display):
        for pt in self.body:
            pygame.draw.rect(display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(display, BLUE2, pygame.Rect(
                pt.x+4, pt.y+4, 12, 12))


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        # init snake
        self.snake = Snake(starting_x=self.w/2, starting_y=self.h/2)

        # init food
        self.food = get_food(self.w, self.h)
        self._place_food()

        # init game state
        self.score = 0

    def _place_food(self):
        self.food = get_food(self.w, self.h)

        if self.food in self.snake.body:
            self.food.place(self.w, self.h)

    def play_step(self):
        # 1. collect user input
        self.snake.control()

        # 2. move
        self.snake.move()  # update the head
        self.snake.body.insert(0, self.snake.head)

        # 3. check if game over
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.snake.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.body.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake.body[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        self.snake.draw(self.display)
        self.food.draw(self.display)

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGameAI()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

        CLOCK.tick(FPS)

    print('Final Score', score)

    pygame.quit()
