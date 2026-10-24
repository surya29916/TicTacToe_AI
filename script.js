
const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");
const restartButton = document.getElementById("restart");

const aiModeButton = document.getElementById("aiMode");
const twoPlayerModeButton = document.getElementById("twoPlayerMode");

let board = Array(9).fill("");
let gameMode = "ai";
let currentPlayer = "X";
let gameOver = false;

let scores = {
    human: 0,
    ai: 0,
    player1: 0,
    player2: 0,
    draw: 0
};

function updateBoard() {
    cells.forEach((cell, index) => {
        cell.textContent = board[index];

        cell.classList.toggle("o", board[index] === "O");

        cell.disabled = gameOver || board[index] !== "";

        cell.setAttribute(
            "aria-label",
            `Square ${index + 1}${board[index] ? ", " + board[index] : ", empty"}`
        );
    });
}

function updateScores() {
    const humanLabel = document.querySelector(
        ".scoreboard .score:nth-child(1) span"
    );

    const aiLabel = document.querySelector(
        ".scoreboard .score:nth-child(3) span"
    );

    if (gameMode === "ai") {
        humanLabel.textContent = "You · X";
        aiLabel.textContent = "AI · O";

        document.getElementById("humanScore").textContent = scores.human;
        document.getElementById("aiScore").textContent = scores.ai;
    } else {
        humanLabel.textContent = "Player 1 · X";
        aiLabel.textContent = "Player 2 · O";

        document.getElementById("humanScore").textContent = scores.player1;
        document.getElementById("aiScore").textContent = scores.player2;
    }

    document.getElementById("drawScore").textContent = scores.draw;
}

function updateModeButtons() {
    aiModeButton.classList.toggle("active", gameMode === "ai");
    twoPlayerModeButton.classList.toggle(
        "active",
        gameMode === "two"
    );
}

function startNewGame() {
    board = Array(9).fill("");
    currentPlayer = "X";
    gameOver = false;

    statusText.textContent =
        gameMode === "ai"
            ? "Your turn! Choose a square."
            : "Player 1's turn (X).";

    updateBoard();
    updateScores();
}

function changeMode(mode) {
    gameMode = mode;
    updateModeButtons();
    startNewGame();
}

function finishGame(status) {
    gameOver = true;

    if (status === "human_win") {
        statusText.textContent = "You win! 🎉";
        scores.human++;
    } else if (status === "computer_win") {
        statusText.textContent = "AI wins! Try again.";
        scores.ai++;
    } else if (status === "player1_win") {
        statusText.textContent = "Player 1 wins! 🎉";
        scores.player1++;
    } else if (status === "player2_win") {
        statusText.textContent = "Player 2 wins! 🎉";
        scores.player2++;
    } else {
        statusText.textContent = "It's a draw! 🤝";
        scores.draw++;
    }

    updateBoard();
    updateScores();
}

function checkWinner() {
    const combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];

    for (const [a, b, c] of combinations) {
        if (
            board[a] &&
            board[a] === board[b] &&
            board[b] === board[c]
        ) {
            return board[a];
        }
    }

    return null;
}

function checkDraw() {
    return board.every(cell => cell !== "");
}

async function playAgainstAI(index) {
    board[index] = "X";
    updateBoard();

    const winner = checkWinner();

    if (winner === "X") {
        finishGame("human_win");
        return;
    }

    if (checkDraw()) {
        finishGame("draw");
        return;
    }

    statusText.textContent = "AI is thinking...";

    try {
        const response = await fetch("/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ board })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not make a move.");
        }

        board = result.board;

        if (result.status === "computer_win") {
            finishGame("computer_win");
        } else if (result.status === "human_win") {
            finishGame("human_win");
        } else if (result.status === "draw") {
            finishGame("draw");
        } else {
            statusText.textContent = "Your turn! Choose a square.";
            updateBoard();
        }
    } catch (error) {
        statusText.textContent =
            "Could not contact AI. Check that Flask is running.";

        console.error(error);
    }
}

function playTwoPlayers(index) {
    board[index] = currentPlayer;

    const winner = checkWinner();

    if (winner === "X") {
        updateBoard();
        finishGame("player1_win");
        return;
    }

    if (winner === "O") {
        updateBoard();
        finishGame("player2_win");
        return;
    }

    if (checkDraw()) {
        updateBoard();
        finishGame("draw");
        return;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";

    statusText.textContent =
        currentPlayer === "X"
            ? "Player 1's turn (X)."
            : "Player 2's turn (O).";

    updateBoard();
}

function handleCellClick(index) {
    if (gameOver || board[index] !== "") {
        return;
    }

    if (gameMode === "ai") {
        playAgainstAI(index);
    } else {
        playTwoPlayers(index);
    }
}

cells.forEach((cell, index) => {
    cell.addEventListener("click", () => {
        handleCellClick(index);
    });
});

aiModeButton.addEventListener("click", () => {
    changeMode("ai");
});

twoPlayerModeButton.addEventListener("click", () => {
    changeMode("two");
});

restartButton.addEventListener("click", startNewGame);

updateModeButtons();
startNewGame();
