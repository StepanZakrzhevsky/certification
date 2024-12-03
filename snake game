import pygame
import random
import sqlite3

pygame.init()

# Параметры экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')

# Цвета
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (2, 100, 62)
white = (255, 255, 255)

# Параметры змейки
snake_block = 10
snake_speed = 15

# Шрифт
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

class Database:
    def __init__(self):  # Изменить на __init__
        self.conn = sqlite3.connect('scores.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER
            )''')
        self.conn.commit()

    def insert_score(self, name, score):
        self.cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        self.conn.commit()

    def get_top_scores(self):
        # Получаем уникальные имена и максимальные баллы
        self.cursor.execute('''
            SELECT name, MAX(score) FROM scores GROUP BY name ORDER BY MAX(score) DESC LIMIT 5''')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class Snake:
    def __init__(self):
        self.snake_List = []
        self.Length_of_snake = 1
        self.x = width / 2
        self.y = height / 2
        self.x_change = 0
        self.y_change = 0

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    def grow(self):
        self.Length_of_snake += 1

    def get_head_pos(self):
        return self.x, self.y

    def get_length(self):
        return self.Length_of_snake

    def reset(self):
        self.snake_List.clear()
        self.Length_of_snake = 1
        self.x = width / 2
        self.y = height / 2
        self.x_change = 0
        self.y_change = 0

    def draw(self):
        for segment in self.snake_List:
            pygame.draw.rect(screen, dark_green, [segment[0], segment[1], snake_block, snake_block])

def your_score(score):
    value = score_font.render("Очки: " + str(score), True, white)
    screen.blit(value, [0, 0])

def message(msg, color):
    lines = msg.split('\n')
    for i, line in enumerate(lines):
        mesg = font_style.render(line, True, color)
        mesg_rect = mesg.get_rect(center=(width / 2, height / 2 + i * 30))
        screen.blit(mesg, mesg_rect)

def display_top_scores(db):
    top_scores = db.get_top_scores()
    time_to_display = 5000  # время отображения в миллисекундах
    start_ticks = pygame.time.get_ticks()  # получить текущее время

    while True:
        screen.fill((0, 255, 0))  # Замените фон на зеленый
        message("Топ Игроков:", white)

        for i, (name, score) in enumerate(top_scores):
            score_msg = f"{i + 1}. {name}: {score}"
            score_render = font_style.render(score_msg, True, white)
            screen.blit(score_render, (width / 2 - score_render.get_width() / 2, height / 2 + (i + 1) * 30))

        pygame.display.update()

        # Проверяем, прошло ли время, чтобы выйти из цикла
        seconds = pygame.time.get_ticks() - start_ticks
        if seconds > time_to_display:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def gameLoop(player_name):
    db = Database()  # Создаем объект базы данных
    db.__init__()  # Инициализировать базу данных
    game_over = False
    game_close = False

    snake = Snake()
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Инициализация часов
    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(blue)
            message("Ты проиграл!\nНажми Пробел,\nчтобы играть заново\nили Q, чтобы выйти", red)
            your_score(snake.get_length() - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop(player_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.x_change = -snake_block
                    snake.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake.x_change = snake_block
                    snake.y_change = 0
                elif event.key == pygame.K_UP:
                    snake.y_change = -snake_block
                    snake.x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake.y_change = snake_block
                    snake.x_change = 0

        # Проверка на столкновение со стенками
        if snake.x >= width or snake.x < 0 or snake.y >= height or snake.y < 0:
            game_close = True

        snake.move()

        # Обновление тела змейки
        snake.snake_List.append((snake.x, snake.y))
        if len(snake.snake_List) > snake.Length_of_snake:
            del snake.snake_List[0]

        # Проверка на столкновение с собственным телом
        for segment in snake.snake_List[:-1]:
            if segment == (snake.x, snake.y):
                game_close = True

        screen.fill(green)
        snake.draw()
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

        your_score(snake.get_length() - 1)

        pygame.display.update()

        # Проверка на поедание еды
        if snake.x == foodx and snake.y == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake.grow()

        clock.tick(snake_speed)

    db.insert_score(player_name, snake.get_length() - 1)
    display_top_scores(db)

    db.close()  # Закрытие соединения базы данных
    pygame.quit()

if __name__ == "__main__":
    player_name = input("Enter your name: ")
    gameLoop(player_name)
