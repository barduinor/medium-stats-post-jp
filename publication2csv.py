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
    default=str(date.today() - timedelta(days=30)),
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
    filename = f"{publication_name}_{date_from.strftime('%Y%m%d')}_{date_to.strftime('%Y%m%d')}_story.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    # click.echo("Getting publication views")
    # pub_views = publication.get_publication_views()

    # click.echo("Getting publication visitors")
    # pub_visitors = publication.get_publication_visitors()

    click.echo("Getting publication events")
    csv = publication.get_aggregate_events_csv()
    filename = f"{publication_name}_{date_from.strftime('%Y%m%d')}_{date_to.strftime('%Y%m%d')}_events.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    click.echo("Getting article events")
    csv = publication.get_article_events_csv()
    filename = f"{publication_name}_{date_from.strftime('%Y%m%d')}_{date_to.strftime('%Y%m%d')}_article_events.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    click.echo("Getting article referrers")
    csv = publication.get_article_referrers_csv()
    filename = f"{publication_name}_{date_from.strftime('%Y%m%d')}_{date_to.strftime('%Y%m%d')}_article_referrers.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")


if __name__ == "__main__":
    # main()
    # main(["box-developer-blog"])
    main(
        [
            "box-developer-blog",
            "--sid",
            "1:HcNhNqsCQtMb98qgTELLbkvPsJe8u1XfLTx83ajIfdi0KzSQwJ9/ilSgHalk8GWF",
            "--uid",
            "19badb385e7",
        ]
    )
