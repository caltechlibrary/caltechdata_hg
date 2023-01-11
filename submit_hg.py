import os, json, datetime, argparse
import hglib
from caltechdata_api import caltechdata_edit
from caltechdata_api import caltechdata_write

# Submits a mercurial repository to CaltechDATA
# To use copy this script and type `python submit_hg.py metadata.json`
# after filling out the metadata.json file with appropriate metadata

# The script will create CaltechDATA entries for every tag in your repository

# You need to get a access token from CaltechDATA
# http://libanswers.caltech.edu/faq/211307 and save it as the RDMTOK
# environment variable

# Requires python 3 and the python-hglib library
# You can install python-hglib by typing pip install python-hglib
# Requires caltechdata_api (https://github.com/caltechlibrary/caltechdata_api)


def build_relation(client, version, metadata):
    if client.paths() != {}:
        # Get url to specific tag from hg repo
        full_url = client.paths()["default".encode("utf-8")].decode("utf-8")
        # Strip username
        split_1 = full_url.split("@")
        back = split_1[1]
        final = "https://" + back + "/commits/tag/" + version
        new = {
            "relatedIdentifier": final,
            "relatedIdentifierType": "URL",
            "relationType": "IsIdenticalTo",
        }
        if "relatedIdentifiers" in metadata:
            metadata["relatedIdentifiers"].append(new)
        else:
            metadata["relatedIdentifiers"] = [new]
    return metadata


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="submit_hg submits a mercurial repository to caltechDATA (Invenio 3)"
    )
    parser.add_argument(
        "json_file", nargs=1, help="file name for json DataCite metadata file"
    )

    args = parser.parse_args()

    token = os.environ["RDMTOK"]

    history_file = ".caltechdata_written"

    production = False
    publish = True

    already_archived = []
    archived_ids = {}
    if os.path.isfile(history_file):
        # This file contains versions we've already submitted
        infile = open(history_file, "r")
        for j in infile:
            line = j.rstrip()
            split = line.split(",")
            archived_version = split[0]
            already_archived.append(archived_version)
            archived_ids[archived_version] = split[1]

    repo = "."
    client = hglib.open(repo)
    tags = client.tags()
    versions = []
    for t in tags:
        version = t[0].decode("utf-8")
        if version != "tip":
            versions.append(version)
    versions.sort()
    for version in versions:
        if version not in already_archived:
            hashv = t[2]
            outfile = version + ".tgz"  # open(version+'.tgz','w')
            client.archive(outfile.encode("utf-8"), hashv)
            split = version.split(".")
            mj = split[0]
            metaf = open(args.json_file[0], "r")
            metadata = json.load(metaf)
            metadata["version"] = version
            metadata = build_relation(client, version, metadata)
            files = outfile
            if already_archived == []:
                print("Creating New Record")
                # We need a New CaltechDATA record
                response = caltechdata_write(
                    metadata, token, files, production, publish=publish
                )
                new_id = response
                already_archived.append(version)
                archived_ids[version] = new_id
            else:
                # Otherwise create a new version of the existing CaltechDATA record
                print("Creating New Version")
                response = caltechdata_edit(
                    archived_ids[versions[0]],
                    metadata,
                    token,
                    files,
                    production,
                    publish=publish,
                )
                new_id = response.split("/")[1]
            outf = open(history_file, "a")
            outf.write(version + "," + new_id + "\n")
            # Cleanup
            os.remove(outfile)
