
import math

HUMAN = "X"
COMPUTER = "O"
EMPTY = " "

board = [EMPTY] * 9

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def display_board():
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            index = row * 3 + col
            value = board[index] if board[index] != EMPTY else str(index + 1)
            cells.append(value)

        print(" " + " | ".join(cells))
        if row < 2:
            print("---+---+---")
    print()


def check_winner(player):
    for combination in WINNING_COMBINATIONS:
        if all(board[i] == player for i in combination):
            return True
    return False


def is_draw():
    return (
        EMPTY not in board
        and not check_winner(HUMAN)
        and not check_winner(COMPUTER)
    )


def minimax(is_computer_turn):
    if check_winner(COMPUTER):
        return 1

    if check_winner(HUMAN):
        return -1

    if EMPTY not in board:
        return 0

    if is_computer_turn:
        best_score = -math.inf

        for i in range(9):
            if board[i] == EMPTY:
                board[i] = COMPUTER
                score = minimax(False)
                board[i] = EMPTY
                best_score = max(best_score, score)

        return best_score

    best_score = math.inf

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = HUMAN
            score = minimax(True)
            board[i] = EMPTY
            best_score = min(best_score, score)

    return best_score


def computer_move():
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = COMPUTER
            score = minimax(False)
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        board[best_move] = COMPUTER
        print("Computer played position:", best_move + 1)


def play_game():
    print("===== TIC-TAC-TOE AI =====")
    print("You are X. The computer is O.")
    print("Choose a position from 1 to 9.")

    while True:
        display_board()

        choice = input("Your move (1-9), or Q to quit: ").strip()

        if choice.lower() == "q":
            print("Game ended.")
            return

        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Invalid input. Enter a number from 1 to 9.")
            continue

        position = int(choice) - 1

        if board[position] != EMPTY:
            print("That position is already occupied. Try again.")
            continue

        board[position] = HUMAN

        if check_winner(HUMAN):
            display_board()
            print("Result: YOU WIN!")
            return

        if is_draw():
            display_board()
            print("Result: DRAW!")
            return

        computer_move()

        if check_winner(COMPUTER):
            display_board()
            print("Result: YOU LOSE! The computer wins.")
            return

        if is_draw():
            display_board()
            print("Result: DRAW!")
            return


if __name__ == "__main__":
    play_game()
