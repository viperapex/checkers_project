import tkinter as tk
import random
import time

# Define constants for the board size and colors
BOARD_SIZE = 8
SQUARE_SIZE = 50
LIGHT_COLOR = "white"
DARK_COLOR = "black"

# Define global variables to track game state
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
player = 1
game_over = False
selected_piece = None

# Function to initialize the board
def initialize_board():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # Set initial pieces for player 1
            if (i + j) % 2 != 0 and i < 3:
                board[i][j] = 1
            # Set initial pieces for player 2
            elif (i + j) % 2 != 0 and i > 4:
                board[i][j] = -1

# Function to create the graphical user interface
def create_gui():
    global root, canvas
    root = tk.Tk()
    root.title("Checkers Game")

    canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
    canvas.pack()

    draw_board()

# Function to draw the checkered board
def draw_board():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x1 = j * SQUARE_SIZE
            y1 = i * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    draw_pieces()

# Function to draw the pieces on the board
def draw_pieces():
    canvas.delete("piece")
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 1:
                canvas.create_oval(j * SQUARE_SIZE, i * SQUARE_SIZE, (j + 1) * SQUARE_SIZE, (i + 1) * SQUARE_SIZE,
                                   fill="red", tags="piece")
            elif board[i][j] == -1:
                canvas.create_oval(j * SQUARE_SIZE, i * SQUARE_SIZE, (j + 1) * SQUARE_SIZE, (i + 1) * SQUARE_SIZE,
                                   fill="blue", tags="piece")

# Function to handle user input
def handle_click(event):
    global player, selected_piece
    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE

    if board[row][col] * player > 0:
        selected_piece = (row, col)
    elif selected_piece:
        dest_row, dest_col = row, col
        if is_valid_move(selected_piece, (dest_row, dest_col)):
            move_piece(selected_piece, (dest_row, dest_col))
            selected_piece = None
            # Switch player after successful move
            player *= -1
        else:
            print("Invalid move!")
            selected_piece = None

# Function to check if a move is valid
def is_valid_move(start_pos, end_pos):
    # Implement logic to check if the move is valid
    pass

# Function to move a piece on the board
def move_piece(start_pos, end_pos):
    # Implement logic to move the piece on the board
    pass

# Function to generate possible moves for a player
def generate_possible_moves(board, player):
    possible_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] * player > 0:
                piece_moves = generate_piece_moves((i, j))
                possible_moves.extend(piece_moves)
    return possible_moves

# Function to generate possible moves for a piece
def generate_piece_moves(piece_pos):
    # Implement logic to generate possible moves for the piece
    pass

# Function to check for game over condition
def check_game_over():
    # Check if the current player has no more legal moves
    if not generate_possible_moves(board, player):
        return True
    return False

# Main function to run the game
def main():
    initialize_board()
    create_gui()
    canvas.bind("<Button-1>", handle_click)
    root.mainloop()

    # Function to move a piece on the board
def move_piece(start_pos, end_pos):
    row_start, col_start = start_pos
    row_end, col_end = end_pos
    board[row_end][col_end] = board[row_start][col_start]
    board[row_start][col_start] = 0
    draw_pieces()

# Function to check if a move is valid
def is_valid_move(start_pos, end_pos):
    row_start, col_start = start_pos
    row_end, col_end = end_pos

    # Check if the destination square is within the board boundaries
    if row_end < 0 or row_end >= BOARD_SIZE or col_end < 0 or col_end >= BOARD_SIZE:
        return False

    # Implement logic to check if the move is valid
    # (e.g., diagonal movement, capturing opponent's piece)

# Function to generate possible moves for a piece
def generate_piece_moves(piece_pos):
    # Implement logic to generate possible moves for the piece
    pass

# Function to check for game over condition
def check_game_over():
    # Check if the current player has no more legal moves
    if not generate_possible_moves(board, player):
        return True
    return False


# Function to check if a move is valid
def is_valid_move(start_pos, end_pos):
    row_start, col_start = start_pos
    row_end, col_end = end_pos

    # Check if the destination square is within the board boundaries
    if row_end < 0 or row_end >= BOARD_SIZE or col_end < 0 or col_end >= BOARD_SIZE:
        return False

    # Check if the destination square is unoccupied
    if board[row_end][col_end] != 0:
        return False

    # Check if the move is diagonal
    if abs(row_end - row_start) != abs(col_end - col_start):
        return False

    # Determine the direction of the move (forward or backward for kings)
    direction = (row_end - row_start) // abs(row_end - row_start)

    # Check if the move is within the range of a regular piece
    if board[row_start][col_start] == 1 and direction == -1:
        return False
    elif board[row_start][col_start] == -1 and direction == 1:
        return False

    # Implement logic for capturing opponent's piece
    if abs(row_end - row_start) == 2:
        # Check if there is an opponent's piece to capture
        captured_row = (row_start + row_end) // 2
        captured_col = (col_start + col_end) // 2
        if board[captured_row][captured_col] == 0 or board[captured_row][captured_col] == player:
            return False

    return True

# Function to generate possible moves for a piece
def generate_piece_moves(piece_pos):
    row, col = piece_pos
    piece = board[row][col]
    possible_moves = []

    # Check all diagonal directions
    for dr in [-1, 1]:
        for dc in [-1, 1]:
            new_row = row + dr
            new_col = col + dc
            jump_row = row + 2 * dr
            jump_col = col + 2 * dc

            # Regular move
            if is_valid_move(piece_pos, (new_row, new_col)):
                possible_moves.append(((row, col), (new_row, new_col)))

            # Jump move (capture)
            if is_valid_move(piece_pos, (jump_row, jump_col)):
                possible_moves.append(((row, col), (jump_row, jump_col)))

    return possible_moves

# Function to check for game over condition
def check_game_over():
    # Check if the current player has no more legal moves
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] * player > 0:
                piece_moves = generate_piece_moves((i, j))
                if piece_moves:
                    return False
    return True

# Function to move a piece on the board
def move_piece(start_pos, end_pos):
    row_start, col_start = start_pos
    row_end, col_end = end_pos

    # Move the piece to the destination square
    board[row_end][col_end] = board[row_start][col_start]
    board[row_start][col_start] = 0

    # Check if it was a jump move (capture)
    if abs(row_end - row_start) == 2:
        # Remove the captured piece from the board
        captured_row = (row_start + row_end) // 2
        captured_col = (col_start + col_end) // 2
        board[captured_row][captured_col] = 0

    # Redraw the pieces on the board
    draw_pieces()    

    # Define the maximum depth for the Minimax algorithm
MAX_DEPTH = 4  # Adjust this value as needed

# Function to make the AI player's move using Minimax with alpha-beta pruning
def make_ai_move():
    best_move = minimax_alpha_beta(board, MAX_DEPTH, float('-inf'), float('inf'), True)[1]
    move_piece(best_move[0], best_move[1])

# Function implementing the Minimax algorithm with alpha-beta pruning
def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_game_over():
        return evaluate_board(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for possible_move in generate_all_moves(board, player):
            eval = minimax_alpha_beta(possible_move, depth - 1, alpha, beta, False)[0]
            if eval > max_eval:
                max_eval = eval
                best_move = possible_move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for possible_move in generate_all_moves(board, -player):
            eval = minimax_alpha_beta(possible_move, depth - 1, alpha, beta, True)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = possible_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Function to generate all possible moves for a player
def generate_all_moves(board, player):
    possible_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] * player > 0:
                piece_moves = generate_piece_moves((i, j))
                for move in piece_moves:
                    new_board = simulate_move(board, (i, j), move)
                    possible_moves.append(new_board)
    return possible_moves

# Function to simulate a move on the board
def simulate_move(board, start_pos, end_pos):
    new_board = [row[:] for row in board]
    row_start, col_start = start_pos
    row_end, col_end = end_pos
    new_board[row_end][col_end] = new_board[row_start][col_start]
    new_board[row_start][col_start] = 0

    # Check if it was a jump move (capture)
    if abs(row_end - row_start) == 2:
        captured_row = (row_start + row_end) // 2
        captured_col = (col_start + col_end) // 2
        new_board[captured_row][captured_col] = 0

    return new_board
    
# Start the game
if __name__ == "__main__":
    main()
