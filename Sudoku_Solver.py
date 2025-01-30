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
        # initial_values = [
        #     [0, 0, 0, 5, 4, 9, 2, 6, 7],
        #     [0, 0, 9, 8, 0, 6, 0, 4, 3],
        #     [6, 4, 2, 0, 3, 7, 8, 0, 9],
        #     [0, 8, 0, 0, 0, 4, 7, 0, 6],
        #     [3, 9, 6, 7, 8, 2, 0, 0, 0],
        #     [0, 7, 4, 9, 6, 1, 3, 0, 0],
        #     [4, 1, 7, 0, 9, 0, 6, 3, 8],
        #     [0, 0, 5, 0, 7, 3, 9, 0, 0],
        #     [0, 2, 0, 6, 1, 0, 0, 7, 5]
        # ]

        initial_values = [
            [0, 6, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 9, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 6, 0, 0, 2, 0, 0],
            [7, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 3, 5],
            [4, 0, 0, 0, 0, 7, 0, 6, 0],
            [0, 0, 0, 0, 9, 0, 0, 0, 0]
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
            progress1 = self.last_possible_number()
            self.gui.update_board(self.board.tolist())
            
            
            progress2 = self.obvious_singles()
            self.gui.update_board(self.board.tolist())
            
            if not progress1 and not progress2:
                break

    def obvious_singles(self):
        
        progress = False
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0 and len(self.hints[row][col]) == 1:
                    
                    # Use iterator to get the num from hints
                    num = next(iter(self.hints[row][col]))
                    self.setvalue(row, col, num)
                    progress = True
        return progress
   
    def setvalue(self, row, col, num):
        self.board[row][col] = num
        self.hints[row][col] = set()
        self.remove_hint(row, col, num)
                    
    def last_remaining_cell(self):
        """
        Check if there is any value that exits only in one cell in either row or column or in sub-grid 
        """
        progress = False

        n_hints = self.rows + 1
        
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

    def last_possible_number(self):
        unique_hints = self.find_unique_hints()

        if unique_hints:
            for row, col, value in unique_hints:
                self.setvalue(row, col, value)

            return True
        else:
            return False


        
        
    def find_unique_hints(self):
        row_counts, col_counts, box_counts = self.compute_hint_counts()

        unique_hints = []  # Store (row, col, value) for unique hints

        # Check rows for unique hints
        for row in range(self.rows):
            for hint, count in row_counts[row].items():
                if count == 1:  # If a hint appears only once in the row
                    
                    # Find the column where this hint exists
                    for col in range(self.cols):
                        if self.board[row][col] == 0 and hint in self.hints[row][col]:
                            unique_hints.append((row, col, hint))
                            break  # Only one occurrence, no need to check further

        # Check columns for unique hints
        for col in range(self.cols):
            for hint, count in col_counts[col].items():
                if count == 1:  # If a hint appears only once in the column
                    # Find the row where this hint exists
                    for row in range(self.rows):
                        if self.board[row][col] == 0 and hint in self.hints[row][col]:
                            unique_hints.append((row, col, hint))
                            break

        # Check boxes for unique hints
        for box_row in range(3):
            for box_col in range(3):
                for hint, count in box_counts[box_row][box_col].items():
                    if count == 1:  # If a hint appears only once in the box
                        # Find the exact cell where this hint exists
                        for r in range(box_row * 3, box_row * 3 + 3):
                            for c in range(box_col * 3, box_col * 3 + 3):
                                if self.board[r][c] == 0 and hint in self.hints[r][c]:
                                    unique_hints.append((r, c, hint))
                                    break
                            else:
                                continue
                            break

        return unique_hints 


    def compute_hint_counts(self):
        # Initialize hint counts for rows, columns, and boxes
        row_hint_counts = [{i: 0 for i in range(1, 10)} for _ in range(self.rows)]
        col_hint_counts = [{i: 0 for i in range(1, 10)} for _ in range(self.cols)]
        box_hint_counts = [[{i: 0 for i in range(1, 10)} for _ in range(3)] for _ in range(3)]

        # Iterate through the board and count hints
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:  # Only consider unsolved cells
                    for hint in self.hints[row][col]:
                        row_hint_counts[row][hint] += 1
                        col_hint_counts[col][hint] += 1
                        box_row, box_col = row // 3, col // 3
                        box_hint_counts[box_row][box_col][hint] += 1

        return row_hint_counts, col_hint_counts, box_hint_counts


if __name__ == "__main__":
    rows = 9
    columns = 9
    SudokuSolver(rows, columns)
