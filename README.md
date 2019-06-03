Description
-----------

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

`yep2tag --lctags --overwritetags -q --addtag=yep`

Installation
------------

I recommend using [pipx](https://github.com/pipxproject/pipx)

`pipx install --spec git+https://github.com/RhetTbull/yep2tag.git yep2tag`

Dependencies
------------

- [osxmetadata](https://pypi.org/project/osxmetadata/)
- [tqdm](https://pypi.org/project/tqdm/)
