import random
import copy

class Cubie:
    """
    Represent a single cubie with 6 sides.
    """

    def __init__(self, top=None, bot=None, front=None, back=None, left=None, right=None, goal_position: list[int]=None) -> None:
        self.top = top
        self.bot = bot
        self.front = front
        self.back = back
        self.left = left
        self.right = right
        self.goal_position: list[int] = goal_position

    def rotate_right_counter_clockwise(self) -> None:
        self.top, self.back, self.bot, self.front = self.back, self.bot, self.front, self.top
    
    def rotate_right_clockwise(self) -> None:
        self.top, self.back, self.bot, self.front = self.front, self.top, self.back, self.bot
    
    def rotate_top_counter_clockwise(self) -> None:
        self.back, self.right, self.front, self.left = self.right, self.front, self.left, self.back
    
    def rotate_top_clockwise(self) -> None:
        self.back, self.right, self.front, self.left = self.left, self.back, self.right, self.front
    
    def rotate_front_counter_clockwise(self) -> None:
        self.top, self.right, self.bot, self.left = self.right, self.bot, self.left, self.top
    
    def rotate_front_clockwise(self) -> None:
        self.top, self.right, self.bot, self.left = self.left, self.top, self.right, self.bot

    def same_color_orientation(self, other) -> bool:
        """
        Compare if two cubie has the same color orientation.
        """

        if not isinstance(other, Cubie):
            return NotImplemented

        for side in ['top', 'bot', 'front', 'back', 'left', 'right']:
            self_side = getattr(self, side)
            other_side = getattr(other, side)

            # ensure both side are None or not None
            if (self_side is None) != (other_side is None):
                return False

            # If not None, then must match
            if self_side is not None and self_side != other_side:
                return False

        return True


    def print(self) -> None:
        print(f'    +---+')
        print(f'    | {self.top} |')
        print(f'+---+---+---+---+')
        print(f'| {self.left} | {self.front} | {self.right} | {self.back} |')
        print(f'+---+---+---+---+')
        print(f'    | {self.bot} |')
        print(f'    +---+')

    def clone(self) -> 'Cubie':
        """
        Return a new deep copy of cubie 
        """
        # return Cubie(
        #     top = self.top,
        #     bot = self.bot,
        #     front = self.front,
        #     back = self.back,
        #     left = self.left,
        #     right = self.right,
        #     goal_position = copy.deepcopy(self.goal_position)
        # )

        return copy.deepcopy(self)


class Cube:
    """
    Represent a Cube that is maded up of cubies.
    DBL is the anchor cubie
    """

    solved_cube = {
        'UFL': Cubie(top='Y', front='B', left='O', goal_position=[0, 0, 1]),
        'UFR': Cubie(top='Y', front='B', right='R', goal_position=[1, 0, 1]),
        'UBL': Cubie(top='Y', back='G', left='O', goal_position=[0, 1, 1]),
        'UBR': Cubie(top='Y', back='G', right='R', goal_position=[1, 1, 1]),
        'DFL': Cubie(bot='W', front='B', left='O', goal_position=[0, 0, 0]),
        'DFR': Cubie(bot='W', front='B', right='R', goal_position=[1, 0, 0]),
        'DBL': Cubie(bot='W', back='G', left='O', goal_position=[0, 1, 0]),
        'DBR': Cubie(bot='W', back='G', right='R', goal_position=[1, 1, 0])
    }

    moves = {
        "F": "rotate_front_clockwise",
        "F'": "rotate_front_counter_clockwise",
        "T": "rotate_top_clockwise",
        "T'": "rotate_top_counter_clockwise",
        "R": "rotate_right_clockwise",
        "R'": "rotate_right_counter_clockwise"
    }

    opposite_moves =  {
        "F": "F'",
        "F'": "F",
        "T": "T'",
        "T'": "T",
        "R": "R'",
        "R'": "R"
    }

    
    # xyz cords of corner cubies
    xyz_positions = {
        'UFL': [0, 0, 1],
        'UFR': [1, 0, 1],
        'UBL': [0, 1, 1],
        'UBR': [1, 1, 1],
        'DFL': [0, 0, 0],
        'DFR': [1, 0, 0],
        'DBL': [0, 1, 0],
        'DBR': [1, 1, 0]
    }

    def __init__(self, UFL=None, UFR=None, UBL=None, UBR=None, DFL=None, DFR=None, DBL=None, DBR=None) -> None:

        # self.UFL = Cubie(top='Y', front='B', left='O', goal_position=[0, 0, 1])
        # self.UFR = Cubie(top='Y', front='B', right='R', goal_position=[1, 0, 1])
        # self.UBL = Cubie(top='Y', back='G', left='O', goal_position=[0, 1, 1])
        # self.UBR = Cubie(top='Y', back='G', right='R', goal_position=[1, 1, 1])
        # self.DFL = Cubie(bot='W', front='B', left='O', goal_position=[0, 0, 0])
        # self.DFR = Cubie(bot='W', front='B', right='R', goal_position=[1, 0, 0])
        # self.DBL = Cubie(bot='W', back='G', left='O', goal_position=[0, 1, 0])
        # self.DBR = Cubie(bot='W', back='G', right='R', goal_position=[1, 1, 0])

        self.UFL = UFL
        self.UFR = UFR
        self.UBL = UBL
        self.UBR = UBR
        self.DFL = DFL
        self.DFR = DFR
        self.DBL = DBL
        self.DBR = DBR

        if self.DBL is None:
            self.reset()



    def reset(self) -> None:
        """
        Reset cube back to solved state.
        """
        for key in Cube.solved_cube.keys():
            setattr(self, key, Cube.solved_cube[key].clone())
    

    def clone(self) -> 'Cube':

        # return(Cube(
        #     UFL=self.UFL.clone(),
        #     UFR=self.UFR.clone(),
        #     UBL=self.UBL.clone(),
        #     UBR=self.UBR.clone(),
        #     DFL=self.DFL.clone(),
        #     DFR=self.DFR.clone(),
        #     DBL=self.DBL.clone(),
        #     DBR=self.DBR.clone(),
        # ))

        return copy.deepcopy(self)

    def print(self) -> None:

        print(f'      +-----+')
        print(f'      | {self.UBL.top} {self.UBR.top} |')
        print(f'      | {self.UFL.top} {self.UFR.top} |')
        print(f'+-----+-----+-----+-----+')
        print(f'| {self.UBL.left} {self.UFL.left} | {self.UFL.front} {self.UFR.front} | {self.UFR.right} {self.UBR.right} | {self.UBR.back} {self.UBL.back} |')
        print(f'| {self.DBL.left} {self.DFL.left} | {self.DFL.front} {self.DFR.front} | {self.DFR.right} {self.DBR.right} | {self.DBR.back} {self.DBL.back} |')
        print(f'+-----+-----+-----+-----+')
        print(f'      | {self.DFL.bot} {self.DFR.bot} |')
        print(f'      | {self.DBL.bot} {self.DBR.bot} |')
        print(f'      +-----+')

    def serialize(self):
        return (
            self.UBL.top, self.UBR.top,
            self.UFL.top, self.UFR.top,

            self.UBL.left, self.UFL.left,
            self.UFL.front, self.UFR.front,
            self.UFR.right, self.UBR.right,
            self.UBR.back, self.UBL.back,

            self.DBL.left, self.DFL.left,
            self.DFL.front, self.DFR.front,
            self.DFR.right, self.DBR.right,
            self.DBR.back, self.DBL.back,

            self.DFL.bot, self.DFR.bot,
            self.DBL.bot, self.DBR.bot
        )

    def __hash__(self):
        return hash(self.serialize())

    def __eq__(self, other):
        return isinstance(other, Cube) and self.serialize() == other.serialize()

    def is_solved(self) -> bool:
        """
        Check if cube is in a solved state
        """

        for key in Cube.solved_cube.keys():
            if(getattr(self, key).same_color_orientation(Cube.solved_cube[key]) == False):
                return False

        return True

    def is_same(self, other) -> bool:

        positions = ['UFL', 'UFR', 'UBL', 'UBR', 'DFL', 'DFR', 'DBL', 'DBR']

        for position in positions:
            self_cubie = getattr(self, position)
            other_cubie = getattr(other, position)

            if self_cubie.same_color_orientation(other_cubie) == False:
                return False

        return True


    def get_heuristic_score(self) -> int:
        """
        Returns heuristic score of the current state. Combination of:
            * manhattan dist between current position and goal position of each cubie
            * color orientation
        """

        positions = ['UFL', 'UFR', 'UBL', 'UBR', 'DFL', 'DFR', 'DBL', 'DBR']
        total_score = 0

        for position in positions:

            current_cubie = getattr(self, position)
            goal_position = current_cubie.goal_position
            current_xyz_position = Cube.xyz_positions[position]

            manhattan_dist = 0
            orientation_score = 0
            
            # not in correect pos
            if(goal_position != current_xyz_position):
                for i in range(3):
                    manhattan_dist += abs( goal_position[i] - current_xyz_position[i] )


            # check orientation
            if Cube.solved_cube[position].same_color_orientation(current_cubie) == False:
                orientation_score = 1


            total_score += (manhattan_dist + orientation_score) / 8

        return total_score


    def rotate_front_clockwise(self) -> None:
        positions = [self.UFL, self.UFR, self.DFR, self.DFL]

        self.UFL, self.UFR, self.DFR, self.DFL = self.DFL, self.UFL, self.UFR, self.DFR

        for position in positions:
            position.rotate_front_clockwise()

    
    def rotate_front_counter_clockwise(self) -> None:
        positions = [self.UFL, self.UFR, self.DFR, self.DFL]

        self.UFL, self.UFR, self.DFR, self.DFL = self.UFR, self.DFR, self.DFL, self.UFL

        for position in positions:
            position.rotate_front_counter_clockwise()


    def rotate_top_clockwise(self) -> None:
        positions = [self.UBL, self.UBR, self.UFR, self.UFL]

        self.UBL, self.UBR, self.UFR, self.UFL = self.UFL, self.UBL, self.UBR, self.UFR

        for position in positions:
            position.rotate_top_clockwise()


    def rotate_top_counter_clockwise(self) -> None:
        positions = [self.UBL, self.UBR, self.UFR, self.UFL]

        self.UBL, self.UBR, self.UFR, self.UFL = self.UBR, self.UFR, self.UFL, self.UBL

        for position in positions:
            position.rotate_top_counter_clockwise()


    def rotate_right_clockwise(self) -> None:
        positions = [self.UFR, self.UBR, self.DBR, self.DFR]

        self.UFR, self.UBR, self.DBR, self.DFR = self.DFR, self.UFR, self.UBR, self.DBR

        for position in positions:
            position.rotate_right_clockwise()

    def rotate_right_counter_clockwise(self) -> None:
        positions = [self.UFR, self.UBR, self.DBR, self.DFR]

        self.UFR, self.UBR, self.DBR, self.DFR = self.UBR, self.DBR, self.DFR, self.UFR

        for position in positions:
            position.rotate_right_counter_clockwise()

    def turn_and_clone(self, move: str) -> 'Cube':

        # does turn
        method_name = Cube.moves[move]
        method = getattr(self, method_name)
        method()

        # clone state
        result = self.clone()

        # reverse
        opposite_move = Cube.opposite_moves[move]
        method_name = Cube.moves[opposite_move]
        method = getattr(self, method_name)
        method()

        return result


    def randomize(self, num_moves: int) -> None:

        if num_moves < 1: return

        sequence = []

        # initial turn
        move = random.choice(list(Cube.moves.keys()))
        method_name = Cube.moves[move]
        method = getattr(self, method_name)
        num_moves -= 1
        method()

        sequence.append(move)

        while num_moves > 0:

            move = random.choice(list(Cube.moves.keys()))

            if move == Cube.opposite_moves[sequence[-1]]:
                continue
            elif len(sequence) > 1 and move == sequence[-1] and move == sequence[-2]:
                continue
            else:
                sequence.append(move)

                method_name = Cube.moves[move]
                method = getattr(self, method_name)
                method()

                num_moves -= 1
        
        return sequence
    

            
def cubieTest():
    sam = Cubie(top='Y', bot='W', front='B', back='G', left='O', right='R')
    sam.print()

    lad = Cubie(top='Y', bot='W', front='B', back='G', left='O', right='R')
    print(sam.same_color_orientation(lad))
    bad = sam.clone()
    print(sam.same_color_orientation(bad))
    


    sam.rotate_front_clockwise()
    sam.print()
    sam.rotate_front_counter_clockwise()
    sam.print()

    sam.rotate_top_clockwise()
    sam.print()
    sam.rotate_top_counter_clockwise()
    sam.print()

    sam.rotate_right_clockwise()
    sam.print()
    sam.rotate_right_counter_clockwise()
    sam.print()

    lad = Cubie(top='Y', bot='W', front='B', back='G', left='O')



def cubeTest():
    blocky = Cube()
    blocky.print()

    alice = blocky.clone()
    alice.rotate_front_clockwise()

    blocky.print()
    alice.print()

    blocky.randomize(5)
    blocky.print()




def interface():

    print('\n2x2 Rubik\'s cube')
    blocky = Cube()

    while(True):

        print('')
        blocky.print()

        print('\nOperations:')
        print('0: Exit')
        print('1: Rotate Front Clockwise')
        print('2: Rotate Front Counterclockwise')
        print('3: Rotate Top Clockwise')
        print('4: Rotate Top Counterclockwise')
        print('5: Rotate Right Clockwise')
        print('6: Rotate Right Counterclockwise')
        print('7: Check isSolved')
        print('8: Randomize')
        print('9: Get Heuristic Score')
        print('10: Reset')

        try:
            operation = int(input('\nSelect: '))

            if operation == 0:
                print("Exiting program.")
                break
            elif operation == 1: 
                blocky.rotate_front_clockwise()
            elif operation == 2: 
                blocky.rotate_front_counter_clockwise()
            elif operation == 3: 
                blocky.rotate_top_clockwise()
            elif operation == 4: 
                blocky.rotate_top_counter_clockwise()
            elif operation == 5: 
                blocky.rotate_right_clockwise()
            elif operation == 6: 
                blocky.rotate_right_counter_clockwise()
            elif operation == 7: 
                print(blocky.isSolved())
            elif operation == 8: 
                moves = int(input('How many rotations? '))
                print(blocky.randomize(moves))
            elif operation == 9: 
                print(blocky.get_heuristic_score())
            elif operation == 10:
                blocky.reset()
            else:
                print('Invalid Operation.')
        except ValueError:
            print("Please enter a valid number.")


if (__name__ == '__main__'):
    interface()
