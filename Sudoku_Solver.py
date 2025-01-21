import tkinter as tk
import numpy as np
from sudoku_display_board import SudokuDisplayBoard


class SudokuSolver:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns

        # Initialize Sudoku Game (board)
        self.board = np.zeros((rows, columns), dtype=int)

        # Initialize hints for each cell 
        self.hints = [[set(range(1, 10)) for _ in range(columns)] for _ in range(rows)]
        
        # Sudoku Display Board
        root = tk.Tk()
        self.gui = SudokuDisplayBoard(root, rows, columns, self)
        root.mainloop()

    # Initialize Game
    def initialize_grid(self):
        initial_values = [
            [0, 0, 0, 5, 4, 9, 2, 6, 7],
            [0, 0, 9, 8, 0, 6, 0, 4, 3],
            [6, 4, 2, 0, 3, 7, 8, 0, 9],
            [0, 8, 0, 0, 0, 4, 7, 0, 6],
            [3, 9, 6, 7, 8, 2, 0, 0, 0],
            [0, 7, 4, 9, 6, 1, 3, 0, 0],
            [4, 1, 7, 0, 9, 0, 6, 3, 8],
            [0, 0, 5, 0, 7, 3, 9, 0, 0],
            [0, 2, 0, 6, 1, 0, 0, 7, 5]
        ]
        self.board = np.array(initial_values)
        
        # Update hints with respect to sudoku initialized value 
        self.update_hints()

        # Update display board
        self.gui.update_board(initial_values)

    # Update Hints
    def update_hints(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
            
                    # Remove hints of current cell as there is hard value
                    self.hints[row][col] = set()
                    self.remove_hint(row, col, self.board[row][col])

    def remove_hint(self, row, col, num):
        # Remove hints from row and col
        for i in range(9):
            self.hints[row][i].discard(num)
            self.hints[i][col].discard(num)

        # Remove hints from sub-grids
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                self.hints[r][c].discard(num)

    # Algorithm Starts to Solve 
    def start_solving(self):
        while True:
            progress = self.obvious_singles()
            if not progress:
                break
        self.gui.update_board(self.board.tolist())

    def obvious_singles(self):
        progress = False
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0 and len(self.hints[row][col]) == 1:
                    
                    # Use iterator to get the num from hints
                    num = next(iter(self.hints[row][col]))
                    self.board[row][col] = num
                    self.hints[row][col] = set()
                    self.remove_hint(row, col, num)
                    progress = True
        return progress

if __name__ == "__main__":
    rows = 9
    columns = 9
    SudokuSolver(rows, columns)
