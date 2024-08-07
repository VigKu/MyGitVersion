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

from utilities import add_file_to_index_in_staging, commit_file_to_repo, download_file, ignore_core_files, intialize_for_mygitversion, mygitversionignore_file_filter, push_file_to_remote, read_log_file, read_username_from_config, remove_files, restore_file_from_local, save_file_to_repo, scan_working_tree

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
@click.argument("directory", default=".")
def status(directory):
    """Show the working tree status"""
    scan_working_tree(directory)


@cli.command()
@click.argument("files", nargs=-1)
def add(files):
    """Add file contents to the index"""
    for file in files:
        click.echo("Adding To Staging::{}".format(file))
        add_file_to_index_in_staging(file)

@cli.command()
@click.option('--message','-m',help='Provide commit message.')
def commit(message):
    """Record changes to the repository"""
    username = read_username_from_config("name")
    # MARKER = '# Everything below is ignored\n'
    # msg = click.edit('\n\n' + MARKER)
    # if msg is not None:
    #     return msg.split(MARKER, 1)[0].rstrip('\n')

    commit_file_to_repo(message, username)
    src_files = ignore_core_files(mygitversionignore_file_filter("."))

    with click.progressbar(src_files) as _files:
        for file in _files:
            save_file_to_repo(file)
        click.echo("Added Files to Local Repo")

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
@click.argument("src")
@click.argument("destination", required=False)
def clone(src, destination):
    """Clone a repository into a new directory"""
    download_file(src)

@cli.command()
def log():
    """Shows a Log history"""
    log_results = read_log_file()
    click.echo_via_pager(log_results)

@cli.command()
@click.argument("repository")
@click.argument("branch")
def push(repository, branch):
    """Update remote refs along with associated
    mygitversion push repo branch
    mygitversion push origin master

    """
    username = click.prompt("Username for https://mygithub.com")
    password = click.prompt(
        f"Password for https://{username}@mygithub.com", hide_input=True
    )
    src_files = ignore_core_files(mygitversionignore_file_filter(".mygitversion/local"))
    with click.progressbar(src_files) as _files:
        for file in _files:
            push_file_to_remote(file)
        click.echo("Push to Remote Repository")

@cli.command()
@click.argument("files", nargs=-1)
def rm(files):
    """Remove files from the working tree"""
    for file in files:
        remove_files(file)


@cli.command()
@click.argument("files", nargs=-1)
def restore(files):
    """Restore working tree files when deleted"""
    for file in files:
        restore_file_from_local(file)
        click.secho(f"Restored {file}", fg="cyan")


if __name__ == "__main__":
    cli()