from flask import Flask, render_template, request, redirect
from models import Board
from pieces import *
from minimax import minimax
from datetime import datetime

app = Flask(__name__)
board = Board()
normalization_factor = 4
pieces = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
teams = ("white", "black")

for i in range(8):
    piece = pieces[i]
    board.add_piece((0, i), piece(teams[0]))
    board.add_piece((1, i), Pawn(teams[0]))
    board.add_piece((7, i), piece(teams[1]))
    board.add_piece((6, i), Pawn(teams[1]))

board.evaluate_worths()

time_taken = 0


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        position = request.form['position']
        destination = request.form['destination']
        position = tuple(map(lambda x: int(x)-1, position.split(",")))
        destination = tuple(map(lambda x: int(x)-1, destination.split(",")))
        board.make_move(position, destination)
        return redirect('/')

    else:
        return render_template('chess.html', board=board, time_taken=time_taken)

@app.route('/compute-move', methods=['POST'])
def compute_move():
    global time_taken
    time_start = datetime.now()

    depth = int(request.form['depth'])
    player = request.form['player']
    alpha = float("-inf")
    beta = float("inf")
    if player == "white":
        max_state = float("-inf")
        position = None
        destinaton = None
        for pos, des in board.max_player_moves:
            state = minimax(pos, des, board, True, alpha=alpha, beta=beta, depth=depth-1)
            # print("State for maximizing: ",state)
            if state > max_state:
                max_state = state
                position, destinaton = pos, des
            
            alpha = max(alpha, state)
            if beta <= alpha:
                break

        board.make_move(position, destinaton)
        time_taken = datetime.now() - time_start
        return redirect('/')
    else:
        min_state = float("inf")
        position = None
        destinaton = None
        for pos, des in board.min_player_moves:
            state = minimax(pos, des, board, False, alpha=alpha, beta=beta, depth=depth-1)
            # print("State for minimizing: ",state)
            if state < min_state:
                min_state = state
                position, destinaton = pos, des
            beta = min(beta, state)
            if beta <= alpha:
                break

        board.make_move(position, destinaton)
        time_taken = datetime.now() - time_start
        return redirect('/')

        
if __name__ == "__main__":
    app.run(debug=True)