#!/usr/bin/python

# Martin O' Gorman
# 09077324
# https://github.com/TeamChocolate/ARC

import os, sys
import json
import numpy as np
import re

# Summary / Reflection
# To solve the tasks listed here, I've mostly used core python and numpy methods. Moving between python lists and NumPy arrays. 
# I used NumPys reshape method to convert a core Python list into a NumPy 2D array for the output step for 2 of my solve functions.
# I used python core methods for splicing the input grids into smaller output grids
# I used NumPy enumeration methods to loop through the 2D input arrays giving me access to the index and the corresponding values

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

def solve_6430c8c4(x):    
    # Task 143/400, 6430c8c4.json
    
    # Verbal description of the required transformation:
    # Task 143 aka 6430c8c4.json, is a task where there's an input grid split in 2 by a yellow row, the top half and the bottom half are equally sized. To solve, one must find where there's matching black squares in the top and bottom half of the grid. And the output must have a grid with green pixels where the matches occured.
    
    # Which training and test grids are solved correctly:
    # ALL training and test grids are solved correctly for the Task 143 / 6430c8c4.json
    
    
    # Workings
    # Divide the grids into two
    # Top has rows with orange, which has values of 2
    # Bottom has rows with red, which has values of 7
    # lose the middle yellow row, which has values of 4
    # Loop through both top and bottom grids trying to find a match for the same coordinates in both grids
    # for any match found, add to output grid
    
    # All input grids are (9, 4) where (row, column), and all outputs are (4, 4)
    
    top_grid = x[0:4, 0:4] # split the input grid into top half
    bottom_grid = x[5:10, 0:4] # split the input grid into bottom half
    yellow_grid = x[4:5, 0:4] # this is unused
    
    # 0 black, 3 green, 7 red, 2 orange, 4 yellow
    #print("top grid is", top_grid)
    #print("bottom grid is", bottom_grid)
    #print("yellow grid is", yellow_grid)
    
    outputlist = []
    
    for index, top_grid_val in np.ndenumerate(top_grid):
        bottom_grid_same_coord = (index[0], index[1])
        bottom_grid_val = bottom_grid[bottom_grid_same_coord]
        if(bottom_grid_val == 0 and top_grid_val == 0):
            # then we have a matching black pair
            # and we want to input green at this coordinate
            # otherwise we set the coordinate to be black
            outputlist.append(3) # 3 is green
            
        else:
            # else, add black to the coordinate
            outputlist.append(0)    
    
    # our outputlist is just a standard python list, here I'm reshaping into NumPy array
    x = np.array(outputlist).reshape(-1, 4)        
    
    return x

def solve_794b24be(x):    
    # Task 185/400, 794b24be.json
    
    # Verbal description of the required transformation:
    # Task 185/400 aka 794b24be.json is a task that has an output grid of (3, 3)(rows, columns). For each pixel that's not black from the input grid, those non-black colours are moved up to the top row in the output grid, coming out from the left hand side to the right until 3 values are there. If there's 4 values, then in the second row, that will be placed in the middle column. 
    
    # Which training and test grids are solved correctly:
    # ALL training and test grids are solved correctly for the Task 185/400, 794b24be.json
   
    pixel_count = 0
    outputlist = []
    # count number of non-black pixels
    # add pixels found to a new list
    for index, val in np.ndenumerate(x): 
        if(val != 0):
            if(pixel_count == 3): # if pixelcount is 3, then we've filled the first row
                outputlist.append(0) # adding buffer black pixel in case now on second row
                outputlist.append(2) # add red pixel to list
            else:
                outputlist.append(2) # add red pixel to list               
            pixel_count = pixel_count + 1    
    
    # after we've counted and populated our new list, the remain values are all black pixels
    for i in range(0, (9-len(outputlist))):
        outputlist.append(0) # add black pixel       
    
    x = np.array(outputlist).reshape(-1, 3) # reshape array into (3 rows, 3 columns)          
    
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

