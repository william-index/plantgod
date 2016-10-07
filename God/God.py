import attr
from random import randint
from Artist import GridSystem

@attr.s
class God(object):
    generationSize = attr.ib()
    grids = GridSystem()
    lifeFormWidth = 16
    lifeFormHeight = 32


    def judgeLifeform(self, lifeFormArray):
        lifeFormGrid = self.grids.arrayToGrid(lifeFormArray, self.lifeFormWidth)

        # Base values of resources needed for any lifeform
        energyNeeded = 100
        nutrientsNeeded = 100

        # Total resources produced by lifeforms
        energyProduced = 0
        nutrientsProduced = 0

        # All energy is calculated by checking all cells
        for y in range(0, self.lifeFormHeight):
            for x in range(0, self.lifeFormWidth):
                cell = self.grids.getCellAtIndex(lifeFormGrid, x, y)
                energyNeeded += self.getCellEnergyConsumption_(cell)
                energyProduced += self.getCellEnergyProduction_(cell)
                nutrientsNeeded += self.getCellNutrientsConsumption_(cell)
                nutrientsProduced += self.getCellNutrientsProduced_(cell)


        print ('energyNeeded', energyNeeded), ('energyProduced', energyProduced)
        print ('nutrientsNeeded', nutrientsNeeded), ('nutrientsProduced', nutrientsProduced)

        energyOffset = abs(energyNeeded - energyProduced)
        nutrientOffset = abs(nutrientsNeeded - nutrientsProduced)
        score = 0
        # Offset of energy and nutrients
        score =  (energyOffset + nutrientOffset) * -1
        # bonus for living cells
        score += self.countRealCells_(lifeFormGrid)

        return 'Score:', score


    """
    Ccounts the number of living cells in a lifeform

    Args:
        lifeFormArray (Array) : lifeform DNA
    Returns:
        int: number of non-zero value cells
    """
    def countRealCells_(self, lifeFormArray):
        return len(lifeFormArray) - lifeFormArray.count(0)


    """
    Calculates the amount of nutirents produced by a cell

    Args:
        cell (GridCell) : cell to calulate energy needed for
    Returns:
        int: nutrients provided by the cell
    """
    def getCellNutrientsProduced_(self, cell):
        nutrients = 0

        if cell.adjacentSiblingsCount == 0:
            return -1

        if cell.y > self.lifeFormHeight * .8:
            nutrients += 1
            nutrients += cell.siblingsCount
            nutrients += cell.adjacentSiblingsCount*2

        return nutrients


    """
    Calculates the nutirents needed for a particular cell to survive.

    Args:
        cell (GridCell) : cell to calulate energy needed for
    Returns:
        int: nutrients needed by the cell
    """
    def getCellNutrientsConsumption_(self, cell):
        nutrients = 0

        if cell.target == 0:
            return nutrients
        else:
            nutrients += 1

        # Unattached cells require MUCH nutrients
        if cell.siblingsCount == 0 or cell.adjacentSiblingsCount == 0:
            nutrients += 99

        return nutrients

    """
    Calculates the amount of energy produced by a cell.
        Cells closer to the sun recieve more energy and cells with
        higher pigment values are better at consuming the energy available
        to them, while cells that are blocked from recieving sublight are
        less performant.

    Args:
        cell (GridCell) : cell to calulate energy needed for
    Returns:
        int: energy produced by the cell
    """
    def getCellEnergyProduction_(self, cell):
        energy = 0

        # Roots do not produce energy
        if cell.y > self.lifeFormHeight * .8:
            return energy

        # Nonfilled cells are not part of plant
        if cell.target == 0:
            return energy

        # High pigment cells produce more energy
        energy += cell.target/4

        # Cells closer to the "Sun" recieve more energy
        energy += self.lifeFormHeight - cell.y

        # Energy penalty for being blocked from sunlight
        if cell.n > 0:
            energy = energy/5

        return energy


    """
    Calculates the amount of energy needed to sustain a cell.
        This is determined by how blocked a cell is by its siblings cells,
        while ensuring that a cell is still connected to the organism at
        large. "Roots" do not require energy, unless they are not connected
        to the rest of the plant (EG are their own organisms).

    Args:
        cell (GridCell) : cell to calulate energy needed for
    Returns:
        int: energy needed by cell to survive
    """
    def getCellEnergyConsumption_(self, cell):
        energy = 0

        # Nonfilled cells are not part of plant
        if cell.target == 0:
            return energy

        # Major deficits for not being attached
        if cell.siblingsCount == 0:
            energy += 99
        elif cell.adjacentSiblingsCount == 0:
            energy += 10

        # Roots do not reqire energy
        if cell.y > self.lifeFormHeight * .8:
            return energy

        # Requires one energy per sibling
        energy += cell.siblingsCount
        # and additional energy if cell above is of a high value pigment
        energy += cell.n

        # High pigment values cells are more performant
        energy -= cell.target/4

        # Energy is conserved by having similar pigment siblings
        for sibling in cell.siblings:
            if cell.target == sibling:
                energy -= 2

        # A non-root cell requires at least one energy
        if energy < 1:
            energy = 1

        return energy


    def createLife(self):
        lifeForms = []

        for i in range(0, self.generationSize):
            lifeForm = self.createRandomLifeform((self.lifeFormWidth, self.lifeFormHeight))
            lifeForms.append(lifeForm)

        return lifeForms


    def createRandomLifeform(self, size):
        lifeForm = []

        for i in range(0, size[0]*size[1]):
            # Favors some empty space for starting generation
            if randint(0, 1) > 0:
                lifeForm.append('0')
            else:
                lifeForm.append(hex(randint(0, 15) )[2:])

        return lifeForm
