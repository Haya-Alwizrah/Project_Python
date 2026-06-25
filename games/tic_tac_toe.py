class TicTacToe:
    def __init__(self):
        # This list represents the Tic Tac Toe board
        self.board = ["-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"]

        # X starts the game first
        self.current_player = "X"

        # At the beginning, there is no winner
        self.winner = None

        # This controls if the game is still running
        self.game_running = True

        # Lambda function to create player turn message
        self.player_message = lambda player: f"Player {player}'s turn"

    # This method takes the player's move from the webpage
    def make_move(self, position:int):
        if position < 0 or position > 8:
            return

        if self.game_running and self.board[position] == "-":
            self.board[position] = self.current_player
            self.check_win()
            self.check_tie()

            if self.game_running:
                self.switch_player()

    # This method checks the horizontal lines
    def check_horizontal(self) -> bool:
        if self.board[0] == self.board[1] == self.board[2] and self.board[0] != "-":
            self.winner = self.board[0]
            return True
        elif self.board[3] == self.board[4] == self.board[5] and self.board[3] != "-":
            self.winner = self.board[3]
            return True
        elif self.board[6] == self.board[7] == self.board[8] and self.board[6] != "-":
            self.winner = self.board[6]
            return True
        return False

    # This method checks the vertical lines
    def check_vertical(self) -> bool:
        if self.board[0] == self.board[3] == self.board[6] and self.board[0] != "-":
            self.winner = self.board[0]
            return True
        elif self.board[1] == self.board[4] == self.board[7] and self.board[1] != "-":
            self.winner = self.board[1]
            return True
        elif self.board[2] == self.board[5] == self.board[8] and self.board[2] != "-":
            self.winner = self.board[2]
            return True
        return False

    # This method checks the diagonal lines
    def check_diagonal(self) -> bool:
        if self.board[0] == self.board[4] == self.board[8] and self.board[0] != "-":
            self.winner = self.board[0]
            return True
        elif self.board[2] == self.board[4] == self.board[6] and self.board[2] != "-":
            self.winner = self.board[2]
            return True
        return False

    # This method checks if there is a tie
    def check_tie(self) -> bool:
        if "-" not in self.board and self.winner is None:
            self.game_running = False

    # This method checks if there is a winner
    def check_win(self) -> bool:
        if self.check_diagonal() or self.check_horizontal() or self.check_vertical():
            self.game_running = False

    # This method switches between X and O
    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    # This method returns the game status message
    def get_status(self) -> str:
        if self.winner:
            return f"The winner is {self.winner}"
        elif not self.game_running:
            return "It is a tie!"
        else:
            return self.player_message(self.current_player)

    # This method resets the game
    def reset(self):
        self.board = ["-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"]
        self.current_player = "X"
        self.winner = None
        self.game_running = True

"""
Reflection:
- The most challenging part was checking all winning conditions correctly.
- The concept I enjoyed the most was using functions and organizing the code inside a class.
- If I had more time, I would add a score system to keep track of each player's wins.
"""
