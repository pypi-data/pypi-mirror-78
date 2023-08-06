import click
from rich import print
from rich.columns import Columns
from rich.table import Table
from gnote import util
import toml


# from gnote import note


@click.group()
def entry(version):
    """
    code-note
    代码笔记本，记录常用的代码例子，解释等
    """


@click.command()
def ls():
    lst = util.list_note().keys()
    t = Table('名称')
    for i in lst:
        t.add_row(i)
    print(t)


@click.command()
@click.argument('name', type=click.STRING, autocompletion=util.auto_complete)
def cat(name):
    md = util.cat(name)
    print(md)


@click.command()
@click.argument('name')
def search(name):
    lst = util.search(name)
    print(Columns(lst, expand=True))


@click.command()
@click.argument('name')
def pyvim(name):
    util.pyvim(name)


@click.command()
@click.argument('name')
def code(name):
    util.code(name)


@click.command()
def path():
    p = util.open_root_path()
    click.echo(str(p))


@click.command()
def push():
    util.push()


entry.add_command(ls)
entry.add_command(cat)
entry.add_command(search)
entry.add_command(pyvim)
entry.add_command(code)
entry.add_command(path)
