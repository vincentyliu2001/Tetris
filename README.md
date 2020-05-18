# Tetris
This is a project that I made in the past few months  
An exact replica of Tetris on https://jstris.jezevec10.com/  
This uses the SRS rotation system https://tetris.wiki/Super_Rotation_System and a 7 piece bag-randomizer  
### Dependencies:
```
import random
import neat
from copy import copy, deepcopy
import os
import pickle
import time
import graphics
import pygame
```
### DAS ARR:
See https://tetris.fandom.com/wiki/DAS  for explanations
```DAS``` is set to a default 70 in Tetris  
To set a custom ```DAS```, change ```line 109``` in ```main.py``` to ```das = <your DAS> / 1000```  
```ARR``` is hard set at 0, you cannot change this, maybe future implementations of the game will allow for customization  

### Controls:
Note: These are my personal keybinds  
```up_arrow_key```: rotate clockwise once  
```down_arrow_key```: soft drop  
```right_arrow_key```: move right  
```left_arrow_key```:  move left  
```z```: rotate counter-clockwise once  
```x```: rotate 180 degrees once  
```left_shift```: hold  
```spacebar```: hard drop  
```F4```: restart/new game
### Making custom Keybinds:
This iteration of Tetris currently does not have
a user friendly way of creating custom keybinds. 
If you want to make your own here are the locations of the key binds, change
all of the locations to the desired key bind to change the key:  
```up_arrow_key```: ```line 79``` in ```pieces.py```  
```down_arrow_key```: ```line 91``` and ```line 100``` in ```pieces.py```  
```right_arrow_key```:  ```line 75``` in ```pieces.py``` and ```line 198``` and ```line 212``` in ```main.py```  
```left_arrow_key```: ```line 71``` in ```pieces.py``` and ```line 205``` and ```line 215``` in ```main.py```  
```z```: ```line 83``` in ```pieces.py```  
```x```: ```line 87``` in ```pieces.py```  
```left_shift```: ```line 181``` in ```main.py```  
```spacebar```: ```line 95``` in ```pieces.py```  
```F4```: ```line 159``` in ```main.py```  
### Overview of files:
Below is the quick overview of what each file does, details can be found in the comments: 
```main.py```: This is the main file to run the user-played game  
```AI_helper.py```: This is the helper file to AI, provides numbers to feed into the training algorithm  
```block.py```: This is where the Block object is  
```board.py```: This is where the Board object is  
```graphics.py```: This is where all the graphics are rendered  
```neat-AI.py```: This is where the training for the algorithm happens  
```pieces.py```: This is where the Pieces class is, the parent class for 7 subclasses, one for each type of Tetromino  
```rotation.py```: This is where all the rotations are handled  
```autoPlay.py```: This is where you run the ai to play tetris at blistering speeds  
```tetris-ai```: This is the file that is needed to run ```autoPlay.py```  
```tetris_checkpoint_adv175```: This is the training checkpoint, more info in AI section  
```neat_configs```: This is the neat config file, more info in AI section  

### AI:
The AI that is currently used has trained for 175 generations using the NEAT algorithm.  
To see an earlier iteration of this AI in action: https://www.youtube.com/watch?v=iKcsKimt5Ds  
To continue training this AI, make sure ```line 261``` in ```neat-ai.py``` is (should already be):  
```population = checkpoints.restore_checkpoint("tetris_checkpoint_adv175")```  
Run the program, and it should save files called ```tetris_checkpoint_adv<generation number>```  
The ```neat_configs``` are the configurations I used to train the AI and the configs the checkpoint has  
See https://neat-python.readthedocs.io/en/latest/ for more detailed documentation  

### Potential Errors:
1. PyCharm bug: PyCharm can't recognize imports but the program runs perfectly
2. No other Errors have been detected, everything should run smoothly

### Future Plans:
1. User friendly customizable keybinds  
2. Continued ```neat-ai``` training, currently plateauing  
3. Definitely going to look into Deep Q Learning to make a more advanced AI  
4. Tetris AI speed adjustment  
5. 1v1 Tetris AI in Tetris Battle  
6. Implement levels in the game  
7. Skins for graphics
8. Known efficiency optimizations: ie ```clear_line``` function in board can definitely be more efficient
