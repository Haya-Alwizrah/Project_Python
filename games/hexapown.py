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

    def _available_moves(self)-> dict[list[tuple]]:
        x_position, o_position = self._players_position()
        if self.player == "X":
            move_dirction = 1
            position = x_position
            enemy = "O"
        else:
            move_dirction = -1
            position = o_position
            enemy = "X"

        available_moves = {}

        for i,j in position:
            available_moves[(i,j)] = []

            new_i, new_j = i+move_dirction, j
            if self._inside_board(new_i, new_j) and self.board[new_i][new_j] == " ":
                available_moves[(i,j)].append((new_i, new_j))

            for z in (1,-1):
                new_i, new_j = i+move_dirction, j+z
                if self._inside_board(new_i, new_j) and self.board[new_i][new_j] == enemy:
                    available_moves[(i,j)].append((new_i, new_j))

            if len(available_moves[(i, j)]) == 0:
                del available_moves[(i, j)]

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

    def _move(self, from_pos, to_pos):
        available_moves = self._available_moves()

        if from_pos not in available_moves or to_pos not in available_moves[from_pos]:
            return False
    
        old_i , old_j = from_pos
        new_i , new_j = to_pos

        self.board[old_i][old_j] = " "
        self.board[new_i][new_j] = self.player

        self.player = "O" if self.player == "X" else "X"

        return True
    
    def get_state(self):
        available_moves = self._available_moves()
        winner = self._check_winner(available_moves)
        movable_pieces = [list(pos) for pos in available_moves.keys()]
        
        return {
            'board': self.board,
            'player': self.player,
            'winner': winner,
            'movable_pieces': movable_pieces
        }
    

# For testing in console -------------------------------------------------------------------
    def start(self):
        self._print_board()
        while self.winner == None:
            
            available_moves = self._available_moves()
            self.winner = self._check_winner(available_moves)

            if self.winner != None:
                print(f"Player '{self.winner}' wins!")
            else:
                print(available_moves)
                from_row = int(input("from row: "))
                from_col = int(input("from col: "))
                to_row = int(input("to row: "))
                to_col = int(input("to col: "))
                self._move((from_row, from_col),(to_row, to_col))
                self._print_board()

    def _print_board(self):
        for i in self.board:
            print(i)

#x = HexaPown()
#x.start()