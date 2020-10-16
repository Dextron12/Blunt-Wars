import pygame, os

class World(object):
    Textures = {}
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    def load_texture(self, texture=Textures):
        for file in os.listdir(self.BASE_DIR + '/Resources/Maps/'):
            if '.png' in file:
                self.Textures[file.strip('.png')] = pygame.image.load(self.BASE_DIR + '/Resources/Maps/%s' % (file))

    def draw_map(self):
        


class Greeter:
    width,height = 1024, 768
    window = pygame.display.set_mode((width,height), pygame.RESIZABLE)
    pygame.display.set_caption("Blunt Wars")


        


world = World()
world.load_texture()