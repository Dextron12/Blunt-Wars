import pygame

from Scripts import PygUI as ui

handler = ui.EventHandler(1024, 648)
availableWeapons = []
for obj in range(24):
    availableWeapons.append(obj)

drawAvailableWeapons = ui.dynamicArray(10, 80, (handler.width-60)//2, handler.height-30, handler.height-100,  availableWeapons)

while True:
    handler.handle()
    handler.window.fill((0,0,255))

    pygame.draw.rect(handler.window, (240, 240, 240), (20,20,handler.width-40, handler.height-30))
    pygame.draw.line(handler.window, (49, 79, 79), ((handler.width-40)//2, 20), ((handler.width-40)//2, handler.height-10), 2)
    pygame.draw.line(handler.window, (49, 79, 79), (20, 80), (handler.width-20, 80))

    drawAvailableWeapons.draw(handler.window, handler, True)

    pygame.display.flip()