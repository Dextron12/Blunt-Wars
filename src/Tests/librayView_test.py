from PyGGUI import PyGGUI as pyui
import pygame

width, height = 1024, 648
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pyui.init.initiate(window, width, height)

while True:
    pyui.init.poll_events()
    window.fill((0,0,255))

    pyui.libViewer.draw(10, 10, (49,79,79), (255,255,255), (19,29,29))

    pygame.display.flip()
