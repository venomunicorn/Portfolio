import random
import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)] # 0-8
        self.human = 'X'
        self.ai = 'O'
    
    def print_board(self):
        print(f"\n {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} \n")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        return False

    def winner(self, square, letter):
        # check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # check col
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]] 
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]] 
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

def minimax(game, state):
    player = state['player']
    
    # Base cases
    if game.winner(state['last_move'], game.human):
        return {'position': None, 'score': -1 * (game.num_empty_squares() + 1)}
    elif game.winner(state['last_move'], game.ai):
        return {'position': None, 'score': 1 * (game.num_empty_squares() + 1)}
    elif not game.empty_squares():
        return {'position': None, 'score': 0}

    if player == game.ai:
        best = {'position': None, 'score': -math.inf} 
    else:
        best = {'position': None, 'score': math.inf}

    for possible_move in game.available_moves():
        # Make move
        game.make_move(possible_move, player)
        
        # Recurse
        sim_score = minimax(game, {'player': game.human if player == game.ai else game.ai, 'last_move': possible_move})
        
        # Undo move
        game.board[possible_move] = ' '
        sim_score['position'] = possible_move

        if player == game.ai:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
                
    return best

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board()

    letter = 'X' # starting letter
    while game.empty_squares():
        if letter == 'O':
            # AI Move
            print("AI (O) is thinking...")
            try:
                # First move hack for speed
                if len(game.available_moves()) == 9:
                    square = 4 # Center
                else: 
                     # pass previous move for winner check opt
                    square = minimax(game, {'player': 'O', 'last_move': -1})['position']
            except:
                square = random.choice(game.available_moves())
        else:
            # Human Move
            valid_square = False
            while not valid_square:
                square_val = input(f'{letter}\'s turn. Input move (0-8): ')
                try:
                    square = int(square_val)
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print('Invalid square. Try again.')

        if game.make_move(square, letter):
            if print_game:
                print(f'{letter} makes a move to square {square}')
                game.print_board()
                print('')

            if game.winner(square, letter):
                if print_game:
                    print(f'{letter} wins!')
                return letter  

            letter = 'O' if letter == 'X' else 'X'  # switch player

        if not game.empty_squares():
            print('It\'s a tie!')
            return 'Tie'

if __name__ == '__main__':
    t = TicTacToe()
    print("Welcome to Tic Tac Toe vs AI!")
    print("Board Positions: 0-8")
    play(t, 'human', 'ai')
