from __future__ import print_function
from collections import Counter
from kelp.kelpplugin import KelpPlugin
from snapshotplugin import SnapshotPlugin
import os
import sys
import kurt

class MovementCheck(SnapshotPlugin):

    def __init__(self):
        super(MovementCheck, self).__init__()
        self._modulename = "movementCheck"
        self._description = "Checks movement for all files"
    def analyze(self, path):
        movementResults = []
        dirname = os.path.dirname(path)
        for file in os.listdir(path):
            if file.endswith(".oct"):
                base = os.path.basename(file)
                filename = os.path.splitext(base)[0]
                oct = kurt.Project.load(os.path.abspath(os.path.join(path, file)))
                movementResults.append([filename, self.movementCheck(oct)]) 
        return movementResults
    def movementCheck(self, scratch):
        results = []
        roosterMove = []
        catMove = []
        roosterFinish = False
        catFinish = False
        for sprite in scratch.sprites:
            sum = 0
            if "Rooster" == sprite.name:
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        for block in script:
                            if "go to" in block.stringify() or "glide" in block.stringify():
                                if (len(roosterMove) == 0):
                                    roosterMove.append(script)
                                    results.append("Rooster Motion Script Type: " + script.blocks[0].stringify())  # records the type of block that starts the movement 
                                    initialized = False
                                    for block in roosterMove[0].blocks:
                                        if "go to" in block.stringify() or "glide to" in block.stringify():
                                            sum = block.args[0]
                                            if (initialized == True): #if this is not the first movement block in the script
                                                if sum > 100: #some backward movement
                                                    results.append("Rooster Initialization: After Race(Absolute)")
                                                if sum < -150: #some forward movement
                                                    roosterFinish = True
                                            if (initialized == False): #if this is the first movement block in the script
                                                if sum > 100:
                                                    results.append("Rooster Initialization Type: Before Race(Absolute)")
                                                    initialized = True
                                                    sum = 0
                                                if sum < -150:
                                                    roosterFinish = True
                                                    initialized = True
                                                    sum = 0
                                        if (("glide" in block.stringify() or "move" in block.stringify()) and "to" not in block.stringify()):
                                            sum += block.args[0]
                                            if (initialized == True): 
                                                if sum < -100: 
                                                    results.append("Rooster Initialization Type: After Race(Relative)" )
                                                if sum > 150: 
                                                    roosterFinish = True
                                            if (initialized == False):
                                                if sum <-100:
                                                    results.append("Rooster Initialization Type: Before Race(Relative)")
                                                    initialized = True
                                                    sum = 0
                                                if sum > 150:
                                                    roosterFinish = True
                                                    initialized = True
                                                    sum = 0
            if "Cat" == sprite.name:
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        for block in script: 
                            if "go to" in block.stringify() or "glide" in block.stringify():
                                if(len(catMove) == 0):
                                    results.append("Cat Motion Script Type: " + script.blocks[0].stringify()) # records the type of block that starts the movement script
                                    catMove.append(script)
                                    initialized = False
                                    for block in catMove[0].blocks:
                                        if "go to" in block.stringify() or "glide to" in block.stringify():
                                            sum += block.args[0]
                                            if (initialized == True): #if this is not the first movement block in the script
                                                if sum > 100: 
                                                    results.append("Cat Initialization Type: After Race(Absolute)")
                                                if sum < -150:
                                                    catFinish = True
                                            if (initialized == False): #if this is the first movement block in the script 
                                                if sum > 100:
                                                    results.append("Cat Initialization Type: Before Race(Absolute)")
                                                    initialized = True
                                                    sum = 0
                                                if sum < -150:
                                                    catFinish = True
                                                    initialized = True
                                                    sum = 0
                                        if (("glide" in block.stringify() or "move" in block.stringify()) and "to" not in block.stringify()):  
                                            sum += block.args[0]
                                            if (initialized == True): 
                                                if sum < -100 : 
                                                    results.append("Cat Initialization Type: After Race(Relative)")
                                                if sum > 150: 
                                                    catFinish = True
                                                    sum = 0
                                            if (initialized == False):
                                                if sum < -100:
                                                    results.append("Cat Initialization: Before Race(Relative)")
                                                    initialized = True
                                                if sum > 150:
                                                    catFinish = True
                                                    sum = 0
                                                    initialized = True
        if roosterFinish == True:
            results.append("Rooster crosses finish line")
        if catFinish == True:
            results.append("Cat crosses finish line")
        if len(results) == 0:
            results.append("No Movement Occurs")
        return results
def movementCheck_display(results):
    output = {}
    html = []
    count = 1
    for item in results:
        html.append("<h2>" + "Project #" + str(count) + "</h2><p>" + '</p>'.join(item[1]))
        count += 1
    output[0] = ''.join(html)
    return output