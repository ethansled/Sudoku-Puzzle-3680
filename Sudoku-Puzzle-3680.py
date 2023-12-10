#Ethan Sledzinski
#esledzinski@oakland.edu
#Sudoku puzzle game using backtracking for solution and checks


import tkinter as tk
from tkinter import messagebox
import random
import time
import sys

class SudokuGame:
    def __init__(self):
        #redirect stdout to a file
        sys.stdout = open('game_results.txt', 'w')

        #initialize the sudok object
        self.root = tk.Tk()
        self.root.title("Sudoku-Puzzle-3680")
        self.attempts = 0
        self.correct_moves = []
        self.current_cell = None
        self.grid = self.generate_sudoku()
        solved_board = self.solve_sudoku([row[:] for row in self.grid])
        self.solution = [row[:] for row in solved_board]
        self.solution2 = [row[:] for row in solved_board]
        self.start_time = time.time()
        self.create_gui()

    def generate_sudoku(self):
        #generate a sudoku puzzle game
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = int(squares * 0.5)
        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = 0

        return board

    def create_gui(self):
        #creates the main frame of the gui
        self.main_frame = tk.Frame(self.root, bg="light green")
        self.main_frame.grid(padx=10, pady=10)

        #creates the grid of cells for the sudoku puzzle
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.grid[i][j]
                self.cells[i][j] = tk.Entry(
                    self.main_frame,
                    width=3,
                    font=("Helvetica", 16),
                    justify="center",
                    bg="light green",
                )
                if value != 0:
                    #if the cell has a prefilled value, insert and disabl it
                    self.cells[i][j].insert(0, str(value))
                    self.cells[i][j].config(state="disabled")

                self.cells[i][j].grid(row=i, column=j, padx=1, pady=1)
                self.cells[i][j].bind("<FocusIn>", lambda event, i=i, j=j: self.cell_focus_in(i, j))

        #creates the label displaying the number of moves made
        self.attempts_label = tk.Label(self.main_frame, text="Moves Made: 0", bg="light green")
        self.attempts_label.grid(row=10, column=0, pady=5, columnspan=9)

        #create the clock label
        self.clock_label = tk.Label(self.main_frame, text="Time: 00:00", bg="light green")
        self.clock_label.grid(row=11, column=0, pady=5, columnspan=9)

        #creates the check, solve, and end Game buttons on the right side
        btn_check = tk.Button(
            self.main_frame, text="Check", command=self.check_cell, bg="light green"
        )
        btn_check.grid(row=0, column=10, pady=5, padx=5, sticky="ew")

        btn_solve = tk.Button(
            self.main_frame, text="Solve Board", command=self.solve_game, bg="light green"
        )
        btn_solve.grid(row=1, column=10, pady=5, padx=5, sticky="ew")

        btn_end = tk.Button(
            self.main_frame, text="End Game", command=self.root.destroy, bg="light green"
        )
        btn_end.grid(row=2, column=10, pady=5, padx=5, sticky="ew")

        #sets up a timer to update the clock every second
        self.root.after(1000, self.update_clock)

        #call update clock at the end of create gui
        self.update_clock()

        self.root.mainloop()

    def cell_focus_in(self, i, j):
        #callback function for when a cell gains focus
        self.current_cell = (i, j)

    def check_cell(self):
        #check the users input for correctness
        if self.current_cell is not None:
            i, j = self.current_cell
            self.attempts += 1
            self.attempts_label.config(text=f"Moves Made: {self.attempts}")

            user_value_str = self.cells[i][j].get()
            if user_value_str.isdigit():
                user_value = int(user_value_str)
                correct_value = self.solution2[i][j]

                print(f"Checking Cell ({i+1}, {j+1}): User Value: {user_value}, Correct Value: {correct_value}")

                if user_value == correct_value:
                    #display correct message and update cell appearance
                    messagebox.showinfo("Correct", "Correct value!")
                    self.cells[i][j].config(disabledbackground="white", disabledforeground="black")
                    self.cells[i][j].config(state="disabled")

                    #save correct move to the list
                    self.correct_moves.append((i+1, j+1, user_value))

                    #check if the entire board is filled and correct
                    if self.is_board_filled_and_correct():
                        self.handle_game_completion()
                else:
                    #display incorrect message and provide debug output
                    messagebox.showwarning("Incorrect", "Incorrect value. Try again!")

                    #debugging output
                    print(f"user_value: {user_value}, correct_value: {correct_value}")
            else:
                #display a warning for invalid input
                messagebox.showwarning("Invalid Input", "Please enter a valid digit.")

        else:
            #display a warning if no cell is selected
            messagebox.showwarning("Cell Not Selected", "Please click on a cell before checking.")

    def handle_game_completion(self):
        #display a congratulatory message and write correct moves to the file
        messagebox.showinfo("Congratulations!", "You solved the puzzle!")

        #write correct moves to the file
        with open("game_results.txt", "w") as file:
            for move in self.correct_moves:
                file.write(f"Move: {move[0]}, {move[1]} - Correct Value: {move[2]}\n")

    def solve_game(self):
        #solve the entire Sudoku puzzle
        solved_board = self.solve_sudoku([row[:] for row in self.grid])

        if solved_board:
            #update the solution and display it in the GUI
            self.solution = [row[:] for row in solved_board]

            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(solved_board[i][j]))
                    self.cells[i][j].config(disabledbackground="white", disabledforeground="black")
                    self.cells[i][j].config(state="disabled")

            #after solving, check the solution
            self.check_solution()
        else:
            #display a message if no solution exists
            messagebox.showinfo("No Solution", "No solution exists for the current board.")

    def check_solution(self):
        #check the user's solution for correctness
        user_solution = [[0 for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].get()
                if value.isdigit():
                    user_solution[i][j] = int(value)
                else:
                    user_solution[i][j] = 0

        if user_solution == self.solution:
            #display a congratulatory message if the solution is correct
            messagebox.showinfo("Congratulations!", "You solved the puzzle!")
        else:
            #display a warning if some cells are incorrect
            messagebox.showwarning("Incorrect", "Some cells are incorrect. Keep trying!")

    def solve_sudoku(self, board):
        #solve the sudoku puzzle using backtracking
        empty = self.find_empty(board)
        if not empty:
            return board

        row, col = empty

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return board 
                board[row][col] = 0  #if placing the number didn't lead to a solution, backtrack
        return None  #no solution found

    def find_empty(self, board):
        #find an empty cell in the Sudoku puzzle
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, board, row, col, num):
        #check if it's safe to place the number in the given position
        if (
            num not in board[row]
            and num not in (board[i][col] for i in range(9))
            and num not in (
                board[i][j]
                for i in range(row - row % 3, row - row % 3 + 3)
                for j in range(col - col % 3, col - col % 3 + 3)
            )
        ):
            return True

        return False

    def is_board_filled_and_correct(self):
        #check if the entire board is filled and correct
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].get() == "" or int(self.cells[i][j].get()) != self.solution2[i][j]:
                    return False
        return True

    def update_clock(self):
        #update the clock label with the elapsed time
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        self.clock_label.config(text=time_str)

        #schedule the function update clock to run again after 1 second
        self.root.after(1000, self.update_clock)

    def handle_game_completion(self):
        #display a congratulatory message and write correct moves to the file
        messagebox.showinfo("Congratulations!", "You solved the puzzle!")

        #write correct moves to the file
        with open("game_results.txt", "w") as file:
            for move in self.correct_moves:
                file.write(f"Move: {move[0]}, {move[1]} - Correct Value: {move[2]}\n")

if __name__ == "__main__":
    SudokuGame()
