# http://blog.gamesolver.org/solving-connect-four/01-introduction/
# https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV&index=1
import numpy as np

BOARD_ROWS = 6
BOARD_COLUMNS = 7


def create_board():
    # Creates a 6*7 2d list with each value equal to 0
    board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def available_location(board, col):
    return board[0][col] == 0
    # This checks if the uppermost location of a column is empty
    # --> If the returned value is True a piece can then actually be dropped into that column


def check_win(board, piece):
    # Checks all possible - horizontal wins
    for c in range(BOARD_COLUMNS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Checks all possible | vertical wins
    for c in range(BOARD_COLUMNS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Checks all possible / diagonal wins
    for c in range(BOARD_COLUMNS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Checks all possible \ diagonal wins
    for c in range(BOARD_COLUMNS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def get_next_open_row(board, col):
    # Checks the lowest possible row a piece can be placed in a chosen column
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == 0:
            return row


def main():
    game_over = False
    board = create_board()
    turn = 0
    print(board)

    while not game_over:

        # Ask player 1 input
        if turn % 2 == 0:
            col = int(input("Player 1, please select a column (0-6): "))
            # Checks if the selected column is actually part of the board and not already full
            while col < 0 or col > 6 or not available_location(board, col):
                print("Invalid Column")
                col = int(input("Player 1, please select a column again (0-6): "))

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

        # Ask Player 2 input
        elif turn % 2 == 1:
            col = int(input("Player 2, please select a column (0-6): "))
            # Checks if the selected column is actually part of the board
            while col < 0 or col > 6 or not available_location(board, col):
                print("Invalid Column")
                col = int(input("Player 2, please select a column again (0-6): "))

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

        print(board)

        if check_win(board, 1):
            print("Player 1 wins! Congratulations!")
            game_over = True
        elif check_win(board, 2):
            print("Player 2 wins! Congratulations! ")
            game_over = True

        turn += 1


if __name__ == "__main__":
    main()
