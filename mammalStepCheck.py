from __future__ import print_function
from collections import Counter
from kelp.kelpplugin import KelpPlugin
from snapshotplugin import SnapshotPlugin
import os
import sys
import kurt

class MammalStepCheck(SnapshotPlugin):

    def __init__(self):
        super(MammalStepCheck,self).__init__()
        #module name and description
        self._modulename = "MammalGame"
        self._description = "Attempts to determine the time it takes to figure out the grid"
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
                results = self.stepCheck(oct)
                sum = 0
                for item in results:
                    sum += int(item)
                if "50" in results or sum%50 ==0:
                    results.append("Student figured out grid")
                #results.append(self.stepCheck(oct))
        return {dirname:results}
    def stepCheck(self, scratch):
        blockargs = []
        for sprite in scratch.sprites:
            if sprite.name == "Net":
                for script in sprite.scripts:
                    for block in script.blocks:
                        if "steps" in block.stringify():
                            blockargs.append(str(block.args[0]))
        print (blockargs)
        return (blockargs)
    
def check_display(results):
    output = {}
    figured = False
    count = 1
    for title, list in results.items():
        htmlout = '<h2>' + 'Project #' + str(count) + '</h2>' + '<p>' + ','.join(list) + '</p>'
        if("figured" in list[-1] and figured == False):
            htmlout = htmlout +('It took ' + str(count) + ' tries to figure out')
            figured = True
        output[count] = ''.join(htmlout)
        count+=1
    return output