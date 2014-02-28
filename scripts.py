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
        # add a name and description that we can put on the website
        self._modulename = "Scripts"
        self._description = "Show the scripts for each file."

    # returns a dictionary of all the scripts organized by sprite for an oct file
    def get_scripts(self, oct):
        scripts = {}
        for sprite in [oct.stage] + oct.sprites:
            scripts[sprite.name] = set()
            self.script_count[sprite.name] = 0
            for script in sprite.scripts:
                if not isinstance(script, kurt.Comment):
                    # update the script count
                    self.script_count[sprite.name] += 1
                    scripts[sprite.name].add(script)
        return scripts


    def analyze(self, path):
        # keep a count of the number of visible scripts for each sprite
        # use this to order them at the end
        # any sprites with zero scripts will be listed separately
        self.script_count = Counter()

        # dictionary of all the scripts
        # scripts[filename] = sprites
        # scripts[filename][spritename] = set of scripts
        scripts = {}

        # get the directory name
        dirname = os.path.dirname(path)
        # go through oct files
       for file in os.listdir(path):
            if file.endswith(".oct"):
                # get file name
                base = os.path.basename(file)
                filename = os.path.splitext(base)[0]

                # set up kurt project
                oct = kurt.Project.load(os.path.abspath(os.path.join(path, file)))

                # get scripts for that file
                scripts[filename] = self.get_scripts(oct)
       #Counter - used to order the sprites on the webpage
       #Scripts - the scripts for each sprite for each file
        return {'counter': self.script_count, 'scripts': scripts}


# Displays the scripts for each sprite for each file
def scripts_display(results):
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
        # main = text that goes across the page
        html = ['\n<div class="main">']

        # add a heading
        html.append('<h2>Scripts for {0}</h2><br></div>'.format(filename))

        # we'll only go through the sprites with scripts
        num = len(script_count.keys()) - len(other)

        # go from most to least amount of scripts 
        for sprite, count in script_count.most_common(num):
            # col = content is split into equal sized columns
            # each sprite will have a column of scripts
            html.append('\n<div class="col">')

            # print the name of the sprite
            # to do?: add a thumbnail
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
        # lots of fancy footwork to get the and in the right place
        # change this if there's a nicer way to do it
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
