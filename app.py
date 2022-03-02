from flask import Flask, render_template, request, redirect
from models import Board, Piece
from minimax import minimax
from datetime import datetime

app = Flask(__name__)
board = Board()

pieces = [("rook", 5.0),
        ("knight", 3.0), 
        ("bishop", 3.0),
        ("king", 500.0),
        ("queen", 10.0),
        ("bishop", 3.0), 
        ("knight", 3.0), 
        ("rook", 5.0)]
pawn = ("pawn", 1.0)
teams = ("white", "black")

for i in range(8):
    name, worth = pieces[i]
    board.add_piece((0, i), Piece(name, teams[0], worth))
    board.add_piece((1, i), Piece(pawn[0], teams[0], pawn[1]))
    board.add_piece((7, i), Piece(name, teams[1], worth))
    board.add_piece((6, i), Piece(pawn[0], teams[1], pawn[1]))

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
            print("State for maximizing: ",state)
            if state > max_state:
                max_state = state
                position, destinaton = pos, des
            
            alpha = max(alpha, state)
            if beta <= alpha:
                print("broken")
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
            print("State for minimizing: ",state)
            if state < min_state:
                min_state = state
                position, destinaton = pos, des
            beta = min(beta, state)
            if beta <= alpha:
                print("broken")
                break

        board.make_move(position, destinaton)
        time_taken = datetime.now() - time_start
        return redirect('/')

        
if __name__ == "__main__":
    app.run(debug=True)