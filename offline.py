#!/usr/bin/env python
from __future__ import print_function
from kelp.octopi import OctopiPlugin
from kelp import *
import scripts
import changes
from optparse import OptionParser
import kurt
import sys
import os

# to run: ./snapshots directory module
modules = {'scripts': [scripts.Scripts],
           'changes': [changes.Changes]}


# 'ClassName': filename.displayfunction
htmlwrappers = {'Scripts': scripts.scripts_display,
                'Changes': changes.changes_display}


def html_view(title):
    html = []
    html.append('\n<html>')
    html.append('\n<head>')
    html.append('\n<meta charset="utf8">')
    #title() makes first letter capital
    html.append('\n<h1 style="text-align:center">{0}</h1>'.format(title.title()))
    html.append('<hr>')
    # include stylesheet
    html.append('<link rel="stylesheet" type="text/css" href="style.css" />')
    #<!-- Include jQuery -->
    html.append('\n<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/'
                'jquery.min.js"></script>')

    #<!-- Include scratchblocks2 files -->
    html.append('\n<link rel="stylesheet" href="//charlottehill.com/'
                'scratchblocks/scratchblocks2.css">')
    html.append('\n<link rel="stylesheet" type="text/css" href="style.css">')
    html.append('\n<script src="//charlottehill.com/scratchblocks/'
                'scratchblocks2.js"></script>')

    #<!-- Parse blocks -->
    html.append('\n<script>')
    html.append('\n$(document).ready(function() {')
    html.append('\n     scratchblocks2.parse("pre.blocks");')
    html.append('\n     scratchblocks2.parse("pre.hidden");')
    html.append('\n     scratchblocks2.parse("pre.error");')
    html.append('\n     });')
    html.append('\n</script>')
    html.append('\n</script>')
    html.append('\n</head>')
    return ''.join(html)


def main():
    parser = OptionParser(usage='%prog DIRECTORY LESSON TARGET')
    options, args = parser.parse_args()
    if len(args) < 2 or len(args) > 4:
        parser.error('Incorrect number of arguments.')
    # go through the command line arguments
    target = '.'
    if len(args) == 3:
        target = args[2]
    path = args[0]
    module = args[1]

    # Verify the plugin
    if module not in modules:
        print('module `{}` not valid. Goodbye!'.format(module))
        sys.exit(1)

    # get the directory from the path
    dirname = os.path.basename(os.path.normpath(path))

    # do you want the results on one page or on different pages for each file?
    single_file = True

    if single_file:
        # add the headers and stuff to the page
        html_list = [html_view(module)]
        for plugin_class in modules[module]:
            plugin = plugin_class()
            name = plugin.__class__.__name__
            results = plugin._process(path)
            # returns a dictionary of html strings for each file
            html_results = htmlwrappers[name](results)
            for file in sorted(html_results.iterkeys()):
                # html for this file for this module
                html_list.append(html_results[file])
            # add on the closing html
            html_list.append('</body>')
            html_list.append('</html>')
            # write the results for all the files 
            with open('{0}/{1}_{2}.html'.format(target, dirname, module), 'w') as fp:
                fp.write(''.join(html_list))
    else:
        for plugin_class in modules[module]:
            # make a directory for all the results pages
            if not os.path.exists('{0}results'.format(dirname)):
                os.makedirs('{0}results'.format(dirname))
            plugin = plugin_class()
            name = plugin.__class__.__name__
            results = plugin._process(path)
            # returns a dictionary of html strings for each file
            html_results = htmlwrappers[name](results)
            for file in sorted(html_results.iterkeys()):
                # add the headers and stuff to the page
                html_list = [html_view(module)]
                # html for this file for this module
                html_list.append(html_results[file])
                # add on the closing html
                html_list.append('</body>')
                html_list.append('</html>')
                # write the results for this file
                with open('{0}/{1}results/{2}_{3}.html'.format(
                        target, dirname, file, module), 'w') as fp:
                    fp.write(''.join(html_list))

if __name__ == '__main__':
    sys.exit(main())
