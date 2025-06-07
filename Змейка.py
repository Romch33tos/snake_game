from tkinter import Tk, Canvas, Label, ALL
import random

class Snake:
  def __init__(self):
    self.body_size = INITIAL_BODY_PARTS
    self.coordinates = []
    self.squares = []

    for _ in range(INITIAL_BODY_PARTS):
      self.coordinates.append([0, 0])

    for x, y in self.coordinates:
      square = canvas.create_rectangle(
        x, y, 
        x + SPACE_SIZE, y + SPACE_SIZE, 
        fill=SNAKE_COLOR, 
        tag="snake"
      )
      self.squares.append(square)

class Food:
  def __init__(self, snake, is_special=False):
    self.is_special = is_special
    while True:
      x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
      y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
      self.coordinates = [x, y]
      
      is_overlapping = any(
        coord[0] == x and coord[1] == y 
        for coord in snake.coordinates
      )
      
      if not is_overlapping:
        break
        
    color = SPECIAL_FOOD_COLOR if is_special else FOOD_COLOR
    tag = "special_food" if is_special else "food"
    canvas.create_oval(
      x, y, 
      x + SPACE_SIZE, y + SPACE_SIZE, 
      fill=color, 
      tag=tag
    )

def next_turn(snake, food):
  global score, GAME_SPEED, special_food, special_food_timer
  
  head_x, head_y = snake.coordinates[0]

  if direction == 'up':
    head_y -= SPACE_SIZE
  elif direction == 'down':
    head_y += SPACE_SIZE
  elif direction == 'left':
    head_x -= SPACE_SIZE
  elif direction == 'right':
    head_x += SPACE_SIZE

  head_x = head_x % GAME_WIDTH
  head_y = head_y % GAME_HEIGHT

  snake.coordinates.insert(0, (head_x, head_y))
  square = canvas.create_rectangle(
    head_x, head_y, 
    head_x + SPACE_SIZE, head_y + SPACE_SIZE, 
    fill=SNAKE_COLOR
  )
  snake.squares.insert(0, square)

  if head_x == food.coordinates[0] and head_y == food.coordinates[1]:
    score += 1
    GAME_SPEED -= 2
    label.config(text="Счёт: {}".format(score))
    canvas.delete("food")
    food = Food(snake)
    
    if score % 5 == 0:
      if special_food_timer:
        window.after_cancel(special_food_timer)
      canvas.delete("special_food")
      special_food = Food(snake, is_special=True)
      special_food_timer = window.after(5000, remove_special_food)
  
  elif special_food and head_x == special_food.coordinates[0] and head_y == special_food.coordinates[1]:
    score += 10
    label.config(text="Счёт: {}".format(score))
    canvas.delete("special_food")
    if special_food_timer:
      window.after_cancel(special_food_timer)
    special_food = None
    special_food_timer = None
  else:
    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1])
    del snake.squares[-1]

  if check_collisions(snake):
    game_over()
  else:
    window.after(GAME_SPEED, next_turn, snake, food)

def remove_special_food():
  global special_food, special_food_timer
  canvas.delete("special_food")
  special_food = None
  special_food_timer = None

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
  head_x, head_y = snake.coordinates[0]
  
  for body_part in snake.coordinates[1:]:
    if head_x == body_part[0] and head_y == body_part[1]:
      return True
  
  return False

def game_over():
  global special_food_timer
  if special_food_timer:
    window.after_cancel(special_food_timer)
  canvas.delete(ALL)
  canvas.create_text(
    canvas.winfo_width()/2, 
    canvas.winfo_height()/2, 
    font=('Arial', 16), 
    text="Конец игры!", 
    fill="black", 
    tag="gameover"
  )
  window.bind('<space>', start_game)

def start_game(event=None):
  global direction, score, GAME_SPEED, special_food, special_food_timer
  score = 0
  GAME_SPEED = 250
  direction = "down"
  special_food = None
  if special_food_timer:
    window.after_cancel(special_food_timer)
  special_food_timer = None
  label.config(text="Счёт: {}".format(score))
  canvas.delete(ALL)
  window.unbind('<space>')
  snake = Snake()
  food = Food(snake)
  next_turn(snake, food)

window = Tk()
window.title("Змейка")
window.resizable(False, False)

score = 0
direction = 'down'
GAME_SPEED = 250
special_food = None
special_food_timer = None

GAME_WIDTH = 330
GAME_HEIGHT = 330
SPACE_SIZE = 30
INITIAL_BODY_PARTS = 3
SNAKE_COLOR = "SpringGreen2"
FOOD_COLOR = "tomato"
SPECIAL_FOOD_COLOR = "yellow"
BACKGROUND_COLOR = "grey75"

label = Label(window, text="Счёт: {}".format(score), font=('Arial', 14))
label.pack(padx=20, pady=5, anchor="e")

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
canvas.create_text(
  GAME_WIDTH/2, 
  GAME_HEIGHT/2, 
  anchor="c", 
  text="Нажмите пробел,\nчтобы начать игру!", 
  fill="#000000", 
  font=('Arial', 16), 
  tag="start", 
  justify="center"
)

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<space>', start_game)

window.geometry(f"{GAME_WIDTH+40}x{GAME_HEIGHT+70}")
window.mainloop()
