import pygame

from slacker_game import Slacker


def main():
    pygame.init()
    slacker = Slacker()
    slacker.main_loop()
    pygame.display.quit()


if __name__ == '__main__': main()
