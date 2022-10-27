"""
Module to read all files from the folder
"""

import json
import os
from enum import Enum

class FileTypes(Enum):
    POST_STATS = 'post-stats'
    DAILY_STATS = 'daily-stats'

def files_list(path: str) -> list[str]:
    """
    Returns the list of files in the given path
    """
    return os.listdir(path)

def file_load(file_name: str) -> dict:
    """
    Loads the file and returns the data
    """
    with open(file_name,'r') as file:
        data = json.load(file)

    return data
    