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
    html.append('<link rel="stylesheet" type="text/css" href="http://octopi.cs.ucsb.edu/analysis/stylesheets/script_style.css" />')
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
    if not os.path.exists('{0}/{1}results'.format(target, dirname)):
        os.makedirs('{0}/{1}results'.format(target, dirname))

    for plugin_class in modules[module]:
        # returns a dictionary of html strings for each file
        single = [html_view(module)]
        # build index.html 
        index =['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ']
        index.append('"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        index.append('\n<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">')
        index.append('\n<!-- InstanceBegin template="/Templates/Template.dwt.php" codeOutsideHTMLILocked="false" -->')
        index.append('\n<head>\n<link href="http://octopi.cs.ucsb.edu/analysis/stylesheets/style.css" rel="stylesheet" type="text/css" />')
        index.append('\n<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />')
        index.append('\n<meta name="language" content="en" />')
        index.append('\n')
        plugin = plugin_class()
        name = plugin.__class__.__name__
        index.append('\n<title>{0}</title>'.format(dirname))
        index.append('\n</head>\n<body>\n<div class="content">')
        index.append('\n<h1>{0} {1}</h1>'.format(dirname, name))
        results = plugin._process(path)
        # returns a dictionary of html strings for each file
        html_results = htmlwrappers[name](results)
        for file in sorted(html_results.iterkeys()):
            index.append('\n<br><a href="./{0}_{1}.html">{0}</a>'.format(file, module))
            # html for this file for this module
            single.append(html_results[file])
            # html for multiple files
            multiple = [html_view(module)]
            multiple.append(html_results[file])
            multiple.append('</body>')
            multiple.append('</html>')
            # write the results for this file
            with open('{0}/{1}results/{2}_{3}.html'.format(
                    target, dirname, file, module), 'w') as fp:
                fp.write(''.join(multiple))
        # add on the closing html
        single.append('</body>')
        single.append('</html>')
        # write the results for all the files
        with open('{0}/{1}results/{1}_{2}.html'.format(target, dirname, module), 'w') as fp:
            fp.write(''.join(single))
        index.append('\n<br><br><a href="./{0}_{1}.html">View all on one page</a>'.format(dirname,module))
        with open('{0}/{1}results/index.html'.format(target, dirname), 'w') as fp:
            fp.write(''.join(index))


if __name__ == '__main__':
    sys.exit(main())
