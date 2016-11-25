import attr

@attr.s
class Plant(object):
    dna = attr.ib()
    fitness = attr.ib()
    _fitness = False

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, newFitness):
        self._fitness = newFitness
