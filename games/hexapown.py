import random

class HexaPown:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [
            ["X", "X", "X"],
            [" ", " ", " "],
            ["O", "O", "O"]
        ]
        self.winner = None
        self.player = random.choice(["X", "O"])

    def start(self):
        self._print_board()
        while self.winner == None:
            
            available_moves = self._available_moves()
            self.winner = self._check_winner(available_moves)

            if self.winner != None:
                print(f"Player '{self.winner}' wins!")
            else:
                selected_move = self._select_move(available_moves)
                self._move(selected_move)
                self._print_board()
                self.player = "O" if self.player == "X" else "X"

    def _print_board(self):
        for i in self.board:
            print(i)

    def _players_position(self) -> list[tuple]:
        x_position = []
        o_position = []
        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if column == "X":
                    x_position.append((i,j))
                elif column == "O":
                    o_position.append((i,j))
        return x_position, o_position

    def _inside_board(self, i:int, j:int)-> bool:
        return 0 <= i < 3 and 0 <= j < 3

    def _available_moves(self)-> list[tuple[tuple]]:
        x_position, o_position = self._players_position()
        if self.player == "X":
            move_dirction = 1
            position = x_position
            enemy = "O"
        else:
            move_dirction = -1
            position = o_position
            enemy = "X"

        available_moves = []

        for i,j in position:
            new_i, new_j = i+move_dirction, j
            if self._inside_board(new_i, new_j) and self.board[new_i][new_j] == " ":
                available_moves.append(((i, j), (new_i, new_j)))

            for z in (1,-1):
                new_i, new_j = i+move_dirction, j+z
                if self._inside_board(new_i, new_j) and self.board[new_i][new_j] == enemy:
                    available_moves.append(((i, j), (new_i, new_j)))

        return available_moves

    def _check_winner(self, available_moves) -> str:
        if "X" in self.board[2]:
            return "X"
        elif "O" in self.board[0]:
            return "O"
        elif len(available_moves) == 0:
            return "O" if self.player == "X"else "X"
        else:
            return None
        
    def _select_move(self, available_moves)-> tuple[tuple]:
        print(f"'{self.player}' choose the number of the movement you want:")
        for i, move in enumerate(available_moves):
            print(f"- {i+1}: {move}")
        user_choose = input()

        while not (user_choose.isdigit() and 1 <= int(user_choose) <= len(available_moves)):
            print("Invalid input. Please choose a valid number:")
            user_choose = input()

        for i, move in enumerate(available_moves):
            if i+1 == int(user_choose):
                return move

    def _move(self, selected_move):
        old_position, new_position = selected_move
        old_i , old_j = old_position
        new_i , new_j = new_position

        self.board[old_i][old_j] = " "
        self.board[new_i][new_j] = self.player
