Description
-----------

This script exports tags/keywords and comments managed by Ironic Software's
Yep application to native OS X tags & Finder comments
Tested with Yep version 1.8.0 See: http://www.ironicsoftware.com

Newer versions of Yep stored metadata using OS X extended attributes but I much
preferred the interface of the "legacy" Yep app which aimed to be "iPhotos for PDFs"

I still use Yep to manage many thousands of document but as an unsupported 32-bit app,
it's days are numbered (Yep 1.8.0 released ~2008).

This script future-proofs all the metadata I've got stored in Yep and makes Yep files
play well with the Finder & Spotlight

I run the script with following options:

`./yep2tag.py --lctags --overwritetags -q --addtag=yep`

Dependencies
------------

- [osxmetadata](https://pypi.org/project/osxmetadata/)
- [tqdm](https://pypi.org/project/tqdm/)
