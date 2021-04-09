
def get_record_count(filename):
    try:
        with open(filename) as f:
            contents = f.read()
    except FileNotFoundError:
        return -1
    return contents.count("%%")
    

def get_fortune(filename, record_number):
    try:
        with open(filename) as f:
            contents = f.read()
            s = contents.split('%%')[record_number]
    except FileNotFoundError:
        s = f"fortune file {filename} Not found."
    return s
    

