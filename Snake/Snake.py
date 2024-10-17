import pygame as pg
import random 

#Inital Pygame
pg.init()

#Game window
WINDOW_SIZE = (700,700)
screen = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption('Snake Game')

#Load sound
sound1 = pg.mixer.Sound(r'sound/tick.wav')
sound2 = pg.mixer.Sound(r'sound/te.wav')
sound3 = pg.mixer.Sound(r'sound/background sound.mp3')

#Initialization
snake_part = 20
x,y = 200,200
x_change, y_change = 0,0
body_snake = []
length = 1 
score, highscore = 0,0 
line_y = 90
line_height = 20

#Create food
food_x = random.randint(0, (WINDOW_SIZE[0] // snake_part) - 1) * snake_part
food_y = random.randint(6, (WINDOW_SIZE[1] // snake_part) - 1) * snake_part

#Snake speed 
clock = pg.time.Clock()
speed = 3

#Def function
def show_start_screen():
    game_font = pg.font.Font('04B_19.TTF', 50)
    title_text = game_font.render('Snake Game', True, (255, 255, 255))
    start_text = game_font.render('Press SPACE to Start', True, (255, 255, 255))

    while True:
        screen.fill((0,0,0))
        screen.blit(title_text, (WINDOW_SIZE[0] // 2 - title_text.get_width() // 2, 250))
        screen.blit(start_text, (WINDOW_SIZE[0] // 2 - start_text.get_width() // 2, 350))
        
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Press Space to start
                    return

def reset_game():
    #Reset game
    global x, y, x_change, y_change, body_snake, length, score
    x,y = 200,200
    x_change, y_change = 0, 0
    body_snake = []
    length = 1 
    score = 0


def check_col():
    if x < 0 or x > WINDOW_SIZE[0] or y < 110 or y > WINDOW_SIZE[1] or (x,y) in body_snake[:-1]:
        pg.mixer.Sound.play(sound2)
        return False
    return True

def score_view():
    game_font = pg.font.Font('04B_19.TTF',40)
    line = game_font.render(f'________________________________', True, (255,255,255))
    screen.blit(line,(0,90))
    if gamePlay:
        score_txt = game_font.render(f'Score: {score}', True, (255,255,255))
        screen.blit(score_txt,(120,40))
        hscore_txt = game_font.render(f'High score: {highscore}', True, (255,255,255))
        screen.blit(hscore_txt,(320,40))
    else:
        note_text = game_font.render(f'Press space to play again: ', True, (255,255,255))
        screen.blit(note_text,(80,40))

#Game loop
show_start_screen()
pg.mixer.Sound.play(sound3)
reset_game()
gamePlay = True
while True:
    for event in pg.event.get():
        #Quit
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        #Snake move
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                x_change -= snake_part
                y_change = 0
            elif event.key == pg.K_RIGHT:
                x_change = snake_part
                y_change = 0
            elif event.key == pg.K_UP:
                x_change = 0
                y_change -= snake_part
            elif event.key == pg.K_DOWN:
                x_change = 0
                y_change = snake_part
            elif event.key == pg.K_SPACE:
                gamePlay = True

        
    #Clear screen
    screen.fill((0,0,0))
    score_view()
    if gamePlay:
        #Update snake position
        x += x_change
        y += y_change

        #Add snake part
        body_snake.append((x,y))

        #Remove snake part
        if len(body_snake)>length:
            del body_snake[0]

        #Check snake eats food
        if x == food_x and y == food_y:
            length += 1
            score += 1
            pg.mixer.Sound.play(sound1)
            if score > highscore: highscore = score
            #Random food
            food_x = random.randint(0, (WINDOW_SIZE[0] // snake_part) - 1) * snake_part
            food_y = random.randint(0, (WINDOW_SIZE[1] // snake_part) - 1) * snake_part
            while food_y >= line_y and food_y <= line_y + line_height:
                food_y = random.randint(0, (WINDOW_SIZE[1] // snake_part) - 1) * snake_part
        
        #Draw snake
        for x,y in body_snake:
            pg.draw.rect(screen,(255,0,0),(x,y,snake_part,snake_part))
        #Draw food
        pg.draw.rect(screen,(255,255,255),(food_x,food_y,snake_part,snake_part))
        gamePlay = check_col()
        clock.tick(speed)
    else:
        #Reset game
        reset_game()

    #Update screen
    pg.display.update()