def print_board(board: list[list]) -> None:
    for i in board:
        print('[' + ' '.join([str(j) if j != 0 else ' ' for j in i]), end=']\n', )


def find_empty_location(board: list[list], l: list):
    for i in range(9):
        for j in range(9):
            if (board[i][j] == 0):
                l[0] = i
                l[1] = j
                return True
    return False


def used_in_row(board: list[list], row: int, num: int) -> bool:
    return num in board[row]


def used_in_col(board: list[list], col: int, num: int) -> bool:
    return num in [board[i][col] for i in range(9)]


def used_in_box(board: list[list], row: int, col: int, num: int) -> bool:
    for i in range(3):
        for j in range(3):
            if board[i + row][j + col] == num:
                return True
    return False


def is_location_safe(board: list[list], row: int, col: int, num: int) -> bool:
    return (not used_in_row(board, row, num)
            and not used_in_col(board, col, num)
            and not used_in_box(board, row - row % 3, col - col % 3, num))


def solve_sudoku(board: list[list]):
    first_empty_location = [0, 0]

    if not find_empty_location(board, first_empty_location):
        return True

    i, j = first_empty_location

    for n in range(1, 10):
        if is_location_safe(board, i, j, n):
            board[i][j] = n

            if solve_sudoku(board):
                return True

            board[i][j] = 0

    return False


board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]]


print_board(board)

solve_sudoku(board)

print()
print_board(board)
