# caltechdata_hg
[![DOI](https://data.caltech.edu/badge/112391986.svg)](https://data.caltech.edu/badge/latestdoi/112391986)

Preserve a mercurial repository in CaltechDATA

Requires python 3 and the python-hglib library
You can install python-hglib by typing pip install python-hglib
Requires caltechdata_api (https://github.com/caltechlibrary/caltechdata_api)

To use:
- Copy submit_hg.py to your repository
- Tag releases with versions in the form of "major.minor"
- Get a CaltechDATA access token: http://libanswers.caltech.edu/faq/211307
- Fill out a metadata file.  An example metadata.json file is included as a
    starting point.  You can also grab metadata from CaltechDATA using the
    get_metadata function in caltechdata_api
- Run the script by typing python submit_hg.py metadata.json

### Note
This script will make permanent records of your code in CaltechDATA.  These
cannot be removed.  Take care to only run this script when you are ready to
preserve your code, and all tags will be uploaded.
