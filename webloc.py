import os
from bs4 import BeautifulSoup
from  configparser import ConfigParser


def get_webloc_files(document_folder, webloc_folder):
    files = []
    path = document_folder + webloc_folder
    try:
        for name in os.listdir(path):
            full_name = os.path.join(path, name)
            if os.path.isfile(full_name):
                _, ext = os.path.splitext(name)
                if ext.lower() in ['.webloc', '.url', '.desktop']:
                    files.append(full_name)
    except FileNotFoundError:
        files = None
    return files


def webloc_get(filename):
    """
    Scan a .webloc file (mac) for a URL
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        data = f.read()
    bs_data = BeautifulSoup(data, 'xml')
    return bs_data.find('string').text


def desktop_get(filename):
    """
    Scan a .desktop file (ubuntu) for a URL
    :param filename:
    :return:
    """
    config = ConfigParser()
    config.read(filename)
    return config['Desktop Entry']['URL']


def url_get(filename):
    """
    Scan a .url file  (windows) for a URL
    :param filename:
    :return:
    """
    config = ConfigParser()
    config.read(filename)
    return config['InternetShortcut']['URL']


def build_url_list(files):
    url_list = dict()
    for filename in files:
        try:
            display_name, ext = os.path.splitext(os.path.basename(filename))
            if ext.lower() == '.webloc':
                url_list[display_name] = webloc_get(filename)
            elif ext.lower() == '.url':
                url_list[display_name] = url_get(filename)
            elif ext.lower() == '.desktop':
                url_list[display_name] = desktop_get(filename)
            else:
                pass

        except FileNotFoundError:
            pass
    return url_list
