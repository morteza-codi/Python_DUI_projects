import tkinter as tk
from tkinter import messagebox, ttk
import time
import random

# Color scheme
BG_COLOR = "#f0f0f0"
GRID_COLOR = "#34495e"
ACCENT_COLOR = "#3498db"
BUTTON_COLOR = "#2ecc71"
BUTTON_HOVER = "#27ae60"
TEXT_COLOR = "#2c3e50"
HIGHLIGHT_COLOR = "#e74c3c"
SOLVED_COLOR = "#2ecc71"
ERROR_COLOR = "#ffebee"


class SudokuGenerator:
    @staticmethod
    def generate_full_board():
        board = [[0] * 9 for _ in range(9)]

        def is_valid(board, row, col, num):
            # Check row
            for i in range(9):
                if board[row][i] == num:
                    return False

            # Check column
            for i in range(9):
                if board[i][col] == num:
                    return False

            # Check 3x3 box
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_row + i][start_col + j] == num:
                        return False
            return True

        def solve_board(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve_board(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        solve_board(board)
        return board

    @staticmethod
    def remove_cells(board, difficulty):
        # Define difficulty levels: Easy (40-45), Medium (46-50), Hard (51-55)
        ranges = {
            "Easy": (40, 45),
            "Medium": (46, 50),
            "Hard": (51, 55)
        }
        min_remove, max_remove = ranges.get(difficulty, (40, 45))
        count = random.randint(min_remove, max_remove)

        removed = 0
        while removed < count:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if board[i][j] != 0:
                board[i][j] = 0
                removed += 1
        return board


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game - By morteza")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("550x700")

        # Game state variables
        self.start_time = None
        self.timer_running = False
        self.hints_remaining = 3
        self.difficulty = "Medium"
        self.errors = 0
        self.completed = False

        # Create main frames
        self.header_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.header_frame.pack(pady=(10, 5))

        self.game_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.game_frame.pack(pady=10)

        self.stats_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.stats_frame.pack(pady=5)

        self.control_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.control_frame.pack(pady=10)

        # Add title
        title_label = tk.Label(
            self.header_frame,
            text="SUDOKU MASTER",
            font=("Arial", 24, "bold"),
            fg=ACCENT_COLOR,
            bg=BG_COLOR
        )
        title_label.pack()

        # Add subtitle with Rachel's name
        subtitle_label = tk.Label(
            self.header_frame,
            text="Created by morteza",
            font=("Arial", 10, "italic"),
            fg=ACCENT_COLOR,
            bg=BG_COLOR
        )
        subtitle_label.pack()

        # Add difficulty selector
        diff_frame = tk.Frame(self.header_frame, bg=BG_COLOR)
        diff_frame.pack(pady=5)

        tk.Label(diff_frame, text="Difficulty:", font=("Arial", 10), bg=BG_COLOR).pack(side=tk.LEFT)

        self.diff_var = tk.StringVar(value=self.difficulty)
        diff_menu = ttk.Combobox(diff_frame, textvariable=self.diff_var,
                                 values=["Easy", "Medium", "Hard"], state="readonly", width=8)
        diff_menu.pack(side=tk.LEFT, padx=5)
        diff_menu.bind("<<ComboboxSelected>>", self.change_difficulty)

        # Initialize game board
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.board = SudokuGenerator.remove_cells(SudokuGenerator.generate_full_board(), self.difficulty)
        self.solution = [[self.board[i][j] for j in range(9)] for i in range(9)]
        # Generate the complete solution
        temp_board = [row[:] for row in self.board]
        self.solve_board(temp_board)
        self.solution = temp_board

        # Create grid frame
        grid_frame = tk.Frame(self.game_frame, bg=GRID_COLOR, padx=5, pady=5)
        grid_frame.pack()

        # Draw the grid
        self.draw_grid(grid_frame)

        # Create stats frame content
        self.timer_label = tk.Label(self.stats_frame, text="Time: 00:00", font=("Arial", 12), bg=BG_COLOR)
        self.timer_label.pack(side=tk.LEFT, padx=20)

        self.hints_label = tk.Label(self.stats_frame, text=f"Hints: {self.hints_remaining}",
                                    font=("Arial", 12), bg=BG_COLOR)
        self.hints_label.pack(side=tk.LEFT, padx=20)

        self.errors_label = tk.Label(self.stats_frame, text=f"Errors: {self.errors}",
                                     font=("Arial", 12), bg=BG_COLOR)
        self.errors_label.pack(side=tk.LEFT, padx=20)

        # Create control buttons
        self.create_buttons()

        # Start the timer
        self.start_timer()

    def draw_grid(self, parent):
        for i in range(9):
            for j in range(9):
                border_width = 3 if i % 3 == 0 and j % 3 == 0 else 1

                cell_frame = tk.Frame(
                    parent,
                    highlightbackground=GRID_COLOR,
                    highlightcolor=GRID_COLOR,
                    highlightthickness=border_width,
                    bg=BG_COLOR
                )
                cell_frame.grid(row=i, column=j, sticky="nsew", padx=0.5, pady=0.5)

                entry = tk.Entry(
                    cell_frame,
                    width=2,
                    font=("Arial", 20, "bold"),
                    justify="center",
                    bg="white",
                    fg=TEXT_COLOR,
                    relief="flat",
                    borderwidth=0
                )
                entry.pack(fill="both", expand=True)

                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(fg=ACCENT_COLOR, state="disabled", disabledbackground="#eaf2f8")
                else:
                    # Bind events for empty cells
                    entry.bind("<FocusIn>", lambda e, i=i, j=j: self.on_entry_focus(i, j))
                    entry.bind("<Key>", self.validate_input)
                    entry.bind("<KeyRelease>", lambda e, i=i, j=j: self.check_cell(i, j))

                self.entries[i][j] = entry

    def on_entry_focus(self, row, col):
        # Highlight related cells
        for i in range(9):
            for j in range(9):
                if self.entries[i][j]['state'] != 'disabled':
                    self.entries[i][j].config(bg="white")

        # Highlight row and column
        for idx in range(9):
            if self.entries[row][idx]['state'] != 'disabled':
                self.entries[row][idx].config(bg="#e8f4f8")
            if self.entries[idx][col]['state'] != 'disabled':
                self.entries[idx][col].config(bg="#e8f4f8")

        # Highlight 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                r, c = start_row + i, start_col + j
                if self.entries[r][c]['state'] != 'disabled':
                    self.entries[r][c].config(bg="#e8f4f8")

        # Highlight the selected cell
        if self.entries[row][col]['state'] != 'disabled':
            self.entries[row][col].config(bg="#d4e6f1")

    def validate_input(self, event):
        # Allow only numbers 1-9 and navigation keys
        if event.char and event.char not in "123456789" and event.keysym not in [
            'BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Tab'
        ]:
            return "break"

    def check_cell(self, row, col):
        # Check if the entered value is correct
        try:
            value = self.entries[row][col].get()
            if value and int(value) != self.solution[row][col]:
                self.entries[row][col].config(bg=ERROR_COLOR)
                self.errors += 1
                self.errors_label.config(text=f"Errors: {self.errors}")
            elif value and int(value) == self.solution[row][col]:
                self.entries[row][col].config(bg="#e8f5e9")  # Light green for correct
        except ValueError:
            pass

        # Check if the game is complete
        if self.is_complete():
            self.complete_game()

    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.entries[i][j].get() == "":
                    return False
                try:
                    if int(self.entries[i][j].get()) != self.solution[i][j]:
                        return False
                except ValueError:
                    return False
        return True

    def complete_game(self):
        self.completed = True
        self.stop_timer()
        messagebox.showinfo("Congratulations!",
                            f"You solved the puzzle in {self.format_time()} with {self.errors} errors!")

    def create_buttons(self):
        button_style = {
            "font": ("Arial", 10, "bold"),
            "width": 12,
            "height": 1,
            "bd": 0,
            "cursor": "hand2"
        }

        solve_btn = tk.Button(
            self.control_frame,
            text="Solve",
            command=self.solve_all,
            bg=BUTTON_COLOR,
            fg="white",
            activebackground=BUTTON_HOVER,
            **button_style
        )
        solve_btn.grid(row=0, column=0, padx=5, pady=5)

        hint_btn = tk.Button(
            self.control_frame,
            text="Hint",
            command=self.provide_hint,
            bg=ACCENT_COLOR,
            fg="white",
            activebackground="#2980b9",
            **button_style
        )
        hint_btn.grid(row=0, column=1, padx=5, pady=5)

        check_btn = tk.Button(
            self.control_frame,
            text="Check Solution",
            command=self.check_solution,
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            **button_style
        )
        check_btn.grid(row=0, column=2, padx=5, pady=5)

        reset_btn = tk.Button(
            self.control_frame,
            text="New Game",
            command=self.reset_board,
            bg=HIGHLIGHT_COLOR,
            fg="white",
            activebackground="#c0392b",
            **button_style
        )
        reset_btn.grid(row=0, column=3, padx=5, pady=5)

        # Add hover effects
        for btn in [solve_btn, hint_btn, check_btn, reset_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=b.cget("activebackground")))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=b.cget("bg")))

    def solve_all(self):
        # Solve the entire board at once
        for i in range(9):
            for j in range(9):
                if self.entries[i][j].get() == "":
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(self.solution[i][j]))
                    self.entries[i][j].config(fg=SOLVED_COLOR, bg="#eafaf1")

        self.completed = True
        self.stop_timer()
        messagebox.showinfo("Puzzle Solved", "The puzzle has been completely solved!")

    def provide_hint(self):
        if self.hints_remaining > 0:
            # Find all empty cells
            empty_cells = []
            for i in range(9):
                for j in range(9):
                    if self.entries[i][j].get() == "":
                        empty_cells.append((i, j))

            if empty_cells:
                # Select a random empty cell
                row, col = random.choice(empty_cells)
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.solution[row][col]))
                self.entries[row][col].config(fg=SOLVED_COLOR, bg="#eafaf1")
                self.hints_remaining -= 1
                self.hints_label.config(text=f"Hints: {self.hints_remaining}")

                # Check if the game is complete after the hint
                if self.is_complete():
                    self.complete_game()
            else:
                messagebox.showinfo("Info", "No empty cells left!")
        else:
            messagebox.showinfo("Info", "No hints remaining!")

    def solve_board(self, board):
        # Helper function to solve the board
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(board, i, j, num):
                            board[i][j] = num
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def is_valid_move(self, board, row, col, num):
        # Check row
        for i in range(9):
            if board[row][i] == num:
                return False

        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def check_solution(self):
        if self.is_complete():
            messagebox.showinfo("Success", "✅ Correct Solution!")
        else:
            # Highlight incorrect cells
            incorrect_cells = []
            for i in range(9):
                for j in range(9):
                    try:
                        value = self.entries[i][j].get()
                        if value and int(value) != self.solution[i][j]:
                            self.entries[i][j].config(bg=ERROR_COLOR)
                            incorrect_cells.append((i, j))
                    except ValueError:
                        self.entries[i][j].config(bg=ERROR_COLOR)
                        incorrect_cells.append((i, j))

            if incorrect_cells:
                messagebox.showerror("Oops!", f"❌ {len(incorrect_cells)} cells are incorrect.")
            else:
                messagebox.showinfo("Almost There", "The solution is not complete yet.")

    def reset_board(self):
        # Reset game state
        self.stop_timer()
        self.difficulty = self.diff_var.get()
        self.board = SudokuGenerator.remove_cells(SudokuGenerator.generate_full_board(), self.difficulty)

        # Regenerate solution
        self.solution = [[self.board[i][j] for j in range(9)] for i in range(9)]
        temp_board = [row[:] for row in self.board]
        self.solve_board(temp_board)
        self.solution = temp_board

        # Reset UI
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal", fg=TEXT_COLOR, bg="white")
                entry.delete(0, tk.END)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(fg=ACCENT_COLOR, state="disabled", disabledbackground="#eaf2f8")
                else:
                    # Rebind events for empty cells
                    entry.bind("<FocusIn>", lambda e, i=i, j=j: self.on_entry_focus(i, j))
                    entry.bind("<Key>", self.validate_input)
                    entry.bind("<KeyRelease>", lambda e, i=i, j=j: self.check_cell(i, j))

        # Reset stats
        self.hints_remaining = 3
        self.errors = 0
        self.completed = False
        self.hints_label.config(text=f"Hints: {self.hints_remaining}")
        self.errors_label.config(text=f"Errors: {self.errors}")

        # Restart timer
        self.start_timer()

    def change_difficulty(self, event):
        self.difficulty = self.diff_var.get()
        self.reset_board()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running and not self.completed:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {self.format_time(elapsed)}")
            self.root.after(1000, self.update_timer)

    def format_time(self, seconds=None):
        if seconds is None:
            seconds = int(time.time() - self.start_time)
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()