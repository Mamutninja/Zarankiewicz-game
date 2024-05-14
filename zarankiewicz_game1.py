import numpy as np
import random
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
    K_BACKSPACE,
    K_RETURN, # enter button
)


pygame.init()

# *********************************** BASIC SCREEN SETTINGS ***********************************

# Size of screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Size of n×m table
n = 3
m = 2

# Margins: how to position our table?
upper_margin = 100
lower_margin = 100
left_margin = 30
right_margin = 30
line_weight = 1 # border of cells

# Calculates height, width of table and the length of the cells' side
table_height = 500
table_width = 500
cell_side_length = 50
if n >= m:
    table_height = SCREEN_HEIGHT - upper_margin - lower_margin
    cell_side_length = (table_height-(n+1)*line_weight)/n
    table_width = (m+1)*line_weight + m*cell_side_length
else:
    table_width = SCREEN_WIDTH - left_margin - right_margin
    cell_side_length = (table_width-(m+1)*line_weight)/m
    table_height = (n+1)*line_weight + n*cell_side_length
    
# Window name
pygame.display.set_caption("Zarankiewicz Game")

    
# *********************************** GAME ENGINE ***********************************

# used to realize the settings
setting = False

# Players' info
# Which player's turn is next? 1 or 2
# switch: abs(player_turn - 3)
player_turn = 1

# Who wins? 0 - not decided yet/draw, 1 - player 1, 2 - player 2
player_won = 0

# Is the game against the computer? 0 - player vs player, 1 - player vs computer, 2 - computer vs computer
against_comp = 0

# One (1) or two (2) cell colors?
cell_colors = 2

# If there are two cell colors, which one to choose?
color_of_cell = 1

# The one who completes a rectangle wins or loses?
rect_complete_wins = True

# Is the game on?
game_on = False

# After the game is over, SPACE can be pressed to go to the "winners" screen.
# This bool manages this
winners_space = False


# Matrix of the game
A = np.zeros((n, m))


# stores free rows and columns (= no cell in there has been colored)
free_row = set()
free_column = set()
        
# initially all the rows and columns are free
for i in range(n):
    free_row.add(i)
for j in range(m):
    free_column.add(j)


# Empty cells of the matrix
empty_cells = set()
for i in range(n):
    for j in range(m):
        if A[i][j] == 0:
            empty_cells.add((i, j))
            

# Which screen is displayed?
current_screen = "welcome"


# the whole game starts again
restart = False


# Creates the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# *********************************** IMPORTANT CLASSES ***********************************

# computer's algorithms
class Computer():
    def __init__(self, player):
        # computer variables
        self.player = player
        
        # stores the last move done with the computer's color
        self.last_move = (-1, -1)
        
        # stores the last move of the other player
        self.other_last_move = (-1, -1)
        
        # if the other player missed an opportunity to win and has the same color
        if cell_colors == 1:
            self.last_move_missed_opportunity = (-1, -1)
        
        # stores other player's last move: is the chosen cell in a free row or column?
        # -1: no move yet, 0: free row/column, 1: not free row/column
        self.last_move_free = (-1, -1)
        # first move of the other player
        self.first_move_free = (-1, -1)
        
        # used for the two color strategy
        # move counter
        self.move_count = 0
        # first move of the computer
        self.first_move = (-1, -1)
        # second move of the computer
        self.second_move = (-1, -1)
        # third move of the computer
        self.third_move = (-1, -1)
        # fourth move of the computer
        self.fourth_move = (-1, -1)
        # fifth move of the computer
        self.fifth_move = (-1, -1)
        
        # first move of the other player
        self.other_first_move = (-1, -1)
        # second
        self.other_second_move = (-1, -1)
        
        # is there a known winning strategy?
        self.winning_strategy_exists = False
        if ((rect_complete_wins == True) and (self.can_complete_rect(self.last_move[0], self.last_move[1], color_of_cell)[0] == True) and (self.last_move[0] != -1)) or ((rect_complete_wins == True) and (cell_colors == 1) and (self.can_complete_rect(self.last_move_missed_opportunity[0], self.last_move_missed_opportunity[1], color_of_cell)[0] == True) and (not self.last_move_missed_opportunity[0] == -1) and (not self.last_move_missed_opportunity[1] == -1)) or ((rect_complete_wins == True) and ((n % 2 == 0 or m % 2 == 0) and (self.player == 2) and (cell_colors == 1))) or ((rect_complete_wins == True) and ((n % 2 != 0 and m % 2 != 0) and (self.player == 1) and (cell_colors == 1))) or ((rect_complete_wins == True) and ((self.player == 1) and (cell_colors == 2) and (((n >= 5) and (m >= 5)) or ((n == 4) and (m == 4))))):
            self.winning_strategy_exists = True
            
    # Checks if a rectangle can be completed
    # a, b: last chosen cell's coordinates; p: color
    # returns True and the cell's coordinates
    def can_complete_rect(self, a, b, p=1):
        for j in range(m):
            if (A[a][j] == p) and (j != b):
                for i in range(n):
                    if (A[i][j] == p) and (i != a) and ((i, b) in empty_cells):
                        return(True, i, b)
                    if (A[i][b] == p) and (i != a) and ((i, j) in empty_cells):
                        return(True, i, j)
        for i in range(n):
            if (A[i][b] == p) and (i != a):
                for j in range(m):
                    if (A[i][j] == p) and (j != b) and ((a, j) in empty_cells):
                        return(True, a, j)
        return(False, -1, -1)
    
    # strategy for even x odd, odd x even and even x even tables if there's ONE color
    # computer must be player 2
    def strategy_even_c1_p2(self):
        # if there's an even number of rows
        if (n % 2) == 0:
            if self.last_move_free[0] == 0: # it must be true, otherwise the computer has already won
                # as it is a one-color game, last_move can be used
                j = self.last_move[1]
                i = random.choice(list(free_row))
                return i, j
            
        # if there's an odd number of rows and an even number of columns
        elif (m % 2) == 0:
            if self.last_move_free[1] == 0: # it must be true, otherwise the computer has already won
                # as it is a one-color game, last_move can be used
                i = self.last_move[0]
                j = random.choice(list(free_column))
                return i, j
                
    # strategy for odd x odd tables if there's ONE color
    # computer must be player 1
    def strategy_odd_c1_p1(self):
        # if all the cells are empty, choose a random cell
        if self.last_move == (-1, -1):
            r = random.choice(list(empty_cells))
            return r
        
        # if player 2 chose a free cell (= in a free column AND row), choose a free cell
        if self.last_move_free[0] == 0 and self.last_move_free[1] == 0:
            i = random.choice(list(free_row))
            j = random.choice(list(free_column))
            return i, j
        
        # if player 2 chose a not free row, choose the same row and a free column
        if self.last_move_free[0] != 0:
            i = self.last_move[0]
            j = random.choice(list(free_column))
            return i, j
        
        # if player 2 chose a not free column and a free row, choose the same row and a free column
        if self.last_move_free[1] != 0:
            i = random.choice(list(free_row))
            j = self.last_move[1]
            return i, j
        
        # else player 2 chose a not free row AND a not free column, which means that can_complete_rect is used
    
    # strategy for min. 4 x 4 tables if there are TWO colors
    # computer must be player 1
    def strategy_4plus_c2_p1(self):
        # if the table's at least 5 x 5
        if (n >= 5) and (m >= 5):
            # first move
            if self.move_count == 1:
                r = random.choice(list(empty_cells))
                self.first_move = r
                return r
            
            # second move: same row as first one
            if self.move_count == 2:
                i = self.first_move[0]
                # choose any empty cell from the row of the first chosen cell
                choose_from = set()
                for c in empty_cells:
                    if (c[0] == i):
                        choose_from.add(c)
                j = random.choice(list(choose_from))[1]
                
                self.second_move = (i, j)
                return i, j
            
            # third and fourth move: same column as first one and no other color in the same row as them and the same column as second move
            if (self.move_count == 3) or (self.move_count == 4):
                j = self.first_move[1]
                i = random.choice(list(free_row))
                
                if self.move_count == 3:
                    self.third_move = (i, j)
                else:
                    self.fourth_move = (i, j)
                return i, j
            
            # fifth move
            if self.move_count == 5:
                i = self.first_move[0]
                choose_from = set()
                for c in empty_cells:
                    if (c[0] == i) and ((self.third_move[0], c[1]) in empty_cells) and ((self.fourth_move[0], c[1]) in empty_cells):
                        choose_from.add(c)
                j = random.choice(list(choose_from))[1]
            
                return i, j
        # if the table is 4x4
        elif (n == 4) and (m == 4):
            if self.move_count == 1:
                r = random.choice(list(empty_cells))
                self.first_move = r
                return r
            
            # if the first move of the other player was in the same row as the computer's first move
            if self.other_first_move[0] == self.first_move[0]:
                if self.move_count == 2:
                    i = self.first_move[0]
                    j = random.choice(list(free_column))
                    self.second_move = (i, j)
                    return i, j
                if (self.move_count == 3) or (self.move_count == 4):
                    j = self.first_move[1]
                    i = random.choice(list(free_row))
                    if self.move_count == 3:
                        self.third_move = (i, j)
                    else:
                        self.fourth_move = (i, j)
                    return i, j

                if (self.move_count == 5):
                    first_move_row_full = set()
                    for c in empty_cells:
                        if c[0] == self.first_move[0]:
                            first_move_row_full.add(c)
                    # if the row of the first move is full there's another free row
                    # in this case, the sixth move is free to choose
                    if first_move_row_full == set():
                        j = self.first_move[1]
                        i = random.choice(list(free_row))
                        self.fifth_move = (-2, -2)
                        return i, j
                    else:
                        # there should be only one empty cell in this row
                        for r in first_move_row_full:
                            self.fifth_move = r
                            return r
                        # the sixth move is the winning move in this case
                    
                if (self.move_count == 6):
                    if self.fifth_move == (-2, -2):
                        r = random.choice(list(empty_cells))
                        return r
                    
            # if the first move of the other player was in the same column as the computer's first move
            elif self.other_first_move[1] == self.first_move[1]:
                if self.move_count == 2:
                    j = self.first_move[1]
                    i = random.choice(list(free_row))
                    self.second_move = (i, j)
                    return i, j
                if (self.move_count == 3) or (self.move_count == 4):
                    i = self.first_move[0]
                    j = random.choice(list(free_column))
                    if self.move_count == 3:
                        self.third_move = (i, j)
                    else:
                        self.fourth_move = (i, j)
                    return i, j

                if (self.move_count == 5):
                    first_move_column_full = set()
                    for c in empty_cells:
                        if c[1] == self.first_move[1]:
                            first_move_column_full.add(c)
                    # if the row of the first move is full there's another free row
                    # in this case, the sixth move is free to choose
                    if first_move_column_full == set():
                        i = self.first_move[0]
                        j = random.choice(list(free_column))
                        self.fifth_move = (-2, -2)
                        return i, j
                    else:
                        # there should be only one empty cell in this row
                        for r in first_move_column_full:
                            self.fifth_move = r
                            return r
                        # the sixth move is the winning move in this case
                    
                if (self.move_count == 6):
                    if self.fifth_move == (-2, -2):
                        r = random.choice(list(empty_cells))
                        return r
                    
            # if player 2 chose a free cell
            elif self.first_move_free == (0, 0):
                if self.move_count == 2:
                    i = self.first_move[0]
                    j = random.choice(list(free_column))
                    self.second_move = (i, j)
                    return i, j
                # if the first two moves are in the same row
                if self.other_first_move[0] == self.other_second_move[0]:
                    if (self.move_count == 3) or (self.move_count == 4):
                        j = self.first_move[1]
                        i = random.choice(list(free_row))
                        if self.move_count == 3:
                            self.third_move = (i, j)
                        else:
                            self.fourth_move = (i, j)
                        return i, j
                    if (self.move_count == 5):
                        i = self.first_move[0]
                        j = random.choice(list(free_column))
                        return i, j
                
                # if the first two moves are in the same column
                if self.other_first_move[1] == self.other_second_move[1]:
                    if self.move_count == 3:
                        j = self.first_move[1]
                        i = random.choice(list(free_row))
                        self.third_move = (i, j)
                        return i, j
                    if (self.move_count == 4):
                        i = self.first_move[0]
                        j = random.choice(list(free_column))
                        return i, j
                    if (self.move_count == 5):
                        j = self.first_move[1]
                        choose_from = set()
                        for c in empty_cells:
                            if (c[1] == j):
                                choose_from.add(c)
                        i = random.choice(list(choose_from))[0]
                        return i, j
                    
                # if the first two moves are not in the same column or the same row
                else:
                    # if the second move of the other player was in the same row as the first move of the computer
                    if self.other_second_move[0] == self.first_move[0]:
                        if (self.move_count == 3) or (self.move_count == 4):
                            j = self.first_move[1]
                            i = random.choice(list(free_row))
                            return i, j
                        
                        if (self.move_count == 5):
                            i = self.first_move[0]
                            choose_from = set()
                            for c in empty_cells:
                                if (c[0] == i):
                                    choose_from.add(c)
                            j = random.choice(list(choose_from))[1]
                            return i, j
                    # if the second move of the other player was in the same column as the first or second move of the computer
                    if (self.other_second_move[1] == self.first_move[1]) or (self.other_second_move[1] == self.second_move[1]):
                        if (self.move_count == 3):
                            j = self.first_move[1]
                            i = random.choice(list(free_row))
                            return i, j
                        if (self.move_count == 4):
                            i = self.first_move[0]
                            j = random.choice(list(free_column))
                            return i, j
                        if (self.move_count == 5):
                            i = self.other_first_move[0]
                            j = self.first_move[1]
                            return i, j
                        
                    # in this case, the second move of the other player is in a separate row and column
                    else:
                        if (self.move_count == 3):
                            j = self.second_move[1]
                            i = random.choice(list(free_row))
                            self.third_move = (i, j)
                            return i, j
                        if (self.move_count == 4):
                            i = self.third_move[0]
                            j = self.other_second_move[1]
                            return i, j
                        if (self.move_count == 5):
                            i = self.other_first_move[0]
                            j = self.second_move[1]
                            return i, j
                        
    # non-losing strategy for player 1 and player 2: 2 colors, the one who completes a forbidden rectangle wins               
    def strategy_draw_2xm_c2(self):
        if self.player == 1:
            # if all the cells are empty, choose a random cell
            if self.other_last_move == (-1, -1):
                r = random.choice(list(empty_cells))
                return r

            if n == 2:
                # if player 2 chose a free column
                if self.last_move_free[1] == 0:
                    # choose the same column
                    i = (self.other_last_move[0] + 1) % 2
                    j = self.other_last_move[1]
                    return (i, j)
                else:
                    choose_from = set()
                    for c in empty_cells:
                        if c[1] not in free_column:
                            choose_from.add(c)
                    if choose_from != set():        
                        r = random.choice(list(choose_from))
                    else:
                        r = random.choice(list(empty_cells))
                    return r
            if m == 2:
                # if player 2 chose a free row
                if self.last_move_free[0] == 0:
                    # choose the same row
                    j = (self.other_last_move[1] + 1) % 2
                    i = self.other_last_move[0]
                    return (i, j)
                else:
                    choose_from = set()
                    for c in empty_cells:
                        if c[0] not in free_row:
                            choose_from.add(c)
                    if choose_from != set():        
                        r = random.choice(list(choose_from))
                    else:
                        r = random.choice(list(empty_cells))
                    return r
                
        # as player 2, choose the cell "next to" the cell that player 1 chose
        # as there's a not losing strategy for both players, none of them can win
        elif self.player == 2:
            if n == 2:
                i = (self.other_last_move[0] + 1) % 2
                j = self.other_last_move[1]
                return i, j
            if m == 2:
                j = (self.other_last_move[1] + 1) % 2
                i = self.other_last_move[0]
                return i, j
    
    def strategy_3xm_c2_p1(self):
        # if all the cells are empty, choose a random cell
        if self.other_last_move == (-1, -1):
            r = random.choice(list(empty_cells))
            self.first_move = r
            return r
        
        if n == 3:
            if self.move_count == 2:
                choose_from = set()
                for c in empty_cells:
                    if c[1] == self.first_move[1]:
                        choose_from.add(c)
                r = random.choice(list(choose_from))
                self.second_move = r
                return r
            if self.move_count == 3:
                i = self.first_move[0]
                j = random.choice(list(free_column))
                self.third_move = (i, j)
                return i, j
            if self.move_count == 4:
                choose_from = set()
                for c in empty_cells:
                    if c[1] == self.third_move[1]:
                        choose_from.add(c)
                r = random.choice(list(choose_from))
                return r
            if self.move_count == 5:
                i = self.first_move[0]
                j = random.choice(list(free_column))
                return i, j
        if m == 3:
            if self.move_count == 2:
                choose_from = set()
                for c in empty_cells:
                    if c[0] == self.first_move[0]:
                        choose_from.add(c)
                r = random.choice(list(choose_from))
                self.second_move = r
                return r
            if self.move_count == 3:
                j = self.first_move[1]
                i = random.choice(list(free_row))
                self.third_move = (i, j)
                return i, j
            if self.move_count == 4:
                choose_from = set()
                for c in empty_cells:
                    if c[0] == self.third_move[0]:
                        choose_from.add(c)
                r = random.choice(list(choose_from))
                return r
            if self.move_count == 5:
                j = self.first_move[1]
                i = random.choice(list(free_row))
                return i, j
                
    
    # returns the computer's next move
    def move(self):

        self.move_count += 1
        
        # if it can win in one move
        if (rect_complete_wins == True) and (self.can_complete_rect(self.last_move[0], self.last_move[1], color_of_cell)[0] == True) and (self.last_move[0] != -1):
            return (self.can_complete_rect(self.last_move[0], self.last_move[1], color_of_cell)[1], self.can_complete_rect(self.last_move[0], self.last_move[1], color_of_cell)[2])
        
        # other player missed the opportinity
        elif (rect_complete_wins == True) and (cell_colors == 1) and (self.can_complete_rect(self.last_move_missed_opportunity[0], self.last_move_missed_opportunity[1], color_of_cell)[0] == True) and (not self.last_move_missed_opportunity[0] == -1) and (not self.last_move_missed_opportunity[1] == -1):
            return (self.can_complete_rect(self.last_move_missed_opportunity[0], self.last_move_missed_opportunity[1], color_of_cell)[1], self.can_complete_rect(self.last_move_missed_opportunity[0], self.last_move_missed_opportunity[1], color_of_cell)[2])
        
        # strategy for even x odd, odd x even and even x even tables if there's ONE color and the computer is player 2
        elif (rect_complete_wins == True) and ((n % 2 == 0 or m % 2 == 0) and (self.player == 2) and (cell_colors == 1)):
            r = self.strategy_even_c1_p2()
            return r
        
        # strategy for odd x odd tables if there's ONE color and the computer is player 1
        elif (rect_complete_wins == True) and ((n % 2 != 0 and m % 2 != 0) and (self.player == 1) and (cell_colors == 1)):
            r = self.strategy_odd_c1_p1()
            return r
        
        # strategy for n x m tables where n, m >= 4 if there are TWO colors and the computer is player 1
        elif (rect_complete_wins == True) and ((self.player == 1) and (cell_colors == 2) and (((n >= 5) and (m >= 5)) or ((n == 4) and (m == 4)))):
            r = self.strategy_4plus_c2_p1()
            return r
        
        # non-losing strategy for 2 x m and n x 2 tables if there are TWO colors
        elif (rect_complete_wins == True) and (cell_colors == 2) and (n == 2 or m == 2):
            r = self.strategy_draw_2xm_c2()
            return r
        
        # strategy for 3 x m (m >=5) and n x 3 (n >= 5) tables for player 1 if there are TWO colors
        elif (rect_complete_wins == True) and (cell_colors == 2) and (self.player == 1) and ((n == 3 and m >= 5) or (m == 3 and n >= 5)):
            r = self.strategy_3xm_c2_p1()
            return r
        
        else:
            #chooses a random empty cell
            r = random.choice(list(empty_cells))
            return r
            
        
                    
    
# background of the table
class Background(pygame.sprite.Sprite):
    def __init__(self, x_center, y_center):
        super(Background, self).__init__()
        self.surf = pygame.Surface((table_width, table_height))
        self.surf.fill((150, 150, 50))  # color of lines
        self.rect = self.surf.get_rect(center=(x_center, y_center))
    def update(self):
        if not current_screen == "table":
            self.kill()

class Text_():
    def __init__(self, text, x = SCREEN_WIDTH/2, y = (SCREEN_HEIGHT-table_height)/4, s = 30, color = (0,0,0)):
        self.x = x #Horizontal center of box
        self.y = y #Vertical center of box
        self.update_text(text, s, color)
    
    def update_text(self, text, s = 30, color = (0,0,0)):
        pygame.font.init()
        font = pygame.font.SysFont("sans", s)
        self.txt = font.render(text, True, color) # True: antialias
        self.size = font.size(text) #(width, height)
        
    def text_blit(self):
        drawX = self.x - (self.size[0] / 2.)
        drawY = self.y - (self.size[1] / 2.)
        screen.blit(self.txt, (drawX, drawY))
    


class Cell(pygame.sprite.Sprite):
    # start_x and start_y are the x and y coordinates of the position of the background
    def __init__(self, matrix_position_x, matrix_position_y, start_x, start_y):
        super(Cell, self).__init__()
        self.x = matrix_position_x
        self.y = matrix_position_y
        self.x_center = start_x + line_weight + cell_side_length/2 + (cell_side_length + line_weight) * matrix_position_y
        self.y_center = start_y + line_weight + cell_side_length/2 + (cell_side_length + line_weight) * matrix_position_x
        self.surf = pygame.Surface((cell_side_length, cell_side_length))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(self.x_center, self.y_center))
    
    def update(self):
        if not current_screen == "table":
            self.kill()

    # If a cell gets clicked change its color & remove it from empty_cells set
    def got_clicked(self, p, color=(120, 120, 10)):
        self.surf.fill(color)
        A[self.x][self.y] = p
        empty_cells.remove((self.x, self.y))
        if self.x in free_row:
            free_row.remove(self.x)
        if self.y in free_column:
            free_column.remove(self.y)
        
    # Is there a forbidden rectangle in the matrix? >> bool
    def forbidden_rectangle (self, p=1):
        for i in range(n):
            if (A[i][self.y] == p) and (i != self.x):
                for j in range(m):
                    if (A[self.x][j] == p) and (j != self.y) and (A[i][j] == p):
                        return True
        return False

# button class
class Button(pygame.sprite.Sprite):    
    def __init__(self, x_center, y_center, b_width, b_height, action, choice=0, clicked_color=(150, 150, 50), color=(120, 120, 10)):
        super(Button, self).__init__()
        self.color = color
        self.clicked_color = clicked_color
        self.action = action # what does the button do?
        
        self.surf = pygame.Surface((b_width, b_height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center=(x_center, y_center))
        
        self.already_clicked = False
        self.choice = choice
        
    def got_clicked(self):
        
        if ((self.action == "start") and (current_screen == "welcome")) or ((self.action == "restart") and (current_screen == "winners")):
            self.kill()
            
        elif ((self.action == "choose players" or self.action == "table size") and (current_screen == "table size")) or ((self.action == "win or lose" or self.action == "colors") and current_screen == "game modes"):
            if (self.already_clicked == True):
                self.surf.fill(self.color)
                self.already_clicked = False
            else:
                self.surf.fill(self.clicked_color)
                self.already_clicked = True
                
                
    
    def change_screen(self):
        # current screen
        c = ""
        
        if (self.action == "start") and (current_screen == "welcome"):
            c = "waiting_room_start"
        
        elif (self.action == "restart") and (current_screen == "winners"):
            c = "waiting_room_restart"
                        
            
        return c
    
class InputBox(pygame.sprite.Sprite):    
    def __init__(self, x_center, y_center, b_width, b_height, user_text, color_inactive=(120, 120, 10), color_active=(150, 150, 50)):
        super(InputBox, self).__init__()
        self.x_center = x_center
        self.y_center = y_center
        self.b_width = b_width
        self.b_height = b_height
        
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = color_inactive
        
        self.base_font = pygame.font.Font(None, 32) 
        self.user_text = user_text
        self.active = False

        self.surf = pygame.Surface((b_width, b_height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center=(x_center, y_center))
        
    def input_blit(self):
        if self.active: 
            self.color = self.color_active 
        else: 
            self.color = self.color_inactive
        self.surf.fill(self.color)

        screen.blit(self.surf, self.rect)

        self.text_surface = self.base_font.render(self.user_text, True, (255, 255, 255)) 

        # render roughly at the beginning of the box
        screen.blit(self.text_surface, (self.x_center-self.b_width/2+5, self.y_center-self.b_height/3)) 
      

            
        
    
# *********************************** SPRITE GROUPS & TEXT ***********************************

table_sprites = pygame.sprite.Group()
cells = pygame.sprite.Group()
buttons = pygame.sprite.Group()
inputboxes = pygame.sprite.Group()

bg = Background(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
table_sprites.add(bg)

for i in range(n):
    for j in range(m):
        cell = Cell(i, j, bg.rect.x, bg.rect.y)
        table_sprites.add(cell)
        cells.add(cell)
        
welcome_sprites = pygame.sprite.Group()
start_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 50, "start")
start_text = Text_("START", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
welcome_sprites.add(start_button)
buttons.add(start_button)

winner_sprites = pygame.sprite.Group()
restart_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 150, 50, "restart")
restart_text = Text_("RESTART", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
winner_sprites.add(restart_button)
buttons.add(restart_button)


table_size_sprites = pygame.sprite.Group()
pvp_buttons = pygame.sprite.Group()
table_size_buttons = pygame.sprite.Group()

# player vs player
pvp_button = Button(SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 130, 50, "choose players", 0)
pvp_text = Text_("Player vs player", SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 15)
table_size_sprites.add(pvp_button)
pvp_buttons.add(pvp_button)
buttons.add(pvp_button)

# player vs computer
pvc_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, 130, 50, "choose players", 1)
pvc_text = Text_("Player vs computer", SCREEN_WIDTH/2, SCREEN_HEIGHT/4, 15)
table_size_sprites.add(pvc_button)
pvp_buttons.add(pvc_button)
buttons.add(pvc_button)

# computer vs computer
cvc_button = Button(3*SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 130, 50, "choose players", 2)
cvc_text = Text_("Computer vs computer", 3*SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 15)
table_size_sprites.add(cvc_button)
pvp_buttons.add(cvc_button)
buttons.add(cvc_button)


# 4x4 table
table_4x4_button = Button(SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 130, 50, "table size", 0)
table_4x4_text = Text_("4 × 4", SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 20)
table_size_sprites.add(table_4x4_button)
table_size_buttons.add(table_4x4_button)
buttons.add(table_4x4_button)

# 5x5 table
table_5x5_button = Button(2*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 130, 50, "table size", 1)
table_5x5_text = Text_("5 × 5", 2*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 20)
table_size_sprites.add(table_5x5_button)
table_size_buttons.add(table_5x5_button)
buttons.add(table_5x5_button)

# 5x6 table
table_5x6_button = Button(3*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 130, 50, "table size", 2)
table_5x6_text = Text_("5 × 6", 3*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 20)
table_size_sprites.add(table_5x6_button)
table_size_buttons.add(table_5x6_button)
buttons.add(table_5x6_button)


game_modes_sprites = pygame.sprite.Group()
win_or_lose_buttons = pygame.sprite.Group()
colors_buttons = pygame.sprite.Group()

# wins button
wins_button = Button(SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 130, 50, "win or lose", 0)
wins_text = Text_("wins", SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 20)
game_modes_sprites.add(wins_button)
win_or_lose_buttons.add(wins_button)
buttons.add(wins_button)

# loses button
loses_button = Button(2*SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 130, 50, "win or lose", 1)
loses_text = Text_("loses", 2*SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 20)
game_modes_sprites.add(loses_button)
win_or_lose_buttons.add(loses_button)
buttons.add(loses_button)

# 1 color button
one_color_button = Button(SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 130, 50, "colors", 1)
one_color_text = Text_("1", SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 20)
game_modes_sprites.add(one_color_button)
colors_buttons.add(one_color_button)
buttons.add(one_color_button)

# 2 colors button
two_colors_button = Button(2*SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 130, 50, "colors", 2)
two_colors_text = Text_("2", 2*SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 20)
game_modes_sprites.add(two_colors_button)
colors_buttons.add(two_colors_button)
buttons.add(two_colors_button)

# game modes screen text
game_modes_text = Text_("GAME MODES", SCREEN_WIDTH/2, SCREEN_HEIGHT/8, 35)
win_or_lose_text = Text_("The player that completes a forbidden rectangle...", SCREEN_WIDTH/2, 9*SCREEN_HEIGHT/32, 20)
colors_text = Text_("Number of colors in the game:", SCREEN_WIDTH/2, 18*SCREEN_HEIGHT/32, 20)

# table size screen text
player_types_text = Text_("PLAYERS", SCREEN_WIDTH/2, SCREEN_HEIGHT/8, 35)
table_size_text = Text_("TABLE SIZE", SCREEN_WIDTH/2, 11*SCREEN_HEIGHT/24, 35)
custom_size_text = Text_("CUSTOM", SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/4, 25)
times_text = Text_("×", 5*SCREEN_WIDTH/8, 3*SCREEN_HEIGHT/4, 30)

n_input = InputBox(SCREEN_WIDTH/2, 3*SCREEN_HEIGHT/4, 50, 30, "n")
inputboxes.add(n_input)
m_input = InputBox(3*SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/4, 50, 30, "m")
inputboxes.add(m_input)


player_text = Text_("Player 1")
winner_text = Text_("Draw")
press_space_text = Text_("[Press SPACE to continue]", SCREEN_WIDTH/2, SCREEN_HEIGHT-(SCREEN_HEIGHT-table_height)/4, 15)


comps = []

# if it is a player vs computer game, the computer is player 1 or player 2?
# it is chosen randomly
comp_which_player = random.randrange(1, 3)

if against_comp == 0:
    comp1 = Computer(0)
elif (against_comp == 2):
    comp1 = Computer(1)
else:
    comp1 = Computer(comp_which_player)
comps.append(comp1)
if against_comp == 2:
    comp2 = Computer(2)
    comps.append(comp2)

# *********************************** GAME RUNNING ***********************************

running = True

while running:
    
    # Fill the background with white
    screen.fill((255, 255, 255))
        
    # Restarts the game
    if (restart == True) or (setting == True):
        
        # basic settings
        if n >= m:
            table_height = SCREEN_HEIGHT - upper_margin - lower_margin
            cell_side_length = (table_height-(n+1)*line_weight)/n
            table_width = (m+1)*line_weight + m*cell_side_length
        else:
            table_width = SCREEN_WIDTH - left_margin - right_margin
            cell_side_length = (table_width-(m+1)*line_weight)/m
            table_height = (n+1)*line_weight + n*cell_side_length
        if restart == True:
            player_turn = 1
            player_won = 0
            against_comp = 0
            cell_colors = 2
            color_of_cell = 1
            rect_complete_wins = True
            game_on = False
        winners_space = False
        A = np.zeros((n, m))
        free_row = set()
        free_column = set()
        for i in range(n):
            free_row.add(i)
        for j in range(m):
            free_column.add(j)
        empty_cells = set()
        for i in range(n):
            for j in range(m):
                if A[i][j] == 0:
                    empty_cells.add((i, j))
        screens = ["welcome", "game modes", "table size", "hint", "table", "winner"]
        if (restart == True):
            current_screen = "welcome"
        # sprites & text
        table_sprites = pygame.sprite.Group()
        cells = pygame.sprite.Group()
        buttons = pygame.sprite.Group()
        inputboxes = pygame.sprite.Group()

        bg = Background(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        table_sprites.add(bg)

        for i in range(n):
            for j in range(m):
                cell = Cell(i, j, bg.rect.x, bg.rect.y)
                table_sprites.add(cell)
                cells.add(cell)

        welcome_sprites = pygame.sprite.Group()
        start_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 50, "start")
        start_text = Text_("START", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        welcome_sprites.add(start_button)
        buttons.add(start_button)

        winner_sprites = pygame.sprite.Group()
        restart_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 150, 50, "restart")
        restart_text = Text_("RESTART", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        winner_sprites.add(restart_button)
        buttons.add(restart_button)


        table_size_sprites = pygame.sprite.Group()
        pvp_buttons = pygame.sprite.Group()
        table_size_buttons = pygame.sprite.Group()

        # player vs player
        pvp_button = Button(SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 130, 50, "choose players", 0)
        pvp_text = Text_("Player vs player", SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 15)
        table_size_sprites.add(pvp_button)
        pvp_buttons.add(pvp_button)
        buttons.add(pvp_button)

        # player vs computer
        pvc_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, 130, 50, "choose players", 1)
        pvc_text = Text_("Player vs computer", SCREEN_WIDTH/2, SCREEN_HEIGHT/4, 15)
        table_size_sprites.add(pvc_button)
        pvp_buttons.add(pvc_button)
        buttons.add(pvc_button)

        # computer vs computer
        cvc_button = Button(3*SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 130, 50, "choose players", 2)
        cvc_text = Text_("Computer vs computer", 3*SCREEN_WIDTH/4, SCREEN_HEIGHT/4, 15)
        table_size_sprites.add(cvc_button)
        pvp_buttons.add(cvc_button)
        buttons.add(cvc_button)


        # 4x4 table
        table_4x4_button = Button(SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 130, 50, "table size", 0)
        table_4x4_text = Text_("4 × 4", SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 20)
        table_size_sprites.add(table_4x4_button)
        table_size_buttons.add(table_4x4_button)
        buttons.add(table_4x4_button)

        # 5x5 table
        table_5x5_button = Button(2*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 130, 50, "table size", 1)
        table_5x5_text = Text_("5 × 5", 2*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 20)
        table_size_sprites.add(table_5x5_button)
        table_size_buttons.add(table_5x5_button)
        buttons.add(table_5x5_button)

        # 5x6 table
        table_5x6_button = Button(3*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 130, 50, "table size", 2)
        table_5x6_text = Text_("5 × 6", 3*SCREEN_WIDTH/4, 7*SCREEN_HEIGHT/12, 20)
        table_size_sprites.add(table_5x6_button)
        table_size_buttons.add(table_5x6_button)
        buttons.add(table_5x6_button)


        game_modes_sprites = pygame.sprite.Group()
        win_or_lose_buttons = pygame.sprite.Group()
        colors_buttons = pygame.sprite.Group()

        # wins button
        wins_button = Button(SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 130, 50, "win or lose", 0)
        wins_text = Text_("wins", SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 20)
        game_modes_sprites.add(wins_button)
        win_or_lose_buttons.add(wins_button)
        buttons.add(wins_button)

        # loses button
        loses_button = Button(2*SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 130, 50, "win or lose", 1)
        loses_text = Text_("loses", 2*SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/16, 20)
        game_modes_sprites.add(loses_button)
        win_or_lose_buttons.add(loses_button)
        buttons.add(loses_button)

        # 1 color button
        one_color_button = Button(SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 130, 50, "colors", 1)
        one_color_text = Text_("1", SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 20)
        game_modes_sprites.add(one_color_button)
        colors_buttons.add(one_color_button)
        buttons.add(one_color_button)

        # 2 colors button
        two_colors_button = Button(2*SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 130, 50, "colors", 2)
        two_colors_text = Text_("2", 2*SCREEN_WIDTH/3, 21*SCREEN_HEIGHT/32, 20)
        game_modes_sprites.add(two_colors_button)
        colors_buttons.add(two_colors_button)
        buttons.add(two_colors_button)

        # game modes screen text
        game_modes_text = Text_("GAME MODES", SCREEN_WIDTH/2, SCREEN_HEIGHT/8, 35)
        win_or_lose_text = Text_("The player that completes a forbidden rectangle...", SCREEN_WIDTH/2, 9*SCREEN_HEIGHT/32, 20)
        colors_text = Text_("Number of colors in the game:", SCREEN_WIDTH/2, 18*SCREEN_HEIGHT/32, 20)

        # table size screen text
        player_types_text = Text_("PLAYERS", SCREEN_WIDTH/2, SCREEN_HEIGHT/8, 35)
        table_size_text = Text_("TABLE SIZE", SCREEN_WIDTH/2, 11*SCREEN_HEIGHT/24, 35)
        custom_size_text = Text_("CUSTOM", SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/4, 25)
        times_text = Text_("×", 5*SCREEN_WIDTH/8, 3*SCREEN_HEIGHT/4, 30)

        n_input = InputBox(SCREEN_WIDTH/2, 3*SCREEN_HEIGHT/4, 50, 30, "n")
        inputboxes.add(n_input)
        m_input = InputBox(3*SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/4, 50, 30, "m")
        inputboxes.add(m_input)


        player_text = Text_("Player 1")
        winner_text = Text_("Draw")
        press_space_text = Text_("[Press SPACE to continue]", SCREEN_WIDTH/2, SCREEN_HEIGHT-(SCREEN_HEIGHT-table_height)/4, 15)


        comps = []
        comp_which_player = random.randrange(1, 3)

        if against_comp == 0:
            comp1 = Computer(0)
        elif (against_comp == 2):
            comp1 = Computer(1)
        else:
            comp1 = Computer(comp_which_player)
        comps.append(comp1)
        if against_comp == 2:
            comp2 = Computer(2)
            comps.append(comp2)

         
        # the whole game starts again
        if restart == True:
            restart = False
        
        # the setting is finished
        if setting == True:
            setting = False
        
    
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            # Was it the Space key? If so and the game is not on, switch to winners screen.
            if (event.key == K_SPACE) and (game_on == False) and (current_screen == "table"):
                winners_space = True
            
            elif (event.key == K_SPACE) and (game_on == False) and (current_screen == "table size"):
                setting = True
                            
                current_screen = "table"
                game_on = True
            
            elif (event.key == K_SPACE) and (game_on == False) and (current_screen == "game modes"):
                            
                current_screen = "table size"
                
                
            if (event.key == K_RETURN) and (current_screen == "table size"):
                if (n_input.active == True):
                    n_input.active = False
                if (m_input.active == True):
                    m_input.active = False
                    
            if (event.key == K_BACKSPACE) and (current_screen == "table size"): 
                if (n_input.active == True):
                    # get text input from 0 to -1
                    n_input.user_text = n_input.user_text[:-1]
                if (m_input.active == True):
                    # get text input from 0 to -1
                    m_input.user_text = m_input.user_text[:-1]
            
            # Unicode standard is used for string formation
            elif (current_screen == "table size"):
                if (n_input.active == True):
                    n_input.user_text += event.unicode
                if (m_input.active == True):
                    m_input.user_text += event.unicode

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
                    
        # Handle MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            # Get a list of all inputboxes that are under the mouse cursor
            inputbox_list = [inp for inp in inputboxes if inp.rect.collidepoint(pos)]
            for inp in inputbox_list:
                if (inp == n_input) and (current_screen == "table size") and (inp.active == False):
                    inp.active = True
                    m_input.active = False
                    for b in table_size_buttons:
                            if (b.already_clicked == True):
                                b.got_clicked()
                    if n_input.user_text == "n":
                        n_input.user_text = ''
                if (inp == m_input) and (current_screen == "table size") and (inp.active == False):
                    inp.active = True
                    n_input.active = False
                    for b in table_size_buttons:
                            if (b.already_clicked == True):
                                b.got_clicked()
                    if m_input.user_text == "m":
                        m_input.user_text = ''
            
            # Get a list of all buttons that are under the mouse cursor
            buttons_list = [b for b in buttons if b.rect.collidepoint(pos)]
            for b in buttons_list:
                if (b == start_button) and (current_screen == "welcome"):
                    b.got_clicked()
                    current_screen = b.change_screen()
                elif (b == restart_button) and (current_screen == "winners"):
                    b.got_clicked()
                    winners_space = False
                    current_screen = b.change_screen()
                    
                elif (b in pvp_buttons) and (current_screen == "table size"):
                    b.got_clicked()
                    if b.already_clicked == True:
                        against_comp = b.choice
                        for other in pvp_buttons:
                            if (other != b) and (other.already_clicked == True):
                                other.got_clicked()
                                
                elif (b in table_size_buttons) and (current_screen == "table size"):
                    b.got_clicked()
                    if b.already_clicked == True:
                        if b.choice == 0:
                            n = 4
                            m = 4
                        elif b.choice == 1:
                            n = 5
                            m = 5
                        elif b.choice == 2:
                            n = 5
                            m = 6
                        for other in table_size_buttons:
                            if (other != b) and (other.already_clicked == True):
                                other.got_clicked()
                        if n_input.active == True:
                            n_input.active = False
                        if m_input.active == True:
                            m_input.active = False
                
                elif (b in win_or_lose_buttons) and (current_screen == "game modes"):
                    b.got_clicked()
                    if b.already_clicked == True:
                        if b.choice == 0:
                            rect_complete_wins = True
                        elif b.choice == 1:
                            rect_complete_wins = False
                        for other in win_or_lose_buttons:
                            if (other != b) and (other.already_clicked == True):
                                other.got_clicked()
                
                elif (b in colors_buttons) and (current_screen == "game modes"):
                    b.got_clicked()
                    if b.already_clicked == True:
                        cell_colors = b.choice
                        for other in colors_buttons:
                            if (other != b) and (other.already_clicked == True):
                                other.got_clicked()
                        
                        
                

            # Get a list of all cells that are under the mouse cursor
            clicked_cells = [s for s in cells if s.rect.collidepoint(pos)]
            if (current_screen == "table") and (game_on == True) and (not comp1.player == player_turn) and (not against_comp == 2):
                for s in clicked_cells:
                    # Has it been clicked before?
                    if (current_screen == "table") and ((s.x, s.y) in empty_cells) and (game_on == True) and (not comp1.player == player_turn) and (not against_comp == 2):
                        # free row, column
                        if (s.x in free_row) and (s.y in free_column):
                            if (cell_colors == 2) and (comp1.move_count == 1):
                                comp1.first_move_free = (0, 0)
                            comp1.last_move_free = (0, 0)
                        elif (not (s.x in free_row)) and (s.y in free_column):
                            comp1.last_move_free = (1, 0)
                        elif (s.x in free_row) and (not (s.y in free_column)):
                            comp1.last_move_free = (0, 1)
                        else:
                            comp1.last_move_free = (1, 1)


                        if cell_colors == 2:
                            comp1.other_last_move = ((s.x, s.y))
                            # if it's the player's first move
                            if comp1.move_count == 1:
                                comp1.other_first_move = ((s.x, s.y))
                            if comp1.move_count == 2:
                                comp1.other_second_move = ((s.x, s.y))


                        # cell gets clicked
                        if color_of_cell == 1:
                            s.got_clicked(1)

                            # if there's only one color, the computer counts this move as the last move
                            if cell_colors == 1:
                                comp1.last_move = ((s.x, s.y))
                        else:
                            s.got_clicked(2, (199, 128, 35))
                        if s.forbidden_rectangle(color_of_cell) == False:
                            if against_comp == 1:
                                current_screen = "table wait"
                            player_turn = abs(player_turn - 3)
                            if cell_colors == 2:
                                color_of_cell = abs(color_of_cell - 3)
                            if player_turn == 1:
                                player_text.update_text("Player 1")
                            else:
                                player_text.update_text("Player 2")

                        else:
                            if rect_complete_wins:
                                player_won = player_turn
                            else:
                                player_won = abs(player_turn - 3)
                            if color_of_cell == 1:
                                s.surf.fill((200, 200, 70))
                            else:
                                s.surf.fill((239, 178, 97))

                            game_on = False
    
    if empty_cells == set():
        player_won = 0
        game_on = False
    
    if against_comp != 0:
        
        # computer's move
        for comp in comps:
            
            if (comp.player == player_turn) and (game_on == True):
                
                mov = comp.move()
                
                for s in cells:
                    # finds the cell with the same coordinates
                    if (s.x == mov[0]) and (s.y == mov[1]) and (mov in empty_cells):
                         # if computer vs computer
                        if against_comp == 2:
                            # if the comp is comp1
                            if (comp == comp1):
                                # free row, column
                                    if (s.x in free_row) and (s.y in free_column):
                                        if (cell_colors == 2) and (comp2.move_count == 1):
                                            comp2.first_move_free = (0, 0)
                                        comp2.last_move_free = (0, 0)
                                    elif (not (s.x in free_row)) and (s.y in free_column):
                                        comp2.last_move_free = (1, 0)
                                    elif (s.x in free_row) and (not (s.y in free_column)):
                                        comp2.last_move_free = (0, 1)
                                    else:
                                        comp2.last_move_free = (1, 1)

                                    # if it's the other computer's first move
                                    if cell_colors == 2:
                                        comp2.other_last_move = ((s.x, s.y))
                                        if comp2.move_count == 1:
                                            comp2.other_first_move = ((s.x, s.y))
                                        if comp2.move_count == 2:
                                            comp2.other_second_move = ((s.x, s.y))

                                    # if there's only one color, the computer counts this move as the last move
                                    if (cell_colors == 1) and (color_of_cell == 1):
                                        comp2.last_move = ((s.x, s.y))

                            # if the comp is comp2
                            if (comp == comp2):
                                # free row, column
                                    if (s.x in free_row) and (s.y in free_column):
                                        if (cell_colors == 2) and (comp1.move_count == 1):
                                            comp1.first_move_free = (0, 0)
                                        comp1.last_move_free = (0, 0)
                                    elif (not (s.x in free_row)) and (s.y in free_column):
                                        comp1.last_move_free = (1, 0)
                                    elif (s.x in free_row) and (not (s.y in free_column)):
                                        comp1.last_move_free = (0, 1)
                                    else:
                                        comp1.last_move_free = (1, 1)

                                    # if it's the other computer's first move
                                    if cell_colors == 2:
                                        comp1.other_last_move = ((s.x, s.y))
                                        if comp1.move_count == 1:
                                            comp1.other_first_move = ((s.x, s.y))
                                        if comp1.move_count == 2:
                                            comp1.other_second_move = ((s.x, s.y))

                                    # if there's only one color, the computer counts this move as the last move
                                    if (cell_colors == 1) and (color_of_cell == 1):
                                        comp1.last_move = ((s.x, s.y))


                        comp.last_move = mov

                        if color_of_cell == 1:
                            if cell_colors == 1:
                                comp.last_move_missed_opportunity = mov
                            s.got_clicked(1)
                        else:
                            s.got_clicked(2, (199, 128, 35))

                        if s.forbidden_rectangle(color_of_cell) == False:
                            player_turn = abs(player_turn - 3)
                            if cell_colors == 2:
                                color_of_cell = abs(color_of_cell - 3)
                            if player_turn == 1:
                                player_text.update_text("Player 1")
                            else:
                                player_text.update_text("Player 2")

                        else:
                            if rect_complete_wins:
                                player_won = player_turn
                            else:
                                player_won = abs(player_turn - 3)
                            if color_of_cell == 1:
                                s.surf.fill((200, 200, 70))
                            else:
                                s.surf.fill((239, 178, 97))

                            game_on = False
                if against_comp == 2:
                    current_screen = "table wait"
                    break
            
            
    
    # switch to the winners screen if the Spacebar is pressed                    
    if winners_space == True:
        current_screen = "winners"
        table_sprites.update()

        if player_won == 1:
            winner_text.update_text("WINNER: Player 1")
        elif player_won == 2:
            winner_text.update_text("WINNER: Player 2")
        else:
            winner_text.update_text("Draw")           
        winner_text.text_blit()
        
        for entity in winner_sprites:
            screen.blit(entity.surf, entity.rect)
        restart_text.text_blit()


    # Draw all our table sprites if the game is on
    elif current_screen == "table" or current_screen == "table wait":
        for entity in table_sprites:
            screen.blit(entity.surf, entity.rect)
        player_text.text_blit()
        
        if game_on == False:
            press_space_text.text_blit()
    
    
    elif current_screen == "welcome":
        for entity in welcome_sprites:
            screen.blit(entity.surf, entity.rect)
        start_text.text_blit()
         
        
    elif current_screen == "waiting_room_start":
        pygame.time.wait(100)
        current_screen = "game modes"
        
    elif current_screen == "waiting_room_restart":
        pygame.time.wait(100)
        current_screen = "welcome"
        restart = True
        
    elif current_screen == "table size":
        n_input.input_blit()
        if n_input.user_text.isdigit():
            if isinstance(int(n_input.user_text), int):
                if (int(n_input.user_text) >= 1):
                    n = int(n_input.user_text)
        if n_input.user_text == '' and n_input.active == False:
            n_input.user_text = "n"
        m_input.input_blit()
        if m_input.user_text.isdigit():
            if isinstance(int(m_input.user_text), int):
                if (int(m_input.user_text) >= 1):
                    m = int(m_input.user_text)
        if m_input.user_text == '' and m_input.active == False:
            m_input.user_text = "m"
                    
        
        for entity in table_size_sprites:
            screen.blit(entity.surf, entity.rect)
        
        player_types_text.text_blit()
        table_size_text.text_blit()
        custom_size_text.text_blit()
        times_text.text_blit()
        pvp_text.text_blit()
        pvc_text.text_blit()
        cvc_text.text_blit()
        table_4x4_text.text_blit()
        table_5x5_text.text_blit()
        table_5x6_text.text_blit()
        
        press_space_text.text_blit()
        
    elif current_screen == "game modes":
        for entity in game_modes_sprites:
            screen.blit(entity.surf, entity.rect)
        game_modes_text.text_blit()
        win_or_lose_text.text_blit()
        colors_text.text_blit()
        wins_text.text_blit()
        loses_text.text_blit()
        one_color_text.text_blit()
        two_colors_text.text_blit()
        
        press_space_text.text_blit()
        

        
        
            
            


    
    
    # Flip everything to the display
    pygame.display.flip()
    
    if current_screen == "table wait":
        pygame.time.wait(1000)
        current_screen = "table"



pygame.quit()

