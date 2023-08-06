# from __future__ import unicode_literals

# import argparse
import platform
import os
import re
import sys
import errno
from shutil import copy2
 


CIO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILENAME = "clarisse.env"
PLATFORM = sys.platform

def main():
    sys.stdout.write("Running Clarisse post install script\n")

    if not PLATFORM in ["darwin", "win32", "linux"]:
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)
    transform_env_files()
    sys.stdout.write("Completed Clarisse post install script\n")

    sys.exit(0)


def transform_env_files():
    """Find env files below the Clarisse dir and add a Conductor location variable."""
    if PLATFORM == "darwin":
        root = os.path.expanduser(os.path.join("~","Library","Preferences","Isotropix","Clarisse"))
    elif PLATFORM == "linux":
        root = os.path.expanduser(os.path.join("~",".isotropix","clarisse"))
    else:  # windows
        appdata=os.environ.get("APPDATA")
        root = os.path.join(appdata, "Isotropix", "Clarisse")
    transform_tree(root)


def transform_tree(root):
    """Walk the filesystem and transform env files."""
    root, dirs, filenames = next(os.walk(root), (None,[], []))
    for fn in filenames:
        if fn == CONFIG_FILENAME:
            transform_env_file(os.path.join(root, fn))
    for dr in dirs:
        transform_tree(os.path.join(root, dr))

def transform_env_file(env_file):
    lines = []
    with open(env_file) as fn:
        for line in fn:
            if line.startswith("CIO_DIR"):
                lines.append("CIO_DIR={}".format(CIO_DIR))
            else:
                lines.append(line.rstrip())

    with open(env_file, "w") as fn:
        for line in lines:
            fn.write(u"{}\n".format(line))
    sys.stdout.write("Wrote Conductor additions to : {}\n".format(env_file))

if __name__ == '__main__':
    main()
