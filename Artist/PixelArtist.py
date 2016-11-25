import attr
from PIL import Image, ImageDraw, ImageOps, ImageFont
from GridSystem import GridSystem
from Settings import colors
from Life import Plant

@attr.s
class PixelArtist(object):
    grids = GridSystem()

    def drawPlantGeneration(self, lifeforms, filename, columns):
        print "Drawing Generation Portrait..."

        gridedForms = []
        for lifeform in lifeforms:
            gridedForms.append(self.grids.arrayToGrid(lifeform.dna, columns))

        lifeFormWidth = len(gridedForms[0][0])
        lifeFormHeight = len(gridedForms[0])

        canvasSize = (lifeFormWidth * (len(gridedForms) + 1), lifeFormHeight)
        spaceBetween = (lifeFormWidth/len(lifeforms))

        interfacedScene = Image.new('RGBA', canvasSize, (0,0,0,0))
        pixel_data = interfacedScene.load()

        plantOffset = spaceBetween/2
        for plant in gridedForms:
            for y in range(0, lifeFormHeight):
                for x in range(0, lifeFormWidth):
                    cellVal = int(plant[y][x], 16)
                    if cellVal != 0:
                        if y > lifeFormHeight * .8:
                            pixel_data[x+plantOffset, y] = (181, 113, 18, 255)
                        else:
                            pixel_data[x+plantOffset, y] = colors[cellVal]

            plantOffset += lifeFormWidth + spaceBetween

        interfacedScene.save('art/rendered/' + filename + '.png')
