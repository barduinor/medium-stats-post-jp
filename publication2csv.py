""" processor for medium stats post """

import click
from config import Config
from scrapper import PublicationStats
from datetime import date, timedelta


@click.command()
@click.argument("publication_name", type=str, required=True)
@click.option(
    "--folder", type=str, default="output", help="folder to save the csv file"
)
@click.option("--sid", type=str, default="", help="your Medium session id from cookie")
@click.option("--uid", type=str, default="", help="your Medium user id from cookie")
@click.option(
    "--date_to",
    type=click.DateTime(["%Y-%m-%d"]),
    default=str(date.today()),
    help="from date in iso format",
)
@click.option(
    "--date_from",
    type=click.DateTime(["%Y-%m-%d"]),
    # default=str(date.today() - timedelta(days=90)),  # 90 days
    # default=str(date.today() - timedelta(days=365)),  # 1 year
    # default=str(date.today() - timedelta(days=1095)), # 3 years
    # default=str(date.today() - timedelta(days=1460)), # 4 years
    # default=str(date.today() - timedelta(days=1825)), # 5 years
    default=str(date.today() - timedelta(days=2190)),  # 6 years
    help="to date in iso format",
)
def main(publication_name, folder, sid, uid, date_from, date_to):
    """
    Simple CLI for getting the stats of a medium post
    """

    # print(f"Config publication: {Config.PUBLICATION}")
    # print(f"Config sid: {Config.SID}")
    # print(f"Config uid: {Config.UID}")

    sid = Config.SID if sid == "" else sid
    uid = Config.UID if uid == "" else uid
    folder = Config.OUTPUT if folder == "" else folder

    date_to = date.now() if date_from == "" else date_to
    date_from = (date_to - timedelta(days=30)) if date_from == "" else date_from

    now = None
    allready_utc = False

    click.echo("Getting publication: " + publication_name)
    click.echo("Start date: " + str(date_from))
    click.echo("Stop date: " + str(date_to))
    click.echo("Session id: " + sid)
    click.echo("User id: " + uid)

    publication = PublicationStats(
        publication_name, sid, uid, date_from, date_to, now, allready_utc
    )

    click.echo("Getting story summary")
    csv = publication.get_story_stats_csv()
    # filename = f"{publication_name}-story.csv"
    filename = f"{publication_name}-articles.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    # click.echo("Getting publication views")
    # pub_views = publication.get_publication_views()

    # click.echo("Getting publication visitors")
    # pub_visitors = publication.get_publication_visitors()

    click.echo("Getting publication stats viewers and readers")
    csv = publication.get_aggregate_events_csv()
    # filename = f"{publication_name}-stats_viewers_readers.csv"
    filename = f"{publication_name}-viewers-readers.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    click.echo("Getting article events")
    csv = publication.get_article_events_csv()
    filename = f"{publication_name}-article-events.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    click.echo("Article referrers are no longer available")
    # csv = publication.get_article_referrers_csv()
    # filename = f"{publication_name}-article_referrers.csv"
    # with open(f"{folder}/{filename}", "w") as file:
    #     for line in csv:
    #         file.write(f"{line}\n")


if __name__ == "__main__":
    # main()
    # main(["box-developer-blog"])
    main(
        [
            "box-developer-japan-blog",
            "--sid",
            # "1:6KArG9WeNRPNcb4rAgU3+FVPAE59/CuRgyi0sjm5HeaWBOuXIpr0pxXGxVX8ugrE",
            "1:NFak+3ufoBlzun9pllxb+jTuxIhLWaZyCDwuG895QLpsAGi7epKfgzZ2A2YglHDv",
            "--uid",
            # "19badb385e7",
            "19badb385e7",
        ]
    )


# Original
# [
#     "box-developer-blog",
#     "--sid",
#     "1:HcNhNqsCQtMb98qgTELLbkvPsJe8u1XfLTx83ajIfdi0KzSQwJ9/ilSgHalk8GWF",
#     "--uid",
#     "19badb385e7",
# ]


# new
# [
#     "box-developer-blog",
#     "--sid",
#     "1:6KArG9WeNRPNcb4rAgU3+FVPAE59/CuRgyi0sjm5HeaWBOuXIpr0pxXGxVX8ugrE",
#     "--uid",
#     "19badb385e7",
# ]
