# Task 6


class TictactoeException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class Board:
    valid_moves = [
        "upper left",
        "upper center",
        "upper right",
        "middle left",
        "center",
        "middle right",
        "lower left",
        "lower center",
        "lower right",
    ]

    def __init__(self) -> None:
        self.board_array = [[" "] * 3 for _ in range(3)]
        self.turn = "X"
        self.last_move = ""

    def __str__(self) -> str:
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    def move(self, move_string: str) -> None:
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row, column = move_index // 3, move_index % 3
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][column] = self.turn
        self.last_move = move_string
        self.turn = "O" if self.turn == "X" else "X"

    def _has_win(self) -> bool:
        for i in range(3):
            if self.board_array[i][0] != " ":
                if self.board_array[i][0] == self.board_array[i][1] == self.board_array[i][2]:
                    return True
        for i in range(3):
            if self.board_array[0][i] != " ":
                if self.board_array[0][i] == self.board_array[1][i] == self.board_array[2][i]:
                    return True
        if self.board_array[1][1] != " ":
            if self.board_array[0][0] == self.board_array[1][1] == self.board_array[2][2]:
                return True
            if self.board_array[0][2] == self.board_array[1][1] == self.board_array[2][0]:
                return True
        return False

    def _board_full(self) -> bool:
        return all(cell != " " for row in self.board_array for cell in row)

    def whats_next(self) -> tuple[bool, str]:
        if self._has_win():
            if self.turn == "O":
                return (True, "X wins!")
            return (True, "O wins!")
        if self._board_full():
            return (True, "Cat's Game.")
        if self.turn == "X":
            return (False, "X's turn.")
        return (False, "O's turn.")


if __name__ == "__main__":
    board = Board()
    print(board)
    done, status = board.whats_next()
    while not done:
        print(status)
        try:
            move = input("Enter your move: ").strip()
            board.move(move)
        except TictactoeException as exc:
            print(exc.message)
            continue
        print(board)
        done, status = board.whats_next()
    print(status)
