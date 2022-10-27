""" processor for medium stats post """

import click

from files import files_read

__author__ = "RB"

@click.group()
def main():
    """
    Simple CLI for getting the stats of a medium post
    """
    pass

@main.command()
@click.option('--path',default='./files', help = 'path of the files to be scaned')
def scan(path):
    """ This function will scan the files in the given path
    and print the stats of the medium post"""
    click.echo(f'Scanning files in the path: {path}')
    files_read(path)


# @main.command()
# @click.argument('id')
# def get(id):
#     """This return a particular book from the given id on Google Books"""
#     url_format = 'https://www.googleapis.com/books/v1/volumes/{}'
#     click.echo(id)

#     response = requests.get(url_format.format(id))

#     click.echo(response.json())


if __name__ == "__main__":
    # main()
    main(['scan'])
