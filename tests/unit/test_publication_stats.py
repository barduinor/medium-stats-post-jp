"""Unit tests for the publication stats class."""

from scrapper import PublicationStats
from config import Config
from datetime import datetime, timedelta, date


def test_publication_stats_object_get() -> PublicationStats:
    """Should return the publication stats object"""
    pub_name = Config.PUBLICATION
    pub_sid = Config.SID
    pub_uid = Config.UID
    date_to = datetime.today()
    date_from = date_to - timedelta(days=2000)

    # should return an object of type PublicationStats
    publication = PublicationStats(pub_name, pub_sid, pub_uid, date_from, date_to, None)
    assert publication is not None
    assert type(publication) == PublicationStats

    return publication


def test_stories_summary():
    """
    Should return the stories summary
    converting the dates from unix to iso format
    with output in csv format
    """

    publication = test_publication_stats_object_get()

    # Stories Summary
    # should return the publication summary stats json object
    story_stats = publication.get_story_stats()
    story_stats = list(story_stats.values())
    assert story_stats is not None
    assert story_stats[0]["type"] == "PostStat"

    # Should have converted dates from unix to iso
    created = datetime.fromisoformat(story_stats[0]["createdAt"])
    published = datetime.fromisoformat(story_stats[0]["firstPublishedAt"])
    assert type(created) is datetime
    assert type(published) is datetime

    # Should include the days since publication
    for i in range(10):
        assert story_stats[i]["daysSincePublished"] >= 0

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
        + "type,"
        + "daysSincePublished"
    )
    assert line_1st != header
    assert line_nth != header


def test_aggregate_events_views():
    """
    Should return publication aggregate events views
    using iso dates
    using read time in minutes
    # in csv format
    """
    publication = test_publication_stats_object_get()

    # Aggregate Events Views
    # Should return publication views
    pub_views = publication.get_publication_views()
    assert pub_views is not None
    assert len(pub_views) > 0  # should have at least one view

    # Should return the date in iso format
    timeWindowStart = datetime.fromisoformat(pub_views[0]["timeWindowStart"])
    assert type(timeWindowStart) is datetime

    # Should return the read time in seconds
    ttrMs = pub_views[0]["ttrMs"]
    assert type(ttrMs) is float


def test_aggregate_events_visitors():
    """
    Should return publication aggregate events visitors
    using iso dates
    using read time in minutes
    # in csv format
    """
    publication = test_publication_stats_object_get()

    # Aggregate Events Visitors
    # Should return publication visitors
    pub_visitors = publication.get_publication_visitors()
    assert pub_visitors is not None
    assert len(pub_visitors) > 0  # should have at least one visitor

    # Should return the date in iso format
    timeWindowStart = datetime.fromisoformat(pub_visitors[0]["timeWindowStart"])
    assert type(timeWindowStart) is datetime


def test_aggregate_events_csv():
    """Should output both aggregate views (views+visitors) in csv format"""

    publication = test_publication_stats_object_get()

    csv = publication.get_aggregate_events_csv()
    header = csv[0]
    line_1st = csv[1]
    line_nth = csv[-1]

    assert header == "timeWindowStart,views,ttr,dailyUniqueVisitors"
    assert line_1st != header
    assert line_nth != header


def test_post_events():
    """
    Should return article/post events
    using iso dates
    using read time in minutes
    # in csv format
    """
    publication = test_publication_stats_object_get()

    # should return article/post events
    article_events = publication.get_article_events()
    assert article_events is not None
    assert len(article_events) > 0  # should have at least one article

    # Should return the date in iso format
    periodStartedAt = datetime.fromisoformat(
        article_events["data"]["post"][0]["dailyStats"][0]["periodStartedAt"]
    )
    assert type(periodStartedAt) is datetime

    # Should return the read time in seconds
    memberTtr = article_events["data"]["post"][0]["dailyStats"][0]["memberTtr"]
    assert type(memberTtr) is float

    # Should return the days since publication
    for i in range(10):
        assert (
            article_events["data"]["post"][i]["dailyStats"][0]["daysSincePublished"]
            >= -1
        )

    # Should return the title of the article
    assert article_events["data"]["post"][0]["title"] is not None

    # Should return the creator id of the article
    assert article_events["data"]["post"][0]["creatorId"] is not None

    # Should return article/post events in csv format
    csv = publication.get_article_events_csv()
    header = csv[0]
    line_1st = csv[1]
    line_nth = csv[-1]

    assert (
        header
        == "periodStartedAt,views,internalReferrerViews,memberTtr,id,daysSincePublished,title,creatorId"
    )
    assert line_1st != header
    assert line_nth != header


def test_post_referrers():
    """
    Should return article/post referrers
    using iso dates
    using read time in minutes
    # in csv format
    """
    publication = test_publication_stats_object_get()

    # should return article referrers
    article_referrers = publication.get_article_referrers()
    assert article_referrers is not None
    assert len(article_referrers) > 0  # should have at least one article

    # Should return the title of the article
    assert article_referrers["data"]["post"][0]["title"] is not None

    # Should return the creator id of the article
    assert article_referrers["data"]["post"][0]["creatorId"] is not None

    # Should return article/post referrers in csv format
    csv = publication.get_article_referrers_csv()
    header = csv[0]
    line_1st = csv[1]
    line_nth = csv[-1]

    assert (
        header
        == "postId,sourceIdentifier,totalCount,type,internal,search,site,platform,internal.postId,internal.collectionId,internal.profileId,internal.type,site.href,site.title,search.domain,search.keywords,title,creatorId"
    )
    assert line_1st != header
    assert line_nth != header
