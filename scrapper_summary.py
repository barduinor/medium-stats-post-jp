""" medium screper methods"""


from datetime import datetime
from distutils.command.config import config
from medium_stats.scraper import StatGrabberPublication
from datetime import datetime
from config import Config
from pandas import DataFrame
import pathlib


def get_publication_stats(publication_name: str, start: datetime, stop: datetime) -> str:
    """This function will return the stats of the given publication"""
    publication = StatGrabberPublication(
        slug=publication_name,
        sid=Config.SID,
        uid=Config.UID,
        start=start,
        stop=stop,
        now=None,
        already_utc=False,
    )
    story_stats = publication.get_all_story_overview()
    return story_stats


def publication_stats_to_csv(publication_name: str, publication_stats: str):
    """This function will convert the stats of the given publication to a csv format"""
    
    df = DataFrame(publication_stats)
    file_path = Config.OUTPUT +'/'+ publication_name + "_stats.csv"
    df.to_csv(file_path, index=False)
    return df


