from flask import Flask, jsonify, request, render_template, redirect, url_for, session
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
    import random
    word, hint = random.choice(list(hg.wordlist.items()))
    session['word'] = word
    session['hint'] = hint
    session['letterGuessed'] = ''
    session['wrong_guesses'] = 0
    session['msg'] = ''
    return redirect(url_for('game_loop'))

@app.route('/game')
def game_loop():
    word = session.get('word')
    letterGuessed = session.get('letterGuessed', '')
    wrong_guesses = session.get('wrong_guesses', 0)
    max_chances = len(hg.stages) - 1

    display_word_str = " ".join([char if char in letterGuessed else "_" for char in word])
    stage_visual = stage_visual = f"img/stage{wrong_guesses}.png"


    from collections import Counter
    game_over = Counter(letterGuessed) == Counter(word)
    is_lost = wrong_guesses == max_chances
    show_hint = wrong_guesses == (max_chances - 1)

    return render_template('hangman.html',
                           display_word=display_word_str,
                           stage_visual=stage_visual,
                           msg=session.get('msg', ''),
                           show_hint=show_hint,
                           hint=session.get('hint'),
                           game_over=game_over,
                           is_lost=is_lost,
                           secret_word=word)

@app.route('/guess', methods=['POST'])
def guess():
    guess_letter = request.form.get('letter', '').lower()
    word = session.get('word')
    letterGuessed = session.get('letterGuessed', '')
    wrong_guesses = session.get('wrong_guesses', 0)

    session['msg'] = ''  # تصفير رسائل الخطأ السابقة

    # تطبيق دالة validate_input الخاصة بكِ بدقة
    if not guess_letter.isalpha():
        session['msg'] = 'Enter only a letter!'
    elif len(guess_letter) > 1:
        session['msg'] = 'Enter only a single letter!'
    elif guess_letter in letterGuessed:

        session['msg'] = 'You already guessed that letter!'
    else:
        # تطبيق منطق التخمين الصحيح والخاطئ من كودك الأصلي
        if guess_letter in word:
            session['letterGuessed'] += guess_letter * word.count(guess_letter)
        else:
            session['wrong_guesses'] += 1

    return redirect(url_for('game_loop'))

# ------------------------------------------[ Wordle ]-----------------------------------------------------------
@app.route('/Wordle', methods=['GET', 'POST'])
def wordle():
    if 'word' not in session:
        game_logic = wordle() # create an instance of the wordle class
        session['word'] = game_logic.word #
        session['attempts'] = 6
        session['history'] = [] #used to store the history of the player's previous guesses and color code the results
        
    message = ""
    
    if request.method == 'POST':
        '''
        This method handles the restart and captures the player's
        '''
        if request.form.get('restart'): #this handles the play again button
            session.pop('word', None)
            session.pop('attempts', None)
            session.pop('history', None)
            return redirect(url_for('wordle'))
        
        guess = request.form.get('guess', '').lower() #checking the formatting of the input 
        if len(guess) == 5 and guess.isalpha():#check if the input is 5 letter long and all alphabets
            target = session['word']
            letters = list(target)
            result = []
            for i, letter in enumerate(guess):
                if letter == target[i]:
                    result.append({letter: letter.upper(), 'status': 'correct'})
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
            session['attempts'] -=1
            session['history'].append(result)
            
            
            if guess == target:
                message = "You Won!"
            elif session['attempts'] <= 0:
                message = f"Game Over! The Word Was {target}"
        else:
                message = "Invalid input! Use 5 Letters"
    
    return render_template('wordle.html', attempts= session['attempts'], history = session['history'], message = message)



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
    ttt.reset()
    return render_template(
        "tictactoe.html",
        board=ttt.board,
        status=ttt.get_status(),
        game_running=ttt.game_running
    )

@app.route("/move/<int:position>")
def move(position):
    ttt.make_move(position)
    return redirect(url_for("tictactoe"))

@app.route("/reset")
def reset():
    ttt.reset()
    return redirect(url_for("tictactoe"))

# ------------------------------------------[ run ]-----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)