#!/usr/bin/env python

import gzip
from pathlib import Path
from plistlib import load
import os.path
import sys
import osxmetadata
import argparse

# from tqdm import tqdm

# TODO: option to add a tag (e.g. yep) on all files (and option to also tag files that don't have tags in yep)
# TODO: option to normalize tags (all lowercase, Mixed Case, etc)
# TODO: option to update or replace tags
# TODO: list tags
# TODO: test
# TODO: ignore tag
# TODO: replace instead of update

# path to default Yep plist file
_yepplist = "/Library/Application Support/Yep/docInfo.plist.gz"

# globals
_args = None

# custom argparse class to show help if error triggered
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def onError(e):
    if not os.path.exists(fname):
        sys.stderr.write("No such file: %s\n" % (fname,))
    else:
        sys.stderr.write(str(e) + "\n")


def process_arguments():
    global _args
    parser = MyParser(
        description="Add Yep tags and comments to files as OS X native tags & Finder comments",
        add_help=False,
    )
    parser.add_argument(
        "--plist", help=f"path to Yep plist file, will default to{_yepplist}"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="list files to be updated but do not actually udpate meta data",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        default=False,
        help="Show this help message",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Print verbose output during processing",
    )

    _args = parser.parse_args()
    # if no args, show help and exit
    if _args.help:
        parser.print_help(sys.stderr)
        sys.exit(1)

def main():
    global _args
    process_arguments()

    plistfile = _args.plist if _args.plist else str(Path.home()) + _yepplist
    plistfile = os.path.expanduser(plistfile)
    if not os.path.exists(plistfile):
        print(f"Could not find plist file: {plistfile}")
        sys.exit(1)

    with gzip.open(plistfile, "rb") as fp:
        pl = load(fp)

    total_items = len(pl["KPDocsInDB"])
    print(f"Found {total_items} items to process")
    items_processed = 0
    items_skipped = 0

    # for item in tqdm(pl['KPDocsInDB']):
    for item in pl["KPDocsInDB"]:

        fname = item["currentPath"]
        yep_tags = []
        yep_comment = None

        if "Keywords" in item:
            yep_tags = item["Keywords"]

        if "Subject" in item:
            yep_comment = item["Subject"]

        if not os.path.isfile(fname):
            print("Skipping: %s, does not appear to be a valid file name" % fname)
            items_skipped += 1
            continue

        try:
            md = osxmetadata.OSXMetaData(fname)
            if _args.verbose:
                print(fname)
            if yep_tags:
                yep_tags.append("yep")
                if _args.verbose:
                    print("yep_tags: %s" % ", ".join(yep_tags))
                md.tags.update(*yep_tags)
            if yep_comment:
                if _args.verbose:
                    print("yep_comment: %s" % yep_comment)
                md.finder_comment = yep_comment
            items_processed += 1
        except (IOError, OSError) as e:
            quit(onError(e))

    print(
        "Processed %d of %d files, skipped %d"
        % (items_processed, total_items, items_skipped)
    )


if __name__ == "__main__":
    main()
