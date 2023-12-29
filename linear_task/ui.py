import tkinter as tk
from tkinter import ttk, simpledialog, scrolledtext

class MatrixSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("Matrix Solver")
        self.create_widgets()

    def create_widgets(self):
        # Style for ttk widgets
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Arial', 12))

        # Frame to hold the input elements
        input_frame = ttk.Frame(self.master, padding=(10, 10))
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Number of Rows Entry
        self.rows_label = ttk.Label(input_frame, text="Enter the number of rows:")
        self.rows_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.rows_entry = ttk.Entry(input_frame)
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Number of Columns Entry
        self.columns_label = ttk.Label(input_frame, text="Enter the number of columns:")
        self.columns_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.columns_entry = ttk.Entry(input_frame)
        self.columns_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Solve Button
        self.solve_button = ttk.Button(input_frame, text="Solve Matrix", command=self.solve_matrix)
        self.solve_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame to hold the output
        output_frame = ttk.Frame(self.master, padding=(10, 10))
        output_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Output Text
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, width=50, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configure weight to make frames expand with window resizing
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)

    def create_matrix(self, rows, columns):
        matrix = []

        for i in range(rows):
            row_values = []
            for j in range(columns):
                value = simpledialog.askfloat(f"Enter value for row {i + 1}, column {j + 1}", "Enter a number")
                row_values.append(value)

            matrix.append(row_values)

        return matrix

    def solve_matrix(self):
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        rows = int(self.rows_entry.get())
        columns = int(self.columns_entry.get())

        if rows <= 0 or columns <= 0:
            self.print_to_output("Invalid input. Please enter valid numbers for rows and columns.")
            return

        matrix = self.create_matrix(rows, columns)

        self.print_to_output('The matrix is:')
        self.print_matrix(matrix)

        self.print_to_output('The matrix in reduced row echelon form is:')
        reduced_matrix = self.gauss_jordan(matrix)
        self.print_matrix(reduced_matrix)

        self.print_to_output('The solutions are:')
        self.print_solutions(reduced_matrix)

    def print_to_output(self, text):
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.see(tk.END)  # Scroll to the end

    def print_matrix(self, matrix):
        for i in range(len(matrix)):
            self.print_to_output(str(matrix[i]))

    def search_for_non_zero_column(self, matrix, row, current_column):
        for j in range(current_column, len(matrix[0])):
            if matrix[row][j] != 0:
                return j
        return -1

    def find_factor(self, n):
        try:
            return 1/n
        except ZeroDivisionError:
            return 1

    def swap_rows(self, matrix, row1, row2):
        if 0 <= row1 < len(matrix) and 0 <= row2 < len(matrix) and row1 != row2:
            self.print_to_output(f'Swapping row {row1} with row {row2}')
            self.print_matrix(matrix)
            matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
        return matrix

    def multiply_row(self, matrix, row, factor):
        self.print_to_output(f'Multiplying row {row} by {factor}')
        self.print_matrix(matrix)
        for i in range(len(matrix[0])):
            matrix[row][i] *= factor
        return matrix

    def add_row(self, matrix, row1, row2, factor):
        self.print_to_output(f'Adding {factor} times row {row2} to row {row1}')
        self.print_matrix(matrix)
        for i in range(len(matrix[0])):
            matrix[row1][i] += factor * matrix[row2][i]
        return matrix

    def gauss_jordan(self, matrix):
        for i in range(len(matrix)):
            # Search for non-zero coefficient in column j, starting from row i:
            j = self.search_for_non_zero_column(matrix, i, i)
            if j == -1:
                continue
            # Swap rows i and j:
            matrix = self.swap_rows(matrix, i, j)
            # Multiply row i by 1/matrix[i][i] to make matrix[i][i] equal to 1:
            matrix = self.multiply_row(matrix, i, self.find_factor(matrix[i][i]))
            # Subtract from each other row (different from i) row i multiplied by matrix[k][i], 
            # with k ranging from 0 to r:
            for k in range(len(matrix)):
                if k == i or matrix[k][i] == 0:
                    continue
                matrix = self.add_row(matrix, k, i, -matrix[k][i])
        return matrix

    def check_last_column(self, matrix):
        last_row = matrix[-1]
        all_zeros = all(element == 0 for element in last_row)
        if all_zeros:
            return True
        return False

    def check_no_solution(self, matrix):
        last_row = matrix[-1]
        all_zeros_except_last = all(element == 0 for element in last_row[:-1]) and last_row[-1] != 0
        if all_zeros_except_last:
            return True
        return False

    def print_solutions(self, matrix):
        if self.check_last_column(matrix):
            self.print_to_output('There are infinitely many solutions')
        elif self.check_no_solution(matrix):
            self.print_to_output('There are no solutions')
        else:
            for row in matrix:
                self.print_to_output(f'{row[-1]}')

root = tk.Tk()
my_gui = MatrixSolverApp(root)
root.mainloop()

