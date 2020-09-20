import sys
import numpy as np


class Results:
    # Result arrays
    results_list = []

    diagonal = np.identity(3, dtype=int)                # Diagonals
    diagonal_flipped = np.flip(diagonal, 0)
    results_list.extend((diagonal, diagonal_flipped))   # Add array to list

    top_row = np.zeros(shape=(3, 3), dtype=int)         # Rows
    top_row[0, :] = 1
    mid_row = np.zeros(shape=(3, 3), dtype=int)
    mid_row[1, :] = 1
    bot_row = np.zeros(shape=(3, 3), dtype=int)
    bot_row[-1, :] = 1
    results_list.extend((top_row, mid_row, bot_row))

    left_column = np.zeros(shape=(3, 3), dtype=int)     # Columns
    left_column[:, 0] = 1
    center_column = np.zeros(shape=(3, 3), dtype=int)
    center_column[:, 1] = 1
    right_column = np.zeros(shape=(3, 3), dtype=int)
    right_column[:, -1] = 1
    results_list.extend((left_column, center_column, right_column))


class Game:
    # Game Grid
    matrix_grid = [[" ", " ", "x", "-", ">", " "],
                   [" ", " ", "|", " ", "|", " "],
                   ["y", "-", "-", "-", "-", "-"],
                   ["|", " ", "|", " ", "|", " "],
                   ["V", "-", "-", "-", "-", "-"],
                   [" ", " ", "|", " ", "|", " "]]

    current_usr = "X"
    usr_moves_one = np.ndarray(shape=(3, 3), dtype=int)
    usr_moves_one.fill(0)
    usr_moves_two = np.ndarray(shape=(3, 3), dtype=int)
    usr_moves_two.fill(0)

    usr_moves = {
        "X": usr_moves_one,
        "O": usr_moves_two
    }

    exit_code = "x"


# Print Matrix
def print_matrix(matrix):
    for row in matrix:
        print(convert_row_to_line(row))     # Print row


# Print matrix row
def convert_row_to_line(row):
    str_row = ""
    for el in row:
        str_row += el
    return str_row


# Get user move and place on grid
def get_user_move():
    move = formatted_input()            # Get usr move in formatted form
    position = get_coordinates(move)    # Get position from move
    set_move(position)                  # Set usr move on grid
    store_move(move)                    # Store usrs move
    print_matrix(g.matrix_grid)         # Update matrix
    check_win()                         # Check if usr won
    change_usr()                        # Update usr


# Get input in correct form and format into list
def formatted_input():
    raw_input = input("User {}: your move (ie: 0,1 for column 0, row 1):\n".format(g.current_usr))

    # Allow usr to exit
    if raw_input.lower() == g.exit_code:
        sys.exit()

    # Recursion till accepted value
    try:
        # Split input into list
        form_input = list(map(int, raw_input.split(',')))

        # Check correct number of paramaters provided
        if len(form_input) != 2:
            print("please provide only two numbers separated by a comma")
            formatted_input()

        # Check values fit in grid
        if form_input[0] < 3 and form_input[1] < 3:
            return form_input
        else:
            print("Enter value between 0 and 2")
            formatted_input()
    except ValueError:
        # Catch non-int values
        formatted_input()


# Get coordinates from position (adjust for matrix walls)
def get_coordinates(move):
    position = [None, None]
    # map usr input to game matrix
    for i in range(len(position)):
        position[i] = move[i] * 2 + 1
    return position


def set_move(position):
    if g.matrix_grid[position[1]][position[0]] == " ":
        g.matrix_grid[position[1]][position[0]] = g.current_usr  # Set move on grid
    else:
        print("You can't move there")
        formatted_input()


# Store usrs moves on matrix
def store_move(move):
    g.usr_moves[g.current_usr][move[0], move[1]] = 1


# Go through results array and check for match
def check_win():
    for res_array in r.results_list:
        comparison = res_array == g.usr_moves[g.current_usr]
        if comparison.all():
            usr_won()
            break


# End game and send win msg
def usr_won():
    print("Congrats User {}! You have won!".format(g.current_usr))
    sys.exit()


def change_usr():
    if g.current_usr != "X":
        g.current_usr = "X"
    else:
        g.current_usr = "O"


if __name__ == '__main__':
    g = Game()                          # Start new Game
    r = Results()
    print_matrix(g.matrix_grid)         # Print matrix

    while True:
        get_user_move()     # Get 1st user move
        get_user_move()     # Get 2nd user move
