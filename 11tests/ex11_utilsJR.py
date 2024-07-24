from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    word = ""
    for index in range(len(path)-1):
        if (path[index+1])not in neighbors(path[index],board) or path.count(path[index])>1:
            return
    for i in path:
        if 0 > i[0] or i[0] >= len(board) or 0 > i[1] or i[1] >= len(board[0]):
            return
        word += board[i[0]][i[1]]
    if word in words:
        return word



def neighbors(ind, board):
    lst = []
    if ind[0] + 1 <= len(board) - 1:
        lst.append((ind[0] + 1, ind[1]))
    if ind[0] - 1 >= 0:
        lst.append((ind[0] - 1, ind[1]))
    if ind[1] + 1 <= len(board[0]) - 1:
        lst.append((ind[0], ind[1] + 1))
    if ind[1] - 1 >= 0:
        lst.append((ind[0], ind[1] - 1))
    if ind[0] - 1 >= 0 and ind[1] - 1 >= 0:
        lst.append((ind[0] - 1, ind[1] - 1))
    if ind[0] + 1 <= len(board) - 1 and ind[1] + 1 <= len(board[0]) - 1:
        lst.append((ind[0] + 1, ind[1] + 1))
    if ind[0] + 1 <= len(board) - 1 and ind[1] - 1 >= 0:
        lst.append((ind[0] + 1, ind[1] - 1))
    if ind[0] - 1 >= 0 and ind[1] + 1 <= len(board[0]) - 1:
        lst.append((ind[0] - 1, ind[1] + 1))
    return lst


# def helper_find_length_n_paths(n, board, words, ind, path=[], lst_paths=[]):
#     path.append(ind)
#     if len(path) == n:
#         if (is_valid_path(board, path, words)):
#             lst_paths.append(path[:])
#         return
#     lst_neighbors = neighbors(ind, board)
#     for i in lst_neighbors:
#         if i not in path:
#             helper_find_length_n_paths(n, board, words, i, path, lst_paths)
#             path.pop()
#
#
# def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
#     path_all = []
#     for i in range(len(board)):
#         for j in range(len(board[0])):
#             index = (i, j)
#             helper_find_length_n_paths(n, board, words, index, [], path_all)
#     return path_all

def find_length_n_paths_helper(current_path, current_word,n,words_set,board,words):
    if len(current_path) == n:
        if current_word in words_set:
            return [current_path]
        else:
            return []

    x, y = current_path[-1]
    neighbors1 = neighbors((x, y), board)
    valid_paths = []

    for neighbor in neighbors1:
        if neighbor not in current_path:
            new_x, new_y = neighbor
            new_word = current_word + board[new_x][new_y]
            if any(word.startswith(new_word) for word in words):
                new_path = current_path + [neighbor]
                valid_paths += find_length_n_paths_helper(new_path, new_word,n,words_set,board,words)

    return valid_paths

def find_length_n_paths(n, board, words):
    paths = []
    words_set = set(words)

    for i in range(len(board)):
        for j in range(len(board[i])):
            start = (i, j)
            initial_word = board[i][j]
            valid_paths = find_length_n_paths_helper([start], initial_word,n,words_set,board,words)
            paths.extend(valid_paths)

    return paths

def helper_find_length_n_words(n, board, words, index, string_word, lst_words, path):
    string_word += board[index[0]][index[1]]
    path.append(index)
    if len(string_word) > n:
        return
    if len(string_word) == n:
        if string_word in words:
            lst_words.append(path[:])
        return
    lst_neighbors = neighbors(index, board)
    for i in lst_neighbors:
        if i not in path:
            helper_find_length_n_words(n, board, words, i, string_word, lst_words, path)
            path.pop()


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    if n>len(board)*len(board[0])*2:
        return []
    lst_words = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            index = (i, j)
            helper_find_length_n_words(n, board, words, index, "", lst_words, [])
    return lst_words





# def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
#     words2 = {}
#     lst_score = []
#     for s in words:
#         find_lenghts = find_length_n_words(len(s), board, [word])
#         for i in find_lenghts:
#             word = ""
#             for j in i:
#                 word += board[j[0]][j[1]]
#             if word in words2:
#                 if len(words2[word]) < len(i):
#                     words2[word] = i
#             else:
#                 words2[word] = i
#     for path in words2:
#         lst_score.append(words2[path])
#     return lst_score

def max_score_paths(board, words):
    lst_score_max = []
    for s in words:
        # max_path = None
        for j in range(len(s), 0, -1):
            find_length = find_length_n_paths(j, board, [s])
            if find_length:
                lst_score_max.append(find_length[0])
                # max_path = find_length[0][:]
                break
        # if max_path:
        #     lst_score_max.append(max_path)
    return lst_score_max

# def check_dic(i,dic):
#     for key,value in dic.items():
#         if key==i:
#             return True
#     return False
# def change_to_word(board,path):
#     s=("")
#     for i in path:
#             s+=board[i[0]][i[1]]
#     return s
# def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
#     dic={}
#     max_path=[]
#     lst = []
#     x = len(board) * len(board[0] * 2)
#     for word in words:
#         if len(word) > x:
#             continue
#         if len(word) not in lst:
#             lst.append(len(word))
#     for s in range(len(board)*len(board[0]),0,-1):
#         # if s not in lst:
#         #     continue
#         # lst.remove(s)
#         find_lenghts = find_length_n_paths(s, board, words)
#         for path in find_lenghts:
#             s=change_to_word(board,path)
#             if s not in dic:
#                 dic[s]=path
#             else:
#                 if len(dic[s])<len(path):
#                     dic[s]=path
#     for key,values in dic.items():
#         max_path.append((key,len(key)**2))
#     return max_path
# def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
#     finall = []
#     for s in words:
#         max = []
#         find_lenghts = find_length_n_words(len(s), board, s)
#         for i in find_lenghts:
#             if len(i) > len(max):
#                max = i[:]
#         if max not in finall:
#             finall.append(max)
#     finall.remove([])
#     return finall

# def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
#         finall = set()  # Use a set for faster membership tests
#         length_cache = {}  # Cache for find_length_n_words results
#         for s in words:
#             if s not in length_cache:
#                 length_cache[s] = find_length_n_words(len(s), board, s)
#             max_length_path = max(length_cache[s], key=len, default=[])  # Get the longest path
#             if max_length_path:
#                 finall.add(tuple(max_length_path))  # Convert to tuple for set membership check
#
#         return list(finall)  # Convert back to list if needed

    # return lst_score



# board = [['a', 'b', 'f'],
#          ['ac', 'g', 'd']]
# words = ['ac', 'ab', 'acb', 'adf', 'a']
# print(find_length_n_words(3,board,words))
# print(finall(board, words))
# print(max_score_paths([['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'G', 'K', 'L'], ['M', 'N', 'O', 'P']],('ABC', 'CDE', 'ABCD')))
