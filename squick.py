
"""
Retrieve a list of quicknotes from a directory, sort them.
Search for a specific string, shorten the list. Repeat.
"""
import os


def list_files(path):
    """
    returns a list of names (with extension, without full path) of all files
    in folder path
    """
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files


def quicknotelist(filelist):
    """
    a quicknote is prefixed with a single, double, or triple integer, or quad.

    :param filelist:  list of potential files
    :return: files that match our specs

    @todo: replace this with with (a simple) regex.
    """
    qlist = []
    for name in filelist:
        _, ext = os.path.splitext(name)
        if not (ext.lower() in ['.txt', '.md']):
            pass
        elif name[0].isdigit() and name[1] in (' ', '-'):
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


def filterout(initfolder, filelist, filterstring):
    """
    check the body and title of quick note for a string match.
    also checks upper and lower cases of the filter string.

    :param initfolder: QUICKNOTES folder; location of documents
    :param filelist: List of (text) files to search
    :param filterstring: String to search for
    :return: list of files containing the search string
    """
    qlist = []
    for name in filelist:
        with open(initfolder + name, "r") as f:
            s = f.read()
            if s.count(filterstring) > 0 or name.count(filterstring):
                qlist.append(name)
            elif s.count(filterstring.upper()) > 0 or name.count(filterstring.upper()):
                qlist.append(name)
            elif s.count(filterstring.lower()) > 0 or name.count(filterstring.lower()):
                qlist.append(name)
            else:
                pass
    return qlist


def dumpQuickNote(initfolder, filename):
    """
    return the first matching file contents

    :param initfolder: QUICKNOTES folder; location of documents
    :param filelist: List of (text) files
    :return:
    """
    s = " quick note was not found!"
    ext = ""
    with open(initfolder+filename,"rU") as f:
        _, ext = os.path.splitext(initfolder+filename)
        s = "<pre>" + filename + "</pre>\n"
        s = s + "\n"
        s = s + f.read()
        f.close()
    return s, ext
