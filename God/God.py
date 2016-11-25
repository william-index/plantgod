import attr
from random import randint, shuffle
from Artist import GridSystem
from Life import Plant

@attr.s
class God(object):
    firstGenerationSize = attr.ib()
    lifeFormWidth = attr.ib()
    lifeFormHeight = attr.ib()
    rootStartPercent = attr.ib()
    grids = GridSystem()


    """
    Picks the most fit members from a group.

    Args:
        lifeforms (Array) : array of lifeform DNAs
        survivorCount (int) : number to pick
    Returns:
        Array: Array of lifeform arrays
    """
    def pickMostFit(self, lifeforms, survivorCount):
        print "Selecting most fit members.."
        lifeforms.sort(self.lifeFormSort)

        # selects best for surviors
        chosenLifeforms = lifeforms[0:survivorCount-1]

        # selects a random survivor
        chosenLifeforms.append(lifeforms[randint(0, len(lifeforms)-1)])

        return chosenLifeforms

    # Sort method for determining which members are most fit
    def lifeFormSort(self, a, b):
        aScore = self.judgeLifeform(a)
        bScore = self.judgeLifeform(b)

        if aScore < bScore:
            return 1
        elif aScore == bScore:
            return 0
        else:
            return -1

    """
    Crossbreeds lifeforms from a a given set of lifeforms.

    Args:
        lifeforms (Array) : array of lifeform DNAs
    Returns:
        Array: Array of lifeform arrays
    """
    def breed(self, lifeforms):
        print "Breeding..."
        nextGen = []

        segments = self.pickRandomDivisor_(len(lifeforms[0].dna))
        print "DNA Splice length: ", segments

        segmentedPlants = self.sliceToSegments_(lifeforms, segments)
        print "Recombinating DNA..."

        for i in range(0, len(segmentedPlants)):
            parent1 = segmentedPlants[i]

            for k in range(0, 2):
                parent2 = segmentedPlants[randint(0, len(segmentedPlants)-1)]#segmentedPlants[(i+1) % len(segmentedPlants)]
                breeders = [parent1, parent2]

                newPlantDNA = []

                for j in range(0, len(segmentedPlants[i])):
                    side = randint(0, 1)
                    newPlantDNA += breeders[side][j]

                plant = Plant(newPlantDNA)
                nextGen.append(plant)

        print len(nextGen), " offspring produced."
        return nextGen

    def sliceToSegments_(self, lifeforms, segments):
        segmentedPlants = []

        for plant in lifeforms:
            plantSegments = []
            for i in range(0, len(plant.dna), segments):
                plantSegments.append(plant.dna[i:i + segments])
            segmentedPlants.append(plantSegments)

        return segmentedPlants

    def pickRandomDivisor_(self, length):
        segments = 1
        moduloRemainder = 1
        while moduloRemainder != 0:
            segments = randint(4, length/6)
            moduloRemainder = length % segments

        return segments

    """
    Performs random mutations on random lifeforms in a set of random lifeforms.

    Args:
        lifeforms (Array) : array of lifeform DNAs
    Returns:
        Array: Array of lifeform arrays
    """
    def mutate(self, lifeforms):
        print "Mutating offspring..."
        mutateLifeforms = []

        for lifeform in lifeforms:
            numMutations = randint(0, 30)
            if randint(0, 100) < 1:
                print "RADICAL MUTATION!!!"
                lifeform = self.createRandomLifeform((self.lifeFormWidth, self.lifeFormHeight))
            else:
                for i in range(0, numMutations):
                    newVal = hex(randint(0, 15) )[2:]
                    lifeform.dna[randint(0, len(lifeform.dna))-1] = newVal

            mutateLifeforms.append(lifeform)

        return mutateLifeforms

    def trimDeadCells(self, lifeforms):
        print "Trimming detached cells..."
        trimmedLifeforms = []

        for lifeform in lifeforms:
            fixedLifeform = []
            lifeFormGrid = self.grids.arrayToGrid(lifeform.dna, self.lifeFormWidth)

            # All energy is calculated by checking all cells
            for y in range(0, self.lifeFormHeight):
                for x in range(0, self.lifeFormWidth):
                    cell = self.grids.getCellAtIndex(lifeFormGrid, x, y)
                    if cell.siblingsCount <= 1 and cell.adjacentSiblingsCount == 0:
                        lifeFormGrid[y][x] = '0'

            for row in lifeFormGrid:
                fixedLifeform += row

            plant = Plant(fixedLifeform)

            trimmedLifeforms.append(plant)

        return trimmedLifeforms

    """
    Calculates the score for a lifeform.

    Args:
        lifeform (Plant) : Plant lifeform
    Returns:
        int: score for how successful a lifeform is
    """
    def judgeLifeform(self, lifeform):
        if lifeform.fitness:
            return lifeform.fitness

        lifeFormGrid = self.grids.arrayToGrid(lifeform.dna, self.lifeFormWidth)

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


        # print ('energyNeeded', energyNeeded), ('energyProduced', energyProduced)
        # print ('nutrientsNeeded', nutrientsNeeded), ('nutrientsProduced', nutrientsProduced)

        energyOffset = energyProduced - energyNeeded#abs(energyNeeded - energyProduced)
        nutrientOffset = nutrientsProduced - nutrientsNeeded#abs(nutrientsNeeded - nutrientsProduced)
        score = 0
        # Offset of energy and nutrients
        score =  energyOffset**2 + nutrientOffset**2
        # bonus for living cells
        score += self.countRealCells_(lifeFormGrid)

        lifeform.fitness = score

        return score


    """
    Counts the number of living cells in a lifeform

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

        if cell.adjacentSiblingsCount == 0 or cell.siblingsCount > 4:
            return -1

        if cell.y > self.lifeFormHeight * self.rootStartPercent:
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
        if cell.y > self.lifeFormHeight * self.rootStartPercent:
            return energy

        # Nonfilled cells are not part of plant
        if cell.target == 0:
            return energy

        # High pigment cells produce more energy when closer to sunlight
        if cell.y < self.lifeFormHeight/4:
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
        if cell.siblingsCount < 2:
            energy += 30
        elif cell.adjacentSiblingsCount == 0:
            energy += 20

        # Roots do not reqire energy
        if cell.y > self.lifeFormHeight * self.rootStartPercent:
            return energy

        if cell.y > self.lifeFormHeight * (1.0 - self.rootStartPercent):
            energy += cell.y

        # Requires one energy per sibling
        energy += cell.siblingsCount - cell.adjacentSiblingsCount
        # and additional energy if cell above is of a high value pigment
        energy += cell.n

        # High pigment values cells are more performant
        energy -= cell.target/4

        # Energy is conserved by having similar pigment siblings
        # @TODO: exclude target from sibling list..
        for sibling in cell.siblings:
            if cell.target == sibling:
                energy -= 2

        # A non-root cell requires at least one energy
        if energy < 1:
            energy = 1

        return energy


    def createLife(self):
        lifeForms = []

        for i in range(0, self.firstGenerationSize):
            lifeForm = self.createRandomLifeform((self.lifeFormWidth, self.lifeFormHeight))
            lifeForms.append(lifeForm)

        return lifeForms


    def createRandomLifeform(self, size):
        lifeFormDNA = []

        for i in range(0, size[0]*size[1]):
            # Favors some empty space for starting generation
            if randint(0, 1) > 0:
                lifeFormDNA.append('0')
            else:
                lifeFormDNA.append(hex(randint(0, 15) )[2:])

        plant = Plant(lifeFormDNA)

        return plant
