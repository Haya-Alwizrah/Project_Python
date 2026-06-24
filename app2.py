from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import random
from collections import Counter

#----------------------------------------------------------------------
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

# --------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "my_secret_key_123"

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
        # {'name': 'Guessing Number', 'url': '/Guessing-Number'}
    ]
    return render_template('category.html', title='Single Player Games', games=games)

@app.route('/multiplayer')
def multiplayer():

    session.pop('ttt_playing', None)

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
# Define the web route/URL for initializing or restarting the game
@app.route('/Hangman')
def hangman():
    # Select random word and its color
    word, hint = random.choice(list(hg.wordlist.items()))

    # Store the variables in the encrypted browser session cookie
    session['hangman_word'] = word
    session['hangman_hint'] = hint

    # Initialize/Reset the player's guessed letters and wrong guesses
    session['hangman_letterGuessed'] = ''
    session['hangman_wrong_guesses'] = 0

    # Clear any existing validation error messages from previous game states
    session['hangman_msg'] = '' 

    return redirect(url_for('game_loop'))


@app.route('/game')
def game_loop():
    
    # Retrieve from the active session storage
    word = session.get('hangman_word')
    letterGuessed = session.get('hangman_letterGuessed', '')
    wrong_guesses = session.get('hangman_wrong_guesses', 0)
    
    max_chances = len(hg.stages) - 1

    # Call the class method to format the word into characters and underscores
    display_word_str = hg.display_word(word, letterGuessed)

    stage_visual = f"img/stage{wrong_guesses}.png"

    # Call your OOP class method to check if the win condition is met
    game_over = hg.check_win(letterGuessed, word)

    # Determine if the user has completely run out of guessing chances
    is_lost = wrong_guesses == max_chances

    # Condition to show the color hint exactly one turn before potential loss
    show_hint = wrong_guesses == (max_chances - 1)

    return render_template('hangman.html',
                           display_word=display_word_str,
                           stage_visual=stage_visual,
                           msg=session.get('hangman_msg', ''),
                           show_hint=show_hint,
                           hint=session.get('hangman_hint'),
                           game_over=game_over,
                           is_lost=is_lost,
                           secret_word=word)

@app.route('/guess', methods=['POST'])
def guess():
    
    # Extract the character from the HTML input field
    guess_letter = request.form.get('letter', '').lower()
    word = session.get('hangman_word')
    letterGuessed = session.get('hangman_letterGuessed', '')

    session['hangman_msg'] = ''

    # Call the class method to validate if the inputted letter is legal
    validation_result = hg.validate_input(guess_letter, letterGuessed)

    if validation_result is True:
        if guess_letter in word:
            session['hangman_letterGuessed'] += guess_letter * word.count(guess_letter)
        else:
            session['hangman_wrong_guesses'] += 1
    else:
        session['hangman_msg'] = validation_result

    return redirect(url_for('game_loop'))

# ------------------------------------------[ Wordle ]-----------------------------------------------------------
@app.route('/Wordle', methods=['GET', 'POST'])
def wordle():
    if request.method == 'GET':
        wo.__init__()
        session['wordle_history'] = [] #used to store the history of the player's previous guesses and color code the results
        session['wordle_attempts'] = 6
        session['wordle_word'] = wo._word_of_the_day()
 
    message = ""
    
    if request.method == 'POST':
        '''
        This method handles the restart and captures the player's
        '''
        if request.form.get('restart'): #this handles the play again button
            session.pop('wordle_word', None)
            session.pop('wordle_attempts', None)
            session.pop('wordle_history', None)
            return redirect(url_for('wordle'))
        
        guess = request.form.get('guess', '').lower() #checking the formatting of the input 
        if len(guess) == 5 and guess.isalpha():#check if the input is 5 letter long and all alphabets
            target = session['wordle_word']
            letters = list(target)
            result = []
            for i, letter in enumerate(guess):
                if letter == target[i]:
                    result.append({'letter': letter.upper(), 'status': 'correct'})
                    letters[i] = None
                else:
                    result.append({'letter': letter.upper(), 'status': 'pending'})
            for i, entry in enumerate(result):
                if entry['status'] != 'pending':
                    continue
                letter = guess[i]
                if letter in letters:
                    entry['status'] = 'present'
                    letters[letters.index(letter)] = None
                else:
                    entry['status'] = 'absent'
            session['wordle_attempts'] -= 1
            session['wordle_history'].append(result)
            
            
            if guess == target:
                message = "You Won!"
            elif session['wordle_attempts'] <= 0:
                message = f"Game Over! The Word Was {target}"
        else:
                message = "Invalid input! Use 5 Letters"
    
    return render_template('wordle.html', attempts= session['wordle_attempts'], history = session['wordle_history'], message = message)

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
    if 'ttt_playing' not in session:
        ttt.reset()
        session['ttt_playing'] = True

    return render_template(
        "tictactoe.html",
        board=ttt.board,
        status=ttt.get_status(),
        game_running=ttt.game_running
    )

@app.route("/tictactoe_move/<int:position>")
def tictactoe_move(position):
    session['ttt_playing'] = True
    ttt.make_move(position)
    return redirect(url_for("tictactoe"))

@app.route("/tictactoe_reset")
def tictactoe_reset():
    ttt.reset()
    session['ttt_playing'] = True
    return redirect(url_for("tictactoe"))

# ------------------------------------------[ run ]-----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
