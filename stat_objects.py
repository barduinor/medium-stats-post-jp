""" objects to hold the files data """

from dataclasses import InitVar, dataclass
from datetime import date
import json
from enum import Enum

class FileTypes(Enum):
    POST_STATS = 'post-stats'
    DAILY_STATS = 'daily-stats'


@dataclass
class Stats:
    """ class to hold a post stat data """
    file_path: InitVar[str] = None
    id: str = None
    title: str = None
    publishDate: date = None
    totalStats: object = None
    dailyStats: object = None
    
    def __post_init__(self, file_path):
        """ post init """
        if file_path is not None:
            self.load_file(file_path)       

    def load_file(self, file_path:  str):
        """ load the file """
        with open(file_path,'r') as file:
            try:
                data = json.load(file)
                file_type = self.identify_file_type(data)
                if file_type == FileTypes.POST_STATS:
                    self.load_post_data(data)
                elif file_type == FileTypes.DAILY_STATS:
                    self.load_daily_data(data)
                else:
                    raise Exception('Unknown file type')
            except Exception as e:
                print(f'Error loading the file {file_path}')
                print(e)
                return None

    def load_post_data(self, data: dict):
        """ load the post data """
        # check if id is new
        if self.id is None:
            self.id = data[0]['data']['post']['id']
        elif self.id != data[0]['data']['post']['id']:
            raise Exception('ID mismatch')

        self.title = data[0]['data']['post']['title']
        self.title = self.title.replace(',',' ')
        self.title = self.title.replace('  ',' ')
        self.totalStats = data[0]['data']['post']['totalStats']
        
    def load_daily_data(self, data: dict):
        """ load the daily data """
        # check if id is new
        if self.id is None:
            self.id = data[0]['data']['post']['id']
        elif self.id != data[0]['data']['post']['id']:
            raise Exception('ID mismatch')

        self.publishDate = date.fromtimestamp(data[0]['data']['post']['dailyStats'][0]['periodStartedAt']//1000)
        self.dailyStats = data[0]['data']['post']['dailyStats']

    
    def identify_file_type(self, data: dict):
        """ identify the file type """
        if 'totalStats' in data[0]['data']['post']:
            return FileTypes.POST_STATS
        elif 'dailyStats' in data[0]['data']['post']:
            return FileTypes.DAILY_STATS
        else:
            return None

    def dump_data(self) -> list:
        """ dump the data to csv """
        data_list = []
        for stat in self.dailyStats:
            daysSincePublish = (date.fromtimestamp(stat['periodStartedAt']//1000) - self.publishDate).days
            data_line = f"{self.id},{self.title},{self.publishDate},{daysSincePublish},{date.fromtimestamp(stat['periodStartedAt']//1000)},{stat['views']},{stat['memberTtr']}"
            data_list.append(data_line)
        return data_list


    def dump_header(self) -> str:
        """ dump the data to csv """
        return f"id,Title,Publish,DaysSincePublish,Date,Impressions,Engagement(min)"