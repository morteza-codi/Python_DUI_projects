import random
from tkinter import *
import os
import sys
class Snake:
    def __init__ (self):
        self.body_size = BODY_SIZE
        # کاشی هایی که مار میره
        self.coordination = []
        # کاشی های رنگی
        self.squares = []
        # موقعیت اولیه مار
        for i in range(0 , BODY_SIZE):
            self.coordination.append([0 , 0])
        # موقعیت اولیه مار بصورت رنگی
        for x , y in self.coordination:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE , fill=SNAKE_COLOR , tag='snake')
            self.squares.append(square)
# ---------------------------------

class Food :
    def __init__ (self):
        x = random.randint(0 , (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0 , (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordination = [x , y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag='food')


# ---------------------------------

def next_turn (snake , food):
    x , y = snake.coordination[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordination.insert(0 , [x , y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0 , square)

    if x == food.coordination[0] and y == food.coordination[1]:
        global score
        score += 1
        label.config(text=f'Score : {score}')
        canvas.delete('food')
        food = Food()
    else:
        del snake.coordination[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    # برسی باخت
    if check_game_over (snake):
        game_over ()
    else:
        # حرکت مار
        window.after(SLOWNESS , next_turn , snake , food)

def change_direction (new_dir):
    global direction

    if new_dir == 'up':
        if direction != 'down':
            direction = new_dir
    elif new_dir == 'down':
        if direction != 'up':
            direction = new_dir
    elif new_dir == 'left':
        if direction != 'right':
            direction = new_dir
    elif new_dir == 'right':
        if direction != 'left':
            direction = new_dir


def check_game_over (snake):
    x , y = snake.coordination[0]

    if x < 0 or x > GAME_WIDTH:
        return True
    if y < 0 or y > GAME_HEIGHT:
        return True

    for i in snake.coordination[1:]:
        if x == i[0] and y == i[1]:
            return True
    return False

def game_over ():
    canvas.delete(ALL)
    canvas.create_text(700 / 2 , 796 / 2 , font=('Terminal' , 60) ,
                       text='GAME OVER !' , fill='red'
                       )

# -------------------------
def restart_game ():
    path = sys.executable
    os.execl(path, path, *sys.argv)
# -------------------------

# طول و عرض بازی
GAME_WIDTH = 700
GAME_HEIGHT = 700
#سایز کاشی ها
SPACE_SIZE = 20
BODY_SIZE = 2
#سرعت مار
SLOWNESS = 200
# رنگ مار و غذای مار
SNAKE_COLOR = 'yellow'
FOOD_COLOR = 'red'
BACKGROUND_COLOR = 'black'
# امتیاز
score = 0
# موقعیت مار
direction = 'down'

# --------------------------------------------

window = Tk()
window.title('Snake Game')
window.resizable(False, False)

label = Label(window, text=f'Score : {score}', font=('Courier', 30))
label.pack()

canvas = Canvas(window , bg = BACKGROUND_COLOR , height=GAME_HEIGHT , width=GAME_WIDTH)
canvas.pack()

restart = Button(window, text='Restart', command=restart_game)
restart.pack()

#----------------------------------------------------------------------

# window_width = window.winfo_width()
# window_height = window.winfo_height()
window_width = 700
window_height = 796
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(window_width, window_height)
print(screen_width, screen_height)

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
print(x, y)

window.geometry(f'{window_width}x{window_height}+{x}+{y}')
window.bind('<Left>' , lambda event: change_direction('left'))
window.bind('<Right>' , lambda event: change_direction('right') )
window.bind('<Up>' , lambda event: change_direction('up'))
window.bind('<Down>' , lambda event: change_direction('down'))

#----------------------------------------------------------------------
snake = Snake()
food = Food()

next_turn (snake, food)

window.mainloop()
















