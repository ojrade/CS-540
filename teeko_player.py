import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    totMoves = 0;

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        if(self.totMoves == 0):
                return [[2,2]]
        (finMove,finVal) = self.Max_Value(state, 2, self.totMoves)
        if(finMove == [[]]):
            return
        return finMove
        
    def Max_Value(self, state, depth, moves):
        successors = self.succ(state,moves,self.my_piece)
        if(self.game_value(state) == 1 or self.game_value(state) == -1):
            return ([()],self.game_value(state))
        elif(depth == 0):
            hVal = self.heuristic_game_value(state,self.my_piece)
            return ([()],hVal)
        else:
            a = -2
            if(moves >= 8):
                move = [(),()]
                dropPhase = False
            else:
                move = [()]
                dropPhase = True
            for s in successors:
                stateCopy = copy.deepcopy(state)
                stateCopy = self.stateFromPoint(stateCopy,s,self.my_piece)
                (m,minVal) = self.Min_Value(stateCopy,depth-1,moves+1)
                if(minVal>a):
                    a = minVal
                    move[0] = s[0]
                    if(not dropPhase):
                        move[1] = s[1]
        return (move,a)
    
    def Min_Value(self, state, depth, moves):
        successors = self.succ(state,moves,self.my_piece)
        if(self.game_value(state) == 1 or self.game_value(state) == -1):
            return ([()],self.game_value(state))
        elif(depth == 0):
            hVal = self.heuristic_game_value(state,self.my_piece)
            return ([()],hVal)
        else:
            b = 2
            if(moves >= 8):
                move = [(),()]
                dropPhase = False
            else:
                move = [()]
                dropPhase = True
            for s in successors:
                if(self.my_piece == 'b'):
                    piece = 'r'
                else:
                    piece = 'b'
                stateCopy = copy.deepcopy(state)
                stateCopy = self.stateFromPoint(stateCopy,s,piece)
                (m,maxVal) = self.Max_Value(stateCopy,depth-1,moves+1)
                if(maxVal<b):
                    b = maxVal
                    move[0] = s[0]
                    if(not dropPhase):
                        move[1] = s[1]
        return (move,b)
    
    def stateFromPoint(self,state,move,piece):
        if len(move) > 1:
            state[move[1][0]][move[1][1]] = ' '
        state[move[0][0]][move[0][1]] = piece
        return state
    
    def succ(self, state, moves, piece):
        if(moves < 8):
            dropPhase = True
        else:
            dropPhase = False
        success = []
        if dropPhase:
            for row in range(5):
                for col in range(5):
                    if(state[row][col] == ' '):
                        success.append([[row,col]])
        else:
            placed = []
            for row in range(5):
                for col in range(5):
                    if (state[row][col] == piece):
                        placed.append([row,col])
            for p in placed:
                for row in range(5):
                    for col in range(5):
                        if(state[row][col] == ' '):
                            success.append([[row,col],p])
        return success
            
    def heuristic_game_value(self, state, piece):
        if(self.game_value == -1 or self.game_value == 1):
            return self.game_value
        #print(depth)
        hVal = 0
        incVal = 0
        inc = 0
        
        if(piece == self.my_piece):
            inc = 0.25
        else:
            inc = -0.25
        
        #horizontal    
        for row in state:
            for i in range(2):
                incVal = 0
                if(row[i] != ' ' and row[i] == piece):
                    incVal += inc
                    if(row[i+1] == row[i]):
                        incVal += inc
                        if(row[i+2] == row[i]):
                            incVal += inc
                            if(row[i+3] == row[i]):
                                incVal += inc
                if(incVal > hVal):
                    hVal = incVal
                incVal = 0

        #vertical   
        for col in range(5):
            for i in range(2):
                incVal = 0
                if(state[i][col] != ' ' and state[i][col] == piece):
                    incVal += inc
                    if(state[i+1][col] == state[i][col]):
                        incVal += inc
                        if(state[i+2][col] == state[i][col]):
                            incVal += inc
                            if(state[i+3][col] == state[i][col]):
                                incVal += inc
                if(incVal > hVal):
                    hVal = incVal
                incVal = 0
                        
        # \ diagonal   
        for col in range(2):
            for i in range(2):
                incVal = 0
                if(state[i][col] != ' ' and state[i][col] == piece):
                    incVal += inc
                    if(state[i+1][col+1] == state[i][col]):
                        incVal += inc
                        if(state[i+2][col+2] == state[i][col]):
                            incVal += inc
                            if(state[i+3][col+3] == state[i][col]):
                                incVal += inc
                if(incVal > hVal):
                    hVal = incVal
                incVal = 0
                
        # / diagonal   
        for col in range(2):
            for i in range(2):
                incVal = 0
                if(state[i][col+3] != ' ' and state[i][col] == piece):
                    incVal += inc
                    if(state[i+1][col+2] == state[i][col]):
                        incVal += inc
                        if(state[i+2][col+1] == state[i][col]):
                            incVal += inc
                            if(state[i+3][col] == state[i][col]):
                                incVal += inc
                if(incVal > hVal):
                    hVal = incVal
                incVal = 0
                        
        # 2x2 box   
        for col in range(4):
            for i in range(4):
                incVal = 0
                if(state[i][col] != ' ' and state[i][col] == piece):
                    incVal += inc
                    if(state[i+1][col] == state[i][col]):
                        incVal += inc
                    if(state[i][col+1] == state[i][col]):
                        incVal += inc
                    if(state[i+1][col+1] == state[i][col]):
                        incVal += inc
                if(incVal > hVal):
                    hVal = incVal
                incVal = 0

        return hVal
    
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)   
    
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        self.totMoves+=1
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for col in range(2):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col+1] == state[i+2][col+2] == state[i+3][col+3]:
                    return 1 if state[i][col]==self.my_piece else -1
        # TODO: check / diagonal wins
        for col in range(2):
            for i in range(2):
                if state[i][col+3] != ' ' and state[i][col+3] == state[i+1][col+2] == state[i+2][col+1] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1
        # TODO: check 2x2 box wins
        for col in range(4):
            for i in range(4):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i][col+1] == state[i+1][col+1]:
                    return 1 if state[i][col]==self.my_piece else -1
        
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

"""
state = [['r','r','b','b',' '],
         [' ',' ',' ',' ',' '],
         [' ',' ','b',' ',' '],
         [' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ']]

ai.board = state
piece_count = 8
ai.totMoves = 5
ai.my_piece = 'r'
succ = ai.succ(state,ai.totMoves,ai.my_piece)
print(ai.heuristic_game_value(state,'r'))

print(ai.Max_Value(state,0,ai.totMoves))
for s in succ:
    #print("s: ",s)
    stateCopy = copy.deepcopy(state)
    stateCopy = ai.stateFromPoint(stateCopy,s,ai.my_piece)
    print(s,": ",ai.heuristic_game_value(stateCopy,ai.my_piece),ai.game_value(stateCopy))


# drop phase
while piece_count < 8 and ai.game_value(ai.board) == 0:
    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board

while ai.game_value(ai.board) == 0:
    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
        print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                 (int(move_from[1]), ord(move_from[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
"""
