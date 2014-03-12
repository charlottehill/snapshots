from __future__ import print_function
from collections import Counter
from kelp.kelpplugin import KelpPlugin
from snapshotplugin import SnapshotPlugin
import os
import sys
import kurt

class SpriteSizeCheck(SnapshotPlugin):

    def __init__(self):
        super(SpriteSizeCheck, self)
        self._modulename = "Sprite Size Check"
        self._moduledescription = "Checks to see if any sprites become abnormally small"
    def checkSize(self, oct):
        results = []
        for sprite in oct.sprites:
            if sprite.size <= 20:
                results.append("Size of " + sprite.name + " is very small")
            else:
                results.append("Size of " + sprite.name + " is normal")
        return results
    def analyze(self, path):
        results = {}
        dirname = os.path.dirname(path)
        for file in os.listdir(path):
            if file.endswith(".oct"):
                base = os.path.basename(file)
                filename = os.path.splitext(base)[0]
                oct = kurt.Project.load(os.path.abspath(os.path.join(path, file)))
                strings = (self.checkSize(oct))
                results[filename] = ''
                for item in strings:
                    results[filename] += item +', ' 
        return results
def size_display(results):
    output = {}
    count = 1
    for filename, htmlout in results.items():
        htmlout = '<h2>' + 'Project #' + str(count) + '</h2>' + '<p>' + str(htmlout) + '</p>'
        output[count] = ''.join(htmlout)
        count+=1
    return output