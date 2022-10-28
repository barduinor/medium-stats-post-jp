""" holds the logic of scaning all files in data folder"""

from files import files_list
from stat_objects import Stats

def scan_files(path) -> list[str]:
    """ scan all files in the given path """
    files = files_list(path)
    stats = Stats()
    for file in files:
        stats.load_file(path+'/'+file)

    output = []
    output.append(stats.dump_header())
    for line in stats.dump_data():
        output.append(line)
    
    return output
    