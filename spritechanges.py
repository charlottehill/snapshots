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


class SpriteChanges(SnapshotPlugin):

    def __init__(self):
        super(SpriteChanges, self).__init__()
        # add a name and description that we can put on the website 
        self._modulename = "Sprite Changes"
        self._description = "Highlight sprites whose scripts have changed since the last snapshot"

    def analyze(self, path):
        # use the Scripts class to get the scripts
        scripts_analyzer = Scripts()
        scripts_results = scripts_analyzer.analyze(path)
        counter = scripts_results['counter']
        files = scripts_results['scripts']

        # make a dictionary of sprites that have changed since the last snapshot
        # changes[filename] = set of sprites who have changed since the last snapshot
        changes = {}

        # store the last file so we can compare
        last = False

        # go through the files
        for file, scriptdict in files.items():
            # this means we're on the first one, so last is false
            if not last:
                last = scriptdict

            # make a set of sprite for this file
            changes[file] = set()

            # go through the scripts for this file
            for sprite, scripts in scriptdict.items():

                # check if the sprite was in the last snapshot
                if sprite in last.keys():

                    # get the diff of this sprite's scripts and
                    # the scripts it had in the last snapshot
                    diff = last[sprite] ^ scripts

                    # if there were any differences, add it to changes
                    if len(diff) != 0:
                        changes[file].add(sprite)
                else:
                    # the sprite wasn't in the last file, so it's changed
                    changes[file].add(sprite)

            # now this will be the alst file
            last = scriptdict

        return {'counter': counter, 'scripts': files,
                'changes': changes}


# Displays the scripts for each sprite for each file 
# Prints the sprite name in blue if it changed since the last snapshot
def sprite_changes_display(results):
    files = results['scripts']
    script_count = results['counter']
    changes = results['changes']

    # this will store the sprites that don't have any visible scripts 
    other = []

    # we will return a dictionary of html strings for each file
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

        # add a heading 
        html.append('<h2>Scripts for {0}</h2><br></div>'.format(filename))

        # we'll only go through the sprites with scripts
        num = len(script_count.keys()) - len(other)

        # go from most to least amount of scripts
        for sprite, count in script_count.most_common(num):
            # col = page is split into four equal columns
            # each sprite will have a column of scripts 
            html.append('\n<div class="col">')

            # print the name of the sprite 
            # if it's in changes, use the heading class "change"
            if sprite in changes[filename]:
                html.append('<h3 class="change">{0}</h3>'.format(sprite))
            else:
                html.append(sprite)

            # this is what scratchblocks uses to make the blocks look pretty
            html.append('<pre class="blocks">')

            # make sure this sprite is in this file
            if sprite in scriptdict.keys():
                 # get the sprite's scripts 
                for script in scriptdict[sprite]:
                    # to scratch blocks prints the script in the 
                    # format needed by scratchblocks 
                    html.append(SnapshotPlugin.to_scratch_blocks(sprite, script))
            else:
                # this sprite isn't in this file, just print an empty line
                html.append('<br>')
            # close the blocks pre class
            html.append('</pre>')
            # close the column div class
            html.append('</div>')

        # List the sprites without scripts
        # to do?: just print this once at the bottom of the page 
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

        # add the html (as a string) to the dictionary 
        output[filename] = ''.join(html)

    return output
