""" test scraper for publication stats """

from config import Config

def test_publication_stats2csv():
    """ test the get_publication_stats function """
    from datetime import datetime, timedelta
    from scrapper_summary import get_publication_stats, publication_stats_to_csv
    start = datetime.today()
    stop = start - timedelta(days=1)
    publication_name = Config.PUBLICATION

    # get publication stats json
    publication_stats = get_publication_stats(publication_name, start, stop)
    assert publication_stats is not None

    # get publication stats csv
    csv = publication_stats_to_csv(publication_name, publication_stats)
    assert csv is not None


    

