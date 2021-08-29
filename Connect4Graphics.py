import numpy as np
import pygame as p
import sys

p.init()

BOARD_ROWS = 6
BOARD_COLUMNS = 7
SQUARE_SIZE = 120
WIDTH = SQUARE_SIZE * BOARD_COLUMNS
HEIGHT = SQUARE_SIZE * (BOARD_ROWS+1)
RADIUS = int(SQUARE_SIZE*9/20)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
text_font = p.font.SysFont("Arial", int(SQUARE_SIZE*3/4))

screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Connect 4")
icon = p.image.load("Images/2x2connect.png")
p.display.set_icon(icon)
screen.fill(BLACK)


def create_board():
    # Creates a 6*7 list with each value equal to 0
    board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def available_location(board, col):
    return board[0][col] == 0
    # This checks if the uppermost location of a column is empty
    # --> If the returned value is True a piece can then actually be dropped into the column


def check_win(board, piece):
    # Checks all possible - horizontal wins
    for c in range(BOARD_COLUMNS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c + 3] == piece:
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
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == 0:
            return row


def draw_board(board):
    for c in range(BOARD_COLUMNS):
        for r in range(BOARD_ROWS):
            p.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 0:
                p.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE*3/2)), RADIUS)
            if board[r][c] == 1:
                p.draw.circle(screen, RED, (int(c * SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE*3/2)), RADIUS)
            elif board[r][c] == 2:
                p.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE*3/2)), RADIUS)


def main():
    game_over = False
    board = create_board()
    turn = 0
    # print(board)
    draw_board(board)

    while not game_over:

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEMOTION:
                p.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                mouseX = event.pos[0]
                if turn % 2 == 0:
                    p.draw.circle(screen, RED, (mouseX, int(SQUARE_SIZE / 2)), RADIUS)
                elif turn % 2 == 1:
                    p.draw.circle(screen, YELLOW, (mouseX, int(SQUARE_SIZE / 2)), RADIUS)
                p.display.update()

            if event.type == p.MOUSEBUTTONDOWN:
                p.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                if turn % 2 == 0:
                    mouseX = event.pos[0]
                    col = int(mouseX // SQUARE_SIZE)

                    if available_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        turn += 1

                        if check_win(board, 1):
                            win_text = text_font.render("Player 1 wins!", True, RED)
                            screen.blit(win_text, (SQUARE_SIZE // 4, SQUARE_SIZE // 10))
                            game_over = True

                # Ask Player 2 input
                elif turn % 2 == 1:
                    mouseX = event.pos[0]
                    col = int(mouseX // SQUARE_SIZE)

                    if available_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        turn += 1

                        if check_win(board, 2):
                            win_text = text_font.render("Player 2 wins!", True, YELLOW)
                            screen.blit(win_text, (SQUARE_SIZE // 4, SQUARE_SIZE // 10))
                            game_over = True

                # print(board)
                draw_board(board)
                p.display.update()

                if game_over:
                    p.time.wait(2500)


if __name__ == "__main__":
    main()
