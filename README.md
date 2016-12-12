# Plantgod
<img src="http://williamanderson.io/static/images/blog/pixelplants/cover.png" />
Plantgod is an Evolutionary Algorithm for generating pixel art "plants".

**READ MORE** about the project here:
**[http://williamanderson.io/blog/ea-for-pixel-plants/](http://williamanderson.io/blog/ea-for-pixel-plants/)**

While "plants" is a very generous term, it does in fact function though ultimately showing a premature bias due to using a truncated selection methods.

## Current Status
This project is "done" from the perspective of its core author, whom will press on to other projects. If anyone is interested though, feel free to fork and PR and I will review and comment/approve.

## Running the project
<img src="http://williamanderson.io/static/images/blog/pixelplants/evolution.gif" />

Plantgod works as a python script. After cloning or pulling the repo, simply run
```
python main.py
```
From within the projects root directory. This will generate a series of images for the plants generated under art/rendered.

Some samples can be found in the repo within subfolders of that directory.

## Configuring plant generations
You can adjust and modify the basic values of plant generation at the top of the main.py script.

#### generations
<int>
The number of generations to run the algorithm over.

#### initialPopSize
<int>
Starting number of randomly generated plants to pick from

#### survivalSize
<int>
Number of survives to select from each generation

#### plantWidth
<int>
Width in pixels of each plant  

#### plantHeight
<int>
Height in pixel of each plant

#### rootStart
<float>
Percent of total height to start root generation at
