import configparser
import datetime
import hashlib
import os
import shutil
import click
import yaml
import json

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

# Status
# Scan files for modified time
def scan_files(myfiles):
    timestamp = os.stat(myfiles).st_mtime
    return timestamp


def log_modification(directory="."):
    result = dict(
        [
            (f, scan_files(f))
            for f in ignore_core_files(mygitversionignore_file_filter(directory))
        ]
    )
    return result


def save_to_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def load_from_file(filename):
    with open(filename) as f:
        data = json.load(f)
        f.close()
    return data


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    unchanged = set(o for o in shared_keys if d1[o] == d2[o])
    return {
        "Added": list(added),
        "Removed": list(removed),
        "Modified": list(modified.keys()),
        "Untracked": list(unchanged),
    }


def scan_working_tree(directory=".", before=".mygitversion/before_logs.json"):
    """
    scan files
    log modification
    save to json file for current scan
    read from previous file :before_json
    compare previous and current files
    """
    try:
        if os.path.isfile(before):
            current_stats = log_modification(directory)
            before_stats = load_from_file(before)
            data = dict_compare(before_stats, current_stats)
            print(yaml.dump(data, default_flow_style=False))
        else:
            current_stats = log_modification(directory)
            save_to_file(".mygitversion/before_logs.json", current_stats)
            before_stats = load_from_file(before)
            data = dict_compare(before_stats, current_stats)
            print(yaml.dump(data, default_flow_style=False))

    except Exception as e:
        raise e


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
    #ignore_files = [f for f in files if not f.startswith("mygitversion")]
    #return ignore_files
    return files

def read_log_file():
    path_to_commit_msg = ".mygitversion/COMMIT_MSG"
    with open(path_to_commit_msg, "r+") as f:
        result = f.read()
    return result

# Push
def push_file_to_remote(source, destination = ".mygitversion/remote"):
    try:
        shutil.copy(source, destination)
        print(": Pushing Files To Remote")
    except:
        shutil.copytree(source, destination, dirs_exist_ok=True)
        print(": Pushing Directories To Remote")
