import numpy as np

r = int(input('Enter the number of rows: '))

if(r<=0):
    print("Invalid input")
    r=int(input('Enter valid number of rows: '))

c = int(input('Enter the number of columns: '))

if(c<=0):
    print("Invalid input")
    c=int(input('Enter valid number of columns: '))

matrix = []


def create_matrix():
    for i in range(r):
        a = input(f"Enter space-separated values for row {i + 1}: ").split()
        a = [int(x) for x in a]  # Convert the input values to integers
        matrix.append(a)
    return matrix

def search_for_non_zero_column(matrix, row, current_column):
    for j in range(current_column, c):
        if matrix[row][j] != 0:
            return j
    return -1

def find_factor(n):
    try:
        return 1/n
    except: 
        return 1

def swap_rows(matrix, row1, row2):
    if 0 <= row1 < len(matrix) and 0 <= row2 < len(matrix) and row1 != row2:
        print(f'Swapping row {row1} with row {row2}')
        print_matrix(matrix)
        matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return matrix

def multiply_row(matrix, row, factor):
    print(f'Multiplying row {row} by {factor}')
    print_matrix(matrix)
    for i in range(c):
        matrix[row][i] *= factor
    return matrix

def add_row(matrix, row1, row2, factor):
    print(f'Adding {factor} times row {row2} to row {row1}')
    print_matrix(matrix)
    for i in range(c):
        matrix[row1][i] += factor * matrix[row2][i]
    return matrix

def print_matrix(matrix):
    for i in range(r):
        print(matrix[i])

def gauss_jordan(matrix):
    for i in range(r):
        # Search for non-zero coefficient in column j, starting from row i:
        j = search_for_non_zero_column(matrix, i, i)
        if j == -1:
            continue
        # Swap rows i and j:
        matrix = swap_rows(matrix, i, j)
        # Multiply row i by 1/matrix[i][i] to make matrix[i][i] equal to 1:
        matrix = multiply_row(matrix, i, find_factor(matrix[i][i]))
        # Subtract from each other row (different from i) row i multiplied by matrix[k][i], 
        # with k ranging from 0 to r:
        for k in range(r):
            if k == i or matrix[k][i] == 0:
                continue
            matrix = add_row(matrix, k, i, -matrix[k][i])
    return matrix

def check_last_column(matrix):
    last_row = matrix[-1]
    all_zeros = all(element == 0 for element in last_row)
    if all_zeros:
        return True
    return False


def check_no_solution(matrix):
    last_row = matrix[-1]
    all_zeros_except_last = all(element == 0 for element in last_row[:-1]) and last_row[-1] != 0
    if all_zeros_except_last:
        return True
    return False

def print_solutions(matrix):
    x=0
    if check_last_column(matrix):
        print('The system has infinite solutions')
        return
    elif check_no_solution(matrix):
        print('The system has no solution,the system is inconsistent')
        return
    else:
        for i in range(r):
            print(f'x{i} = {round(matrix[i][-1],2)}')
            x+=1
        if x<c:
            while x<c:
                print(f'x{x} is a free variable')
                x+=1
            print('\n')

if __name__ == '__main__':
    print('Enter the values for the matrix:')
    matrix = create_matrix()
    print('The matrix is:')
    print_matrix(matrix)
    print('The matrix in reduced row echelon form is:')
    print_matrix(gauss_jordan(matrix))
    print('The solutions are:')
    print_solutions(matrix)



