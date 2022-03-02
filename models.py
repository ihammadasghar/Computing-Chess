from pieces import Pawn, King

class Cell:
    def __init__(self, piece=None) -> None:
        self.piece = piece
        self.worth = 0
        

class Piece:
    def __init__(self, name, team, points) -> None:
        self.name = name
        self.team = team
        self.points = points
        self.image = f"{name}-{team}.png"


class Board:
    def __init__(self) -> None:
        self.cells = {(0,0): Cell(), (0,1): Cell(), (0,2): Cell(), (0,3): Cell(), (0,4): Cell(), (0,5): Cell(), (0,6): Cell(), (0,7): Cell(), 
                    (1,0): Cell(), (1,1): Cell(), (1,2): Cell(), (1,3): Cell(), (1,4): Cell(), (1,5): Cell(), (1,6): Cell(), (1,7): Cell(), 
                    (2,0): Cell(), (2,1): Cell(), (2,2): Cell(), (2,3): Cell(), (2,4): Cell(), (2,5): Cell(), (2,6): Cell(), (2,7): Cell(), 
                    (3,0): Cell(), (3,1): Cell(), (3,2): Cell(), (3,3): Cell(), (3,4): Cell(), (3,5): Cell(), (3,6): Cell(), (3,7): Cell(), 
                    (4,0): Cell(), (4,1): Cell(), (4,2): Cell(), (4,3): Cell(), (4,4): Cell(), (4,5): Cell(), (4,6): Cell(), (4,7): Cell(), 
                    (5,0): Cell(), (5,1): Cell(), (5,2): Cell(), (5,3): Cell(), (5,4): Cell(), (5,5): Cell(), (5,6): Cell(), (5,7): Cell(), 
                    (6,0): Cell(), (6,1): Cell(), (6,2): Cell(), (6,3): Cell(), (6,4): Cell(), (6,5): Cell(), (6,6): Cell(), (6,7): Cell(), 
                    (7,0): Cell(), (7,1): Cell(), (7,2): Cell(), (7,3): Cell(), (7,4): Cell(), (7,5): Cell(), (7,6): Cell(), (7,7): Cell() }
        
        self.max_player_moves = []
        self.min_player_moves = []
        self.max_total_points = 0
        self.min_total_points = 0
        self.piece_positions = {}
        self.state = 0
        self.game_over = False
            

    def set_state(self, board):
        for piece, position in board.piece_positions.items():
            self.add_piece(position, piece)


    def add_piece(self, position, piece):
        self.cells[position].piece = piece
        if piece.team == "white":
            self.max_total_points += piece.points
        else:
            self.min_total_points += piece.points
        self.piece_positions[piece] = position


    def make_move(self, position, destination):
        cell = self.cells[position]
        piece = cell.piece

        destination_cell = self.cells[destination]
        destination_piece = destination_cell.piece
        #  Capturing
        if destination_piece:
            del self.piece_positions[destination_piece]
            if destination_piece.team == "white":
                self.max_total_points -= destination_piece.points
            else:
                self.min_total_points -= destination_piece.points
            #  Game Ended
            if type(destination_piece) == King:
                self.game_over = True
        
        # Replace piece
        self.piece_positions[piece] = destination
        self.cells[destination].piece = piece
        self.cells[position].piece = None

        # Resets
        self.cells[position].worth = 0
        self.max_player_moves = []
        self.min_player_moves = []
        self.evaluate_worths()

        return False


    def evaluate_worths(self):
        self.state = self.max_total_points - self.min_total_points
        for piece, position in self.piece_positions.items():
            #  Reset
            self.cells[position].worth = 0

            #  Caculate ranges and possible moves
            piece.calculate_range(position, self)

        self.state += (len(self.max_player_moves) - len(self.min_player_moves))//10


    def optimize_state(self, position, destination):
        row, col = destination
        #  Out of board
        if not ((0 <= row <=7) and (0 <= col <=7)):
            return True

        cell = self.cells[position]
        piece = cell.piece
        in_range_cell = self.cells[destination]
        in_range_piece = in_range_cell.piece

        #  If there is a piece in the destination
        if in_range_piece:
            #  Enemy Piece
            #  In range points

            if in_range_piece.team != piece.team:
                advantage = in_range_piece.points//10
                cell.worth += advantage
                if piece.team == "white":
                    self.state += cell.worth
                    #  If a good trade increase priority
                    if piece.points <= in_range_piece.points:
                        self.max_player_moves.insert(0, (position, destination))
                    else:
                        self.max_player_moves.append((position, destination))
                else:
                    self.state -= cell.worth
                    #  If a good trade then increase priority
                    if piece.points <= in_range_piece.points:
                        self.min_player_moves.insert(0, (position, destination))
                    else:
                        self.min_player_moves.append((position, destination))
                return True

            #  Own piece
            return True

        if type(piece) == Pawn:
            return False

        if piece.team == "white":
            self.max_player_moves.append((position, destination))
        else:
            self.min_player_moves.append((position, destination))
        return False
