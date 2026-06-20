import random
class Wordle:
  def __init__(self):
    self.Attemps = 6 #number of allowed attempts to guess the word
    self.guess = "" #user guessing
    self.word = self._word_of_the_day().lower() #this function stores the word
  def _word_of_the_day(self):
      words_list = [
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
      random_selection = random.randint(0,99)
      word_chosen_for_today = words_list[random_selection]
      return word_chosen_for_today

  def _checking_guess_length(self, guess):
      return len(guess)

  def  _in_word(self, letter, word):
      if letter in word:
          return True
      else:
        return False

  def  _right_position(self,answer,letter, word):
        if self._in_word(letter, word)== True and answer.find(letter) == word.find(letter):
          return True

  def  _wrong_position(self, answer,letter, word):
      if self._in_word(letter, word)== True and answer.find(letter) != word.find(letter):
          return True
  def _bring_index(self, actual_answer, letter, pos):
      index_of_the_word = actual_answer.find(letter, pos)
      return index_of_the_word


  def start(self):

      #starting the game now
      while self.Attemps > 0:
        user_guess_list = [""] *5 #creating a list of 5 empty positions to store the answer
                #while the user did not guess the answer correctly from the first time
        guess = input(str("Enter Your Guess (input should be 5 letters long):")).lower()#ensuring that everything inputed is lower case to avoid any miss counting from same letters
        if (self._checking_guess_length(guess) == 5 and guess.isalpha()== True):
                pos =0
                for letter in guess:
                    if self._right_position(guess, letter, self.word) == True :
                        index = self._bring_index(guess, letter, pos)
                        user_guess_list[index] = letter.upper()

                    elif self._wrong_position(guess ,letter, self.word) == True:
                          index = self._bring_index(guess , letter, pos)
                          user_guess_list[index] = "*"+ letter.lower()+"*"
                    else:
                      user_guess_list[pos] = "_" + letter + "_"
                    pos += 1
                print(f"{user_guess_list}")
                if guess == self.word:
                  print(f"The Word of the day is {guess} You Won! Congrats")
                  break

        else:
                f"Output is unacceptable"

      self.Attemps -=1
      print(f"You Have {str(self.Attemps)} Attempt(s) Left")
      if self.Attemps == 0:
          print(f"Game Over, You Lost")
          print(f"The Word Of Today Is {self.word}")

wo = wordle()
wo.start()