
from tkinter import *
import random

class Snake:
  def __init__(self):
    self.body_size = BODY_PARTS
    self.coordinates = []
    self.squares = []

    for i in range(0, BODY_PARTS):
      self.coordinates.append([0, 0])

    for x, y in self.coordinates:
      square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="snake")
      self.squares.append(square)

class Food:
  def __init__(self, snake):
    while True:
      x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
      y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
      self.coordinates = [x, y]
      
      overlap = False
      for coord in snake.coordinates:
        if coord[0] == x and coord[1] == y:
          overlap = True
          break
          
      if not overlap:
        break
        
    canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")

def next_turn(snake, food):
  x, y = snake.coordinates[0]

  if direction == 'up':
    y -= SPACE_SIZE
  elif direction == 'down':
    y += SPACE_SIZE
  elif direction == 'left':
    x -= SPACE_SIZE
  elif direction == 'right':
    x += SPACE_SIZE

  snake.coordinates.insert(0, (x, y))
  square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)
  snake.squares.insert(0, square)

  if x == food.coordinates[0] and y == food.coordinates[1]:
    global score 
    global SPEED
    score += 1
    SPEED -= 5

    label.config(text="Счёт: {}".format(score))
    canvas.delete("food")
    food = Food(snake)
  else:
    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1])
    del snake.squares[-1]

  if check_collisions(snake):
    game_over()
  else:
    window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
  global direction 
  if new_direction == 'left' and direction != 'right':
    direction = new_direction
  elif new_direction == 'right' and direction != 'left':
    direction = new_direction
  elif new_direction == 'up' and direction != 'down':
    direction = new_direction
  elif new_direction == 'down' and direction != 'up':
    direction = new_direction

def check_collisions(snake):
  x, y = snake.coordinates[0]

  if x < 0 or x >= GAME_WIDTH:
    return True
  elif y < 0 or y >= GAME_HEIGHT:
    return True
  
  for body_part in snake.coordinates[1:]:
    if x == body_part[0] and y == body_part[1]:
      return True
    
  return False

def game_over():
  canvas.delete(ALL)
  canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('Arial', 16), text="Конец игры!", fill="black", tag="gameover")
  canvas.bind("<ButtonPress-1>", start_game)

def start_game(event=None):
  global direction   
  global score
  global SPEED
  score = 0
  SPEED = 250
  direction = "down"
  label.config(text="Счёт: {}".format(score))
  canvas.delete(ALL)
  canvas.unbind("<ButtonPress-1>")
  snake = Snake()
  food = Food(snake)
  next_turn(snake, food)

window = Tk()
window.title("Змейка")
window.resizable(False, False)

score = 0
direction = 'down'
SPEED = 250

GAME_WIDTH = 330
GAME_HEIGHT = 330
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOUR = "SpringGreen2"
FOOD_COLOUR = "tomato"
BACKGROUND_COLOUR = "grey75"

label = Label(window, text="Счёт: {}".format(score), font=('Arial', 14))
label.pack(padx=20, pady=5, anchor="e")

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, anchor="c", text="Кликни, чтобы начать игру!", fill="#000000", font=('Arial', 16), tag="start")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

canvas.bind("<ButtonPress-1>", start_game)

window.geometry(f"{GAME_WIDTH+40}x{GAME_HEIGHT+70}")
window.mainloop()
