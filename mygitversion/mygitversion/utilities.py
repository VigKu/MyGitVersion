import os
import click

def touch(path):
    """Create file
    """
    with open(path, "a"):
        os.utime(path,None)
        
def intialize_for_mygitversion():
    try:
        base_dir = ".mygitversion/local"
        base_remote_dir = ".mygitversion/remote"
        os.makedirs(base_dir)
        os.makedirs(base_remote_dir)
        mygitversion_basic_files = ["config", "index", "logs", "COMMIT_MSG"]
        for file in mygitversion_basic_files:
            touch(f".mygitversion/{file}")
        click.secho("Initialized Directory", fg="cyan")
        click.secho("Please configure user with 'mygitversion config user.name YOURNAME'", fg="yellow")
             
    except FileExistsError as e:
        click.secho("Directory already initialized", fg="cyan")
        click.secho("ReInitializing Directory", fg="cyan")