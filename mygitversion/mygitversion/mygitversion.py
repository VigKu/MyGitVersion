import click
import os
import configparser
import yaml
import datetime
import hashlib
import shutil
import json
import requests
#from click_help_colors import HelpColorsGroup,HelpColorsCommand
#from click_didyoumean import DYMGroup

from utilities import intialize_for_mygitversion

# convert main function as CLI using #click.xxx
#@click.command()
@click.group()
@click.version_option('0.0.1',prog_name='mygitversion')
def cli():
    pass

@cli.command()
def init():
    """Create an empty mygitversion repository"""
    intialize_for_mygitversion()

@cli.command()
def status():
    """Show the working tree status"""
    pass

@cli.command()
@click.argument("files", nargs=-1)
def add(files):
    """Add file contents to the index"""
    for file in files:
        click.echo("Adding To Staging::{}".format(file))
        add_file_to_index_in_staging(file)

@cli.command()
def commit():
    """Record changes to the repository"""
    pass

@cli.command()
@click.argument('key')
@click.argument('value')
def config(key, value):
    """Get and set repository or global options.

    mygitversion config user.name <name>

    """

    app_dir = click.get_app_dir("mygitversion")
    # app_dir = C:\Users\vigne\AppData\Roaming\mygitversion

    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    cfg = os.path.join(app_dir, "config")

    config = configparser.ConfigParser()
    config.read(cfg)
    section, key = key.split(".")
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)

    with open(cfg, "w") as configfile:
        config.write(configfile)

@cli.command()
def clone():
    """Clone a repository into a new directory"""
    pass

@cli.command()
def log():
    """Shows a Log history"""
    pass

@cli.command()
def push():
    """Update remote refs along with associated
    mygitversion push repo branch
    mygitversion push origin master
    """
    pass

@cli.command()
def rm():
    """Remove files from the working tree"""
    pass


@cli.command()
def restore():
    """Restore working tree files when deleted - undo"""
    pass


def add_file_to_index_in_staging(filename):
    path = ".mygitversion/index"
    content = "{},{}\n".format(filename, datetime.datetime.now())
    with open(path, "a+") as f:
        f.write(content)

if __name__ == "__main__":
    cli()