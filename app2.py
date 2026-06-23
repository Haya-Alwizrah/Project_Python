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
            'name': 'HangmanGame',
            'url': '/HangmanGame'
        },
        {
            'name': 'Wordle',
            'url': '/Wordle'
        },
        {
            'name': 'GuessingNumberGame',
            'url': '/GuessingNumberGame'
        }
    ]
    return render_template('category.html', title='Single Player Games', games=games)

@app.route('/multiplayer')
def multiplayer():
    games = [
        {
            'name': 'HexaPown',
            'url': '/hexapown'
        },
        {
            'name': 'TicTacToe',
            'url': '/TicTacToe'
        }
    ]
    return render_template('category.html', title='Two Player Games', games=games)

# ------------------------------------------[ HangmanGame ]-----------------------------------------------------------
@app.route('/HangmanGame')
def hangman():
    return render_template('hangman.html')

# ------------------------------------------[ Wordle ]-----------------------------------------------------------
@app.route('/Wordle')
def wordle():
    return render_template('wordle.html')

# ------------------------------------------[ GuessingNumberGame ]-----------------------------------------------------------
@app.route('/GuessingNumberGame')
def guessing_number():
    return render_template('guessing_number.html')

# ------------------------------------------[ HexaPown ]-----------------------------------------------------------
@app.route('/hexapown')
def hexapown():
    hp.reset()
    return render_template('hexapown.html')

@app.route('/hexapown/state', methods=['GET'])
def hexapown_state():
    return jsonify(hp.get_state())

@app.route('/hexapown/available_moves', methods=['POST'])
def hexapown_available_moves():
    data = request.json
    row, col = int(data.get('row')), int(data.get('col'))
    
    available_moves = hp.available_moves()
    piece_moves = available_moves.get((row, col), [])
    
    return jsonify({'moves': piece_moves})

@app.route('/hexapown/move', methods=['POST'])
def hexapown_move():
    data = request.json
    from_pos = (int(data.get('from_row')), int(data.get('from_col')))
    to_pos = (int(data.get('to_row')), int(data.get('to_col')))
    
    success = hp.move(from_pos, to_pos)
    
    state = hp.get_state()
    state['success'] = success
    return jsonify(state)

@app.route('/hexapown/reset', methods=['POST'])
def hexapown_reset():
    hp.reset()
    return jsonify(hp.get_state())

# ------------------------------------------[ TicTacToe ]-----------------------------------------------------------
@app.route('/TicTacToe')
def tictactoe():
    return render_template('tictactoe.html')

# ------------------------------------------[ run ]-----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)