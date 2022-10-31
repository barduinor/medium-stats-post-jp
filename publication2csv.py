""" processor for medium stats post """

import click

@click.group()
def main():
    """
    Simple CLI for getting the stats of a medium post
    """
    pass

@main.command()
@click.argument('publication', type=str, required=True)
def summary(publication):
    """ Capture the publication stories summary"""

    click.echo(f'Getting stories summary for {publication}')


if __name__ == "__main__":
    # main()
    main(['summary', 'box-developer-blog'])
