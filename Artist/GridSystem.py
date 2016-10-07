import attr
from GridCell import GridCell

@attr.s
class GridSystem(object):

    def arrayToGrid(self, array, columns):
        grid = []
        for i in range(0, len(array), columns):
            grid.append(array[i:i + columns])
        return grid

    def getCellAtIndex(self, grid, x, y):
        cell = GridCell(grid=grid, x=x, y=y)
        return cell
