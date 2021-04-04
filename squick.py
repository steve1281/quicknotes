
"""
Retrieve a list of quicknotes from a directory, sort them.
Search for a specific string, shorten the list. Repeat.
"""
import os
import re


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
    a quicknote is prefixed with 2 digits, 3 digits, or 4
    followed by a dash.

    a quicknote must be a .md or a .txt file.

    :param filelist:  list of potential files
    :return: files that match our specs

    """
    qlist = []
    for name in filelist:
        _, ext = os.path.splitext(name)
        if not (ext.lower() in ['.txt', '.md']):
            continue
        if re.search("^[0-9]{2,4}-.*$", name):
            qlist.append(name)
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


def dump_quicknote(initfolder, filename):
    """
    return the first matching file contents

    :param initfolder: QUICKNOTES folder; location of documents
    :param filename: return contents of a quicknote
    :return:
    """
    s = f"{filename}: quick note was not found!"
    ext = ""
    with open(initfolder+filename, "rU") as f:
        _, ext = os.path.splitext(initfolder+filename)
        s = "<pre>" + filename + "</pre>\n\n"
        s = s + f.read()
    return s, ext
