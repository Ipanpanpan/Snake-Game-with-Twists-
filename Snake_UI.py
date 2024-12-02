import pygame, sys
from button import Button
import snake_example as s
from pygame import mixer 

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Assets\snake_bg(4).png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets\EatingPasta-pgxXZ.ttf", size)

# Load music
menu_music = "Assets\Bouncy.mp3"  # Replace with your actual menu music file
game_music = "Assets\Tetris.mp3"  # Replace with your actual game music file
time_music = "Assets\Mario.mp3"

# Game states
MENU = "menu"
GAME = "game"

# Set initial state
state = MENU

# Function to play music
def play_music(file):
    pygame.mixer.music.stop()  # Stop any current music
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)  # Loop music

# Play menu music initially
play_music(menu_music)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(pygame.image.load("Assets\\time_limit2.png"), (0, 0))

        three_minute = Button(image=None, pos=(750, 90), 
                            text_input="3:00", font=get_font(170), base_color="#1c2127", hovering_color="#72921f") #Green
        twonahalf_minute = Button(image=None, pos=(1150, 230), 
                            text_input="0:30", font=get_font(115), base_color="#1c2127", hovering_color="#5e4893") #Purple
        thirty_sec = Button(image=None, pos=(780, 620), 
                            text_input="2:30", font=get_font(200), base_color="#1c2127", hovering_color="#416acc") #blue
        three_minute.changeColor(PLAY_MOUSE_POS)
        three_minute.update(SCREEN)
        twonahalf_minute.changeColor(PLAY_MOUSE_POS)
        twonahalf_minute.update(SCREEN)
        thirty_sec.changeColor(PLAY_MOUSE_POS)
        thirty_sec.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if three_minute.checkForInput(PLAY_MOUSE_POS):
                    play_music(game_music)
                    s.game_loop() # add time
                if twonahalf_minute.checkForInput(PLAY_MOUSE_POS):
                    play_music(game_music)
                    s.game_loop() # add time
                if thirty_sec.checkForInput(PLAY_MOUSE_POS):
                    play_music(game_music)
                    s.game_loop() # add time

        pygame.display.update()
    
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("Assets\\trans_play.png"), pos=(178, 520), 
                            text_input="> PLAY", font=get_font(100), base_color="#f4e9db", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("Assets\\trans_play.png"), pos=(170, 630), 
                            text_input="> QUIT", font=get_font(100), base_color="#f4e9db", hovering_color="#d7fcd4")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_music(time_music)
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()