""" holds the logic of scaning all files in data folder"""

from os import stat
from files import files_list
from stat_objects import Stats

def scan_single(path:str) -> list[str]:
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

def scan_files(path:str) -> list[str]:
    """ scan all files in the given path """
    files = files_list(path)
    stats_all = dict()
    
    for file in files:
        stats = Stats()
        stats.load_file(path+'/'+file)
        # get the object from the dict
        stats_obj = stats_all.get(stats.id)
        # reload the file if new
        if stats_obj is None:
            stats_obj=stats
        else:
            stats_obj.load_file(path+'/'+file)
            
        # add the object to the dict
        stats_all[stats_obj.id] = stats_obj

    output = []
    output.append(stats.dump_header())
    for key in stats_all:
        for line in stats_all[key].dump_data():
            output.append(line)
    
    return output
    