from rubikcube import Cubie, Cube
import time
import heapq
import math
import csv
import os

class Node:
    def __init__(self, parent, state, action) -> None:
        self.parent: Node = parent
        self.state: Cube = state
        self.action = action

    def get_action_sequence(self):
        """
        Returns action sequence for a given state
        """

        sequence = []
        current_node = self
        
        while current_node.parent is not None:

            sequence.append(current_node.action)

            current_node = current_node.parent

        sequence.reverse()
        return sequence


    def get_path_cost(self) -> int:
        """
        Returns path cost for a given state
        """
        pathCost = 0
        current_node = self

        while current_node.parent is not None:

            pathCost += 1

            current_node = current_node.parent

        return pathCost

    
    def get_eval_score(self):
        return float(self.get_path_cost() + self.state.get_heuristic_score())


    # used for eval in heap
    def __lt__(self, other):

        self_eval_score = self.get_eval_score()
        other_eval_score = other.get_eval_score()

        return self_eval_score < other_eval_score

class Result:
    def __init__(self, time_taken, nodes_on_pqueue, nodes_expanded, sequence=None):
        self.time_taken = time_taken
        self.nodes_on_pqueue = nodes_on_pqueue
        self.nodes_expanded = nodes_expanded
        self.sequence = sequence

    def __str__(self):
        return(f'Time: {self.time_taken} | Nodes in pqueue: {self.nodes_on_pqueue} | Nodes expanded: {self.nodes_expanded} | Sequence: {self.sequence}')

class Solution:

    def __init__(self, state: Cube) -> None:
        self.root = Node(parent=None, state=state, action=None)

        self.total_nodes_visited = 0
        self.nodes_visited = 0


    def breadth_first_search(self) -> list[str]:

        start_time = time.process_time()

        explored = set()
        explored.add(self.root.state)
        frontier = []

        # start initial frontier
        for move in Cube.moves.keys(): 
            new_state = self.root.state.turn_and_clone(move)
            frontier.append(Node(self.root, new_state, move))

        
        while len(frontier) != 0:

            # print(f'Explored: {len(explored)} | Frontier: {len(frontier)}')

            current_node = frontier.pop(0)

            if current_node.state in explored:
                continue

            # check if solved
            if current_node.state.is_solved() == True:
                end_time = time.process_time()
                # print(f'Explored: {len(explored)} | Frontier: {len(frontier)}')
                return Result(end_time-start_time, len(frontier), len(explored), current_node.get_action_sequence())

            # generate nodes
            for move in Cube.moves.keys():

                if move == Cube.opposite_moves[current_node.action]:
                    continue
                
                new_state = current_node.state.turn_and_clone(move)

                frontier.append(Node(current_node, new_state, move))

            explored.add(current_node.state)


    def iterative_deepening_depth_first_search(self) -> list[str]:
        
        self.total_nodes_visited = 0
        start_time = time.process_time()
        depth = 0

        while True:

            self.nodes_visited = 0

            result = self.depth_limited_search(self.root, depth)
                
            if result is not None:
                end_time = time.process_time()
                self.total_nodes_visited += self.nodes_visited
                return Result(end_time-start_time, self.nodes_visited, self.total_nodes_visited, result.get_action_sequence())

            
            depth += 1

            self.total_nodes_visited += self.nodes_visited
       

    def depth_limited_search(self, current_node, depth_limit) -> list[str]:
        
        self.nodes_visited += 1
        
        if(current_node.state.is_solved() == True):
            return current_node

        if depth_limit == 0:
            return None

        # generate nodes
        for move in Cube.moves.keys():

            if (current_node.action is not None) and (move == Cube.opposite_moves[current_node.action]):
                continue
            
            new_state = current_node.state.turn_and_clone(move)

            new_node = Node(current_node, new_state, move)

            result = self.depth_limited_search(new_node, depth_limit - 1)

            # success return
            if result is not None:
                return result

        #failure
        return None


    def a_star(self):

        start_time = time.process_time()

        explored = set()
        explored.add(self.root.state)
        frontier = []

        # start initial frontier
        for move in Cube.moves.keys(): 
            new_state = self.root.state.turn_and_clone(move)
            new_node = Node(self.root, new_state, move)
            # eval_score = new_node.get_path_cost() + new_node.state.get_heuristic_score()

            heapq.heappush(frontier, new_node)
        
        while len(frontier) != 0:

            # print(f'Explored: {len(explored)} | Frontier: {len(frontier)}')

            current_node = heapq.heappop(frontier)

            if current_node.state in explored:
                continue

            # check if solved
            if current_node.state.is_solved() == True:
                end_time = time.process_time()
                sequence = current_node.get_action_sequence()
                print(f'Explored: {len(explored)} | Frontier: {len(frontier)}')
                return [sequence, end_time-start_time]

            # generate nodes
            for move in Cube.moves.keys():

                if move == Cube.opposite_moves[current_node.action]:
                    continue
                
                new_state = current_node.state.turn_and_clone(move)
                new_node = Node(current_node, new_state, move)
                # new_eval_score = new_node.get_path_cost() + new_node.state.get_heuristic_score()
            
                heapq.heappush(frontier, new_node)

            explored.add(current_node.state)


    def iterative_deepening_a_star(self):
        
        self.total_nodes_visited = 0
        start_time = time.process_time()
        threshold = self.root.get_eval_score()

        while True:
            self.nodes_visited = 0
            result = self.ida(self.root, threshold)

            if isinstance(result, Node):
                end_time = time.process_time()
                self.total_nodes_visited += self.nodes_visited
                return Result(end_time-start_time, self.nodes_visited, self.total_nodes_visited, result.get_action_sequence())

            threshold = result
            self.total_nodes_visited += self.nodes_visited

            

    def ida(self, current_node, threshold):

        self.nodes_visited += 1

        eval_score = current_node.get_eval_score()

        # too far away
        if eval_score > threshold:
            return eval_score

        
        if(current_node.state.is_solved() == True):
            return current_node

        
        new_threshold = math.inf

        # generate nodes
        for move in Cube.moves.keys():

            if (current_node.action is not None) and (move == Cube.opposite_moves[current_node.action]):
                continue
            
            new_state = current_node.state.turn_and_clone(move)

            new_node = Node(current_node, new_state, move)

            result = self.ida(new_node, threshold)

            if isinstance(result, Node):
                return result

            if result < new_threshold:
                new_threshold = result


        return new_threshold


        




def testing():
    blocky = Cube()
    blocky.print()
    sequence = blocky.randomize(6)
    print(sequence)
    blocky.print()

    solution = Solution(blocky)

    result = solution.breadth_first_search()
    print(f'BFS: {result[0]} | Time: {result[1]}')

    result = solution.iterative_deepening_depth_first_search()
    print(f'IDDFS: {result[0]} | Time: {result[1]} | Nodes Visited: {result[2]} | Total Nodes: {result[3]}')

    # result = solution.a_star()
    # print(f'A*: {result[0]} | Time: {result[1]}')

    result = solution.iterative_deepening_a_star()
    print(f'IDA*: {result[0]} | Time: {result[1]} | Nodes Visited: {result[2]} | Total Nodes: {result[3]}')





def run_experiment(search_method, output_file_name, bound=None):
    
    method_name = ''
    if search_method == 'bfs':  
        method_name = 'breadth_first_search'
    elif search_method == 'iddfs':  
        method_name = 'iterative_deepening_depth_first_search'
    elif search_method == 'ida':  
        method_name = 'iterative_deepening_a_star'

    print(f'Running {method_name} Experiment...')

    lower_bound = 1
    upper_bound = 15

    if bound is not None:
        lower_bound = bound[0]
        upper_bound = bound[1]

    # max num turns is 14
    for depth in range(lower_bound, upper_bound): 

        print(f'\nDepth: {depth}\n')

        cubes = []

        results = []

        # create 20 cubes per depth
        for i in range(20):
            new_cube = Cube()
            print(f'Cube {i} randomized sequence: {new_cube.randomize(depth)}')
            cubes.append(new_cube)

        
        for i in range(len(cubes)):

            new_solution = Solution(cubes[i])

            method = getattr(new_solution, method_name)
            result = method()

            print(f'Cube {i} solution: {result}')

            results.append(result)

        avg_time_taken = sum(result.time_taken for result in results) / len(results)
        avg_nodes_on_pqueue = sum(result.nodes_on_pqueue for result in results) / len(results)
        avg_nodes_expanded = sum(result.nodes_expanded for result in results) / len(results)

        avg_result = Result('', avg_nodes_expanded, avg_time_taken, avg_nodes_on_pqueue)
        avg_result = Result(avg_time_taken, avg_nodes_on_pqueue, avg_nodes_expanded)

        print(f'\nAverage:\n{avg_result}\n')

        # os.makedirs('results', exist_ok=True)
        file_path = os.path.join('A1 and A2/results', output_file_name)
        with open(file_path, 'a', newline='', encoding='utf-8') as file:

            writer = csv.writer(file)
            writer.writerow([depth, avg_result.time_taken, avg_result.nodes_on_pqueue, avg_result.nodes_expanded])
            print(f'Average appended to file.')



def main():

    # run_experiment('ida', 'ida_data.csv', [13,14])
    run_experiment('iddfs', 'iddfs_data.csv', [11,15])
    # run_experiment('bfs', 'bfs_data.csv')


if (__name__ == '__main__'):
    main()