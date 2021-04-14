import os
from bs4 import BeautifulSoup


def get_webloc_files(document_folder, webloc_folder):
    files = []
    path = document_folder + webloc_folder
    try:
        for name in os.listdir(path):
            full_name = os.path.join(path, name)
            if os.path.isfile(full_name):
                _, ext = os.path.splitext(name)
                if ext.lower() == '.webloc':
                    files.append(full_name)
    except FileNotFoundError:
        files = None
    return files


def build_url_list(files):
    url_list = dict()
    for filename in files:
        try:
            with open(filename, 'r') as f:
                data = f.read()
            bs_data = BeautifulSoup(data, 'xml')
            url = bs_data.find('string').text
            url_list[os.path.splitext(os.path.basename(filename))[0]] = url
        except FileNotFoundError:
            pass
    return url_list
