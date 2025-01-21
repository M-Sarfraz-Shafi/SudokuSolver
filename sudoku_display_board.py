import tkinter as tk

class SudokuDisplayBoard:
    def __init__(self, root, rows, columns, solver):
        self.root = root
        self.rows = rows
        self.cols = columns
        self.solver = solver

        # Create sudoku display board
        self.create_board()

    # Create a sudoku cell (entry) 
    def create_entry(self, parent):
        def validate_input(self, event):
            entry = event.widget
            value = entry.get()
            if not value.isdigit() or not (1 <= int(value) <= 9):
                entry.delete(0, tk.END)
        entry = tk.Entry(parent, width=2, justify='center', font=('Arial', 18))
        entry.bind('<KeyRelease>', validate_input)
        return entry

    def create_board(self):
        self.root.title("Sudoku Solver")
        grid_frame = tk.Frame(self.root)
        grid_frame.grid(row=0, column=0, padx=10, pady=10)

        self.entries = [[self.create_entry(grid_frame) for _ in range(self.cols)] for _ in range(self.rows)]  
        for row in range(self.rows):
            for col in range(self.cols):
                self.entries[row][col].grid(row=row, column=col, padx=2, pady=2)

        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=10, column=0, pady=10)

        initialize_button = tk.Button(button_frame, text="Initialize Grid", command=self.solver.initialize_grid, font=('Arial', 12))
        initialize_button.grid(row=0, column=0, padx=5)

        solve_button = tk.Button(button_frame, text="Solve", command=self.solver.start_solving, font=('Arial', 12))
        solve_button.grid(row=0, column=1, padx=5)


    def update_board(self, board):
        for row in range(self.rows):
            for col in range(self.cols):
                value = board[row][col]
                self.entries[row][col].delete(0, tk.END)
                if value != 0:
                    self.entries[row][col].insert(0, str(value))
                    self.entries[row][col].config(state='disabled')