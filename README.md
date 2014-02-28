snapshots
=========

Kelp plugins for sets of projects

Snapshots expects a directory of Octopi files that are for the same assignment from the same user.

## Installation
Snapshots inherits from Kelp Plugin, so you need Kelp Plugin and all its requirements.

## Running Snapshots
From outside of the snapshots directory:
	./snapshots/snapshots MODULE [options] DIRECTORY TARGET
Module: the module you want to run, for example, "scripts"
Option: Tells snapshots what kind of directory you're giving it.
	-s  or --student-dir : the directory is a directory of a student's snapshots for a project
	-p or --project-dir : the directory is a project directory that contains one or more student directories (see above)
	-a or --all-dir : the directory contains one or more project directories (see above)
Directory: the directory of files, see above
Target: where you want the created files to go. If you don't specify this it'll just put them on your current path

## Output
Snapshots creates new results directories for the output if they don't already exist. Additionally, snapshots will only run plugins for a module if it doesn't see the results already in the results directories - this is because it creates index pages, and we don't want to add a bunch of links to them that all go to the same place. If you want to rerun modules in the same place, delete the old results files first.
