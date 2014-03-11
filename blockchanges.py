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


class BlockChanges(SnapshotPlugin):

    def __init__(self):
        super(BlockChanges, self).__init__()
        # add a name and description that we can put on the website 
        self._modulename = "Blocks Changes"
        self._description = "Highlight blocks that have changed since the last snapshot."

    def compare(self, old, curr):
        for script in curr:
            for name, level, block in self.iter_blocks(script):
                print(name, block.args)

    def sprite_compare(self, old, curr):
        scripts = set()
        # find exact matches
        # TO DO don't really do exact, just do exact names and levels and string args
        for script in curr:
            for s in old:
                if s == script:
                    scripts.add(script)
                    old.remove(s)
                    curr.remove(script)
        for script in curr:
            best = script
            best_score = 0
            found = False
            for s in old:
                if not found:
                    if script == s:
                        found = True
                    else:
                        score, new_script = self.script_compare(s, script)
                        if score > best_score:
                            best_score = score
                            best = new_script
            scripts.add(best)
        return scripts


    def script_compare(self, old, curr):
        best = script
        best_score = 0
        for name, level, block in self.block_iter(curr):
            print(block)
        return best


    def block_compare(self, oldname, oldlevel, oldblock,
                     currname, currlevel, currblock):
        if oldname == currname:
            return 100
        else:
            return 0

    def analyze(self, path):
        # use the Scripts class to get the scripts
        scripts_analyzer = Scripts()
        scripts_results = scripts_analyzer.analyze(path)
        counter = scripts_results['counter']
        files = scripts_results['scripts']

        last = False
        # go through the files
        for file, scriptdict in files.items():
            # make sure there's a previous snapshot
            if last:
                # Go through all the sprites
                for sprite, scripts in scriptdict.items():
                    counter[sprite] += 1
                    # Only go through the scripts for sprites with changes
                    if counter[sprite] > 0:
                        # if this sprite was in the last file, compare their scripts
                        if sprite in last.keys():
                            scriptdict[sprite] = self.compare(last[sprite], scripts)
                        else:
                            # otherwise, mark all of this sprites scripts as changed
                            for script in scripts:
                                for name, level, block in KelpPlugin.iter_blocks(script):
                                    block.changed = True
            last = scriptdict
        return {'counter': counter, 'scripts': files}


# Displays the scripts for each sprite for each file 
#TO D: highlight blocks that changed
''' This is hard because I'm not sure how to change individual blocks in a script.
Before I only changed separate blocks or scripts
I think I'll have to make a new block format thing?
Like, maybe something like how it parses the comments
Maybe but a * next to all the blocks that need to be highlighted, and then overwrite/modify the color?
It would be really nice if there was an outline color that we could just add
So that would be something to look up
'''
def block_changes_display(results):
    files = results['scripts']
    script_count = results['counter']

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

            html.append(sprite)

            # this is what scratchblocks uses to make the blocks look pretty
            html.append('<pre class="blocks">')

            # make sure this sprite is in this file
            if sprite in scriptdict.keys():
                 # get the sprite's scripts 
                for script in scriptdict[sprite]:
                    # to scratch blocks prints the script in the 
                    # format needed by scratchblocks 
                    # TO DO: highlight any block that has an attribute block.changed == True
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
