
"""
Retrieve a list of quick notes from a directory, sort them.
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


def build_quick_note_list(file_list):
    """
    a quick note is prefixed with 2 digits, 3 digits, or 4
    followed by a dash.

    a quick note must be a .md or a .txt file.

    :param file_list:  list of potential files
    :return: files that match our specs

    """
    quick_list = []
    for name in file_list:
        _, ext = os.path.splitext(name)
        if not (ext.lower() in ['.txt', '.md']):
            continue
        if re.search("^[0-9]{2,4}-.*$", name):
            quick_list.append(name)
    return quick_list


def build_filtered_file_list(document_folder, file_list, filter_string):
    """
    check the body and title of quick note for a string match.
    also checks upper and lower cases of the filter string.

    :param document_folder: location of documents
    :param file_list: List of (text) files to search
    :param filter_string: String to search for
    :return: list of files containing the search string
    """
    quick_list = []
    for name in file_list:
        with open(document_folder + name, "r") as f:
            s = f.read()
            if s.count(filter_string) > 0 or name.count(filter_string):
                quick_list.append(name)
            elif s.count(filter_string.upper()) > 0 or name.count(filter_string.upper()):
                quick_list.append(name)
            elif s.count(filter_string.lower()) > 0 or name.count(filter_string.lower()):
                quick_list.append(name)
            else:
                pass
    return quick_list


def dump_quick_note(document_folder, filename):
    """
    return the first matching file contents

    :param document_folder: location of documents
    :param filename: return contents of a quick note
    :return:
    """
    with open(document_folder + filename, "rU") as f:
        _, ext = os.path.splitext(document_folder + filename)
        s = "<pre>" + filename + "</pre>\n\n"
        s = s + f.read()
    return s, ext
