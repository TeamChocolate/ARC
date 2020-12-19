#!/usr/bin/python

# Martin O' Gorman
# 09077324
# https://github.com/TeamChocolate/ARC

import os, sys
import json
import numpy as np
import re

def solve_1cf80156(x):
    # Task 30/400, 1cf80156
    # Dimensions (rows, columns)
    # Demo 1: (10, 12) -> (4, 4)
    # Demo 2: (11, 12) -> (5, 3)
    # Demo 3: (12, 12) -> (3, 5)
    # Test input: (12, 12) -> (4, 6)
    # Input/Output 2D NumPy array
    
    # Verbal description of the required transformation:
    # Task 30 aka 1cf80156.json, is a task where the demonstration makes clear that grid is resized to match the the max height and width of       the shape, so in order to be able to solve the task, one must constrain the grid size to the size of the shape.
    # To do this, I found and tracked the first/last row when colours appeared, and the first/last column where colours appeared
    # Using the 4 captured values above, I was able to slice the NumPy array from the input parameter to correctly size the grid.
    # No other transformations were required for the shape for a correct solution
    
    # Which training and test grids are solved correctly:
    # ALL training and test grids are solved correctly for the Task 30 / 1cf80156.json
            
    first_row_where_data = 0
    last_row_where_data = 0
    last_column_where_colour = 0
    first_column_where_colour = 99
    
    # index[0], index[1] gives coordinates of the pixel in the grid
    # loop through every coordinate in the input grid
    for index, val in np.ndenumerate(x):
        # if not black aka 0
        if(val != 0):            
            row = index[0]
            column = index[1]
            if(first_row_where_data == 0):
                first_row_where_data = row 
            if(row > last_row_where_data):
                last_row_where_data = row
            if(column > last_column_where_colour):
                last_column_where_colour = column
            if(column < first_column_where_colour):
                first_column_where_colour = column
                
    last_row_where_data = last_row_where_data + 1
    last_column_where_colour = last_column_where_colour + 1
    
    # splice the input grid using the values obtained above into the correct output grid
    x = x[first_row_where_data:last_row_where_data, first_column_where_colour:last_column_where_colour]       
    
    return x

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print("TaskID is: ", taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

