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

def ask_tutorial():
    while True:
        TUTOR_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("Assets\\skiptutorial.png"), (0, 0))
        next_page = Button(image=None, pos=(370, 505), text_input="YES", font=get_font(270), base_color="white", hovering_color="#d7fcd4")
        next_page.changeColor(TUTOR_MOUSE_POS)
        next_page.update(SCREEN)

        back_page = Button(image=None, pos=(1000, 505), text_input="NO", font=get_font(270), base_color="white", hovering_color="#d7fcd4")
        back_page.changeColor(TUTOR_MOUSE_POS)
        back_page.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_page.checkForInput(TUTOR_MOUSE_POS):
                    gamemode()
                if back_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial1()
        pygame.display.update()


def tutorial1():
    while True:
        TUTOR_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("Assets\\Tutorial-1.png"), (0, 0))
        next_page = Button(image=None, pos=(1150, 605), text_input="NEXT", font=get_font(35), base_color="black", hovering_color="brown")
        next_page.changeColor(TUTOR_MOUSE_POS)
        next_page.update(SCREEN)

        back_page = Button(image=None, pos=(1150, 673), text_input="BACK", font=get_font(35), base_color="black", hovering_color="brown")
        back_page.changeColor(TUTOR_MOUSE_POS)
        back_page.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial2()
                if back_page.checkForInput(TUTOR_MOUSE_POS):
                    ask_tutorial()
        pygame.display.update()

def tutorial2():
    while True:
        TUTOR_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("Assets\\Tutorial-2.png"), (0, 0))
        next_page = Button(image=None, pos=(1150, 605), text_input="NEXT", font=get_font(35), base_color="black", hovering_color="brown")
        next_page.changeColor(TUTOR_MOUSE_POS)
        next_page.update(SCREEN)

        back_page = Button(image=None, pos=(1150, 673), text_input="BACK", font=get_font(35), base_color="black", hovering_color="brown")
        back_page.changeColor(TUTOR_MOUSE_POS)
        back_page.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial3()
                if back_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial1()
        
        pygame.display.update()

def tutorial3():
    while True:
        TUTOR_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("Assets\\Tutorial-3.png"), (0, 0))
        next_page = Button(image=None, pos=(1150, 605), text_input="NEXT", font=get_font(35), base_color="black", hovering_color="brown")
        next_page.changeColor(TUTOR_MOUSE_POS)
        next_page.update(SCREEN)

        back_page = Button(image=None, pos=(1150, 673), text_input="BACK", font=get_font(35), base_color="black", hovering_color="brown")
        back_page.changeColor(TUTOR_MOUSE_POS)
        back_page.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial4()
                if back_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial2()
        
        pygame.display.update()

def tutorial4():
    while True:
        TUTOR_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("Assets\\Tutorial-4.png"), (0, 0))
        next_page = Button(image=None, pos=(1150, 605), text_input="NEXT", font=get_font(35), base_color="black", hovering_color="brown")
        next_page.changeColor(TUTOR_MOUSE_POS)
        next_page.update(SCREEN)

        back_page = Button(image=None, pos=(1150, 673), text_input="BACK", font=get_font(35), base_color="black", hovering_color="brown")
        back_page.changeColor(TUTOR_MOUSE_POS)
        back_page.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial5()
                if back_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial3()

        pygame.display.update()

def tutorial5():
    while True:
        TUTOR_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("Assets\\Tutorial-5.png"), (0, 0))
        next_page = Button(image=None, pos=(1150, 605), text_input="NEXT", font=get_font(35), base_color="black", hovering_color="brown")
        next_page.changeColor(TUTOR_MOUSE_POS)
        next_page.update(SCREEN)

        back_page = Button(image=None, pos=(1150, 673), text_input="BACK", font=get_font(35), base_color="black", hovering_color="brown")
        back_page.changeColor(TUTOR_MOUSE_POS)
        back_page.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_page.checkForInput(TUTOR_MOUSE_POS):
                    gamemode()
                if back_page.checkForInput(TUTOR_MOUSE_POS):
                    tutorial4()

        pygame.display.update()

def gamemode():
        while True:
            TUTOR_MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.blit(pygame.image.load("Assets\\gamemode_select.png"), (0, 0))
            solo = Button(image=None, pos=(170, 640), text_input="SOLO", font=get_font(130), base_color="white", hovering_color="#81c3ff")
            solo.changeColor(TUTOR_MOUSE_POS)
            solo.update(SCREEN)

            deathmatch = Button(image=None, pos=(920, 430), text_input="DEATHMATCH", font=get_font(120), base_color="white", hovering_color="#f9e694")
            deathmatch.changeColor(TUTOR_MOUSE_POS)
            deathmatch.update(SCREEN)

            time_atk = Button(image=None, pos=(360, 220), text_input="TIME ATTACK", font=get_font(120), base_color="white", hovering_color="#ffc0cb")
            time_atk.changeColor(TUTOR_MOUSE_POS)
            time_atk.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if solo.checkForInput(TUTOR_MOUSE_POS):
                        sys.exit()
                    if deathmatch.checkForInput(TUTOR_MOUSE_POS):
                        tutorial4()
                    if time_atk.checkForInput(TUTOR_MOUSE_POS):
                        play()

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
                    ask_tutorial()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()