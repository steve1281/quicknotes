#!/usr/bin/env python
"""
Retrieve a list of quicknotes from a directory, sort them.
Search for a specific string, shorten the list. Repeat.


"""
import os
import io
import sys
import time
import re

#initfolder = '//stone/svf$/Quicknotes/'
#initfolder = '/Users/sfalcign/Documents/quicknotes/'
#initfolder = '/home/steve/Documents/quicknotes/'
initfolder = os.getenv('QUICKNOTES','/home/steve/Documents/quicknotes/')

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
    # a quicknote is prefixed with a single, double, or triple integer, or quad.
    #
    qlist = []
    for name in filelist:
        if name[0].isdigit() and name[1] in (' ', '-'):
            qlist.append(name)
        elif name[0].isdigit() and name[1].isdigit() and name[2] in (' ', '-'):
            qlist.append(name)
        elif name[0].isdigit() and name[1].isdigit() and name[2].isdigit() and name[3] in (' ', '-') :
            qlist.append(name)
        elif name[0].isdigit() and name[1].isdigit() and name[2].isdigit() and name[3].isdigit() and name[4] in (' ', '-'):
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
    print " |    * will list all quick notes in the folder and reset filter.    |"
    print " |    a number will print the quick note                             |"
    print " |       (if you want to search by a number, preface witha space)    |"
    print " |    enter on its own will quit the program                         |"
    print " |    / followed by a string will change the search folder.          |"
    print " |    ~ will list the quicknotes on the current filter.              |"
    print " |    - will step you back one in the filter. (can only use once!    |"
    print " |    ? will display this help                                       |"
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
        initfolder = initfolder # os.getcwd() + "/"

    if ln > 1:
         initfolder = str(sys.argv[1])
         print "the search folder is: " + initfolder
        
    files = list_files(initfolder)
    quicknotes = sorted(quicknotelist(files),key = lambda x: int(re.split("-| ",x)[0]))
    
    banner()
    filterstring = ""
    filterhistory ="*"
    while True:
        
        
        newfilterstring = raw_input("\n"+str(len(quicknotes)) + " records, filter history: "+filterhistory+"\nEnter a single filter string: ")
        
        print " "
        if newfilterstring == "":
            break
        elif newfilterstring[0].isdigit() :
            print dumpQuickNote(quicknotes,newfilterstring)
            continue
        elif newfilterstring[0] == "/" :
            if not newfilterstring.endswith("/"):
                newfilterstring = newfilterstring + "/"
            initfolder = newfilterstring
            files = list_files(initfolder)
            quicknotes = sorted(quicknotelist(files),key = lambda x: int(re.split("-| ",x)[0]))
            continue            
        elif newfilterstring[0] == "~" :
            None
        elif newfilterstring[0] == "?" :
            banner()
            continue
        elif newfilterstring[0] == "-" :
            filterstring = newfilterstring
            filterhistory =  filterhistory +"->" + filterstring
            quicknotes = oldnotes
            dump(quicknotes)
            continue
        elif newfilterstring == '*':
            files = list_files(initfolder)
            quicknotes = sorted(quicknotelist(files),key = lambda x: int(re.split("-| ",x)[0]))
            filterstring = ""
            filterhistory = "*"
        else:
            filterstring = newfilterstring
            filterhistory =  filterhistory +"->" + filterstring
            
        print " "
        oldnotes = quicknotes
        quicknotes = filterout(quicknotes,filterstring)
        dump(quicknotes)
        print " "


if __name__ == '__main__':
    main()    
