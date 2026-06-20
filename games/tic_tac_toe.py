class TicTacToe:
    def __init__(self):
        # This list represents the Tic tac toe board
        self.board = ["-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"]

        # X starts the game first
        self.current_player = "X"

        # At the beginning, there is no winner
        self.winner = None

        # This controls if the game is still running
        self.game_running = True

        # Lambda function to create a player message
        self.player_message = lambda player: f"Player {player}, enter a number 1-9: "

    # This method starts and runs the game
    def start(self):
        print("Welcome to Tic Tac Toe!")

        while self.game_running:
            self._print_board()
            self._player_input()
            self._check_win()
            self._check_tie()

            if self.game_running:
                self._switch_player()

    # This method prints the board
    def _print_board(self):
        print(self.board[0] + " | " + self.board[1] + " | " + self.board[2])
        print("----------")
        print(self.board[3] + " | " + self.board[4] + " | " + self.board[5])
        print("----------")
        print(self.board[6] + " | " + self.board[7] + " | " + self.board[8])

    # This method takes input from the player
    def _player_input(self):
        choice = int(input(self.player_message(self.current_player)))

        if choice >= 1 and choice <= 9 and self.board[choice - 1] == "-":
            self.board[choice - 1] = self.current_player
        else:
            print("This spot is already taken!")

    # This method checks the horizontal lines
    def _check_horizontal(self):
        if self.board[0] == self.board[1] == self.board[2] and self.board[0] != "-":
            self.winner = self.board[0]
            return True
        elif self.board[3] == self.board[4] == self.board[5] and self.board[3] != "-":
            self.winner = self.board[3]
            return True
        elif self.board[6] == self.board[7] == self.board[8] and self.board[6] != "-":
            self.winner = self.board[6]
            return True

    # This method checks the vertical lines
    def _check_vertical(self):
        if self.board[0] == self.board[3] == self.board[6] and self.board[0] != "-":
            self.winner = self.board[0]
            return True
        elif self.board[1] == self.board[4] == self.board[7] and self.board[1] != "-":
            self.winner = self.board[1]
            return True
        elif self.board[2] == self.board[5] == self.board[8] and self.board[2] != "-":
            self.winner = self.board[2]
            return True

    # This method checks the diagonal lines
    def _check_diagonal(self):
        if self.board[0] == self.board[4] == self.board[8] and self.board[0] != "-":
            self.winner = self.board[0]
            return True
        elif self.board[2] == self.board[4] == self.board[6] and self.board[2] != "-":
            self.winner = self.board[2]
            return True

    # This method checks if there is a tie
    def _check_tie(self):
        if "-" not in self.board and self.winner is None:
            self._print_board()
            print("It is a tie!")
            self.game_running = False

    # This method checks if there is a winner
    def _check_win(self):
        if self._check_diagonal() or self._check_horizontal() or self._check_vertical():
            self._print_board()
            print(f"The winner is {self.winner}")
            self.game_running = False

    # This method switches between X and O
    def _switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"