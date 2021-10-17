import time
import random
from search import *
from utils import *

def make_rand_StagePuzzle():
    """need to return a new instance of a StagePuzzle problem with a random 
    inital state that is solvable"""
    goal   = [1, 2 , 3 , 4 , 5 , 6, 7, 8, 9, 0]
    puzzle = None
    
    while True:
        initial = goal[:] #keeps the goal list for the later use by using deep copy
        random.shuffle(initial) #making random initial state
        puzzle = StagePuzzle(tuple(initial), goal = tuple(goal)) #keep the goal as default value
        if puzzle.check_solvability(initial): #check whether a random initial state is solvable
            break
    
    return puzzle

def display(state):
    """this function takes a StagePuzzle state as input and prints a neat and 
   readable representation of it. 0 is blank and should be printed as a * character"""
    def index_to_row(index): #indicating row index
        row = -1
        if index in [0, 1]:
            row = 0
        elif index in [2, 3, 4, 5]:
            row = 1
        elif index in [6, 7, 8, 9]:
            row = 2
        
        assert row >= 0 and row <= 2
        return row
    
    def index_to_col(index): #indicating column index
        col = -1
        if index in [2, 6]:
            col = 0
        elif index in [0, 3, 7]:
            col = 1
        elif index in [1, 4, 8]:
            col = 2
        elif index in [5, 9]:
            col = 3
        
        assert col >= 0 and col <= 3
        return col
    
    def index_to_row_col_val(state, index): #assigning row, col index to the state
        row = index_to_row(index)
        col = index_to_col(index)
        val = state[index]
        return row, col, val
    
    max_col = 4
    max_row = 3
        
    disp_buf = [[-1]*max_col for i in range(max_row)] #creating empty temporary matrix of -1
        
    for i in range(len(state)):
        row, col, val = index_to_row_col_val(state, i)
        disp_buf[row][col] = val
            
    for r in range(max_row):
        line = ""
        for c in range(max_col):
            val = disp_buf[r][c]
            if val == -1: line += "  " #not in the StagePuzzle
            elif val == 0: line += "* " #blank character
            else: line += str(val) + " " #other values
        print(line)
            
    
def experimental_simulation(heuristic_specifier, instances):
    total_elapsed  = 0.0 #total running time in second
    total_length   = 0.0 #the length of the solution
    total_removed = 0.0 #total number of nodes that were removed from the frontier
    
    for i, puzzle in enumerate(instances):
        print('Start {}: #{}'.format(heuristic_specifier, i))
        display(puzzle.initial)

        start = time.perf_counter()
        node, length, removed = astar_search(puzzle, heuristic_specifier, display = True) 
        elapsed = time.perf_counter() - start
        print('{}: Solving instance #{} time elapsed = {:.3f} length = {}  removed nodes = {}'.format(heuristic_specifier, i, elapsed, length, removed))
        sys.stdout.flush()
        
        total_elapsed  += elapsed
        total_length   += length
        total_removed += removed

    print('Summarization: mean time elapsed = {:.3f}  mean length = {:.3f}   mean removed nodes = {:.3f}'.format(
        total_elapsed / len(instances),
        total_length / len(instances),
        total_removed / len(instances)))
          
if __name__ == '__main__':
    instances = []
    for i in range(8):
        puzzle = make_rand_StagePuzzle() #creating 8 random StagePuzzle instances
        instances.append(puzzle)
    
    experimental_simulation('h_misplaced', instances)
    experimental_simulation('h_manhattan', instances)
    experimental_simulation('h_max', instances)