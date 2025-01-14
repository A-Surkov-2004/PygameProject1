from PIL import Image

from wall import Wall


class Mapreader():
    def __init__(self,game):
        self.map = self.image2list()
        self.game = game
        pass
    def image2list(self):
        im = Image.open('images/CoinMap1.png') # Can be many different formats.
        pix = im.load()

        print(im.size)  # Get the width and hight of the image for iterating over
        mas = [[0] * im.size[0] for i in range(im.size[1])]
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                if pix[i,j] == (0,0,0,255):
                    mas[j][i] = 1

        print(pix[0,0])  # Get the RGBA Value of the a pixel of an image

        for i in mas:
            print(i)

        return mas

    def generate_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 1:
                    w1 = Wall(self.game, (j)*40, (i)*40)
                    self.game.walls.add(w1)


