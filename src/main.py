from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def parse_sudoku(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    sudoku = [[int(num) if num != '-' else 0 for num in line.strip().split()] for line in lines]
    return sudoku

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    sudoku = None
    solution = None
    if request.method == 'POST':
        file = request.files['sudoku_file']
        if file and file.filename.endswith('.txt'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            sudoku = parse_sudoku(file_path)

            solution = [row[:] for row in sudoku]
            if solve_sudoku(solution):
                print(solution)
            else:
                solution = "Could not solve sudoku."

    return render_template('home.html', sudoku=sudoku, solution=solution)

if __name__ == '__main__':
    app.run(debug=True)
