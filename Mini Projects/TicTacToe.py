class Tic:
    def __init__(self):
        self.board = self.make_board()

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_num():
        num_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in num_board:
            print("| " + " | ".join(row) + " |")


game = Tic
print(game.print_board())
