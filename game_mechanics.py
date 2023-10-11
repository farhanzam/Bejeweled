import project4
from collections import namedtuple


class GameState():
    def __init__(self, rows, cols, rows_list=None):
        self.rows = rows
        self.cols = cols
        self.falling_tuple = None
        self._landed = False
        self._game_over = False
        field_list = []
        if rows_list is not None:
            for i in range(cols):
                column_list = []
                for j in range(rows):
                    column_list.append(rows_list[j][i])
                field_list.append(column_list)
        else:
            field_list = [list(' ' * rows) for i in range(cols)]
        self.field = field_list

    def create_faller_list(self, inpt):
        faller_col = str(int(inpt[2]) - 1)
        faller_list = list(inpt[4:].replace(' ', ''))
        self.falling_tuple = [faller_list, # the list of character to insert
                              int(faller_col),  # column in game board to insert into
                              len(faller_list)-1,  # index to faller_list for the next letter to insert
                              []]  # indices in the game board, where letters have been already inserted
        self.drop_faller_list()

    def is_frozen(self):
        return self.falling_tuple is None and not self._landed
    
    def is_landed(self):
            return self._landed
    
    def drop_faller_list(self):
        if self._landed:
            # if there's still letters not in the board from the faller_list, then game over
            if self.falling_tuple[2] > 0:
                self._game_over = True
            self.falling_tuple = None 
            self._landed = False
            return
        self.drop_gems_by_one_space()
        faller_col = self.falling_tuple[1]
        next_letter_index = self.falling_tuple[2]
        if self.field[faller_col][0] == ' ' and next_letter_index > -1:
            self.field[faller_col][0] = self.falling_tuple[0][next_letter_index]
            self.falling_tuple[2] -= 1
            self.falling_tuple[3].append((faller_col, 0))
        if not self.board_has_gaps() and len(self.get_matches()) == 0:
            self._landed = True

    def _update_falling_tuple_index(self, col, row):
        if self.falling_tuple is None: return
        just_modified_index = (col, row)
        if just_modified_index in self.falling_tuple[3]:
            i = self.falling_tuple[3].index(just_modified_index)
            self.falling_tuple[3][i] = (col, row + 1)

    def rotate(self):
        # perform rotation on faller_list
        last_gem = self.falling_tuple[0][-1]
        del self.falling_tuple[0][-1]
        self.falling_tuple[0].insert(0, last_gem)
        # update the values in game board
        for i in range(len(self.falling_tuple[3])):
            curr_col, curr_row = self.falling_tuple[3][i]
            self.field[curr_col][curr_row] = self.falling_tuple[0][-1 * (i + 1)]

    def remove_gaps(self):
        while self.board_has_gaps():
            self.drop_gems_by_one_space()

    def board_has_gaps(self):
        if self.rows == 1: return
        for i in range(len(self.field)):
            for j in range(1, len(self.field[i])):
                if self.field[i][j] == ' ' and self.field[i][j - 1] != ' ':
                    return True

    def drop_gems_by_one_space(self):
        '''Moves gems down ONE space, if possible'''
        for i in range(len(self.field)):
            for j in range(len(self.field[i]) - 1, 0, -1):
                if self.field[i][j] == ' ' and self.field[i][j - 1] != ' ':
                    self.field[i][j] = self.field[i][j - 1]
                    self.field[i][j - 1] = ' '
                    self._update_falling_tuple_index(i, j - 1)

    def game_is_over(self):
        if self._game_over: 
            return True
        # check if board is full
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if self.field[i][j] == ' ':
                    return False
        return True

    def get_matches(self):
        def flatten(lst):
            new_list = []
            for l in lst:
                new_list.extend(l)
            return new_list

        if not self.is_frozen(): 
            return []
        field = self.field
        def vertical_match_check(ff=None):
            if ff is not None: local_field = ff
            else: local_field = field
            matches = []
            def create_vertical_match(counter, i, j):
                if counter >= 3:
                    match = [(i,j-k) for k in range(counter-1,-1,-1)]
                    matches.append(match)
            for i in range(len(local_field)):
                counter = 1
                for j in range(1, len(local_field[i])):
                    if (local_field[i][j] == local_field[i][j - 1]) and (local_field[i][j] != ' '):
                        counter += 1
                    elif counter >= 3:
                        j -= 1
                        create_vertical_match(counter, i, j)
                        counter = 1
                    else:
                        counter = 1
                if counter >= 3:
                    create_vertical_match(counter, i, j)
            return matches
        
        def horizontal_match_check():
            rows = len(field)
            cols = len(field[0])
            field_list = []
            for i in range(cols):
                column_list = []
                for j in range(rows):
                    column_list.append(field[j][i])
                field_list.append(column_list)
            
            matches = vertical_match_check(field_list)
            if len(matches) >= 0:
                for m in range(len(matches)):
                    matches[m] = [(j,i) for i,j in matches[m]]
            return matches

        def diagonal_right_match_check(ff=None):
            if ff is not None: local_field = ff
            else: local_field = field
            rows, cols = len(local_field), len(local_field[0])
            matches = []
            def create_diagonal_right_match(counter, i, j):
                if counter >= 3:
                    match = [(i-k,j-k) for k in range(counter,0,-1)]
                    matches.append(match)
            # check for matches from (1,1) -> (1,col)
            # GOES DOWN
            for start_i in range(2, rows):
                i,j = start_i, 1
                counter = 1
                while i < rows and j < cols:
                    if local_field[i-1][j-1] == local_field[i][j] and local_field[i][j] != ' ':
                        counter += 1
                    elif counter >= 3:
                        create_diagonal_right_match(counter, i, j)
                        counter = 1
                    else:
                        counter = 1
                    i += 1
                    j += 1
                if counter >= 3: 
                    create_diagonal_right_match(counter, i, j)
            # GOES RIGHT
            for start_j in range(1, cols):
                i,j = 1, start_j
                counter = 1
                while i < rows and j < cols:
                    if local_field[i-1][j-1] == local_field[i][j] and local_field[i][j] != ' ':
                        counter += 1
                    elif counter >= 3:
                        create_diagonal_right_match(counter, i, j)
                        counter = 1
                    else:
                        counter = 1
                    i += 1
                    j += 1
                if counter >= 3:
                    create_diagonal_right_match(counter, i, j)
            return matches
        
        def diagonal_left_match_check():
            # do a horizontal flip
            cols = len(field)
            rows = len(field[0])
            flipped_matrix = [[' ' for _ in range(rows)] for _ in range(cols)]
            for i in range(cols):
                for j in range(rows):
                    flipped_matrix[cols - i - 1][j] = field[i][j]
            # pass flipped matrix into diagonal_right_match_check
            matches = diagonal_right_match_check(flipped_matrix)
            # flip matches
            for m in range(len(matches)):
                matches[m] = [(cols - col - 1, row) for col,row in matches[m]]
            return matches
        
        return flatten(vertical_match_check() + 
                        horizontal_match_check() + 
                        diagonal_right_match_check() +
                        diagonal_left_match_check())

    def move_faller_right(self):
        # check to make sure there is a faller
        if self.falling_tuple is None: return
        # check if there is another column to the right
        if self.falling_tuple[1] == self.cols - 1:
            return
        # check if there are any gems in the way
        for index in self.falling_tuple[3]:
            col, row = index
            if self.field[col + 1][row] != ' ':
                return
        # move faller column to the right
        self.falling_tuple[1] += 1
        # replace the indices of where the faller was with spaces
        for i in range(len(self.falling_tuple[3])):
            col, row = self.falling_tuple[3][i]
            self.field[col][row] = ' '
            self.falling_tuple[3][i] = (col + 1, row)
            col, row = self.falling_tuple[3][i]
            self.field[col][row] = self.falling_tuple[0][-1 * (i + 1)]
        # check if we need to change self._landed
        next_row = self.falling_tuple[3][0][1] + 1
        if next_row < self.rows - 1:
            if self.field[self.falling_tuple[1]][next_row] == ' ':
                self._landed = False
            else: self._landed = True

    def move_faller_left(self):
        # check to make sure there is a faller
        if self.falling_tuple is None: return
        # check if there is another column to the right
        if self.falling_tuple[1] == 0:
            return
        # check if there are any gems in the way
        for index in self.falling_tuple[3]:
            col, row = index
            if self.field[col - 1][row] != ' ':
                return
        # move faller column to the right
        self.falling_tuple[1] -= 1
        # replace the indices of where the faller was with spaces
        for i in range(len(self.falling_tuple[3])):
            col, row = self.falling_tuple[3][i]
            self.field[col][row] = ' '
            self.falling_tuple[3][i] = (col - 1, row)
            col, row = self.falling_tuple[3][i]
            self.field[col][row] = self.falling_tuple[0][-1 * (i + 1)]
        # check if we need to change self._landed
        next_row = self.falling_tuple[3][0][1] + 1  # get index of next row
        if next_row < self.rows - 1: # if there exists a next row (if we're not at the end of the grid)
            if self.field[self.falling_tuple[1]][next_row] == ' ': # if we're above a space, we're NOT landed
                self._landed = False
            else: self._landed = True # if we're above a letter, we ARE landed

    def letter_is_faller(self, col, row):
        # check if (col,row) is in  self.falling_tuple[3]
        return (col, row) in self.falling_tuple[3]

    def remove_match(self, matches):
        for i,j in matches:
            self.field[i][j] = ' '
        self.remove_gaps()



if __name__=='__main__':
	pass
