"""Display all the sprites' visible scripts."""

from __future__ import print_function
from collections import Counter
from kelp.kelpplugin import KelpPlugin
from snapshotplugin import SnapshotPlugin
from scripts import Scripts
import os
import sys
import kurt

BASE_PATH = './results'


class Changes(SnapshotPlugin):

    def __init__(self):
        super(Changes, self).__init__()

    def analyze(self, path):
        # use the Scripts class to get the scripts
        scripts_analyzer = Scripts()
        scripts_results = scripts_analyzer.analyze(path)
        counter = scripts_results['counter']
        files = scripts_results['scripts']

        # make a dict of highlighted scripts for each file
        changes = {}
        last = False
        for file, scriptdict in files.items():
            if not last:
                last = scriptdict
            changes[file] = set()
            for sprite, scripts in scriptdict.items():
                if sprite in last.keys():
                    diff = last[sprite] ^ scripts
                    if len(diff) != 0:
                        changes[file].add(sprite)
                else:
                    changes[file].add(sprite)
            last = scriptdict

        return {'counter': counter, 'scripts': files,
                'changes': changes}


# Displays sprite names and pictures
def changes_display(results):
    files = results['scripts']
    script_count = results['counter']
    changes = results['changes']
    other = []
    # return a dictionary of html strings for each file
    output = {}

    # make a list of sprites without scripts
    for sprite, count in script_count.most_common():
        if count == 0:
            other.append(sprite)
    
    # go through the files
    for filename, scriptdict in files.items():
        scriptdict = files[filename]
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
            if sprite in changes[filename]:
                html.append('<h3 class="change">{0}</h3>'.format(sprite))
            else:
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
