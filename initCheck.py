from __future__ import print_function
from collections import Counter
from kelp.kelpplugin import KelpPlugin
from snapshotplugin import SnapshotPlugin
import os
import sys
import kurt

class InitCheck(SnapshotPlugin):

    def __init__(self):
        super(InitCheck,self).__init__()
        #module name and description
        self._modulename = "InitCheck"
        self._description = "Check whether or not extra code has been implemented"

    def check_finish(self, oct):
        results = []
        scripts = {'Cat': set(), 'Rooster': set()}
        for sprite in oct.sprites:
            if sprite.name == 'Cat' or sprite.name == 'Rooster':
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        if KelpPlugin.script_start_type(script) == self.HAT_GREEN_FLAG:
                            scripts[sprite.name].add(script)

        #initialize boolean initialization variables to False
        catPos = False
        catSize = False
        roosterPos = False
        roosterOrien = False
        roosterSet = False
        catSet = False

        #access the Cat's blocks
        sum = 0
        for script in scripts['Cat']:
            for block in script:
                if "steps" in block.stringify():
                    if (catPos == True):
                        sum += block.args[0]
                if block.type.text == 'go to x:%s y:%s':
                    if catPos == True:
                        if(block.args[0] <= -105):
                            results.append("Student code moves Cat to finish")
                    if block.args[0] >= 145:
                        catPos = True
                elif block.type.text == 'set x to %s':
                    if catPos == True:
                        if(block.args[0] <= -105):
                            results.append("Student code moves Cat to finish")
                    if block.args[0] >= 145:
                        if catSet: # already set y
                            catPos = True
                        else:
                            catSet = True
                elif block.type.text == 'set y to %s':
                    if catSet: # already set x
                        catPos = True
                    else:
                        catSet = True
            if sum > 105:
                results.append("Student code moves Cat to finish")
        #access the Rooster's blocks
        sum = 0
        for script in scripts['Rooster']:
            for block in script:
                if "steps" in block.stringify():
                        if (roosterOrien == True):
                            sum+= block.args[0]
                if block.type.text == 'point towards %s':
                    if block.args[0] == 'finish line':
                        roosterOrien = True
                elif block.type.text == 'point in direction %s':
                	if block.args[0] == -90:
                		roosterOrien = True
                elif block.type.text == 'go to x:%s y:%s':
                    if roosterPos == True:
                        if block.args[0] <= -105:
                            results.append("Student code moves Rooster to finish")
                    if block.args[0] >= 145:
                        roosterPos = True
                elif block.type.text == 'set x to %s':
                    if roosterPos == True:
                        if block.args[0] <= -105:
                            results.append("Student code moves Rooster to finish")
                    if block.args[0] >= 145:
                        if roosterSet: # already set y
                            roosterPos = True
                        else:
                            catSet = True
                elif block.type.text == 'set y to %s':
                    if roosterSet: # already set x
                        roosterPos = True
                    else:
                        roosterSet = True
            if(sum >= 150):
                results.append("Student code moves Rooster to finish")
        return results

    def analyze (self, Path):
        results = []
        dirname = os.path.dirname(Path)
        for file in os.listdir(Path):
            if file.endswith(".oct"):
                # get file name
                base = os.path.basename(file)
                filename = os.path.splitext(base)[0]

                # set up kurt project
                oct = kurt.Project.load(os.path.abspath(os.path.join(Path, file)))

                # check for unnecessary additional completion of scripts in animalRace
                results.append([filename, self.check_finish(oct)])
        for item in results:
            if len(item[1]) == 0:
                item[1] = ["Student code does not attempt to move Cat/Rooster to finish"]
        return results
def check_display(results):
    output = {}
    count = 1
    for item in results:
        htmlout = '<h2>' + 'Project #' + str(count) + '</h2>' + '<p>' + ", ".join(item[1]) + '</p>'
        output[count] = ''.join(htmlout)
        count+=1
    return output