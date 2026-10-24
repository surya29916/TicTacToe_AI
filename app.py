
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

HUMAN = "X"
COMPUTER = "O"
EMPTY = ""

WINNING_COMBINATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def check_winner(board):
    """Return X or O if a player wins; otherwise None."""
    for combo in WINNING_COMBINATIONS:
        a, b, c = combo

        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    return None


def is_draw(board):
    """Check whether the board is full and nobody has won."""
    return (
        all(cell != EMPTY for cell in board)
        and check_winner(board) is None
    )


def minimax(board, is_maximizing):
    """Calculate the best possible outcome for the AI."""
    winner = check_winner(board)

    if winner == COMPUTER:
        return 1

    if winner == HUMAN:
        return -1

    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")

        for i in range(9):
            if board[i] == EMPTY:
                board[i] = COMPUTER
                score = minimax(board, False)
                board[i] = EMPTY

                best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = HUMAN
            score = minimax(board, True)
            board[i] = EMPTY

            best_score = min(best_score, score)

    return best_score


def computer_move(board):
    """Choose the best available move for the AI."""
    best_score = -float("inf")
    best_move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = COMPUTER
            score = minimax(board, False)
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    """Receive the player's move and calculate the AI response."""
    data = request.get_json(silent=True) or {}
    board = data.get("board")

    # Validate the board structure.
    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Invalid board"}), 400

    if any(cell not in [HUMAN, COMPUTER, EMPTY] for cell in board):
        return jsonify({"error": "Invalid board values"}), 400

    human_count = board.count(HUMAN)
    computer_count = board.count(COMPUTER)

    # The player has just placed X, so X must have one extra move.
    if human_count != computer_count + 1:
        return jsonify({"error": "Invalid turn"}), 400

    # Check that X and O are arranged according to a valid game.
    for combo in WINNING_COMBINATIONS:
        a, b, c = combo
        if board[a] == board[b] == board[c] == HUMAN:
            return jsonify({"error": "Player already won"}), 400

    if check_winner(board) == COMPUTER:
        return jsonify({"error": "Game already finished"}), 400

    # The player must have placed X in an empty square.
    if EMPTY not in board:
        return jsonify({"error": "No empty squares"}), 400

    updated_board = board.copy()

    # Calculate and place the computer's move.
    index = computer_move(updated_board)

    if index is not None:
        updated_board[index] = COMPUTER

    winner = check_winner(updated_board)

    if winner == HUMAN:
        status = "human_win"
    elif winner == COMPUTER:
        status = "computer_win"
    elif is_draw(updated_board):
        status = "draw"
    else:
        status = "playing"

    return jsonify({
        "board": updated_board,
        "status": status,
        "winner": winner
    })


if __name__ == "__main__":
    app.run(debug=True)
