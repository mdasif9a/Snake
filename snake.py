# import modules and class which is uses
import pygame
from sys import exit
from pygame import Vector2
from random import randint


# initilaize pygame
pygame.init()


#set pixel size and number of pixel in one row or column
pixel_size = 20
num_of_pixel = 30


# make window for pygame
screen_width = pixel_size * num_of_pixel
screen_height = pixel_size * num_of_pixel
main_screen = pygame.display.set_mode((screen_width, screen_height))

#Class for our Snake
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 27), Vector2(5, 27), Vector2(4, 27),]
        self.direction = Vector2(0, 0)

        #all snake image/sprite load
        self.body_bl = pygame.image.load("images/body_bl.png")
        self.body_br = pygame.image.load("images/body_br.png")
        self.body_horizontal = pygame.image.load("images/body_horizontal.png")
        self.body_tl = pygame.image.load("images/body_tl.png")
        self.body_tr = pygame.image.load("images/body_tr.png")
        self.body_vertical = pygame.image.load("images/body_vertical.png")
        self.head_down = pygame.image.load("images/head_down.png")
        self.head_left = pygame.image.load("images/head_left.png")
        self.head_right = pygame.image.load("images/head_right.png")
        self.head_up = pygame.image.load("images/head_up.png")
        self.tail_down = pygame.image.load("images/tail_down.png")
        self.tail_left = pygame.image.load("images/tail_left.png")
        self.tail_right = pygame.image.load("images/tail_right.png")
        self.tail_up = pygame.image.load("images/tail_up.png")
    
    #logic for Draw Snake
    def draw_snake(self):
        for index, item in enumerate(self.body):
            snake_head = self.snake_head()
            snake_tail = self.snake_tail()
            x = int(item.x)*pixel_size
            y = int(item.y)*pixel_size
            if index == 0:
                main_screen.blit(snake_head, [x, y])
            elif index == len(self.body) - 1:
                main_screen.blit(snake_tail, [x, y])
            else:
                previous_block = self.body[index + 1] - item
                next_block = self.body[index - 1] - item
                if previous_block.x == next_block.x:
                    main_screen.blit(self.body_vertical, [x,y])
                elif previous_block.y == next_block.y:
                    main_screen.blit(self.body_horizontal, [x,y])
                else:
                    if previous_block.x == -1 and next_block.y == -1 or next_block.x == -1 and previous_block.y == -1:
                        main_screen.blit(self.body_tl, [x,y])
                    elif previous_block.x == 1 and next_block.y == -1 or next_block.x == 1 and previous_block.y == -1:
                        main_screen.blit(self.body_tr, [x,y])
                    elif previous_block.x == 1 and next_block.y == 1 or next_block.x == 1 and previous_block.y == 1:
                        main_screen.blit(self.body_br, [x,y])
                    elif previous_block.x == -1 and next_block.y == 1 or next_block.x == -1 and previous_block.y == 1:
                        main_screen.blit(self.body_bl, [x,y])

    #return a Snake head image
    def snake_head(self):
        if (self.body[0].x - self.body[1].x) == 1:
            head_img = self.head_right
        elif (self.body[0].x - self.body[1].x) == -1:
            head_img = self.head_left
        elif (self.body[0].y - self.body[1].y) == 1:
            head_img = self.head_down
        elif (self.body[0].y - self.body[1].y) == -1:
            head_img = self.head_up
        return head_img

    #return a Snake tail image
    def snake_tail(self):
        if (self.body[-2].x - self.body[-1].x) == -1:
            tail_img = self.tail_right
        elif (self.body[-2].x - self.body[-1].x) == 1:
            tail_img = self.tail_left
        elif (self.body[-2].y - self.body[-1].y) == -1:
            tail_img = self.tail_down
        elif (self.body[-2].y - self.body[-1].y) == 1:
            tail_img = self.tail_up
        return tail_img

    # Snake Move logic
    def snake_move(self):
        if not food.eated:
            copy_body = self.body[:-1]
            copy_body.insert(0, self.body[0] + self.direction)
            self.body = copy_body
        else:
            copy_body = self.body[:]
            copy_body.insert(0, self.body[0] + self.direction)
            self.body = copy_body
            food.eated = False

#class for our Food
class Food:
    def __init__(self):
        self.randomize()
        self.score = 0
        self.eated = False
        self.eat_sound = pygame.mixer.Sound("sounds/crunch.wav")

        #Food Image
        self.apple = pygame.image.load("images/apple.png")
    
    def randomize(self):
        self.x = randint(0, num_of_pixel-1)
        self.y = randint(0, num_of_pixel-1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        main_screen.blit(self.apple, [self.x*pixel_size, self.y*pixel_size])
    
    def apple_eat(self):
        if snake.body[0] == self.pos:
            self.randomize()
            self.score += 1
            self.eat_sound.play()
            self.eated = True


#Game Window, Run, over And play
class Main:
    def __init__(self):
        self.start = False
        self.start_image = pygame.image.load("images/Snake.png")
        self.start_image = pygame.transform.scale(self.start_image, [400, 400])
        pygame.mixer.music.load("sounds/BackGround.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        self.gameover_sound = pygame.mixer.Sound("sounds/game_over.wav")

    def score_window(self):
        font = pygame.font.Font("fonts/RideTheFader-1XKg.ttf", 15)
        score = font.render("Score "+str(food.score), True, (0, 0, 255))
        main_screen.blit(score, [25*pixel_size, 29*pixel_size])

    
    def game_window(self):
        food.draw_fruit()
        food.apple_eat()
        snake.draw_snake()
        if snake.direction != Vector2(0, 0):
            snake.snake_move()
        self.check_fail()
        self.score_window()

    
    def check_fail(self):
        for item in snake.body[1:]:
            if snake.body[0] == item:
                self.game_over()

        if (snake.body[0].x == -1 or snake.body[0].x == 30) or (snake.body[0].y == -1 or snake.body[0].y == 30):
            self.game_over()

    def game_over(self):
        global gameRun
        self.overscore = food.score
        food.score = 0
        self.gameover_sound.play()
        pygame.mixer.music.set_volume(0.25)
        snake.body = [Vector2(6, 27), Vector2(5, 27), Vector2(4, 27),]
        snake.direction = Vector2(0, 0)
        gameRun = False
    
    def startScreen(self):
        font = pygame.font.SysFont("Arial", 25, True)
        font3 = pygame.font.SysFont("Arial", 40, True)
        surf1 = font.render("SNAKE GAME", True, (10, 150, 10))
        surf1_width = surf1.get_width()
        surf2 = font.render("BY- Md Asif@Creation", True, (10, 150, 10))
        surf2_width = surf2.get_width()
        surf3 = font3.render("Press Enter or Click To Start", True, (10, 100, 10))
        surf3_width = surf3.get_width()
        main_screen.fill((0, 255, 0))
        main_screen.blit(self.start_image, [80, 100])
        main_screen.blit(surf1, [(screen_width-surf1_width)//2, 30])
        main_screen.blit(surf2, [(screen_width-surf2_width)//2, 60])
        main_screen.blit(surf3, [(screen_width-surf3_width)//2, 500])
    
    def gameOverScreen(self):
        font1 = pygame.font.SysFont("Arial", 50, True)
        font2 = pygame.font.SysFont("Arial", 35, True)
        surf1 = font1.render("GAME OVER", True, (10, 100, 10))
        surf1_width = surf1.get_width()
        surf2 = font2.render("Your Score - "+str(self.overscore), True, (10, 50, 110))
        surf2_width = surf2.get_width()
        surf3 = font2.render("Press Enter or Click To Restart", True, (10, 120, 10))
        surf3_width = surf3.get_width()
        main_screen.fill((0, 255, 0))
        main_screen.blit(self.start_image, [80, 100])
        main_screen.blit(surf1, [(screen_width-surf1_width)//2, 30])
        main_screen.blit(surf2, [(screen_width-surf2_width)//2, 550])
        main_screen.blit(surf3, [(screen_width-surf3_width)//2, 500])


    def grass_board(self):
        for i in range(num_of_pixel):
            for j in range(num_of_pixel):
                if i%2 == 0:
                    if j%2 == 0:
                        pygame.draw.rect(main_screen, (13, 200, 0), [i*pixel_size, j*pixel_size, pixel_size, pixel_size], )
                    else:
                        pygame.draw.rect(main_screen, (10, 231, 40), [i*pixel_size, j*pixel_size, pixel_size, pixel_size],)
                else:
                    if j%2 == 0:
                        pygame.draw.rect(main_screen, (10, 231, 40), [i*pixel_size, j*pixel_size, pixel_size, pixel_size], )
                    else:
                        pygame.draw.rect(main_screen, (13, 200, 0), [i*pixel_size, j*pixel_size, pixel_size, pixel_size],)


# set fps
clock = pygame.time.Clock()
fps = 10 #10 frame pr second

snake = Snake()
food = Food()
game = Main()

gameRun = False
startScreen = True
#pygame window loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                gameRun = True
                pygame.mixer.music.set_volume(1)
            if gameRun:
                if event.key == pygame.K_LEFT:
                    if snake.direction != Vector2(1, 0):
                        snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if snake.direction != Vector2(-1, 0):
                        snake.direction = Vector2(1, 0)
                if event.key == pygame.K_UP:
                    if snake.direction != Vector2(0, 1):
                        snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if snake.direction != Vector2(0, -1):
                        snake.direction = Vector2(0, 1)
        if not gameRun:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[0]:
                    gameRun = True
                    pygame.mixer.music.set_volume(1)
    if gameRun:
        game.grass_board()
        game.game_window()
        startScreen = False
    elif startScreen:
        game.startScreen()
    else:
        game.gameOverScreen()
    pygame.display.update()
    clock.tick(fps)