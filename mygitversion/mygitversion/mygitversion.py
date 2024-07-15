import click

# convert main function as CLI using #click.xxx
#@click.command()
@click.group()
@click.version_option('0.0.1',prog_name='mygitversion')
def cli():
    pass

@cli.command()
def init():
    """Create an empty mygitversion repository"""
    pass

@cli.command()
def status():
    """Show the working tree status"""
    pass

@cli.command()
def add():
    """Add file contents to the index"""
    pass

@cli.command()
def commit():
    """Record changes to the repository"""
    pass


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

if __name__ == '__main__':
    cli()