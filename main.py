from God import God
from Artist import PixelArtist

# Default settings
generations = 200
initialPopSize = 20
survivalSize = 8
plantWidth = 16
plantHeight = 32
rootStart = 0.8

# Create the almighty creator
print "Initializing God."
god = God(
            firstGenerationSize=initialPopSize,
            lifeFormWidth = plantWidth,
            lifeFormHeight = plantHeight,
            rootStartPercent = rootStart
         )

# Initializes PixelArtist
pixelArtist = PixelArtist()

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
    print "----------------------------------"
    print "Starting generation: ", i
    offspring = god.breed(parents)
    offspring = god.mutate(offspring)
    offspring = god.trimDeadCells(offspring)
    parents = god.pickMostFit(offspring, survivalSize)
    print "TODO: Save image for survivors"

print "Initial Scores:"
for p in parentGen:
    print god.judgeLifeform(p)

print "Final Scores:"
finalForms = parents
for p in finalForms:
    print god.judgeLifeform(p)

pixelArtist.drawPlantGeneration(lifeforms=finalForms, filename='generation_final', columns=plantWidth)
