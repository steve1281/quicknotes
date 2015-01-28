#!/usr/bin/env python
import os
import time
import shutil


def tagFiles(direname):
    os.chdir(direname)
    for filename in os.listdir("."):
    	if filename.endswith(".txt"):
                newfile = os.path.splitext(filename)[0] +" ["+time.ctime(os.path.getmtime(filename))+"]"+os.path.splitext(filename)[1]
                newfile = newfile.replace(":"," ")
                shutil.copy(filename, newfile)

def main():
    print "this is meant to be a run once tool"
    tagFiles("//stone/svf$/quicknotes")

		
if __name__ == '__main__':
    main()
