from re import U
import pygame as pg
from pygame.locals import *
import sys
import time
import color
from scipy.misc import central_diff_weights

board = [[None]*3 for _ in range(3)]
current_player = 1 # player 1 takes first turn, player 2 takes second turn
board_size = 600
turn_number = 0

board_line_width = 7
game_window_width = 900
game_window_length = 600
game_scene_menu_column_width = game_window_width - board_size
game_scene_button_center_x = game_scene_menu_column_width / 2 + board_size
board_square_size=200

x_img = pg.image.load('X.png')
o_img = pg.image.load('O.png')

x_img = pg.transform.scale(x_img, (100,100))
o_img = pg.transform.scale(o_img, (100,100))

pg.init()
fps = 30
cl = pg.time.Clock()
screen = pg.display.set_mode((900, 600), 0, 32)
pg.display.set_caption("Board Game Master")

x_img = pg.image.load('X.png')
o_img = pg.image.load('O.png')

x_img = pg.transform.scale(x_img, (100,100))
o_img = pg.transform.scale(o_img, (100,100))

scene = "menu"

def draw_menu():
    global start_button_rect
    screen.fill(color.black) # white
    #button
    start_button_rect = pg.Rect(299,350,300,100)
    pg.draw.rect(screen, (255, 119, 15), start_button_rect)
    #words
    font = pg.font.Font(None, 80)
    text = font.render("Board Game Master", 1, (255, 119, 15))
    font.set_italic(True)
    font.set_bold(True)
    # put the title at the center of the screen
    text_rect = text.get_rect(center=(game_window_width / 2, 200))
    screen.blit(text, text_rect)
    font = pg.font.Font(None,56)
    start_button = font.render("Start Game", 1, (0,0,0))
    start_rect = start_button.get_rect(center=(game_window_width / 2, 400))
    screen.blit(start_button, start_rect)
    pg.display.update()

def draw_game():
    global board_rect
    global back_button_rect
    global instructions_font
    global player_rect
    global restart_button_rect
    global pause_button_rect
    player_rect = pg.Rect(640,20,200,55)
    board_rect = pg.Rect(0, 0, board_size, board_size)
    screen.fill(color.white)
    instructions_font = pg.font.Font(None, 32)
    instructions = instructions_font.render('Player ' + str(current_player) + '\'s turn', 1, (0, 0, 0))
    instructions_rect = instructions.get_rect(center=(game_scene_button_center_x, 50))
    screen.blit(instructions, instructions_rect)
    button_font = pg.font.Font(None, 56)
    # write the menu buttons
    ## HWK: can i use constants to make this more legible?
    ## HWK - bonus: can i use a loop to make this better?
    ## HWK: how can i adjust the buttons so that they do not cover the board?
    pause_text = button_font.render('PAUSE', 1, color.black)
    back_text = button_font.render('BACK', 1, (0, 0, 0))
    restart_text = button_font.render('RESTART', 1, (0, 0, 0))
    ## get the center position for the menu text
    pause_rect = pause_text.get_rect(center=(game_scene_button_center_x, 150))
    back_rect = back_text.get_rect(center=(game_scene_button_center_x, 250))
    restart_rect = restart_text.get_rect(center=(game_scene_button_center_x, 350))
    ## create the button rectangles at the specified position
    pause_button_rect = pg.Rect(board_size, 100, 300, 100)
    back_button_rect = pg.Rect(board_size, 200, 300, 100)
    restart_button_rect = pg.Rect(board_size, 300, 300, 100)
    ## draw the rectangles on the 
    pg.draw.rect(screen, (250, 0, 0), pause_button_rect)
    pg.draw.rect(screen, (122, 122, 122), back_button_rect)
    pg.draw.rect(screen, (160, 184, 135), restart_button_rect)
    screen.blit(pause_text, pause_rect)
    screen.blit(back_text, back_rect)
    screen.blit(restart_text, restart_rect)
    pg.display.update()
    #棋盘
    screen.fill((222 , 184 , 135) , (0 , 0 , 600 , 600))
    pg.draw.line(screen,(0,0,0),(0,0),(0,board_size),board_line_width)
    pg.draw.line(screen,(0,0,0),(0,0),(board_size,0),board_line_width)
    pg.draw.line(screen,(0,0,0),(0,200),(board_size,200),board_line_width)
    pg.draw.line(screen,(0,0,0),(0,400),(board_size,400),board_line_width)
    pg.draw.line(screen,(0,0,0),(0,600),(board_size,600),board_line_width)
    pg.draw.line(screen,(0,0,0),(200,0),(200,board_size),board_line_width)
    pg.draw.line(screen,(0,0,0),(400,0),(400,board_size),board_line_width)
    pg.draw.line(screen,(0,0,0),(600,0),(600,board_size),board_line_width)
    

def draw_pause():
    global pause_message_dialogue, scene
    message_width = 400
    message_height = 150
    pause_message_dialogue = pg.Rect((game_window_width - message_width) / 2 , (game_window_length - message_height) / 2 , message_width , message_height)   
    pg.draw.rect(screen,  color.pure_red  , pause_message_dialogue)

    pause_font = pg.font.Font(None, 50)
    pause_message = pause_font.render("Game Paused", 1 , color.white)
    pause_message_rect = pause_message.get_rect(center=(game_window_width/2 , game_window_length/2))
    screen.blit(pause_message,pause_message_rect)


def draw_result(result):
    global result_dialogue, scene
    scene = 'result'
    message_width = 400
    message_height = 150
    result_dialogue = pg.Rect((game_window_width - message_width) / 2 , (game_window_length - message_height) / 2 , message_width , message_height)   
    pg.draw.rect(screen,  color.green  , result_dialogue)

    font = pg.font.Font(None, 50)
    win_message = font.render(result, 1 , color.white)
    win_message_rect = win_message.get_rect(center=(game_window_width/2 , game_window_length/2))
    screen.blit(win_message,win_message_rect)


def draw_step(mouse_pos):
    global current_player, turn_number
    global player
    mouse_x, mouse_y = mouse_pos
    column = mouse_x // board_square_size
    row = mouse_y // board_square_size

    if board[column][row] is not None:
        return

    board[column][row] = current_player
    print(board)

    draw_x = column * board_square_size + board_square_size / 4
    draw_y = row * board_square_size + board_square_size / 4


    ## HWK: check which square the mouse_pos was on and draw the image at the center of that squar

    if current_player == 1:
        screen.blit(x_img, (draw_x,draw_y))
        player = current_player
        current_player = 2
        pg.draw.rect(screen, color.white, player_rect)
        instructions = instructions_font.render('Player ' + str(current_player) + '\'s turn', 1, (0, 0, 0))
        instructions_rect = instructions.get_rect(center=(game_scene_button_center_x, 50))
        screen.blit(instructions, instructions_rect)
    else:
        screen.blit(o_img, (draw_x,draw_y))
        player = current_player
        current_player = 1
        pg.draw.rect(screen, color.white, player_rect)
        instructions = instructions_font.render('Player ' + str(current_player) + '\'s turn', 1, (0, 0, 0))
        instructions_rect = instructions.get_rect(center=(game_scene_button_center_x, 50))
        screen.blit(instructions, instructions_rect)

    win_text = check_win()
    
    if win_text:
        draw_result(win_text)
    else:
        turn_number +=1
        if turn_number >= 9:
            draw_result('It\'s a draw')
        update_instruction


def draw_previous_steps():
    for row in range(3):
        for col in range(3):
            draw_x = col * board_square_size + board_square_size / 4
            draw_y = row * board_square_size + board_square_size / 4   
            
            if board[row][col] == 1:
                screen.blit(x_img,(draw_y, draw_x))
                print(draw_x, draw_y)
            elif board[row][col] == 2:
                screen.blit(o_img, (draw_y, draw_x))
                print(draw_x, draw_y)

def reset():
    global current_player
    global board
    current_player = 1
    turn_number = 0
    board = [[None]*3 for _ in range(3)]

def check_win():
    for row in board:
        if row[0] is None:
            continue
        if row[0] == row[1] == row[2]:
            return 'Player ' + str(player) + ' ' +' wins'
    for column in range(3):
        if board[0][column] is None:
            continue
        if board[0][column] == board[1][column] == board[2][column]:
            return 'Player ' + str(player) + ' ' +'wins'
    if board[1][1] is not None and board[0][0] == board[1][1] == board[2][2]:
        return 'Player ' + str(player) + ' ' +' wins'
    if board[1][1] is not None and board[0][2] == board[1][1] == board[2][0]:
        return 'Player ' + str(player) + ' ' + 'wins'

def update_instruction():
    pass


draw_menu()
pg.event.clear()
# run the game loop forever
while True:
    if scene == 'menu':
        for event in pg.event.get():
            if event.type == QUIT: 
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print('mouse button clicked', event)
                print('mouse is at', pg.mouse.get_pos())
                if start_button_rect.collidepoint(pg.mouse.get_pos()):
                    print('start clicked')
                    scene = 'game'
                    draw_game()
    if scene == 'game':
        for event in pg.event.get():
            if event.type == MOUSEBUTTONDOWN:
                print('mouse is at', pg.mouse.get_pos())
                print('mouse clikced on game')
                if back_button_rect.collidepoint(pg.mouse.get_pos()):
                    reset()
                    scene='menu'
                    draw_menu()
                elif board_rect.collidepoint(event.pos):
                    draw_step(event.pos)
                elif restart_button_rect.collidepoint(pg.mouse.get_pos()):
                    reset()
                    draw_game()
                elif pause_button_rect.collidepoint(pg.mouse.get_pos()):
                    scene = 'pause'
                    draw_pause()
    if scene == 'pause':
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if pause_message_dialogue.collidepoint(event.pos):
                    scene = 'game'
                    draw_game()
                    draw_previous_steps()
    if scene == 'result':
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if result_dialogue.collidepoint(event.pos):
                    scene = 'game'
                    draw_game()
                    reset()

    pg.display.update()
    cl.tick(fps)
  