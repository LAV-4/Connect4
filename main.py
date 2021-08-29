import numpy as np
import pygame as p
import sys
import random
import math

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

PLAYER = 0
AI = 1
EMPTY_SPACE = 0
PLAYER_PIECE = 1
AI_PIECE = 2

ANALYZED_AREA_LENGTH = 4

screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Connect 4")
icon = p.image.load("Images/2x2connect.png")
p.display.set_icon(icon)
screen.fill(BLACK)


def create_board():
    # Creates a 6*7 list with each value equal to 0
    board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
    return board


def available_location(board, col):
    return board[0][col] == 0
    # This checks if the uppermost location of a column is empty
    # --> If the returned value is true a piece can then actually be dropped into the column


def get_next_open_row(board, col):
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == 0:
            return row


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def draw_board(board):
    for c in range(BOARD_COLUMNS):
        for r in range(BOARD_ROWS):
            p.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 0:
                p.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE*3/2)), RADIUS)
            if board[r][c] == PLAYER_PIECE:
                p.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE*3/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                p.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE*3/2)), RADIUS)


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


def evaluate_analyzed_area(analyzed_area, piece):
    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    if analyzed_area.count(piece) == 4:
        score += 100
    elif analyzed_area.count(piece) == 3 and analyzed_area.count(EMPTY_SPACE) == 1:
        score += 5
    elif analyzed_area.count(piece) == 2 and analyzed_area.count(EMPTY_SPACE) == 2:
        score += 2
    if analyzed_area.count(opponent_piece) == 3 and analyzed_area.count(EMPTY_SPACE) == 1:
        score -= 4
    return score


def score_position(board, piece):
    score = 0
    # Calculates score giving preference to the middle column
    center_array = [int(i) for i in list(board[:, BOARD_COLUMNS//2])]
    center_count = center_array.count(piece)
    score += center_count*3
    # Calculates score based on horizontal possible connections
    for r in range(BOARD_ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(BOARD_COLUMNS-3):
            analyzed_area = row_array[c:c+ANALYZED_AREA_LENGTH]
            score += evaluate_analyzed_area(analyzed_area, piece)
    # Calculates score based on vertical possible connections
    for c in range(BOARD_COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(BOARD_ROWS-3):
            analyzed_area = col_array[r:r+ANALYZED_AREA_LENGTH]
            score += evaluate_analyzed_area(analyzed_area, piece)
    # Calculates score based on positive diagonal possible connections
    for r in range(BOARD_ROWS-3):
        for c in range(BOARD_COLUMNS-3):
            analyzed_area = [board[r+i][c+i] for i in range(ANALYZED_AREA_LENGTH)]
            score += evaluate_analyzed_area(analyzed_area, piece)
    # Calculates score based on negative diagonal possible connections
    for r in range(BOARD_ROWS-3):
        for c in range(BOARD_COLUMNS-3):
            analyzed_area = [board[r+3-i][c+i] for i in range(ANALYZED_AREA_LENGTH)]
            score += evaluate_analyzed_area(analyzed_area, piece)
    return score


def get_available_locations(board):
    valid_locations = []
    for col in range(BOARD_COLUMNS):
        if available_location(board, col):
            valid_locations.append(col)
    return valid_locations


def choose_best_move(board, piece):
    valid_locations = get_available_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        board_copy = board.copy()
        drop_piece(board_copy, row, col, piece)
        score = score_position(board_copy, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def is_terminal_node(board):
    return check_win(board, PLAYER_PIECE) or check_win(board, AI_PIECE) or len(get_available_locations(board)) == 0


def minimax(board, depth, maximizingPlayer):
    # https://en.wikipedia.org/wiki/Minimax
    available_locations = get_available_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI_PIECE):
                return (None, 100000)
            elif check_win(board, PLAYER_PIECE):
                return (None, -100000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = - math.inf
        column = random.choice(available_locations)
        for col in available_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, AI_PIECE)
            new_score = minimax(board_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    elif not maximizingPlayer:
        value = math.inf
        column = random.choice(available_locations)
        for col in available_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            new_score = minimax(board_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def random_AI():
    selected_col = random.randint(0, BOARD_COLUMNS-1)
    return selected_col


def intermediate_AI(board):
    selected_col = choose_best_move(board, AI_PIECE)
    return selected_col


def advanced_AI(board, depth):
    selected_col, minimax_score = minimax(board, depth, True)
    return selected_col


def main():
    game_over = False
    board = create_board()
    turn = random.randint(PLAYER, AI)
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
                if turn % 2 == PLAYER:
                    p.draw.circle(screen, RED, (mouseX, int(SQUARE_SIZE/2)), RADIUS)
                p.display.update()

            if event.type == p.MOUSEBUTTONDOWN:
                p.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                if turn % 2 == PLAYER:
                    mouseX = event.pos[0]
                    col = int(mouseX // SQUARE_SIZE)

                    if available_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                        turn += 1

                        if check_win(board, PLAYER_PIECE):
                            win_text = text_font.render("Player 1 wins!", True, RED)
                            screen.blit(win_text, (SQUARE_SIZE // 4, SQUARE_SIZE // 10))
                            game_over = True

            # Ask AI for input
            elif turn % 2 == AI and not game_over:
                # col = random_AI()
                # col = intermediate_AI(board)
                col = advanced_AI(board, 4)
                if available_location(board, col):
                    p.time.wait(random.randint(100, 200))   # This time wait gives the impression that AI is thinking
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)
                    turn += 1

                    if check_win(board, AI_PIECE):
                        win_text = text_font.render("AI wins!", True, YELLOW)
                        screen.blit(win_text, (SQUARE_SIZE // 4, SQUARE_SIZE // 10))
                        game_over = True

            # print(board)
            draw_board(board)
            p.display.update()

            if game_over:
                p.time.wait(2000)


if __name__ == "__main__":
    main()
