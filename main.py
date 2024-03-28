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

# Function to move a piece on the board and update the player
def move_piece(start_pos, end_pos):
    global player, game_over  # Declare global due to modification
    row_start, col_start = start_pos
    row_end, col_end = end_pos
    board[row_end][col_end] = board[row_start][col_start]
    board[row_start][col_start] = 0

    # Check if it was a jump move (capture)
    if abs(row_end - row_start) == 2:
        # Remove the captured piece from the board
        captured_row = (row_start + row_end) // 2
        captured_col = (col_start + col_end) // 2
        board[captured_row][captured_col] = 0

    draw_pieces()
    # Switch player after a successful move
    player *= -1

    # Check if the game is over after the move
    game_over = check_game_over()
    if game_over:
        print("Game Over")

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

def handle_click(event):
    global selected_piece, player
    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE

    # Check if the click is within bounds
    if row >= 0 and row < BOARD_SIZE and col >= 0 and col < BOARD_SIZE:
        # If a piece is already selected
        if selected_piece:
            # Attempt to move the selected piece to the clicked square
            start_pos = selected_piece
            end_pos = (row, col)
            if is_valid_move(start_pos, end_pos):
                move_piece(start_pos, end_pos)
                selected_piece = None  # Deselect piece after moving
                # Switch player after a valid move
                player *= -1
            else:
                # If the destination is not valid, check if another piece was selected
                if board[row][col] * player > 0:
                    selected_piece = (row, col)  # Select a new piece
                else:
                    selected_piece = None  # Deselect if clicked on an empty square or enemy piece
        else:
            # If no piece is selected and the clicked square has the player's piece, select it
            if board[row][col] * player > 0:
                selected_piece = (row, col)

    draw_board()  # Redraw the board to reflect any changes
    if selected_piece:
        # Highlight the selected piece
        highlight_square(selected_piece[0], selected_piece[1])

def highlight_square(row, col):
    """Highlight the square at the given row and col to indicate it is selected."""
    canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                            outline="yellow", width=2)


# Function to check for game over condition
def check_game_over():
    # Initialize counters for both players
    player1_pieces, player2_pieces = 0, 0

    # Iterate through the board to count pieces for both players
    for row in board:
        player1_pieces += row.count(1)
        player2_pieces += row.count(-1)

    # Check for no pieces or no possible moves condition
    if player1_pieces == 0 or player2_pieces == 0:
        return True
    if not any(generate_piece_moves((i, j)) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if
               board[i][j] == player):
        return True
    return False

# Define the maximum depth for the Minimax algorithm
MAX_DEPTH = 4  # Adjust this value as needed

def make_ai_move():
    global player
    if player != -1:  # Ensure it's AI's turn
        return

    possible_moves = generate_all_moves(board, player)
    if possible_moves:
        # Use Minimax here in the actual implementation to get the best move
        selected_move = random.choice(possible_moves)  # For demo, randomly choose a move
        apply_move(board, selected_move)
        draw_pieces()

        # After AI makes a move, check if the game is over
        global game_over
        game_over = check_game_over()
        if game_over:
            print("Game Over")

        # Switch to the other player
        player *= -1
    else:
        print("AI has no valid moves.")

# Function implementing the Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or check_game_over(board):
        return evaluate_board(board), None

    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for move in generate_all_moves(board, player):
            # Simulate the move
            captured_pieces = apply_move(board, move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            undo_move(board, move, captured_pieces)
            if eval > maxEval:
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in generate_all_moves(board, -player):
            captured_pieces = apply_move(board, move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            undo_move(board, move, captured_pieces)
            if eval < minEval:
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move


# Function to evaluate the board
def evaluate_board():
    player1_pieces = sum(row.count(1) for row in board)
    player2_pieces = sum(row.count(-1) for row in board)
    return player1_pieces - player2_pieces

# Function to generate all possible moves for a player
def generate_all_moves(board, current_player):
    moves = []
    captures = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] * current_player > 0:  # Check for AI's pieces
                piece_moves, piece_captures = generate_piece_moves((row, col))
                moves.extend(piece_moves)
                captures.extend(piece_captures)

    # If any captures are available, the AI should prioritize them
    return captures if captures else moves

def generate_piece_moves(board, position, piece):
    moves = []
    captures = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
    for direction in directions:
        for distance in [1, 2]:  # Move or capture distance
            new_row = position[0] + direction[0] * distance
            new_col = position[1] + direction[1] * distance
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if distance == 1 and board[new_row][new_col] == 0:
                    moves.append((position, (new_row, new_col)))
                elif distance == 2 and board[new_row][new_col] == 0 and board[position[0] + direction[0]][position[1] + direction[1]] * piece < 0:
                    captures.append((position, (new_row, new_col)))
    return moves, captures


def apply_move(board, move):
    start_pos, end_pos = move
    board[end_pos[0]][end_pos[1]] = board[start_pos[0]][start_pos[1]]
    board[start_pos[0]][start_pos[1]] = 0

    # Determine if the move is a capture
    if abs(start_pos[0] - end_pos[0]) == 2:
        # Calculate the position of the captured piece
        captured_row = (start_pos[0] + end_pos[0]) // 2
        captured_col = (start_pos[1] + end_pos[1]) // 2
        # Remove the captured piece
        board[captured_row][captured_col] = 0

def undo_move(board, move, captured_piece=None):
    # Reverse the move
    start_pos, end_pos = move
    board[start_pos[0]][start_pos[1]] = board[end_pos[0]][end_pos[1]]
    board[end_pos[0]][end_pos[1]] = 0  # This assumes no kinging or promotion logic is in place

    # If the move was a capture, restore the captured piece
    if abs(start_pos[0] - end_pos[0]) == 2:
        captured_row = (start_pos[0] + end_pos[0]) // 2
        captured_col = (start_pos[1] + end_pos[1]) // 2
        board[captured_row][captured_col] = captured_piece if captured_piece else -board[start_pos[0]][start_pos[1]]


# Main function to run the game
def main():
    initialize_board()
    create_gui()
    canvas.bind("<Button-1>", handle_click)  # Bind left mouse click to handle_click function
    root.mainloop()




# Start the game
if __name__ == "__main__":
    main()
