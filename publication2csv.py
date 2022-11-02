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
    "--date-to",
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
def main(publication_name, folder, sid, uid, start, stop):
    """
    Simple CLI for getting the stats of a medium post
    """

    print(f"Config publication: {Config.PUBLICATION}")
    print(f"Config sid: {Config.SID}")
    print(f"Config uid: {Config.UID}")

    sid = Config.SID if sid == "" else sid
    uid = Config.UID if uid == "" else uid
    folder = Config.OUTPUT if folder == "" else folder

    date_to = date.now() if date_from == "" else start
    date_from = (date_to - timedelta(days=30)) if stop == "" else stop

    now = None
    allready_utc = False

    # click.echo("Getting publication: " + publication_name)
    # click.echo("Start date: " + str(start))
    # click.echo("Stop date: " + str(stop))
    # click.echo("Session id: " + sid)
    # click.echo("User id: " + uid)

    publication = PublicationStats(
        publication_name, sid, uid, date_from, date_to, now, allready_utc
    )

    click.echo("Getting story summary")
    csv = publication.get_story_stats_csv()
    filename = f"{publication_name}_{start.strftime('%Y%m%d')}_{stop.strftime('%Y%m%d')}_story.csv"
    with open(f"{folder}/{filename}", "w") as file:
        for line in csv:
            file.write(f"{line}\n")

    click.echo("Getting publication views")
    pub_views = publication.get_publication_views()
    print(f"Publication views: {pub_views}")

    click.echo("Getting publication visitors")
    pub_visitors = publication.get_publication_visitors()
    print(f"Publication visitors: {pub_visitors}")

    click.echo("Getting article events")
    article_events = publication.get_article_events()
    print(f"Article events: {article_events}")

    click.echo("Getting article referrers")
    article_referrers = publication.get_article_referrers()
    print(f"Article referrers: {article_referrers}")


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
