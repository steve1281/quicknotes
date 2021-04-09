
def get_record_count(filename):
    with open(filename) as f:
        contents = f.read()
    return contents.count("%%")
    

def get_fortune(filename, record_number):
    with open(filename) as f:
        contents = f.read()
        s = contents.split('%%')[record_number]
    return s
    

