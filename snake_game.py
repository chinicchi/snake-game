import pygame
import random
import sys

pygame.init()
pygame.font.init()

# COLOR
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

rows = cols = 25

width = height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")


class Cube:
    rows = cols = 25
    width = 500

    def __init__(self, position, color, direction_x=1, direction_y=0):
        self.position = position
        self.color = color
        self.direction_x = direction_x
        self.direction_y = direction_y

    def move_cube(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y

        self.position = (
            self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw_cube(self, window):
        distance = width//rows

        x = self.position[0]
        y = self.position[1]

        pygame.draw.rect(window, self.color, (x*distance,
                         y*distance, distance, distance))


class Snake:
    rows = cols = 25
    purple = (100, 100, 255)

    def __init__(self, position, color=purple):
        self.position = position
        self.color = color
        self.body = []
        self.turns = {}
        self.head = Cube(self.position, self.color)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 0

    def move_snake(self):
        keys = pygame.key.get_pressed()

        for key in keys:
            if self.head.direction_x == 1 or self.head.direction_x == -1:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.head.position[:]] = [
                        self.direction_x, self.direction_y]
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.head.position[:]] = [
                        self.direction_x, self.direction_y]
            elif self.head.direction_y == 1 or self.head.direction_y == -1:
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.position[:]] = [
                        self.direction_x, self.direction_y]
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.position[:]] = [
                        self.direction_x, self.direction_y]

        for index, cube in enumerate(self.body):
            pos = cube.position[:]
            if pos in self.turns:
                turn = self.turns[pos]
                cube.move_cube(turn[0], turn[1])
                if index == len(self.body)-1:
                    self.turns.pop(pos)
            else:
                if cube.direction_x == 1 and cube.position[0] >= cols-1:
                    cube.position = (0, cube.position[1])
                elif cube.direction_x == -1 and cube.position[0] <= 0:
                    cube.position = (cube.cols-1, cube.position[1])
                elif cube.direction_y == -1 and cube.position[1] <= 0:
                    cube.position = (cube.position[0], cube.rows-1)
                elif cube.direction_y == 1 and cube.position[1] >= rows-1:
                    cube.position = (cube.position[0], 0)
                else:
                    cube.move_cube(cube.direction_x, cube.direction_y)

    def add_tail(self):
        tail = self.body[-1]
        dir_x, dir_y = tail.direction_x, tail.direction_y

        if dir_x == 1 and dir_y == 0:
            self.body.append(
                Cube((tail.position[0]-1, tail.position[1]), self.color))
        elif dir_x == -1 and dir_y == 0:
            self.body.append(
                Cube((tail.position[0]+1, tail.position[1]), self.color))
        elif dir_x == 0 and dir_y == 1:
            self.body.append(
                Cube((tail.position[0], tail.position[1]-1), self.color))
        elif dir_x == 0 and dir_y == -1:
            self.body.append(
                Cube((tail.position[0], tail.position[1]+1), self.color))

        self.body[-1].direction_x = dir_x
        self.body[-1].direction_y = dir_y

    def reset_snake(self, position, color=purple):
        self.body = []
        self.turns = {}
        self.head = Cube(position, color)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 0

    def draw_snake(self, window):
        for cube in self.body:
            cube.draw_cube(window)


def draw_window(snake, food):
    window.fill(black)
    snake.draw_snake(window)
    food.draw_cube(window)
    pygame.display.update()


def random_food(snake):
    while True:
        x = random.randrange(rows)
        y = random.randrange(cols)

        for cube in snake.body:
            if cube == (x, y):
                continue
            else:
                break

        break

    return (x, y)


def draw_score(score):
    main_font = pygame.font.SysFont('comicsans', 25)
    text = main_font.render('Score: ' + str(score), 1, white)
    window.blit(text, (200, 200))
    pygame.display.update()


def main():
    snake = Snake((12, 12))
    food = Cube(random_food(snake), red)

    fps = 30
    speed_delay = 200
    score = 0

    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(speed_delay)
        clock.tick(fps)

        snake.move_snake()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # EAT FOOD
        if snake.body[0].position == food.position:
            snake.add_tail()
            food = Cube(random_food(snake), red)

            if speed_delay <= 100:
                speed_delay -= 5
            else:
                speed_delay -= 10

            score += 1

        # GAME OVER
        for i in range(len(snake.body)):
            if i+1 < len(snake.body):
                if snake.body[0].position == snake.body[i+1].position:
                    draw_score(score)
                    pygame.time.delay(3000)
                    snake.reset_snake((12, 12))
                    speed_delay = 200
                    score = 0
                    break

        draw_window(snake, food)


if __name__ == '__main__':
    main()
