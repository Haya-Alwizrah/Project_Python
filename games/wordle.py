import random
class Wordle:
    '''
    Rules of The Game:
    -6 Attwmpts to guess a hidden 5-letter word.
    - (D)   Uppercase indicate the correct letter in the correct position
    - (*d*) Asterisks indicate the letter in the word but in the wrong position
    - (_d_) Underscore indicate that the letter does not exist in the word
    '''
    def __init__(self):
        self.Attempts = 6 #number of attempts each user is allowed before they lose
        self.guess = ""
        self.word = self._word_of_the_day().lower() # ensure each word is all in lower case
      
    def _word_of_the_day(self):
        '''
        returns a word chosen randomly from the words list.

        '''
        words_list = [ #list consist of 100 words, each is 5 letters long
            "Apple", "Bread", "Chair", "Dance", "Eagle", "Faith", "Giant", "House", "Image", "Jelly",
            "Knife", "Lemon", "Mango", "Night", "Ocean", "Piano", "Queen", "River", "Smile", "Tiger",
            "Under", "Visit", "Whale", "Youth", "Zebra", "Alert", "Brave", "Cloud", "Dream", "Earth",
            "Frost", "Grace", "Heart", "Ideal", "Judge", "Kneel", "Light", "Magic", "Noble", "Olive",
            "Proud", "Quick", "Rough", "Sweet", "Trust", "Unity", "Value", "World", "Yield", "Zesty",
            "Angle", "Blaze", "Crane", "Drift", "Enjoy", "Flame", "Glory", "Humor", "Ivory", "Jolly",
            "Karma", "Lucky", "Merry", "Novel", "Opine", "Pilot", "Quiet", "Relay", "Shiny", "Topic",
            "Urban", "Vivid", "Witty", "Xenon", "Young", "Zonal", "Adapt", "Begin", "Catch", "Delay",
            "Entry", "Fresh", "Greet", "Habit", "Infer", "Joint", "Known", "Learn", "Model", "North",
            "Order", "Peace", "Quest", "Reach", "Scale", "Teach", "Usage", "Voice", "Watch", "Write"
        ]
        return random.choice(words_list).lower()  #brings the word from the word list randomly

    def  _letter_in_word(self, letter, word):
        '''
        checks if a letter in the word.
        '''
        if letter in word:
              return True
        else:
            return False

    def  _right_position(self,letter, word, guess):
        '''
        checks if the letter exist in the right position.

        '''
        if self._letter_in_word(letter, word)== True and guess.find(letter) == word.find(letter):
              return True

    def  _wrong_position(self,letter, word, guess):
        '''
        checks if the letter in the word but in the wrong position.

        '''
        if self._letter_in_word(letter, word)== True and guess.find(letter) != word.find(letter):
              return True
        
    def _bring_index(self, guess, letter, position):
        '''
        return the position of each letter found in the user answer

        '''
        index_of_the_word = guess.find(letter, position)
        return index_of_the_word


    def start(self):
        #starting the game now
        while self.Attempts > 0:
            guess = input("Enter Your Guess (input should be 5 letters long):").lower() #ensuring that everything inputed is lower case to avoid any miss counting from same letters
            
            if len(guess) != 5 or not guess.isalpha() or not guess.isascii(): #checks if the input is 5 letter long and all alphabetic
                print("Invalid input. Please enter exactly 5 English alphabetic letters.")

            else:
                user_guess_list = [""] * 5 #creating a list of 5 empty slots to store the answer while the user did not guess the answer correctly from the first time
                position =0

                for i, letter in enumerate(guess):
                    # Case A -> correct letter in the correct positon (uppercase)
                    if self._right_position(letter, self.word, guess) == True :
                        user_guess_list[i] = letter.upper()

                    # Case B -> correct letter in the wrong position (Asteriks)
                    elif self._wrong_position(letter, self.word, guess) == True:
                        user_guess_list[i] = "*"+ letter.lower()+"*"

                    # Case C -> letter does not exist in the word (Underscore)
                    else:
                        user_guess_list[i] = "_" + letter + "_"
                    
                    position += 1 #since .find() and .index() only return the first occurance of the letter, sometimes the word contain the same letter twice like in (attic), position used to track the position of each letter so repeated letter are counted too
                
                print(f"{user_guess_list}") #display the current guess list made
                self.Attempts -=1
                print(f"You Have {self.Attempts} Attempt(s) Left")
                
                if guess == self.word:
                    print(f"The Word of the Day is {guess} You Won! Congrats")
                    break

        if self.Attempts == 0:
            print(f"Game Over, You Lost")
            print(f"The Word Of Today Is {self.word}")
            
    '''
    Reflection:
    What was the most challenging part?
    - Differentiating between the position of two same letters in the word like (attic) 
    
    Which concept did you enjoy the most?
    - Creating the game and making it interactive with the user
    - customizing the output to make it more user friendly and easy to understand
    
    What would you improve if you had more time?
    - Checking if the word exist in the dictionary or not
    - Game in Arabic
    - Specific theme that the people can choose, like guessing programming concepts, or medical terms
    '''
    