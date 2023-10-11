import game_mechanics


def game_start_info():
    '''
    gets the necessary inputs at the beginning of the game and makes a call
        to the game_mechanics's GameState class in order to construct the field
    '''
    rows = int(input())
    columns = int(input())
    field_type = input()
    rows_list = None
    if field_type == 'CONTENTS':
        rows_list = [list(input()) for i in range(rows)]
    elif field_type != 'EMPTY': 
        raise ValueError('Unrecognized input.')  # TODO
    return game_mechanics.GameState(rows, columns, rows_list)


def display_game_board(game_state, matches):
    ''' performs the functionality to display the field '''
    rows = game_state.rows
    cols = game_state.cols
    field = game_state.field
    for i in range(len(field[0])):
        field_row = '|'
        for j in range(len(field)):
            if game_state.is_frozen() and (j,i) in matches:
                field_row += f'*{field[j][i]}*'
            elif game_state.is_landed() and (j,i) in game_state.falling_tuple[3]:
                field_row += f'|{field[j][i]}|'
            elif not game_state.is_frozen() and (j,i) in game_state.falling_tuple[3]:
                field_row += f'[{field[j][i]}]'
            else:
                field_row += f' {field[j][i]} '
        field_row += '|'
        print(field_row)
    print(' ' + '-' * 3 * cols + ' ')


def get_inputs(game_state):
    ''' gets inputs '''
    while True:
        inpt = input()
        if inpt == 'Q':
            break
        elif inpt == '' and not game_state.is_frozen():
            game_state.drop_faller_list()
        elif len(inpt) > 0 and inpt[0] == 'F' and game_state.is_frozen():
            faller_col = inpt[2]
            game_state.create_faller_list(inpt)
        elif inpt == 'R' and not game_state.is_frozen():
            game_state.rotate()
        elif inpt == '>' and not game_state.is_frozen():
            game_state.move_faller_right()
        elif inpt == '<' and not game_state.is_frozen():
            game_state.move_faller_left()
        else:
            raise ValueError('Unrecognized input.')
        matches = game_state.get_matches()
        display_game_board(game_state, matches)
        if len(matches) > 0:  # if there are any matches, remove them and display board again
            if game_state.is_frozen():
                if input() != '': raise ValueError('Unexpected input.')
                game_state.remove_match(matches)
                display_game_board(game_state, [])
        if game_state.game_is_over():
            print("GAME OVER")
            return


def run_program():
    '''
    ties the programs from this module and the game_mechanics module together 
        to run the game
    '''
    game_state = game_start_info()
    game_state.remove_gaps()
    display_game_board(game_state, [])
    get_inputs(game_state)


if __name__=='__main__':
    run_program()



