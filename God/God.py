import attr
from random import randint

@attr.s
class God(object):
    generationSize = attr.ib()

    @property
    def testing(self):
        return 'this connected'


    def createLife(self):
        lifeForms = []

        for i in range(0, self.generationSize):
            lifeForm = self.createRandomLifeform((16,32))
            lifeForms.append(lifeForm)

        return lifeForms


    def createRandomLifeform(self, size):
        lifeForm = []

        for i in range(0, size[0]*size[1]):
            lifeForm.append(hex(randint(0, 15) )[2:])

        return lifeForm
