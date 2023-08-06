""" this module read the verstion tag number
and set the project version to the git tag version. """

import os
import re
import tempfile
from git import Repo

def replace_line_in_file(fpath, old_line_start, new_line):
    """ find and delete string in a file """
    assert os.path.exists(fpath)
    assert (old_line_start and str(old_line_start))
    assert (new_line and str(new_line))

    replaced = False
    written = False

    try:
        with open(fpath, 'r+') as fhandle:  # open for read/write -- alias to f
            lines = fhandle.readlines()  # get all lines in file

            breaks = True

            for line in lines:
                if old_line_start in line:
                    breaks = False  # line not found in file, do nothing

            if breaks:
                pass
            else:
                tmpf = tempfile.NamedTemporaryFile(
                    delete=True, mode='r+')  # temp file opened for writing

                for line in lines:  # process each line
                    if old_line_start in line:  # find the line we want
                        tmpf.write(new_line)  # replace it
                        replaced = True
                    else:
                        tmpf.write(line)  # write old line unchanged

                tmpf.flush()
                tmpf.seek(0, os.SEEK_SET)

                if replaced:  # overwrite the original file
                    fhandle.seek(0)  # beginning of file
                    fhandle.truncate()  # empties out original file
                    for tmplines in tmpf.readlines():
                        fhandle.write(
                            tmplines)  # writes each line to original file
                        written = True

                tmpf.close()  # tmpfile auto deleted
            fhandle.close()  # we opened it , we close it

    except IOError as ioe:  # if something bad happened.
        print("ERROR", ioe)
        fhandle.close()
        return False

    return replaced and written  # replacement happened with no errors = True


def setversion(repopath, versionfile):
    """ set the version number in a given file """

    repo = Repo.init(repopath, bare=False)
    assert not repo.bare

    try:
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        latest_tag = tags[-1]

        print(f"found tag {latest_tag}")

        match_obj = re.match(r'v(\d+).(\d+).(\d+)', str(latest_tag), re.I)

        major = match_obj.group(1)
        minor = match_obj.group(2)
        patch = match_obj.group(3)

        replace_line_in_file(
            versionfile, "__version__",
            f"__version__ = ({int(major)}, {int(minor)}, {int(patch)})\n")
    except: # pylint: disable=W0702
        print("set the version to 0.1.0 because no tag set")
        replace_line_in_file(versionfile, "__version__",
                             "__version__ = (0, 1, 0)\n")
