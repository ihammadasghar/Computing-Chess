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
    def __init__(self, max_player, min_player) -> None:
        self.cells = {}
        for row in range(8):
            for col in range(8):
                self.cells[(row, col)] = Cell()

        self.max_player = max_player
        self.min_player = min_player
        self.max_player_moves = {}
        self.min_player_moves = {}
        self.state = 0.0
            

    def set_state(self, board):
        self.state = float(board.state)
        self.max_player_moves = board.max_player_moves.copy()
        self.min_player_moves = board.min_player_moves.copy()
        for row in range(8):
            for col in range(8):
                position = (row, col)
                cell = board.cells[position]
                if cell.piece:
                    self.cells[position].piece = cell.piece
                    self.cells[position].worth = float(cell.worth)


    def make_move(self, position, destination):
        cell = self.cells[position]
        piece = cell.piece
        if piece == teams[0]:
            self.state -= cell.worth - piece.points
        else:
            self.state += cell.worth - piece.points
        self.cells[position].piece = None

        destination_cell = self.cells[destination]
        destination_piece = destination_cell.piece
        #  Capturing
        if destination_piece:
            if destination_piece.team == teams[0]:
                self.state -= (destination_cell.worth - destination_piece.points)
                self.state -= destination_piece.points
            else:
                self.state += (destination_cell.worth - destination_piece.points)
                self.state += destination_piece.points

            #  Game Ended
            if destination_piece.name == "king":
                return True
        
        self.cells[destination].piece = piece
        self.evaluate_worths()

        return False

    def evaluate_worths(self):
        self.max_player_moves = {}
        self.min_player_moves = {}

        for row in range(8):
            for col in range(8):
                position = (row, col)
                cell = self.cells[position]
                piece = cell.piece
                if piece is None:
                    continue

                #  Reset
                cell.worth = piece.points

                if piece.team == teams[0]:
                    self.max_player_moves[position] = []
                else:
                    self.min_player_moves[position] = []

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
                
                if piece.team == teams[0] and self.max_player_moves[position] == []:
                    self.max_player_moves.pop(position)
                elif piece.team == teams[1] and self.min_player_moves[position] == []:
                    self.min_player_moves.pop(position)

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
                else:
                    self.state -= in_range_advantage

                if piece.team == teams[0]:
                    self.max_player_moves[position].append(destination)
                else:
                    self.min_player_moves[position].append(destination)
                return True
            return True

        if piece.name == "pawn":
            return False

        if piece.team == teams[0]:
            self.max_player_moves[position].append(destination)
        else:
            self.min_player_moves[position].append(destination)
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
                destination = (row-i, col)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                up = not is_End_or_Blocked
            
            if down:
                destination = (row+i, col)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                down = not is_End_or_Blocked

            if left:
                destination = (row, col-i)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                left = not is_End_or_Blocked

            if right:
                destination = (row, col+i)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                right = not is_End_or_Blocked

    def calculate_x_range(self, position):
        row, col = position
        
        top_left = True
        top_right = True
        bottom_left = True
        bottom_right = True
        for i in range(1, 8):
            if top_left:
                destination = (row-i, col-i)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                top_left = not is_End_or_Blocked
            
            if top_right:
                destination = (row-i, col+i)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                top_right = not is_End_or_Blocked

            if bottom_left:
                destination = (row+i, col-i)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
                bottom_left = not is_End_or_Blocked

            if bottom_right:
                destination = (row+i, col+i)
                is_End_or_Blocked = self.check_and_update_worth(position, destination)
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
        if self.cells[(fr, fc)].piece is None and 0 <= fr <= 7:
            if team == teams[0]:
                self.max_player_moves[position].append(forward)
            else:
                self.min_player_moves[position].append(forward)

        #  Initial pawn position double forward move
        double_forward = (row+2, col) if team == teams[0] else (row-2, col)
        dr, dc = double_forward
        if self.cells[(dr, dc)].piece is None:
            if team == teams[0] and row == 1:
                self.max_player_moves[position].append(double_forward)
            elif team == teams[1] and row == 6:
                self.min_player_moves[position].append(double_forward)

    def calculate_king_range(self, position):
        row, col = position
        destinations = [(row+1, col-1), (row+1, col), (row+1, col+1), 
                    (row, col-1), (row, col+1), 
                    (row-1, col-1), (row-1, col), (row-1, col+1),]
        for destination in destinations:
            self.check_and_update_worth(position, destination)