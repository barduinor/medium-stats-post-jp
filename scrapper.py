""" medium screper methods"""

from datetime import datetime, date
from medium_stats.scraper import StatGrabberPublication
from datetime import datetime
from pandas import DataFrame, json_normalize
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
        "daysSincePublished",
    ]

    referrer_columns = [
        # 'postId,sourceIdentifier,totalCount,type,internal,search,site,platform,
        # __typename,internal.postId,internal.collectionId,internal.profileId,
        # internal.type,internal.__typename,site.href,site.title,site.__typename,
        # search.domain,search.keywords,search.__typename'
        "postId",
        "sourceIdentifier",
        "totalCount",
        "type",
        "internal",
        "search",
        "site",
        "platform",
        # "__typename",
        "internal.postId",
        "internal.collectionId",
        "internal.profileId",
        "internal.type",
        # "internal.__typename",
        "site.href",
        "site.title",
        # "site.__typename",
        "search.domain",
        "search.keywords",
        # "search.__typename",
        # "title",
    ]

    article_event_columns = [
        # 'periodStartedAt,views,internalReferrerViews,memberTtr,id'
        "periodStartedAt",
        "views",
        "internalReferrerViews",
        "memberTtr",
        # "__typename",
        "id",
        "daysSincePublished",
    ]

    publication: StatGrabberPublication = None
    # article_list: list = None

    # Stories Summary
    story_stats: dict = None
    # Aggregate Events
    view_stats: dict = None
    visitor_stats: dict = None
    publication_events: dict = None
    # Post Events
    article_events: dict = None
    # Post Referrers
    article_referrers: dict = None

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
        story_stats_list = self.publication.get_all_story_overview()

        # Convert the list to a dict indexed by the post id
        self.story_stats = dict()
        for story in story_stats_list:
            post_id = story["postId"]
            self.story_stats[post_id] = story
        self._fix_story_stats_dates()
        self._add_days_since_published_to_story_stats()

    def _fix_story_stats_dates(self):
        """Convert the dates in the story stats from unix to iso"""
        for story in self.story_stats.values():
            story["createdAt"] = datetime.fromtimestamp(
                story["createdAt"] // 1000
            ).isoformat()
            story["firstPublishedAt"] = datetime.fromtimestamp(
                story["firstPublishedAt"] // 1000
            ).isoformat()

    def _add_days_since_published_to_story_stats(self):
        """Add the days since published to the story stats"""
        for story in self.story_stats.values():
            story["daysSincePublished"] = (
                date.today() - datetime.fromisoformat(story["firstPublishedAt"]).date()
            ).days

    def _load_view_stats(self):
        """Load the view stats"""
        self.view_stats = self.publication.get_events(type_="views")
        self._fix_view_stats_dates()
        self._fix_view_stats_read_time()

    def _fix_view_stats_dates(self):
        """Convert the dates in the view stats from unix to iso"""
        for view in self.view_stats:
            view["timeWindowStart"] = datetime.fromtimestamp(
                view["timeWindowStart"] // 1000
            ).isoformat()

    def _fix_view_stats_read_time(self):
        """Convert the read time in the view stats from milliseconds to seconds"""
        for view in self.view_stats:
            view["ttrMs"] = view["ttrMs"] / 1000.0

    def _load_visitor_stats(self):
        """Load the visitor stats"""
        self.visitor_stats = self.publication.get_events(type_="visitors")
        self._fix_visitor_stats_dates()

    def _fix_visitor_stats_dates(self):
        """Convert the dates in the visitor stats from unix to iso"""
        for visitor in self.visitor_stats:
            visitor["timeWindowStart"] = datetime.fromtimestamp(
                visitor["timeWindowStart"] // 1000
            ).isoformat()

    def _load_article_events(self):
        """Load the article events"""

        # self.article_list = self.publication.get_article_ids(self.story_stats.values())
        self.article_events = self.publication.get_all_story_stats(
            self.story_stats.keys()
        )
        self._fix_article_events_dates()
        self._fix_article_events_read_time()
        self._add_days_since_published()

    def _fix_article_events_dates(self):
        """Convert the dates in the article events from unix to iso"""
        for post in self.article_events["data"]["post"]:
            for event in post["dailyStats"]:
                event["periodStartedAt"] = datetime.fromtimestamp(
                    event["periodStartedAt"] // 1000
                ).isoformat()

    def _fix_article_events_read_time(self):
        """Convert the read time in the article events from milliseconds to seconds"""
        for post in self.article_events["data"]["post"]:
            for event in post["dailyStats"]:
                event["memberTtr"] = event["memberTtr"] / 1000.0

    def _add_days_since_published(self):
        """Add the days since published to the article events"""

        for post in self.article_events["data"]["post"]:
            # get date from story stats
            post["daysSincePublished"] = self.story_stats[post["id"]][
                "daysSincePublished"
            ]

    def _load_article_referrers(self):
        """Load the article referrers"""

        # self.article_list = self.publication.get_article_ids(self.story_stats)
        # "type" param must be either "view_read" or "referrer"')
        self.article_referrers = self.publication.get_all_story_stats(
            self.story_stats.keys(), type_="referrer"
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
        df = DataFrame(self.story_stats.values())

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

    def _load_publication_events(self):
        """Load the publication events"""

        # create new json object mashing views and visitors together
        self.publication_events = dict()

        # get the views
        for view in self.view_stats:
            self.publication_events[view["timeWindowStart"]] = {
                "views": view["views"],
                "ttr": view["ttrMs"],
            }

        # mash up the visitors
        for visitor in self.visitor_stats:
            if visitor["timeWindowStart"] in self.publication_events:
                self.publication_events[visitor["timeWindowStart"]][
                    "dailyUniqueVisitors"
                ] = visitor["dailyUniqueVisitors"]
            else:
                self.publication_events[visitor["timeWindowStart"]] = {
                    "dailyUniqueVisitors": visitor["dailyUniqueVisitors"]
                }

    def get_aggregate_events_csv(self) -> dict:
        """return the publication aggregate events csv object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.view_stats is None:
            self._load_view_stats()
        if self.visitor_stats is None:
            self._load_visitor_stats()
        if self.article_events is None:
            self._load_publication_events()

        # convert the json to a dataframe
        # df = json_normalize(
        #     self.publication_events,
        # )

        # # convert the dataframe to csv
        # csv_str = df.to_csv(index=False, header=True)
        # csv = csv_str.splitlines()

        csv = []
        header = "timeWindowStart,views,ttr,dailyUniqueVisitors"
        csv.append(header)
        for key, value in self.publication_events.items():
            event_date = key
            views = value["views"] if "views" in value else 0
            ttr = value["ttr"] if "ttr" in value else 0
            daily_unique_visitors = (
                value["dailyUniqueVisitors"] if "dailyUniqueVisitors" in value else ""
            )
            csv.append(f"{event_date},{views},{ttr},{daily_unique_visitors}")

        return csv

    def get_article_events(self):
        """return the article events json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()
        if self.article_events is None:
            self._load_article_events()

        return self.article_events

    def get_article_events_csv(self):
        """return the article events csv object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()
        if self.article_events is None:
            self._load_article_events()

        # convert the json to csv

        df = json_normalize(
            self.article_events["data"]["post"],
            record_path=["dailyStats"],
            meta=["id", "daysSincePublished"],
        )

        csv_str = df.to_csv(
            index=False,
            header=True,
            columns=self.article_event_columns,
        )
        csv = csv_str.splitlines()
        return csv

    def get_article_referrers(self):
        """return the article referrers json object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()
        if self.article_referrers is None:
            self._load_article_referrers()

        return self.article_referrers

    def get_article_referrers_csv(self):
        """return the article referrers csv object"""
        if self.publication is None:
            self._load_stat_grabber()
        if self.story_stats is None:
            self._load_story_stats()
        if self.article_referrers is None:
            self._load_article_referrers()

        df = json_normalize(
            self.article_referrers["data"]["post"],
            record_path=["referrers"],
            # meta=["title"],
            errors="ignore",
        )

        csv_str = df.to_csv(
            index=False,
            header=True,
            columns=self.referrer_columns,
        )
        csv = csv_str.splitlines()
        return csv
