import random
from collections import Counter

class HangmanGame:

    def __init__(self):
        """
        A simple Hangman game with hints based on fruit colors.
        Player guesses letters until they discover the hidden word.
        """
        # Dictionary: word -> hint (fruit color description)
        self.wordlist = {
            "apple": "color: red",
            "banana": "color: yellow",
            "mango": "color: orange",
            "orange": "color: orange",
            "grape": "color: purple",
            "strawberry": "color: red",
            "pineapple": "color: yellow",
            "watermelon": "colors: green outside, red inside",
            "melon": "colors: green outside, orange inside",
            "peach": "color: pink-orange",
            "pear": "color: green",
            "cherry": "color: red",
            "kiwi": "colors: brown outside, green inside",
            "lemon": "color: yellow",
            "lime": "color: green",
            "coconut": "colors: brown outside, white inside",
            "papaya": "color: orange",
            "guava": "colors: green outside, pink inside",
            "pomegranate": "color: red",
            "fig": "color: purple",
            "date": "color: brown",
            "blueberry": "color: blue",
            "raspberry": "color: red",
            "blackberry": "color: black",
            "cranberry": "color: red",
            "grapefruit": "color: pink",
            "tangerine": "color: orange",
            "mandarin": "color: orange",
            "avocado": "color: green",
            "passionfruit": "color: purple",
            "dragonfruit": "color: pink"
        }

        # Hangman visual stages (wrong guesses progression)
        self.stages = [
'''
  -----
  |   |
      |
      |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
      |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
  |   |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|   |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|\\  |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|\\  |
 /    |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
---------
'''
        ]

    def start(self):
        """
        Starts the Hangman game loop.
        Randomly selects a word and handles user guesses.
        """
        # Pick random (word, hint)
        word, hint = random.choice(list(self.wordlist.items()))
        print('Guess the word! HINT: word is a fruit.')

        # Display hidden word
        for _ in word:
            print('_', end=' ')
        print()

        letterGuessed = '' # stores correct guessed letters
        wrong_guesses = 0
        max_chances = len(self.stages) - 1

        try:
            while wrong_guesses < max_chances:
                print()
                guess = input('Enter a letter to guess: ').lower()

                # Validate input
                if not self.validate_input(guess, letterGuessed):
                    continue

                # Correct guess
                if guess in word:
                    letterGuessed += guess * word.count(guess)
                # Wrong guess
                else:
                    wrong_guesses += 1
                    print(self.stages[wrong_guesses])

                    # Show hint before the last chance
                    if wrong_guesses == (max_chances - 1):
                        print(f"\n Hint! {hint} ")

                # Show current progress
                self.display_word(word, letterGuessed)
                print()

                # Check win condition
                if self.check_win(letterGuessed, word):
                    print("\nCongratulations! You guessed the word:", word)
                    break

            # Lose condition
            if wrong_guesses == max_chances:
                print('\nYou lost! The word was:', word)

        except KeyboardInterrupt:
            print('\nGame interrupted. Bye!')

    def display_word(self, word:str, letterGuessed:str) -> str:
        """
        Displays the word with underscores for unguessed letters.
        """
        result = []
        for char in word:
            if char in letterGuessed:
                result.append(char)
            else:
                result.append('_')
        return " ".join(result)

    def check_win(self, letterGuessed:str, word:str) -> bool:
        """
        Checks if player has guessed the full word correctly.
        """
        return Counter(letterGuessed) == Counter(word)

    def validate_input(self, guess:str, letterGuessed:str):
        """
        Ensures input is a single valid letter and not repeated.
        """
        if not guess.isalpha():
            return 'Enter only a letter!'
        elif not guess.isascii():
            return 'Enter only English letter!'
        elif len(guess) > 1:
            return 'Enter only a single letter!'
        elif guess in letterGuessed:
            return 'You already guessed that letter!'

        return True