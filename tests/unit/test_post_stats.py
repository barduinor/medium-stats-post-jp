from datetime import date
from stat_objects import Stats

def test_stats_object():
    """ test the stats object """
    stats = Stats()
    stats.load_file('tests/data/post-stats.json')
    stats.load_file('tests/data/daily-stats.json')
    assert stats.id == '2f12edf92a5c'
    assert stats.title == 'New Box App Center (formally App Gallery) Launch'
    assert stats.publishDate == date(2022, 4, 11) 
    assert stats.totalStats['views'] == 364
    assert stats.dailyStats is not None

def test_stats_object_output_data():
    """ test the stats object output """
    stats = Stats()
    stats.load_file('tests/data/post-stats.json')
    stats.load_file('tests/data/daily-stats.json')
    data = stats.dump_data()
    
    assert data[0] == '2f12edf92a5c,New Box App Center (formally App Gallery) Launch,2022-04-11,8,0'

def test_stats_object_output_header():
    """ test the stats object output """
    stats = Stats()
    stats.load_file('tests/data/post-stats.json')
    stats.load_file('tests/data/daily-stats.json')
    data = stats.dump_header()
    
    assert data == 'id,Title,Date,Impressions,Engagement(min)'

    