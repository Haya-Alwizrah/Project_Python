from flask import Flask, jsonify, request, render_template
from games.hangman import HangmanGame
from games.wordle import Wordle
#from guessing_number import GuessingNumberGame
from games.hexapown import HexaPown
from games.tic_tac_toe import TicTacToe

hg = HangmanGame()
wo = Wordle()
#gn = GuessingNumberGame()
hp = HexaPown()
ttt = TicTacToe()

app = Flask(__name__)

# ------------------------------------------[ home ]-----------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# ------------------------------------------[ category ]-----------------------------------------------------------
@app.route('/singleplayer')
def singleplayer():
    games = [
        {
            'name': 'Hangman',
            'url': '/Hangman'
        },
        {
            'name': 'Wordle',
            'url': '/Wordle'
        },
        {
            'name': 'Guessing Number',
            'url': '/Guessing-Number'
        }
    ]
    return render_template('category.html', title='Single Player Games', games=games)

@app.route('/multiplayer')
def multiplayer():
    games = [
        {
            'name': 'Hexa Pawn',
            'url': '/hexapawn'
        },
        {
            'name': 'Tic Tac Toe',
            'url': '/TicTacToe'
        }
    ]
    return render_template('category.html', title='Two Player Games', games=games)

# ------------------------------------------[ HangmanGame ]-----------------------------------------------------------
@app.route('/Hangman')
def hangman():
    return render_template('hangman.html')

# ------------------------------------------[ Wordle ]-----------------------------------------------------------
@app.route('/Wordle')
def wordle():
    return render_template('wordle.html')

# ------------------------------------------[ GuessingNumberGame ]-----------------------------------------------------------
@app.route('/Guessing-Number')
def guessing_number():
    return render_template('guessing_number.html')

# ------------------------------------------[ HexaPown ]-----------------------------------------------------------
@app.route('/hexapawn')
def hexapawn():
    hp.reset()
    return render_template('hexapawn.html')

@app.route('/hexapawn/state', methods=['GET'])
def hexapawn_state():
    return jsonify(hp.get_state())

@app.route('/hexapawn/available_moves', methods=['POST'])
def hexapawn_available_moves():
    data = request.json
    row, col = int(data.get('row')), int(data.get('col'))
    
    available_moves = hp.available_moves()
    piece_moves = available_moves.get((row, col), [])
    
    return jsonify({'moves': piece_moves})

@app.route('/hexapawn/move', methods=['POST'])
def hexapawn_move():
    data = request.json
    from_pos = (int(data.get('from_row')), int(data.get('from_col')))
    to_pos = (int(data.get('to_row')), int(data.get('to_col')))
    
    success = hp.move(from_pos, to_pos)
    
    state = hp.get_state()
    state['success'] = success
    return jsonify(state)

@app.route('/hexapawn/reset', methods=['POST'])
def hexapawn_reset():
    hp.reset()
    return jsonify(hp.get_state())

# ------------------------------------------[ TicTacToe ]-----------------------------------------------------------
@app.route('/TicTacToe')
def tictactoe():
    return render_template('tictactoe.html')

# ------------------------------------------[ run ]-----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)