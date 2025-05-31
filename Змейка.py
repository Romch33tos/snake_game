from tkinter import *
import random

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares =[]

        for i in range (0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE , y + SPACE_SIZE , fill=SNAKE_COLOUR, tag = "snake")
            self.squares.append(square)


class Food:
    
    def __init__(self):

        x= random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1)* SPACE_SIZE
        y= random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1)* SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x, y, x+ SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOUR, tag="food")



def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == 'up':
        y-=SPACE_SIZE
        
    elif direction == 'down':
        y+=SPACE_SIZE

    elif direction == 'left':
        x-=SPACE_SIZE

    elif direction == 'right':
        x+=SPACE_SIZE


    snake.coordinates.insert(0, (x,y))

    square = canvas.create_rectangle(x,y , x + SPACE_SIZE , y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0,square)

    if x==food.coordinates[0] and y == food.coordinates[1]:

        global score 
        
        score += 1

        label.config(text="Счёт: {}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisons(snake):
        game_over()

    else:
        window.after(SPEED,next_turn,snake,food)


def change_direction(new_direction):

    global direction 

    if new_direction =='left':
        if direction!= 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction!= 'left':
            direction = new_direction

    if new_direction =='up':
        if direction!= 'down':
            direction = new_direction

    if new_direction =='down':
        if direction!= 'up':
            direction = new_direction


def check_collisons(snake):
    x , y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

def game_over():    
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('Airal',16),text= "Конец игры!", fill = "red", tag = "gameover")

    rbtn = Button(text = "Ещё раз?", font=('Arial',10),command = reset)
    canvas.create_window(280,400,window = rbtn)

def reset():
    global direction
    score = 0
    label.config(text="Счёт: {}".format(score))
    canvas.delete(ALL)
    direction= "down"
    snake = Snake()
    
    food = Food()
    next_turn(snake,food)

window = Tk()
window.title("Змейка")
window.resizable(False,False)
window.geometry("600x850")
score = 0
direction = 'down'

GAME_WIDTH = 550
GAME_HEIGHT = 550
SPEED = 180
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "SpringGreen2"
FOOD_COLOUR = "tomato"
BACKGROUND_COLOUR = "grey75"

label = Label(window, text= "Счёт: {}".format(score),font=('Arial', 10))
label.pack(pady = 5)

canvas = Canvas(window, bg = BACKGROUND_COLOUR,height = GAME_HEIGHT,width = GAME_WIDTH)
canvas.pack()

f1 = Frame(window)

btn = Button(f1, text = "ВВЕРХ", width = 4, height = 2,command = lambda: change_direction('up'))
btn.pack(side = "top", pady = 10)

btn2 = Button(f1, text = "ВЛЕВО", width = 4, height = 2,command = lambda: change_direction('left'))
btn2.pack(side = "left", padx = 40)

btn3 = Button(f1, text = "ВПРАВО", width = 4, height= 2, command = lambda: change_direction('right'))
btn3.pack(side = "right", padx = 40)

btn4 = Button(f1, text = "ВНИЗ", width = 4, height= 2, command = lambda: change_direction('down'))
btn4.pack(side = "bottom")

f1.pack()

snake = Snake()

food = Food()

next_turn(snake,food)

window.mainloop()
