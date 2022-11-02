""" medium screper methods"""

from datetime import datetime
from medium_stats.scraper import StatGrabberPublication
from datetime import datetime
from pandas import DataFrame
from requests import HTTPError


class PublicationStats(object):
    """Handles the publication stats:
    - get the stats from the medium api
    - holds json data
    - exports to csv
    """

    story_columns = [
        "postId",
        "slug",
        # "previewImage",
        "title",
        "creatorId",
        "collectionId",
        "upvotes",
        "views",
        "reads",
        "createdAt",
        "firstPublishedAt",
        "visibility",
        "firstPublishedAtBucket",
        "readingTime",
        "syndicatedViews",
        "claps",
        "updateNotificationSubscribers",
        "isSeries",
        "internalReferrerViews",
        "friendsLinkViews",
        # "primaryTopic",
        "type",
    ]

    story_stats: dict = None
    view_stats: dict = None
    visitor_stats: dict = None
    article_list: list = None
    article_events: dict = None
    article_referrers: dict = None
    publication: StatGrabberPublication = None

    def __init__(
        self,
        publication_name: str,
        sid: str,
        uid: str,
        date_from: datetime,
        date_to: datetime,
        now: datetime | None,
        already_utc=False,
    ):
        self.publication_name = publication_name
        self.sid = sid
        self.uid = uid
        self.date_from = date_from
        self.date_to = date_to
        self.now = now
        self.already_utc = already_utc
        self._load_stat_grabber()

    def _load_stat_grabber(self):
        """Load the stat grabber"""

        if self.sid is None or self.uid is None or self.publication_name is None:
            raise Exception("publication name, sid and uid are required")
        self.publication = StatGrabberPublication(
            slug=self.publication_name,
            sid=self.sid,
            uid=self.uid,
            start=self.date_from,
            stop=self.date_to,
            now=self.now,
            already_utc=self.already_utc,
        )

    def _load_story_stats(self):
        """Load the story stats"""
        self.story_stats = self.publication.get_all_story_overview()
        self._fix_story_stats_dates()

    def _fix_story_stats_dates(self):
        """Convert the dates in the story stats from unix to iso"""
        for story in self.story_stats:
            story["createdAt"] = datetime.fromtimestamp(
                story["createdAt"] // 1000
            ).isoformat()
            story["firstPublishedAt"] = datetime.fromtimestamp(
                story["firstPublishedAt"] // 1000
            ).isoformat()

    def _load_view_stats(self):
        """Load the view stats"""
        self.view_stats = self.publication.get_events(type_="views")

    def _load_visitor_stats(self):
        """Load the visitor stats"""
        self.visitor_stats = self.publication.get_events(type_="visitors")

    def _load_article_events(self):
        """Load the article events"""

        self.article_list = self.publication.get_article_ids(self.story_stats)
        self.article_events = self.publication.get_all_story_stats(self.article_list)

    def _load_article_referrers(self):
        """Load the article referrers"""

        self.article_list = self.publication.get_article_ids(self.story_stats)
        # "type" param must be either "view_read" or "referrer"')
        self.article_referrers = self.publication.get_all_story_stats(
            self.article_list, type_="referrer"
        )

    def get_story_stats(self) -> dict:
        """return the publication stats json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()

        return self.story_stats

    def get_story_stats_csv(self) -> list:
        """return the publication stats csv object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()

        # convert the json to a dataframe
        # data frame is a bit overkill for this, but others have more complex json
        # and this is a good way to keep it consistent
        df = DataFrame(self.story_stats)

        # convert the dataframe to csv
        csv_str = df.to_csv(index=False, header=True, columns=self.story_columns)
        csv = csv_str.splitlines()
        return csv

    def get_publication_views(self) -> dict:
        """return the publication views json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.view_stats is None:
            self._load_view_stats()

        return self.view_stats

    def get_publication_visitors(self) -> dict:
        """return the publication visitors json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.visitor_stats is None:
            self._load_visitor_stats()

        return self.visitor_stats

    def get_article_events(self):
        """return the article events json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()
        if self.article_events is None:
            self._load_article_events()

        return self.article_events

    def get_article_referrers(self):
        """return the article referrers json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()
        if self.article_referrers is None:
            self._load_article_referrers()

        return self.article_referrers
