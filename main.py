from God import God
from Settings import colors
from PIL import Image, ImageDraw, ImageOps, ImageFont

generations = 30
initialPopSize = 10
survivalSize = 4

god = God(initialPopSize)

# generate initial population
initialPop = god.createLife()
print "Initial pop created!"

parents = god.pickMostFit(initialPop, survivalSize)
parentGen = parents
print "Starting generation selected."

print "TODO: Save image starting generation"
# Generations should be drawn together as a single image
# With the point value of the plant underneath it

for i in range(0, generations):
    print "Starting generation: ", i
    offspring = god.breed(parents)
    offspring = god.mutate(offspring)
    parents = god.pickMostFit(offspring, survivalSize)
    print "Completed generation: ", i

    print "TODO: Save image for survivors"

print "Initial Scores:"
for p in parentGen:
    print god.judgeLifeform(p)

print "Final Scores:"
finalForms = parents
for p in finalForms:
    print god.judgeLifeform(p)
