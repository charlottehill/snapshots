"""Display all the sprites' visible scripts."""

from __future__ import print_function
from collections import Counter
from kelp.kelpplugin import KelpPlugin
from snapshotplugin import SnapshotPlugin
import os
import sys
import kurt

BASE_PATH = './results'


class Scripts(SnapshotPlugin):

    def __init__(self):
        super(Scripts, self).__init__()

    # returns a dictionary of all the scripts organized by sprite for an oct file
    def get_scripts(self, oct):
        scripts = {}
        for sprite in [oct.stage] + oct.sprites:
            scripts[sprite.name] = set()
            self.script_count[sprite.name] = 0
            for script in sprite.scripts:
                if not isinstance(script, kurt.Comment):
                    self.script_count[sprite.name] += 1
                    scripts[sprite.name].add(script)
        return scripts

    def analyze(self, path):
        # keep a count of the number of visible scripts for each sprite
        # use this to order them at the end
        # any with zero scripts will be listed separately
        self.script_count = Counter()
        scripts = {}
        dirname = os.path.dirname(path)
        for file in os.listdir(path):
            if file.endswith(".oct"):
                # get file name
                base = os.path.basename(file)
                filename = os.path.splitext(base)[0]
                # set up kurt project
                oct = kurt.Project.load(os.path.abspath(os.path.join(path, file)))
                scripts[filename] = self.get_scripts(oct)
        return {'counter': self.script_count, 'scripts': scripts}


# Displays sprite names and pictures
def scripts_display(results):
    files = results['scripts']
    script_count = results['counter']
    other = []
    # return a dictionary of html strings for each file
    output = {}

    # make a list of sprites without scripts
    for sprite, count in script_count.most_common():
        if count == 0:
            other.append(sprite)

    # go through the files
    for filename, scriptdict in files.items():
        # main = text that goes across the page
        html = ['\n<div class="main">']
        html.append('<h2>Scripts for {0}</h2><br></div>'.format(filename))
        # only go through the sprites with scripts
        # go from most to least amount of scripts
        num = len(script_count.keys()) - len(other)
        for sprite, count in script_count.most_common(num):
            # col = page is split into four equal columns
            html.append('\n<div class="col">')
            # for each sprite, print all its scripts in a column
            html.append(sprite)
            html.append('<pre class="blocks">')
            if sprite in scriptdict.keys():
                for script in scriptdict[sprite]:
                    html.append(SnapshotPlugin.to_scratch_blocks(sprite, script))
            else:
                html.append('<br>')
            html.append('</pre>')
            html.append('</div>')

        # List the sprites without scripts
        html.append('\n<div class="main">')
        if len(other) != 0:
            html.append('\n<br>')
            html.append('Sprites that don\'t ever have visible scripts: ')
            if len(other) == 1:
                html.append('{}'.format(other[0]))
            else:
                for n in range(len(other)-2):
                    html.append('{}, '.format(other[n]))
                html.append('and {}.'.format(other[-1]))
        html.append('<br><br><br>')
        output[filename] = ''.join(html)
    return output
