"""Unit tests for the publication stats class."""

from scrapper import PublicationStats
from config import Config
from datetime import datetime, timedelta


def test_publication_story():
    """Test the publication class object."""
    pub_name = Config.PUBLICATION
    pub_sid = Config.SID
    pub_uid = Config.UID
    date_to = datetime.today()
    date_from = date_to - timedelta(days=10)

    # should return an object of type PublicationStats
    publication = PublicationStats(pub_name, pub_sid, pub_uid, date_from, date_to, None)
    assert publication is not None
    assert type(publication) == PublicationStats

    # should return the publication summary stats json object
    story_stats = publication.get_story_stats()
    assert story_stats is not None
    assert story_stats[0]["type"] == "PostStat"

    # Should have converted dates from unix to iso
    try:
        created = datetime.fromisoformat(story_stats[0]["createdAt"])
        published = datetime.fromisoformat(story_stats[0]["firstPublishedAt"])
        assert type(created) is datetime
        assert type(published) is datetime
    except ValueError:
        assert False

    # Should return data in csv format
    csv = publication.get_story_stats_csv()

    header = csv[0]
    line_1st = csv[1]
    line_nth = csv[-1]

    assert header == (
        "postId,"
        + "slug,"
        # + "previewImage,"
        + "title,"
        + "creatorId,"
        + "collectionId,"
        + "upvotes,"
        + "views,"
        + "reads,"
        + "createdAt,"
        + "firstPublishedAt,"
        + "visibility,"
        + "firstPublishedAtBucket,"
        + "readingTime,"
        + "syndicatedViews,"
        + "claps,"
        + "updateNotificationSubscribers,"
        + "isSeries,"
        + "internalReferrerViews,"
        + "friendsLinkViews,"
        # + "primaryTopic,"+
        + "type"
    )
    assert line_1st != header
    assert line_nth != header

    # Aggregate Events Views
    # Should return publication views
    pub_views = publication.get_publication_views()
    assert pub_views is not None
    assert len(pub_views) > 0  # should have at least one view

    # Aggregate Events Visitors
    # Should return publication visitors
    pub_visitors = publication.get_publication_visitors()
    assert pub_visitors is not None
    assert len(pub_visitors) > 0  # should have at least one visitor

    # should return article events
    article_events = publication.get_article_events()
    assert article_events is not None

    # should return article referrers
    article_referrers = publication.get_article_referrers()
    assert article_referrers is not None
