#################################################################
# FILE : ex11_utils.py
# WRITER : mohammad,ahmad , mohammad.ftemi,ahmad.ftemi , 213620115,213621279
# EXERCISE : intro2cse ex11 2023
# DESCRIPTION: A program that contains a code to the boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: ahmad.ftemi.
# WEB PAGES I USED: www.stackoverflow.com/www.w3schools.com
# NOTES: ...
#################################################################
from typing import List, Tuple, Iterable, Optional


Board = List[List[str]]
Path = List[Tuple[int, int]]


def get_neighbors(current, board):
    """this function get neighboring positions for a given position on the board."""
    x, y = current
    neighbors = []
    # Iterate through possible relative offsets to find neighbors
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0):
                # Calculate the coordinates of a potential neighbor
                neighbor_x = x + dx
                neighbor_y = y + dy

                # Check if the potential neighbor is within the bounds of the board
                if 0 <= neighbor_x < len(board) and 0 <= neighbor_y < len(board[0]):
                    neighbors.append((neighbor_x, neighbor_y))
    return neighbors


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """this function check if a given path on the board corresponds
     to a valid word in the provided word list."""
    word = ""

    # Check for revisiting the same cell in the path
    for k in range(len(path) - 1):
        for j in range(k + 1, len(path)):
            if path[k] == path[j]:
                return None
    # Iterate through the path and check for validity
    for i in range(len(path)):
        x, y = path[i]
        # Check if the path goes out of bounds of the board
        if x >= len(board) or y >= len(board[0]):
            return None
        # Get neighbors of the current cell
        neighbors = get_neighbors(path[i], board)
        if i == len(path) - 1:
            # If it's the last cell in the path, add the character to the word
            word += board[path[i][0]][path[i][1]]
        else:
            # If the next cell is a valid neighbor, add the character to the word
            if path[i + 1] in neighbors:
                word += board[path[i][0]][path[i][1]]
    # Check if the constructed word is in the list of valid words
    if word in words:
        return word
    else:
        return None


def find_length_n_paths_helper(current_path, current_word, n, words_set, board, words):
    """this helper function to find all the valid paths of length n on the board"""
    if len(current_path) == n:
        # Check if the current_word is a valid word
        if current_word in words_set:
            return [current_path]
        else:
            return []
    # Get the coordinates of the last position in the current path
    x, y = current_path[-1]
    # Find neighboring positions on the board
    neighbors = get_neighbors((x, y), board)
    valid_paths = []
    # Iterate through neighboring positions
    for neighbor in neighbors:
        if neighbor not in current_path:
            new_x, new_y = neighbor
            new_word = current_word + board[new_x][new_y]

            # Check if any valid word starts with the new_word
            if any(word.startswith(new_word) for word in words):
                new_path = current_path + [neighbor]
                valid_paths += find_length_n_paths_helper(new_path, new_word, n, words_set, board, words)

    return valid_paths


def find_length_n_paths(n, board, words):
    """this function find all the valid paths of length n on the board"""
    paths = []
    words_set = set(words)

    for i in range(len(board)):
        for j in range(len(board[i])):
            start = (i, j)# Define the starting coordinate for the path.
            initial_word = board[i][j] # Initialize the current word with the character at the starting coordinate.
            valid_paths = find_length_n_paths_helper([start], initial_word, n, words_set, board, words)  # Find valid paths starting from the \
            # current cell using the helper function.
            paths.extend(valid_paths)

    return paths


def find_length_n_words_helper(current_path, current_word, n, words_set, board, words):
    """this helper function to find all valid words of length n on the board."""
    if len(current_word) == n:
        # Check if the current_word is a valid word
        if current_word in words_set:
            return [current_path]
        else:
            return []

    # Get the coordinates of the last position in the current path
    x, y = current_path[-1]
    # Find neighboring positions on the board
    neighbors = get_neighbors((x, y), board)
    valid_paths = []

    # Iterate through neighboring positions
    for neighbor in neighbors:
        if neighbor not in current_path:
            new_x, new_y = neighbor
            new_word = current_word + board[new_x][new_y]

            # Check if any valid word starts with the new_word
            if any(word.startswith(new_word) for word in words):
                new_path = current_path + [neighbor]
                valid_paths += find_length_n_words_helper(new_path, new_word, n, words_set, board, words)

    return valid_paths


def find_length_n_words(n, board, words):
    """this function finds all valid words of length n on the board."""
    paths = []
    words_set = set(words)

    for i in range(len(board)):
        for j in range(len(board[i])):
            start = (i, j)# Define the starting coordinate for the path.
            initial_word = board[i][j] # Initialize the current word with the character at the starting coordinate.
            valid_paths = find_length_n_words_helper([start], initial_word, n, words_set, board, words)# Find valid paths starting from the \
            # current cell using the helper function.
            paths.extend(valid_paths)

    return paths

def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """this function finds the paths on the board that have the maximum possible score."""
    max_score_paths = []
    # Iterate through each word in the input collection.
    for word in words:
        # Find all paths of the same length as the word on the board.
        paths_for_word = find_length_n_words(len(word), board, [word])
        for path in paths_for_word:
            # Add the path to the result list if it's not already present.
            if path not in max_score_paths:
                max_score_paths.append(path)
    min_paths = []
    # Compare each pair of paths in the result list.
    for i in range(len(max_score_paths) - 1):
        for k in range(i + 1, len(max_score_paths)):
            # Check if the validity of the paths is the same.
            if is_valid_path(board, max_score_paths[i], words) == is_valid_path(board, max_score_paths[k], words):
                min_paths.append(min(max_score_paths[k], max_score_paths[i]))# Add the smaller of the two paths to the list of paths to remove.

    # Remove the paths marked for removal from the result list.
    for k in min_paths:
        if k in max_score_paths:
            max_score_paths.remove(k)
    return max_score_paths
