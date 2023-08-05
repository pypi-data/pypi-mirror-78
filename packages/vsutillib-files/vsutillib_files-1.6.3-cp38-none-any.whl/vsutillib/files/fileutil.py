"""
Convenience functions related to files and file system
"""

import os
import platform
import shlex

from pathlib import Path, PurePath


def findFileInPath(element, dirPath=None):
    """
    Convenience function that finds a file in the
    PATH environment variable

    Args:
        dirPath (str): search in the specified PATH

    Returns:
        list: list of :py:class:`pathlib.Path`

    I really like the :mod:`threading` module which has the
    :class:`threading.Thread` class.

    Here is a link :func:`time.time`.
    """

    filesFound = []

    if dirPath is None:
        dirPath = os.getenv("PATH")

    if isinstance(dirPath, str):
        dirs = dirPath.split(os.pathsep)
    else:
        dirs = dirPath

    for dirname in dirs:
        candidate = Path(PurePath(dirname).joinpath(element))
        if candidate.is_file():
            filesFound.append(candidate)

    return filesFound


def getFileList(
    strPath, wildcard="*.*", fullpath=False, recursive=False, strName=False
):
    """
    Get files in a directory
    strPath has to be an existing directory or file
    in case of a file the parent directory is used
    strExtFilter in the form -> .ext
    """

    doubleWildcard = False
    argWildcard = wildcard
    lstObjFileNames = []

    p = Path(strPath)

    try:
        if p.is_file():
            p = p.parent
    except OSError:
        pass

    try:
        if not p.is_dir():
            p = p.parent
    except OSError:
        wildcard = p.stem
        p = p.parent
        doubleWildcard = True  # wildcard found on strPath argument

    try:
        if not p.is_dir():
            # Wrong argument for strPath
            return []
    except OSError:
        # Wrong argument for strPath
        return []

    if (not p.is_file()) and (not p.is_dir()):
        return []

    lstFilesFilter = []

    if p.is_file():
        p = p.parent

    wc = wildcard
    awc = argWildcard

    if doubleWildcard:

        lstFiles = [x for x in p.glob(wc) if x.is_file()]

        if recursive:
            awc = "**/" + stripEncaseQuotes(argWildcard)

            for d in lstFiles:
                if d.is_dir():
                    oFiles = [x for x in d.glob(awc) if x.is_file()]
                    lstObjFileNames.extend(oFiles)
        else:
            lstObjFileNames.extend(lstFiles)

    else:
        if recursive:
            wc = "**/" + stripEncaseQuotes(wildcard)

        # print("Path = {}\nWith wildcard ={}\n".format(p, wc))

        lstObjFileNames = [x for x in p.glob(wc) if x.is_file()]

    if not fullpath:
        lstFilesFilter = [x.name for x in lstObjFileNames]
        return lstFilesFilter

    if strName:
        lstFilesFilter = [str(x) for x in lstObjFileNames]
        return lstFilesFilter

    return lstObjFileNames


def getDirectoryList(
    strPath, wildcard="*", fullpath=False, recursive=False, strName=False
):
    """
    Get files in a directory
    strPath has to be an existing directory or file
    in case of a file the parent directory is used
    strExtFilter in the form -> .ext
    """

    doubleWildcard = False
    argWildcard = wildcard
    lstObjFileNames = []

    p = Path(strPath)

    try:
        if p.is_file():
            p = p.parent
    except OSError:
        pass

    try:
        if not p.is_dir():
            p = p.parent
    except OSError:
        wildcard = p.stem
        p = p.parent
        doubleWildcard = True  # wildcard found on strPath argument

    try:
        if not p.is_dir():
            # Wrong argument for strPath
            return []
    except OSError:
        # Wrong argument for strPath
        return []

    lstFilesFilter = []

    wc = wildcard
    awc = argWildcard

    if doubleWildcard:
        dirs = [x for x in p.glob(wc) if x.is_dir()]

        if recursive:
            awc = "**/" + stripEncaseQuotes(argWildcard)
            for d in dirs:
                if d.is_dir():
                    lstObjFileNames.append(d)
                    oDirs = [x for x in d.glob(awc) if x.is_dir()]
                    lstObjFileNames.extend(oDirs)

        else:
            lstObjFileNames.extend(dirs)
    else:
        if recursive:
            wc = "**/" + stripEncaseQuotes(wildcard)

        lstObjFileNames = [x for x in p.glob(wc) if x.is_dir()]

    if not fullpath:
        lstFilesFilter = [x.name for x in lstObjFileNames]
        return lstFilesFilter

    if strName:
        lstFilesFilter = [str(x) for x in lstObjFileNames]
        return lstFilesFilter

    return lstObjFileNames


def getExecutable(search):
    """
    search for executable for macOS and
    """

    fileToSearch = search

    currentOS = platform.system()

    if currentOS == "Darwin":

        lstTest = Path("/Applications").glob("**/" + fileToSearch)

        for l in lstTest:
            if (p := Path(l)).stem == fileToSearch:
                return p

    elif currentOS == "Windows":

        if fileToSearch.find(".") < 0:
            # assume is binary executable
            fileToSearch += ".exe"

        dirs = []
        dirs.append(os.environ.get("ProgramFiles") or "")
        dirs.append(os.environ.get("ProgramFiles(x86)") or "")

        # search 64 bits
        for d in dirs:
            if search := sorted(Path(d).rglob(fileToSearch)):
                if (executable := Path(search[0])).is_file():
                    return executable

    if searchFile := findFileInPath(fileToSearch):
        for e in searchFile:
            if (executable := Path(e)).is_file():
                return executable

    return None


def stripEncaseQuotes(strFile):
    """
    Strip single quote at start and end of file name
    if they are found

    Args:
        strFile (str): file name

    Returns:
        str:

        file name without start and end single quoute
    """

    # Path or str should work
    s = str(strFile)

    if (s[0:1] == "'") and (s[-1:] == "'"):
        s = s[1:-1]

    return s


def fileQuote(oFile):

    f = shlex.quote(str(oFile))
    s = f.replace('"\'"', r"\'")

    return s
