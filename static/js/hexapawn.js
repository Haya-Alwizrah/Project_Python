let selectedPiece = null;
let movablePieces = [];
let highlightedMoves = [];
let currentBoard = [];
let currentPlayer = "";
let currentWinner = null;

document.addEventListener("DOMContentLoaded", loadGameState);

async function loadGameState() {
    selectedPiece = null;
    highlightedMoves = [];
    
    let response = await fetch('/hexapawn/state');
    let data = await response.json();
    
    currentBoard = data.board;
    currentPlayer = data.player;
    currentWinner = data.winner;
    movablePieces = data.movable_pieces;
    
    renderBoard();
}

async function resetGame() {
    selectedPiece = null;
    highlightedMoves = [];
    
    let response = await fetch('/hexapawn/reset', { method: 'POST' });
    let data = await response.json();
    
    currentBoard = data.board;
    currentPlayer = data.player;
    currentWinner = data.winner;
    movablePieces = data.movable_pieces;
    
    renderBoard();
}

function renderBoard() {
    const boardDiv = document.getElementById('game-board');
    boardDiv.innerHTML = ''; 

    if (currentWinner) {
        document.getElementById('status-text').innerText = `Winner is Player: ${currentWinner}!`;
    } else {
        document.getElementById('status-text').innerText = `Turn: Player ${currentPlayer}`;
    }

    for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            
            if ((r + c) % 2 === 0) cell.classList.add('light');
            else cell.classList.add('dark');

            const piece = currentBoard[r][c];
            if (piece !== " ") {
                cell.innerText = piece;
                cell.classList.add(`pawn-${piece}`);
            }

            if (!currentWinner) {
                const isMovable = movablePieces.some(p => parseInt(p[0]) === r && parseInt(p[1]) === c);
                if (isMovable) {
                    cell.classList.add('movable');
                }
            }

            if (selectedPiece && parseInt(selectedPiece.row) === r && parseInt(selectedPiece.col) === c) {
                cell.classList.add('selected');
            }

            const isHighlight = highlightedMoves.some(m => parseInt(m[0]) === r && parseInt(m[1]) === c);
            if (isHighlight) {
                cell.classList.add('highlight-move');
            }

            cell.addEventListener('click', () => handleCellClick(r, c));

            boardDiv.appendChild(cell);
        }
    }
}

async function handleCellClick(row, col) {
    if (currentWinner) return; 

    const isDestination = highlightedMoves.some(m => parseInt(m[0]) === parseInt(row) && parseInt(m[1]) === parseInt(col));
    if (isDestination && selectedPiece) {
        let response = await fetch('/hexapawn/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_row: selectedPiece.row,
                from_col: selectedPiece.col,
                to_row: row,
                to_col: col
            })
        });
        let data = await response.json();
        if (data.success) {
            selectedPiece = null;
            highlightedMoves = [];
            currentBoard = data.board;
            currentPlayer = data.player;
            currentWinner = data.winner;
            movablePieces = data.movable_pieces;
            renderBoard();
        }
        return;
    }

    const isMovable = movablePieces.some(p => parseInt(p[0]) === parseInt(row) && parseInt(p[1]) === parseInt(col));
    if (isMovable) {
        selectedPiece = { row, col };
        
        let response = await fetch('/hexapawn/available_moves', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row, col })
        });
        let data = await response.json();
        
        highlightedMoves = data.moves.map(m => [parseInt(m[0]), parseInt(m[1])]);

        renderBoard();
    } else {
        selectedPiece = null;
        highlightedMoves = [];
        renderBoard();
    }
}