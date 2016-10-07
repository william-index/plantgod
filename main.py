from God import God
from Settings import colors
from PIL import Image, ImageDraw, ImageOps, ImageFont

generations = 3
initialPopSize = 10
survivalSize = 4

god = God(initialPopSize)

# generate initial population
initialPop = god.createLife()

parents = god.pickMostFit(initialPop, survivalSize)
print "TODO: Save image starting generation"

for i in range(0, generations):
    offspring = god.breed(parents)
    offspring = god.mutate(offspring)
    parents = god.pickMostFit(offspring, survivalSize)
    print "TODO: Save image for survivors"

finalForms = parents
for p in finalForms:
    print god.judgeLifeform(p)
