teams = ("white", "black")

class Player:
    def __init__(self, name, team) -> None:
        self.name = name
        self.team = team

class Cell:
    def __init__(self, piece=None) -> None:
        self.piece = piece
        self.worth = 0.0


class Piece:
    def __init__(self, name, team, points) -> None:
        self.name = name
        self.team = team
        self.points = points


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
        self.piece_positions = {}
        self.state = 0.0
            

    def set_state(self, board):
        self.state = board.state
        self.max_player_moves = board.max_player_moves
        self.min_player_moves = board.min_player_moves

        for piece, position in board.piece_positions.items():
            self.add_piece(position, piece)
            self.cells[position].worth = board.cells[position].worth


    def add_piece(self, position, piece):
        self.cells[position].piece = piece
        self.piece_positions[piece] = position


    def make_move(self, position, destination):
        cell = self.cells[position]
        piece = cell.piece

        if piece == teams[0]:
            self.state -= cell.worth - piece.points
        else:
            self.state += cell.worth - piece.points

        destination_cell = self.cells[destination]
        destination_piece = destination_cell.piece
        #  Capturing
        if destination_piece:
            self.piece_positions.pop(destination_piece)
            if destination_piece.team == teams[0]:
                self.state -= (destination_cell.worth - destination_piece.points)
                self.state -= destination_piece.points
            else:
                self.state += (destination_cell.worth - destination_piece.points)
                self.state += destination_piece.points

            #  Game Ended
            if destination_piece.name == "king":
                return True
        
        self.piece_positions[piece] = destination
        self.cells[destination].piece = piece
        self.cells[position].piece = None
        self.max_player_moves = []
        self.min_player_moves = []
        self.evaluate_worths()

        return False


    def evaluate_worths(self):
        for piece, position in self.piece_positions.items():
            #  Reset
            self.cells[position].worth = piece.points

            #  Caculate ranges and possible moves
            if piece.name == "queen":
                self.calculate_queen_range(position)
            elif piece.name == "king":
                self.calculate_king_range(position)
            elif piece.name == "knight":
                self.calculate_knight_range(position)
            elif piece.name == "bishop":
                self.calculate_x_range(position)
            elif piece.name == "rook":
                self.calculate_plus_range(position)
            elif piece.name == "pawn":
                self.calculate_pawn_range(position)


    def check_and_update_worth(self, position, destination):
        row, col = destination
        #  Out of board
        if not (0 <= row <=7) or not (0 <= col <=7):
            return True

        cell = self.cells[position]
        piece = cell.piece
        in_range_cell = self.cells[destination]
        in_range_piece = in_range_cell.piece
        if in_range_piece:
            if in_range_piece.team != piece.team:
                in_range_advantage = in_range_cell.worth/2

                cell.worth += in_range_advantage
                if piece.team == teams[0]:
                    self.state += in_range_advantage
                    self.max_player_moves.append((position, destination))
                else:
                    self.state -= in_range_advantage
                    self.min_player_moves.append((position, destination))
                    
                return True
            return True

        if piece.name == "pawn":
            return False

        if piece.team == teams[0]:
            self.max_player_moves.append((position, destination))
        else:
            self.min_player_moves.append((position, destination))
        return False


    def calculate_queen_range(self, position):
        self.calculate_plus_range(position)
        self.calculate_x_range(position)


    def calculate_plus_range(self, position):
        row, col = position

        up = True
        down = True
        left = True
        right = True
        for i in range(1, 8):
            if up:
                is_End_or_Blocked = self.check_and_update_worth(position, (row-i, col))
                up = not is_End_or_Blocked
            
            if down:
                is_End_or_Blocked = self.check_and_update_worth(position, (row+i, col))
                down = not is_End_or_Blocked

            if left:
                is_End_or_Blocked = self.check_and_update_worth(position, (row, col-i))
                left = not is_End_or_Blocked

            if right:
                is_End_or_Blocked = self.check_and_update_worth(position, (row, col+i))
                right = not is_End_or_Blocked


    def calculate_x_range(self, position):
        row, col = position
        
        top_left = True
        top_right = True
        bottom_left = True
        bottom_right = True
        for i in range(1, 8):
            if top_left:
                is_End_or_Blocked = self.check_and_update_worth(position, (row-i, col-i))
                top_left = not is_End_or_Blocked
            
            if top_right:
                is_End_or_Blocked = self.check_and_update_worth(position, (row-i, col+i))
                top_right = not is_End_or_Blocked

            if bottom_left:
                is_End_or_Blocked = self.check_and_update_worth(position, (row+i, col-i))
                bottom_left = not is_End_or_Blocked

            if bottom_right:
                is_End_or_Blocked = self.check_and_update_worth(position, (row+i, col+i))
                bottom_right = not is_End_or_Blocked
            

    def calculate_knight_range(self, position):
        row, col = position
        destinations = [(row-2, col-1), (row-2, col+1),
                    (row-1, col-2), (row-1, col+2),
                    (row+1, col-2), (row+1, col+2),
                    (row+2, col-1), (row+2, col+1),
                    ]
        for destination in destinations:
            self.check_and_update_worth(position, destination)


    def calculate_pawn_range(self, position):
        cell = self.cells[position]
        team = cell.piece.team
        row, col = position
        destinations = [(row+1, col-1), (row+1, col+1)] if team == teams[0] else [(row-1, col-1), (row-1, col+1)]
        for destination in destinations:
            self.check_and_update_worth(position, destination)
        
        forward = (row+1, col) if team == teams[0] else (row-1, col)
        fr, fc = forward
        if 0 <= fr <= 7:
            if self.cells[(fr, fc)].piece is None:
                if team == teams[0]:
                    self.max_player_moves.append((position, forward))
                else:
                    self.min_player_moves.append((position, forward))

        #  Initial pawn position double forward move
        double_forward = (row+2, col) if team == teams[0] else (row-2, col)
        dr, dc = double_forward
        if 0 <= dr <= 7:
            if self.cells[(dr, dc)].piece is None:
                if team == teams[0] and row == 1:
                    self.max_player_moves.append((position, double_forward))
                elif team == teams[1] and row == 6:
                    self.min_player_moves.append((position, double_forward))


    def calculate_king_range(self, position):
        row, col = position
        destinations = [(row+1, col-1), (row+1, col), (row+1, col+1), 
                    (row, col-1), (row, col+1), 
                    (row-1, col-1), (row-1, col), (row-1, col+1),]
        for destination in destinations:
            self.check_and_update_worth(position, destination)