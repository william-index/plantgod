import attr
from random import randint
from Artist import GridSystem

@attr.s
class God(object):
    generationSize = attr.ib()
    grids = GridSystem()
    lifeFormWidth = 16
    lifeFormHeight = 32

    @property
    def testing(self):
        return 'this connected'


    def judgeLifeform(self, lifeFormArray):
        lifeFormGrid = self.grids.arrayToGrid(lifeFormArray, self.lifeFormWidth)
        # for y in range(0, len(self.lifeFormHeight)):
        #     for x in range(0, len(self.lifeFormWidth)):
        cell = self.grids.getCellAtIndex(lifeFormGrid, 0, 0)
        return cell.adjacentSiblingsCount


    def createLife(self):
        lifeForms = []

        for i in range(0, self.generationSize):
            lifeForm = self.createRandomLifeform((self.lifeFormWidth, self.lifeFormHeight))
            lifeForms.append(lifeForm)

        return lifeForms


    def createRandomLifeform(self, size):
        lifeForm = []

        for i in range(0, size[0]*size[1]):
            lifeForm.append(hex(randint(0, 15) )[2:])

        return lifeForm
