""" medium screper methods"""

from datetime import datetime, date
from medium_stats.scraper import StatGrabberPublication
from pandas import DataFrame, json_normalize
from otosky import build_summary_stats_payload, build_blog_events_payload


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
        "title",
        "creatorId",
        "firstPublishedAt",
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
        "title",
        "creatorId",
        "firstPublishedAt",
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
    # Blog Stats
    blog_stats_viewers_readers: dict = None

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
        # story_stats_list = self.publication.get_all_story_overview()

        # get summary stats for all publication articles
        gql_endpoint = "https://medium.com/_/graphql"
        payload = build_summary_stats_payload(self.publication.id)
        response = self.publication.session.post(gql_endpoint, json=payload)
        response.raise_for_status()
        story_stats_list = response.json()

        # Convert the list to a dict indexed by the post id
        self.story_stats = dict()
        for story in story_stats_list["data"]["publication"][
            "publicationPostsConnection"
        ]["edges"]:
            post_id = story["node"]["id"]
            self.story_stats[post_id] = {}
            # Map to columns format
            self.story_stats[post_id]["postId"] = post_id
            self.story_stats[post_id]["slug"] = story.get("node").get("uniqueSlug")
            # # self.story_stats[post_id]["previewImage"] =
            self.story_stats[post_id]["title"] = story["node"]["title"]
            self.story_stats[post_id]["creatorId"] = story["node"]["creator"]["id"]
            self.story_stats[post_id]["collectionId"] = story["node"]["collection"][
                "id"
            ]
            self.story_stats[post_id]["upvotes"] = 0
            self.story_stats[post_id]["views"] = story["node"]["totalStats"]["views"]
            self.story_stats[post_id]["reads"] = story["node"]["totalStats"]["reads"]
            self.story_stats[post_id]["createdAt"] = story["listedAt"]
            self.story_stats[post_id]["firstPublishedAt"] = story["node"][
                "firstPublishedAt"
            ]
            self.story_stats[post_id]["visibility"] = story["node"]["visibility"]
            self.story_stats[post_id]["firstPublishedAtBucket"] = story["node"][
                "firstPublishedAt"
            ]
            self.story_stats[post_id]["readingTime"] = story["node"]["readingTime"]
            self.story_stats[post_id]["syndicatedViews"] = 0
            self.story_stats[post_id]["claps"] = 0
            self.story_stats[post_id]["updateNotificationSubscribers"] = 0
            self.story_stats[post_id]["isSeries"] = story["node"]["isSeries"]
            self.story_stats[post_id]["internalReferrerViews"] = 0
            self.story_stats[post_id]["friendsLinkViews"] = 0
            # # self.story_stats[post_id]["primaryTopic"] =
            self.story_stats[post_id]["type"] = "PostStat"
            self.story_stats[post_id]["daysSincePublished"] = 0

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

    def _load_blog_stats_viewer_readers(self):
        """Load the view stats"""
        # get summary stats for all publication articles
        gql_endpoint = "https://medium.com/_/graphql"
        payload = build_blog_events_payload(
            self.publication.id, self.date_from, self.date_to
        )
        response = self.publication.session.post(gql_endpoint, json=payload)
        response.raise_for_status()
        view_stats_list = response.json()

        self.blog_stats_viewers_readers = dict()
        for day in view_stats_list["data"]["publicationAggregateStats"]["points"]:
            timeWindowStart = datetime.fromtimestamp(
                day["timestamp"] / 1000
            ).isoformat()
            self.blog_stats_viewers_readers[timeWindowStart] = {
                "viewers": day["stats"]["total"]["viewers"],
                "readers": day["stats"]["total"]["readers"],
            }

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
        self._add_days_since_published_to_article_events()
        self._add_title_to_article_events()
        self._add_creator_to_article_events()
        self._add_date_published_to_article_events()

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

    def _add_days_since_published_to_article_events(self):
        """Add the days since published to the article events"""

        for post in self.article_events["data"]["post"]:
            # claculate how old was the article on the date this was collected
            publish_date = datetime.fromisoformat(
                self.story_stats[post["id"]]["firstPublishedAt"]
            )
            for daily_stat in post["dailyStats"]:
                post_date = datetime.fromisoformat(daily_stat["periodStartedAt"])
                days_since_published = (
                    (post_date - publish_date).days if post_date > publish_date else 0
                )
                daily_stat["daysSincePublished"] = days_since_published

    def _add_title_to_article_events(self):
        """Add the title to the article events"""

        for post in self.article_events["data"]["post"]:
            # get date from story stats
            post["title"] = self.story_stats[post["id"]]["title"]

    def _add_creator_to_article_events(self):
        """Add the creator to the article events"""

        for post in self.article_events["data"]["post"]:
            # get date from story stats
            post["creatorId"] = self.story_stats[post["id"]]["creatorId"]

    def _add_date_published_to_article_events(self):
        """Add the first published at to the article events"""

        for post in self.article_events["data"]["post"]:
            # get date from story stats
            post["firstPublishedAt"] = self.story_stats[post["id"]]["firstPublishedAt"]

    def _load_article_referrers(self):
        """Load the article referrers"""

        # self.article_list = self.publication.get_article_ids(self.story_stats)
        # "type" param must be either "view_read" or "referrer"')
        self.article_referrers = self.publication.get_all_story_stats(
            self.story_stats.keys(), type_="referrer"
        )
        self._add_creator_to_referrers()
        self._add_publish_date_to_referrers()

    def _add_creator_to_referrers(self):
        """Add the creator to the referrers"""

        for post in self.article_referrers["data"]["post"]:
            # get date from story stats
            post["creatorId"] = self.story_stats[post["id"]]["creatorId"]

    def _add_publish_date_to_referrers(self):
        """Add the first published at to the referrers"""

        for post in self.article_referrers["data"]["post"]:
            # get date from story stats
            post["firstPublishedAt"] = self.story_stats[post["id"]]["firstPublishedAt"]

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
        if self.blog_stats_viewers_readers is None:
            self._load_blog_stats_viewer_readers()
        # if self.visitor_stats is None:
        #     self._load_visitor_stats()
        # if self.article_events is None:
        #     self._load_publication_events()

        # convert the json to a dataframe
        # df = json_normalize(
        #     self.publication_events,
        # )

        # # convert the dataframe to csv
        # csv_str = df.to_csv(index=False, header=True)
        # csv = csv_str.splitlines()

        csv = []
        header = "timeWindowStart,viewers,readers"
        csv.append(header)
        for key, value in self.blog_stats_viewers_readers.items():
            event_date = key
            viewers = value["viewers"] if "viewers" in value else 0
            readers = value["readers"] if "readers" in value else 0
            # daily_unique_visitors = (
            #     value["dailyUniqueVisitors"] if "dailyUniqueVisitors" in value else ""
            # )
            csv.append(f"{event_date},{viewers},{readers}")

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
            meta=["id", "title", "creatorId", "firstPublishedAt"],
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
            meta=["title", "creatorId", "firstPublishedAt"],
            errors="ignore",
        )

        csv_str = df.to_csv(
            index=False,
            header=True,
            columns=self.referrer_columns,
        )
        csv = csv_str.splitlines()
        return csv
