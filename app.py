from hangman import HangmanGame
from wordle import Wordle
#from guessing_number import GuessingNumberGame
from hexapown import HexaPown
# from tic_tac_toe import TicTacToe

hg = HangmanGame()
wo = Wordle()
#gn = GuessingNumberGame()
hp = HexaPown()
#ttt = TicTacToe()

print("Welcome to the game hub")
print("Choose from the menu:")
print("1) TwoPlayers Games\n 2) Single PLayer Games")
x = int(input("choose from the menu:"))

if int == 1:
    print("Choose from the menu:")
    print("1) Hangman\n2) Wordle\n3) Guessing Number" )
    y = int(input("choose from the menu:"))
    if y == 1:
        hg.start()
    elif y == 2:
        wo.start()
    elif y == 3:
        #gn.start()
        pass
    else:
        print("Invalid Input")

elif int == 2:
    print("Choose from the menu:")
    print("1) HexaPown\n2) Tic Tac Toe")
    z = int(input("choose from the menu:"))
    if z == 1:
        hp.start()
    elif z == 2:
        #ttt.start()
        pass
    else:
        print("Invalid Input")