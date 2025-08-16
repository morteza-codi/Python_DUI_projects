from tkinter import *
import math
from tkinter import font as tkfont
from tkinter import scrolledtext

# Create main window
var = Tk()
var.title("Advanced Calculator")
var.geometry("800x600")
var.configure(bg='#2c3e50')  # Background color

# Font settings
title_font = tkfont.Font(family='Helvetica', size=18, weight='bold')
button_font = tkfont.Font(family='Arial', size=12, weight='bold')
entry_font = tkfont.Font(family='Courier New', size=18, weight='bold')
history_font = tkfont.Font(family='Courier New', size=12)

# Colors
bg_color = '#2c3e50'
entry_bg = '#34495e'
entry_fg = '#ecf0f1'
num_button_bg = '#7f8c8d'
num_button_fg = '#2c3e50'
op_button_bg = '#3498db'
op_button_fg = 'white'
func_button_bg = '#9b59b6'
func_button_fg = 'white'
clear_button_bg = '#e74c3c'
clear_button_fg = 'white'
equal_button_bg = '#2ecc71'
equal_button_fg = 'white'

# Create frame for display
display_frame = Frame(var, bg=bg_color)
display_frame.pack(pady=10)

# History display (scrolled text)
history_text = scrolledtext.ScrolledText(display_frame, width=40, height=4,
                                         font=history_font, bg=entry_bg, fg='#95a5a6',
                                         wrap=WORD, state='disabled')
history_text.pack()

# Current entry display
e = Entry(display_frame, width=40, font=entry_font, borderwidth=0,
          bg=entry_bg, fg=entry_fg, justify='right', insertbackground='white')
e.pack(ipady=10, ipadx=10)

# Create frame for buttons
button_frame = Frame(var, bg=bg_color)
button_frame.pack()


# Function to create consistent buttons
def create_button(parent, text, row, col, command, bg=num_button_bg, fg='white',
                  width=5, colspan=1, rowspan=1):
    btn = Button(parent, text=text, padx=10, pady=10, font=button_font,
                 bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                 command=command, borderwidth=0, highlightthickness=0)
    btn.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,
             sticky="nsew", padx=5, pady=5)
    return btn


# Function to update history
def update_history(operation_text):
    history_text.configure(state='normal')
    history_text.insert(END, operation_text + "\n")
    history_text.configure(state='disabled')
    history_text.see(END)  # Auto-scroll to bottom


# Backend Functions
def button_click(num):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(num))


def clear():
    e.delete(0, END)


def add():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        global operation_text
        operation = "addition"
        functionnum = float(num1)
        operation_text = f"{num1} + "
        e.delete(0, END)
        update_history(operation_text)


def equals():
    num2 = e.get()
    if num2 and 'operation' in globals():
        e.delete(0, END)
        try:
            result = 0
            if operation == "addition":
                result = functionnum + float(num2)
                full_op = f"{operation_text}{num2} = {result}"
            elif operation == "subtraction":
                result = functionnum - float(num2)
                full_op = f"{operation_text}{num2} = {result}"
            elif operation == "multiplication":
                result = functionnum * float(num2)
                full_op = f"{operation_text}{num2} = {result}"
            elif operation == "division":
                result = functionnum / float(num2)
                full_op = f"{operation_text}{num2} = {result}"
            elif operation == "power":
                result = functionnum ** float(num2)
                full_op = f"{operation_text}{num2} = {result}"
            elif operation == "sqrt":
                result = math.sqrt(functionnum)
                full_op = f"√({functionnum}) = {result}"
            elif operation == "percentage":
                result = functionnum / 100
                full_op = f"{functionnum}% = {result}"
            elif operation == "sin":
                rad = functionnum * (math.pi / 180)
                result = math.sin(rad)
                full_op = f"sin({functionnum}°) = {result}"
            elif operation == "cos":
                rad = functionnum * (math.pi / 180)
                result = math.cos(rad)
                full_op = f"cos({functionnum}°) = {result}"
            elif operation == "tan":
                rad = functionnum * (math.pi / 180)
                result = math.tan(rad)
                full_op = f"tan({functionnum}°) = {result}"
            elif operation == "csc":
                rad = functionnum * (math.pi / 180)
                result = 1 / math.sin((rad))
                full_op = f"csc({functionnum}°) = {result}"
            elif operation == "sec":
                rad = functionnum * (math.pi / 180)
                result = 1 / math.cos((rad))
                full_op = f"sec({functionnum}°) = {result}"
            elif operation == "cot":
                rad = functionnum * (math.pi / 180)
                result = 1 / math.tan((rad))
                full_op = f"cot({functionnum}°) = {result}"
            elif operation == "average":
                result = (functionnum + float(num2)) / 2
                full_op = f"avg({functionnum}, {num2}) = {result}"
            elif operation == "square":
                result = functionnum ** 2
                full_op = f"{functionnum}² = {result}"
            elif operation == "cube":
                result = functionnum ** 3
                full_op = f"{functionnum}³ = {result}"
            elif operation == "ln":
                result = math.log(functionnum)
                full_op = f"ln({functionnum}) = {result}"
            elif operation == "exp":
                result = math.exp(functionnum)
                full_op = f"e^{functionnum} = {result}"
            elif operation == "log10":
                result = math.log10(functionnum)
                full_op = f"log10({functionnum}) = {result}"
            elif operation == "negate":
                result = functionnum * -1
                full_op = f"-({functionnum}) = {result}"
            elif operation == "abs":
                result = abs(functionnum)
                full_op = f"|{functionnum}| = {result}"
            elif operation == "factorial":
                result = math.factorial(int(functionnum))
                full_op = f"{functionnum}! = {result}"
            elif operation == "pow2":
                result = 2 ** functionnum
                full_op = f"2^{functionnum} = {result}"
            elif operation == "inverse":
                result = functionnum ** (-1)
                full_op = f"1/({functionnum}) = {result}"
            elif operation == "asin":
                rad = functionnum * (math.pi / 180)
                result = math.asin(rad)
                full_op = f"sin⁻¹({functionnum}°) = {result}"
            elif operation == "acos":
                rad = functionnum * (math.pi / 180)
                result = math.acos(rad)
                full_op = f"cos⁻¹({functionnum}°) = {result}"
            elif operation == "atan":
                rad = functionnum * (math.pi / 180)
                result = math.atan(rad)
                full_op = f"tan⁻¹({functionnum}°) = {result}"

            e.insert(0, str(result))
            update_history(full_op)

        except Exception as ex:
            e.insert(0, "Error")
            update_history(f"Error in operation: {str(ex)}")


# Other operation functions (modified to include operation_text)
def subtract():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        global operation_text
        operation = "subtraction"
        functionnum = float(num1)
        operation_text = f"{num1} - "
        e.delete(0, END)
        update_history(operation_text)


def multiply():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        global operation_text
        operation = "multiplication"
        functionnum = float(num1)
        operation_text = f"{num1} × "
        e.delete(0, END)
        update_history(operation_text)


def divide():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        global operation_text
        operation = "division"
        functionnum = float(num1)
        operation_text = f"{num1} ÷ "
        e.delete(0, END)
        update_history(operation_text)


def power():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        global operation_text
        operation = "power"
        functionnum = float(num1)
        operation_text = f"{num1} ^ "
        e.delete(0, END)
        update_history(operation_text)


def sqrt():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "sqrt"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def percent():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "percentage"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def sin():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "sin"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def cos():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "cos"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def tan():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "tan"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def csc():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "csc"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def sec():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "sec"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def cot():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "cot"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def avg():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        global operation_text
        operation = "average"
        functionnum = float(num1)
        operation_text = f"avg({num1}, "
        e.delete(0, END)
        update_history(operation_text)


def square():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "square"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def cube():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "cube"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def natural_log():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "ln"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def exp():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "exp"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def log10():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "log10"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def negate():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "negate"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def absolute():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "abs"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def factorial():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "factorial"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def power2():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "pow2"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def reciprocal():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "inverse"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def asin():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "asin"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def acos():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "acos"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


def atan():
    num1 = e.get()
    if num1:
        global functionnum
        global operation
        functionnum = float(num1)
        operation = "atan"
        e.delete(0, END)
        equals()  # Calculate immediately for unary operations


# Frontend - Create buttons with new appearance
# Row 1
create_button(button_frame, "sin", 1, 0, sin, func_button_bg)
create_button(button_frame, "cos", 1, 1, cos, func_button_bg)
create_button(button_frame, "tan", 1, 2, tan, func_button_bg)
create_button(button_frame, "π", 1, 3, lambda: button_click(math.pi), func_button_bg)
create_button(button_frame, "C", 1, 4, clear, clear_button_bg)

# Row 2
create_button(button_frame, "sin⁻¹", 2, 0, asin, func_button_bg)
create_button(button_frame, "cos⁻¹", 2, 1, acos, func_button_bg)
create_button(button_frame, "tan⁻¹", 2, 2, atan, func_button_bg)
create_button(button_frame, "x²", 2, 3, square, func_button_bg)
create_button(button_frame, "x³", 2, 4, cube, func_button_bg)

# Row 3
create_button(button_frame, "√", 3, 0, sqrt, func_button_bg)
create_button(button_frame, "x^y", 3, 1, power, func_button_bg)
create_button(button_frame, "log", 3, 2, log10, func_button_bg)
create_button(button_frame, "ln", 3, 3, natural_log, func_button_bg)
create_button(button_frame, "e^x", 3, 4, exp, func_button_bg)

# Row 4
create_button(button_frame, "7", 4, 0, lambda: button_click(7), num_button_bg)
create_button(button_frame, "8", 4, 1, lambda: button_click(8), num_button_bg)
create_button(button_frame, "9", 4, 2, lambda: button_click(9), num_button_bg)
create_button(button_frame, "/", 4, 3, divide, op_button_bg)
create_button(button_frame, "!", 4, 4, factorial, func_button_bg)

# Row 5
create_button(button_frame, "4", 5, 0, lambda: button_click(4), num_button_bg)
create_button(button_frame, "5", 5, 1, lambda: button_click(5), num_button_bg)
create_button(button_frame, "6", 5, 2, lambda: button_click(6), num_button_bg)
create_button(button_frame, "×", 5, 3, multiply, op_button_bg)
create_button(button_frame, "|x|", 5, 4, absolute, func_button_bg)

# Row 6
create_button(button_frame, "1", 6, 0, lambda: button_click(1), num_button_bg)
create_button(button_frame, "2", 6, 1, lambda: button_click(2), num_button_bg)
create_button(button_frame, "3", 6, 2, lambda: button_click(3), num_button_bg)
create_button(button_frame, "-", 6, 3, subtract, op_button_bg)
create_button(button_frame, "(-)", 6, 4, negate, func_button_bg)

# Row 7
create_button(button_frame, "0", 7, 0, lambda: button_click(0), num_button_bg, colspan=2)
create_button(button_frame, ".", 7, 2, lambda: button_click('.'), num_button_bg)
create_button(button_frame, "+", 7, 3, add, op_button_bg)
create_button(button_frame, "=", 7, 4, equals, equal_button_bg, rowspan=2)

# Row 8
create_button(button_frame, "avg", 8, 0, avg, func_button_bg)
create_button(button_frame, "%", 8, 1, percent, func_button_bg)
create_button(button_frame, "2^x", 8, 2, power2, func_button_bg)
create_button(button_frame, "1/x", 8, 3, reciprocal, func_button_bg)

# Set button sizes
for i in range(9):
    button_frame.grid_rowconfigure(i, weight=1)
for i in range(5):
    button_frame.grid_columnconfigure(i, weight=1)

var.mainloop()