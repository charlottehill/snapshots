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

# to run: ./snapshots option module directory target
modules = {'scripts': [scripts.Scripts],
           'changes': [changes.Changes]}


# 'ClassName': filename.displayfunction
htmlwrappers = {'Scripts': scripts.scripts_display,
                'Changes': changes.changes_display}

def main():
    parser = OptionParser(usage='%prog LESSON [options] DIRECTORY TARGET')
    parser.add_option('-s', '--student-dir', action="store", type="string", dest="student", default=False,
                      help=('Analyze a directory of a student\'s snapshots for a project.'))
    parser.add_option('-p', '--project-dir', action="store", type="string", dest="project", default=False,
                      help=('Analyze a directory of students\' submissions for a project.'))
    parser.add_option('-a', '--all-dir', action="store", type="string", dest="all", default=False,
                      help=("Analyze a directory of all the students\' submissions for all the projects."))
    options, args = parser.parse_args()
    path = ''
    if options.all:
        path = options.all
    elif options.project:
        path = options.project
    elif options.student:
        path = options.student
    else:
        parser.error('Incorrect option.')
    if len(args) < 2 or len(args) > 4:
        parser.error('Incorrect number of arguments.')
    # go through the command line arguments
    target = '.'
    if len(args) == 3:
        target = args[2]
    module = args[0]

    # Verify the plugin
    if module not in modules:
        print('module `{}` not valid. Goodbye!'.format(module))
        sys.exit(1)

    if options.student:
        process_dir(path, target, module)
    elif options.project:
        for folder in os.listdir(project):
            if os.path.isdir(folder):
                process_dir(folder, target, module)
    elif options.all:
        for folder in os.listdir(all):
            if os.path.isdir(folder):
                for f in os.listdir(folder):
                    if os.path.isdir(f):
                        process_dir(f, target, module)

# run the module on a student directory
#(all the snapshots for a student's project submsision)
def process_dir(path, target, module):
    dirname = os.path.basename(os.path.normpath(path))
    #check if folder exists
    if not os.path.exists('{0}/{1}results'.format(target, dirname)):
        os.makedirs('{0}/{1}results'.format(target, dirname))
    # check if index exists
    index_path = '{0}/{1}results/index.html'.format(target, dirname)
    if not os.path.exists(index_path):
        # make index page
        index =['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ']
        index.append('"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        index.append('\n<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">')
        index.append('\n<!-- InstanceBegin template="/Templates/Template.dwt.php" '
                     'codeOutsideHTMLILocked="false" -->')
        index.append('\n<head>\n<link href="http://octopi.cs.ucsb.edu/analysis/'
                     'stylesheets/style.css" rel="stylesheet" type="text/css" />')
        index.append('\n<meta http-equiv="Content-Type" content="text/html; '
                     'charset=iso-8859-1" />')
        index.append('\n<meta name="language" content="en" />\n')
        index.append('\n<title>{0}</title>'.format(dirname))
        index.append('\n</head>\n<body>\n<div class="content">')
        index.append('\n<h1>{0}</h1><br>'.format(dirname))
        index.append('\n</body>\n</html>')
        with open(index_path, 'w') as fp:
            fp.write(''.join(index))
    #process modules
    index = []
    for plugin_class in modules[module]:
        # set up plugin
        plugin = plugin_class()
        name = plugin.__class__.__name__

        # check if the module has already been done
        file_path = '{0}/{1}results/{1}_{2}.html'.format(target, dirname, module)
        if not os.path.exists(file_path):

            # delete the last two lines of index (\n</body>\n</html>)
            with open(index_path, 'rb+') as filehandle:
                filehandle.seek(-18, os.SEEK_END)
                filehandle.truncate()

            # set up html file headers
            html = []
            html.append('\n<html>\n<head>\n<meta charset="utf8">')
            html.append('\n<h1 style="text-align:center">{0} {1}</h1>\n\n<hr>'.format(dirname, name))
            # include stylesheet
            html.append('<link rel="stylesheet" type="text/css" ')
            html.append('href="http://octopi.cs.ucsb.edu/analysis/'
                        'stylesheets/script_style.css" />')
            #Include jQuery
            html.append('\n<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/'
                        'jquery.min.js"></script>')

            #Include scratchblocks2 files
            html.append('\n<link rel="stylesheet" href="//charlottehill.com/'
                        'scratchblocks/scratchblocks2.css">')
            html.append('\n<link rel="stylesheet" type="text/css" href="style.css">')
            html.append('\n<script src="//charlottehill.com/scratchblocks/'
                        'scratchblocks2.js"></script>')
            #Parse blocks
            html.append('\n<script>\n$(document).ready(function() {')
            html.append('\n scratchblocks2.parse("pre.blocks");')
            html.append('\n scratchblocks2.parse("pre.hidden");')
            html.append('\n scratchblocks2.parse("pre.error");')
            html.append('\n});\n</script>\n</script>\n</head>')
            html.append('\n</body>\n</html>')

            #run the module
            results = plugin._process(path)
            # returns a dictionary of html strings for each file
            html_results = htmlwrappers[name](results)
            # print the results in order
            for file in sorted(html_results.iterkeys()):
                # html for this file for this module 
                html.append(html_results[file])

            # add on the closing html 
            html.append('\n</body>\n</html>')

            # write the results for all the files
            with open(file_path, 'w') as fp:
                fp.write(''.join(html))

            # add a link to the index
            index.append('\n<br><br><a href="./{0}_{1}.html">{1}</a>'.format(dirname,module))
            index.append('\n</body>\n</html>')
            with open('{0}/{1}results/index.html'.format(target, dirname), 'a') as fp:
                fp.write(''.join(index))

if __name__ == '__main__':
    sys.exit(main())
