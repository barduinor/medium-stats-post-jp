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
    publication: StatGrabberPublication = None

    def __init__(
        self,
        publication_name: str,
        sid: str,
        uid: str,
        start: datetime,
        stop: datetime,
        now: datetime | None,
        already_utc=False,
    ):
        self.publication_name = publication_name
        self.sid = sid
        self.uid = uid
        self.start = start
        self.stop = stop
        self.now = now
        self.already_utc = already_utc
        self._load_stat_grabber()

    def _load_stat_grabber(self):
        """Load the stat grabber"""
        # print(f"loading stat grabber for {self.publication_name}")
        # print(f"sid: {self.sid}")
        # print(f"uid: {self.uid}")
        if self.sid is None or self.uid is None or self.publication_name is None:
            raise Exception("publication name, sid and uid are required")
        self.publication = StatGrabberPublication(
            slug=self.publication_name,
            sid=self.sid,
            uid=self.uid,
            start=self.start,
            stop=self.stop,
            now=self.now,
            already_utc=self.already_utc,
        )
        # print(f"finished loading stat grabber for {self.publication.slug}")
        # print(f"sid: {self.publication.sid}")
        # print(f"uid: {self.publication.uid}")

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
