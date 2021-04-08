#!/usr/bin/env python
"""
synopisis:

file contain records seperated by %%
count the number of %% in a file
select a random n from 1 to count
read and display the record.

"""
import argparse
import logging
import os
import random

# --- argparse

_parser = argparse.ArgumentParser()
_parser.add_argument('-o', '--obscene', action='store_true', default=False, help="Activate adult humor.")
_parser.add_argument('-d', '--debug', action='store_true', default=False, help="Turn on debugging.")
args = _parser.parse_args()

# --- log level
LOG_LEVEL = os.environ.get('LOG_LEVEL', "TRUE")

if LOG_LEVEL == "DEBUG":
    log_level = logging.DEBUG
elif LOG_LEVEL == "INFO":
    log_level = logging.INFO
elif LOG_LEVEL == "WARNING":
    log_level = logging.WARNING
elif LOG_LEVEL == "ERROR":
    log_level = logging.ERROR
else:
    log_level = logging.ERROR

if args.debug:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level)



def get_record_count(filename):
    logging.debug(f"scanning for total number of fortunes in {filename}")
    with open(filename) as f:
        contents = f.read()
    return contents.count("%%")
    

def get_fortune(filename, record_number):
    logging.debug(f"loading fortune {record_number}")
    with open(filename) as f:
        contents = f.read()
        s = contents.split('%%')[record_number]
    return s
    

def main():
    if args.obscene:
        filename = "obscene"
    else:
        filename = "scene"

    logging.debug(f"Fortune file is {filename}")
    record_count = get_record_count(filename)
    logging.debug(f"{record_count} records were found.")
    random_record = random.randint(0, record_count-1)
    print(get_fortune(filename, random_record))
    

if __name__ == '__main__':
    main()


