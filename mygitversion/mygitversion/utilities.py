import configparser
import datetime
import hashlib
import os
import shutil
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

def add_file_to_index_in_staging(filename):
    path = ".mygitversion/index"
    content = "{},{}\n".format(filename, datetime.datetime.now())
    with open(path, "a+") as f:
        f.write(content)

def read_username_from_config(key):
    app_dir = click.get_app_dir("mygitversion")
    cfg = os.path.join(app_dir, "config")
    config = configparser.ConfigParser()
    result = config.read(cfg)
    result_key = config.get("user", key)
    return result_key

# Commit
def generate_commit_hash(message):
    result = hashlib.md5(str(message).encode("utf-8")).hexdigest()
    return result


def commit_file_to_repo(message, username=None):
    path_to_commit_msg = ".mygitversion/COMMIT_MSG"
    hash_msg = generate_commit_hash(message)
    msg_format = f"""
	commit {hash_msg}
	Author: {username}
	Date:   {datetime.datetime.now()}

	    {message}

	"""
    print(msg_format)
    with open(path_to_commit_msg, "a+") as f:
        f.write(msg_format)


def save_file_to_repo(source):
    destination = ".mygitversion/local"
    try:
        shutil.copy(source, destination)
        print(": Adding Files")
    except:
        shutil.copytree(source, destination, dirs_exist_ok=True)
        print(": Adding Directories")

def mygitversionignore_file_filter(path):
    ignore_files = [f for f in os.listdir(path) if not f.startswith(".")]
    return ignore_files


def ignore_core_files(files):
    ignore_files = [f for f in files if not f.startswith("mygitversion")]
    return ignore_files

def read_log_file():
    path_to_commit_msg = ".mygitversion/COMMIT_MSG"
    with open(path_to_commit_msg, "r+") as f:
        result = f.read()
    return result
