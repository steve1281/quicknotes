#!/usr/bin/python
"""
Retrieve a list of quicknotes from a directory, sort them.
Search for a specific string, shorten the list. Repeat.


"""
import os
import io
import sys
import time

initfolder = '//stone/svf$/Quicknotes/'

def list_files(path):
    # returns a list of names (with extension, without full path) of all files 
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files

def dump(filelist):
    for name in filelist:
        print(name)

def quicknotelist(filelist):
    # a quicknote is prefixed with a single, double, or triple integer.
    #
    qlist = []
    for name in filelist:
        if name[0].isdigit() and name[1]==' ':
            qlist.append(name)
        elif name[0].isdigit() and name[1].isdigit() and name[2]==' ':
            qlist.append(name)
        elif name[0].isdigit() and name[1].isdigit() and name[2].isdigit() and name[3]==' ':
            qlist.append(name)
        else:
            None
    return qlist

def filterout(filelist, filterstring):
    # check the body and title of quick note for a string match.
    # also checks upper and lower cases of the filter string.
    # 
    qlist=[]
    for name in filelist:
        f = open(initfolder+name,"r")
        s = f.read()
        if s.count(filterstring) > 0 or name.count(filterstring):
            qlist.append(name)
        elif s.count(filterstring.upper()) > 0  or name.count(filterstring.upper()):
            qlist.append(name)
        elif s.count(filterstring.lower()) > 0 or name.count(filterstring.lower()):
            qlist.append(name)
        else:
            None
            
        f.close()
        
    return qlist

def dumpQuickNote(filelist,quick):
    # return the first matching file contents
    #
    s = quick + " quick note was not found!"
    for name in filelist:
        if name.startswith(quick):
            f = open(initfolder+name)
            s = name + "\n"
            s = s + "Last modified: " + time.ctime(os.path.getmtime(name)) + "\n"
            s = s + "\n"
            s = s + f.read()
            f.close()
            break
    return s

def banner():
    #
    #
    print " "
    print " +-------------------------------------------------------------------+"
    print " |                                                                   |"
    print " |    QuickNotes: Search and Display                                 |"
    print " |                                                                   |"
    print " |    Source folder is: " +  initfolder
    print " |                                                                   |"
    print " |    * will list all quick notes in the folder                      |"
    print " |    a number will print the quick note                             |"
    print " |    enter on its own will quit the program                         |"
    print " |    / followed by a string will change the search folder.          |"
    print " |                                                                   |"
    print " +-------------------------------------------------------------------+"
    print " "
    return
        
def main():
    #
    #
    global initfolder
    
    ln = len(sys.argv)
    if ln == 1:
        initfolder = os.getcwd() + "/"

    if ln > 1:
         initfolder = str(sys.argv[1])
         print "the search folder is: " + initfolder
        
    files = list_files(initfolder)
    quicknotes = sorted(quicknotelist(files),key = lambda x: int(x.split(" ")[0]))
    
    
    filterstring = ""
    while True:
        banner()
        filterstring = raw_input("Enter a single filter string: ")
        print " "
        if filterstring == "":
            break
        elif filterstring[0].isdigit() :
            print dumpQuickNote(quicknotes,filterstring)
            continue
        elif filterstring[0] == "/" :
            if not filterstring.endswith("/"):
                filterstring = filterstring + "/"
            initfolder = filterstring
            files = list_files(initfolder)
            quicknotes = sorted(quicknotelist(files),key = lambda x: int(x.split(" ")[0]))
            continue            
        elif filterstring == '*':
            files = list_files(initfolder)
            quicknotes = sorted(quicknotelist(files),key = lambda x: int(x.split(" ")[0]))
            filterstring = ""
        else:
            None
        print " "
        quicknotes = filterout(quicknotes,filterstring)
        dump(quicknotes)
        print " "

main()    
