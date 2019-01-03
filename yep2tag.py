#!/usr/bin/env python

"""
This script exports tags/keywords and comments managed by Ironic Software's
Yep application to native OS X tags & Finder comments
Tested with Yep version 1.8.0 See: http://www.ironicsoftware.com

Yep versions 1.x store metadata in a plist file.  This script reads the file and
exports the metadata to OX X tags (Yep tags) and Finder comments (Yep description),

Newer versions of Yep already store metadata using OS X extended attributes but 
I much preferred the interface of the "legacy" Yep app which aimed to be "iPhotos 
for PDFs."  If you use Yep 2.x+, you don't need this script.

I still use Yep 1.8.0 to manage many thousands of document but as an unsupported 32-bit app,
it's days are numbered (Yep 1.8.0 released ~2008).

This script future-proofs all the metadata I've got stored in Yep and makes Yep files
play well with the Finder & Spotlight.

I run the script with following options:
./yep2tag.py --lctags --overwritetags -q --addtag=yep

"""

import gzip
from pathlib import Path
from plistlib import load
import os.path
import sys
import argparse
from collections import Counter
import osxmetadata
from tqdm import tqdm

# TODO: ignore tag

# path to default Yep plist file
_yepplist = str(Path.home()) + "/Library/Application Support/Yep/docInfo.plist.gz"
DEBUG = False

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
        help="list files to be updated but do not actually udpate meta data, "
        + "most useful with --verbose",
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
    parser.add_argument(
        "--overwritetags",
        action="store_true",
        default=False,
        help="Overwrite tags when exporting metadata; default is to merge tags, "
        + "Finder comments are always overwritten with yep comments",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Be extra quiet when running. Doesn't print out messages about skipped files.",
    )
    parser.add_argument(
        "--noprogress",
        action="store_true",
        default=False,
        help="Disable the progress bar while running",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="List all tags found in Yep; does not update any files",
    )
    parser.add_argument(
        "--addtag",
        action="append",
        help="Add additional tag(s) to every Yep document: e.g. --addtag=yep --addtag=foo",
    )
    parser.add_argument(
        "--lctags",
        action="store_true",
        default=False,
        help="Convert all tags to lowercase before exporting metadata",
    )
    parser.add_argument(
        "--clearall",
        action="store_true",
        default=False,
        help="Clears all metadata from Yep documents (tags/keywords and Finder comments)",
    )

    args = parser.parse_args()
    # if no args, show help and exit
    if args.help:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return args


def main():
    global _yepplist
    global DEBUG

    args = process_arguments()

    plistfile = args.plist if args.plist else _yepplist
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

    if args.list:
        tags = []
        for item in pl["KPDocsInDB"]:
            if "Keywords" in item:
                tags += item["Keywords"]
        tagcount = Counter(tags)
        for tag in tagcount.most_common():
            print(f"{tag[0]}, {tag[1]}")
    else:
        for item in tqdm(iterable=pl["KPDocsInDB"], disable=args.noprogress):
            fname = item["currentPath"]
            yep_tags = []
            yep_comment = None

            if "Keywords" in item:
                yep_tags = item["Keywords"]

            if "Subject" in item:
                yep_comment = item["Subject"]

            if not os.path.isfile(fname):
                if not args.quiet:
                    tqdm.write(
                        "Skipping: %s, does not appear to be a valid file name" % fname
                    )
                items_skipped += 1
                continue

            try:
                md = osxmetadata.OSXMetaData(fname)
                if args.clearall:
                    if DEBUG:
                        print(f"wiping metadata from {fname}")
                    md.tags.clear()
                    md.finder_comment = ""
                    continue
                if args.verbose:
                    tqdm.write(f"Processing: {fname}")
                if args.lctags:
                    if DEBUG:
                        print(f"lctags: {yep_tags}")
                    yep_tags = [x.lower() for x in yep_tags]
                    if DEBUG:
                        print(f"lctags: {yep_tags}")
                if args.addtag:
                    yep_tags += args.addtag
                if yep_tags:
                    if args.verbose:
                        tqdm.write("yep_tags: %s" % ", ".join(yep_tags))
                    if not args.test:
                        if args.overwritetags:
                            if DEBUG:
                                print("clear()")
                            md.tags.clear()
                        if DEBUG:
                            print(f"update({yep_tags})")
                        md.tags.update(*yep_tags)
                if yep_comment:
                    if args.verbose:
                        tqdm.write("yep_comment: %s" % yep_comment)
                    if not args.test:
                        if DEBUG:
                            print(f"finder_comment: {yep_comment}")
                        md.finder_comment = yep_comment
                items_processed += 1
            except (IOError, OSError) as e:
                quit(onError(e))

        tqdm.write(
            "Processed %d of %d files, skipped %d"
            % (items_processed, total_items, items_skipped)
        )


if __name__ == "__main__":
    main()
