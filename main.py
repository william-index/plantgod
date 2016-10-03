from God import God
from Settings import colors
from PIL import Image, ImageDraw, ImageOps, ImageFont

god = God(4)

# generate initial population
initialPop = god.createLife()
print initialPop

# ||: for N cycles or to stop criteria
    # determine success for all members
        # select N members from generation to pass along

    # Cross Breed members
    # Apply Mutations
# :||
