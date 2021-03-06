import attr

@attr.s
class GridCell(object):
    grid = attr.ib()
    x = attr.ib()
    y = attr.ib()
    adj = []
    currentX = -1
    currentY = -1

    @property
    def siblings(self):
        # Caching is still on previous cell
        if self.adj and self.x == self.currentX and self.y == self.currentY:
            return self.adj

        # Clears cache
        self.adj = []
        self.currentX = self.x
        self.currentY = self.y

        # calculates siblings for cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                yIndex = self.y+i
                xIndex = self.x+j
                cellVal = False

                if xIndex < 0 or xIndex >= len(self.grid[0]):
                    cellVal = -1
                elif yIndex < 0 or yIndex >= len(self.grid):
                    cellVal = -1
                else:
                    cellVal = self.grid[yIndex][xIndex]
                    cellVal = int(cellVal, 16)

                self.adj.append(cellVal)
        return self.adj

    @property
    def siblingsCount(self):
        return 8 - self.siblings.count(-1)

    @property
    def adjacentSiblingsCount(self):
        adjacents = [self.n, self.w, self.e, self.s]
        return 4 - adjacents.count(-1) - adjacents.count(0)

    @property
    def nw(self):
        return self.siblings[0]

    @property
    def n(self):
        return self.siblings[1]

    @property
    def ne(self):
        return self.siblings[2]

    @property
    def w(self):
        return self.siblings[3]

    @property
    def target(self):
        return self.siblings[4]

    @property
    def e(self):
        return self.siblings[5]

    @property
    def sw(self):
        return self.siblings[6]

    @property
    def s(self):
        return self.siblings[7]

    @property
    def se(self):
        return self.siblings[8]
