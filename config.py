"""
Scraper configurations

sid	your Medium session id from cookie
uid	your Medium user id from cookie

"""
from dotenv import load_dotenv
import os

class Config(object):
    """ app  configuration class."""

    SID = os.getenv('SID')
    UID = os.getenv('UID')

    PUBLICATION = os.getenv('PUBLICATION')
    OUTPUT = os.getenv('OUTPUT')

    def __init__(self):
        load_dotenv()





