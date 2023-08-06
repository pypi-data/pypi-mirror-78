import logging
import sys
from typing import List


def create_module_logger(mn):
    ml = logging.getLogger(mn)
    ml.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - {%(name)s} - "
        "{%(filename)s:%(funcName)s:%(lineno)d} - "
        "%(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    ml.addHandler(ch)
    return ml


module_name = str(__name__)
module_logger = create_module_logger(module_name)


def find_path_to_ancestor(target_dir=None):
    """Find path to parent directory among the ancestors

    target_dir is the base name of a directory  (without path separator) that
    will be discovered from amogn the parent directories

    If the target_dir is given a strinf that contains a path separator, it just
    returns the target_dir.  This is useful for testing, so we can explicitly
    pass an absolute path.

    :param str target_dir: target directory

    :rtype: str
    """
    import os

    if os.path.sep in target_dir:
        logging.info(
            "Target directory contains path separators.  "
            "Returning the parameter itself"
        )
        return target_dir
    logging.info("Searching ancestors for directory: {}".format(target_dir))
    ancestors = os.getcwd().split(os.path.sep)
    if target_dir not in ancestors:
        raise RuntimeError(
            "Current directory is not a subdirectory of {}".format(target_dir)
        )
    else:
        # iterate through the last dirs until we hit the one we want
        while not ancestors[-1] == target_dir:
            ancestors.pop()
    # rejoin: we lose the first separator in the split/join
    return os.path.sep + os.path.join(*ancestors)


def find_path_to_subdirectory(target_dir, search_path=None) -> List[str]:
    """Find a directory name among subdirs

    searching for target_dir: 'testdata' from '/home/nate':
    '/home/nate/testdata' would match
    '/home/nate/testdata/something' would NOT match
    '/home/nate/testdata/something/testdata' would  match

    The result would be a list containing both matching paths


    Args:
        target_dir (str): Base directory name to search for among
            sub-directories

        search_path (str, optional): If no search path is provided, start in
        current directory. Defaults to None.

    Returns:
        List[str]: List of absolute paths to subdirectories matching the
        target_dir
    """
    import os

    if search_path is None:
        search_path = os.getcwd()
    res = []  # type: List[str]

    def contains_target(tp) -> bool:
        words = tp.split(os.path.sep)
        return target_dir == words[-1]

    all_subdirs = [x[0] for x in os.walk(search_path)]
    for sd in all_subdirs:
        if contains_target(sd):
            res.append(sd)
    res.sort()
    return res


def file_to_string(file_path):
    """Return file contents as a string

    :param str file_path: absolute path to a file
    :rtype: str

    """
    with open(file_path, "rb") as f:
        try:
            data = f.read()
        except UnicodeDecodeError as err:
            msg = """Failed to read file: {0}
            You probably need to set the locale in your environment
            This is often a proiblem inside docker containers
            something like this might work:
            RUN locale-gen en_US.UTF-8
            ENV LANG en_US.UTF-8
            ENV LANGUAGE en_US:en
            ENV LC_ALL en_US.UTF-8
            """.format(
                file_path
            )
            raise RuntimeError(msg) from err
    return data.decode("utf8", "ignore")


def string_to_file(input_string, file_path):
    """Write/Over-write a file's contents with a string


    :param str input_string: string data
    :param str file_path: absolute path to a file
    """
    with open(file_path, "w") as f:
        f.write(input_string)


def string_to_log_level(log_level_string):
    """Given a string convert it to a logging level for use by logging.log

    Accept the string ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG') or the
    integer ('10', '20', '30', '40', '50') format

    :param str log_level_string: case insensitive

    """
    import logging

    if log_level_string.upper() in [
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
    ]:
        return getattr(logging, log_level_string.upper())

    integer_levels = {
        "50": "CRITICAL",
        "40": "ERROR",
        "30": "WARNING",
        "20": "INFO",
        "10": "DEBUG",
    }
    return getattr(logging, integer_levels[log_level_string])


def mkdir_p(target, is_file=False):
    """Create the directory path to the target.
    If the target is a file, create the path to its parent (directory)

    :param str target: path to a target directory or file
    :param bool is_file: Indicates whether the target is a file


    :rtype: str
    """
    import pathlib
    import errno
    import os

    path = pathlib.Path(target)
    if is_file:
        path = path.parent

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    return path


def get_all_files(target_dir):
    """Recurse the all subdirs and list os abs paths

    :param str target_dir: Indicates whether the target is a file


    :rtype: List[str]
    """
    import os

    res = []
    for root, d_names, f_names in os.walk(target_dir):
        for f in f_names:
            res.append(os.path.join(root, f))
    return res


def strip_suffix(s, suffix):
    """Remove suffix frm the end of s
    is s = "aaa.gpg" and suffix = ".gpg", return "aaa"
    if s is not a string return None
    if suffix is not a string, return s

    :param str s: string to modify
    :param str suffix: suffix to remove

    :rtype: Optional[str]=None
    """
    if not isinstance(s, str):
        return None
    if not isinstance(suffix, str):
        return s
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def strip_prefix(s, prefix):
    """Remove prefix frm the beginning of s
    is s = "some_something" and prefix = "some_", return "something"
    if s is not a string return None
    if prefix is not a string, return s

    :param str s: string to modify
    :param str prefix: prefix to remove

    :rtype: Optional[str]=None
    """
    if not isinstance(s, str):
        return None
    if not isinstance(prefix, str):
        return s
    if s.startswith(prefix):
        return s[len(prefix) :]  # noqa: E203
    return s


def validate_path(ip=None):
    """Give a valid path return absolute

    If the provided relative or absoltue path is invalide, raise
    RuntimeError exception

    If none is provided, use current working directory

    :param str ip: absolute or relative path

    :rtype: str
    """
    import os

    if ip is None:
        ip = os.getcwd()
    rp = os.path.realpath(ip)
    if os.path.exists(rp):
        return rp
    else:
        raise RuntimeError("Invalid path: {}".format(rp))


#
# def path_type(ip):
#     """ return a string describing the ype of object represented by a path
#
#     examples:
#      - "dir" (if it's a directory)
#      - 'text/plain; charset=us-ascii' (mimetype if not)
#
#     :param str ip: absolute path to file or directory
#
#     :rtype: str
#     """
#     import magic
#     import os
#     if os.path.isdir(ip):
#         return "dir"
#
#     if os.path.isfile(ip):
#         m = magic.Magic()
#         return m.from_file(ip)


def file_name_from_path(ff):
    """Return the file name given a path

    "a/b/g/file.txt" -> "file.txt

    :param str ff: pathto file

    :rtype: str
    """
    import os

    words = ff.split(os.path.sep)
    return words[-1]


def output_file_from_input_file(input_root, output_root, input_file):
    # normalize root formats to make sure both have trialing slashes
    import os

    in_r = os.path.join(input_root, "")
    out_r = os.path.join(output_root, "")
    # /a/b/c/file.txt, /a/b/ -> c/file.txt
    file_relative = strip_prefix(input_file, in_r)
    # if there's a leading slash, remove it
    if file_relative.startswith(os.path.sep):
        file_relative = file_relative[1:]
    res = os.path.join(out_r, file_relative)
    return res


def locate_subdir(target_dir):
    """Recursively look for subdir and return absolute path

    This is really useful in locating resource directories  for tests when
    the test could be run from the project directory or tests directory.

    :param str target_dir: directory to locate

    :rtype: List[Dict[str, str]]
    """
    import os

    for root, d_names, f_names in os.walk(os.getcwd()):
        for d in d_names:
            if d == target_dir:
                return os.path.join(root, d)
    return None


def compare_directories(d1, d2):
    """Compare directories that should be exact matches



    :param str d1: left directory
    :param str d2: left directory


    :rtype: bool
    """
    import filecmp

    # iterate d1 files and compare to companion d2 file
    for left in get_all_files(d1):
        right = output_file_from_input_file(d1, d2, left)
        if not filecmp.cmp(left, right, shallow=False):
            return False

    # iterate d2 files and compare to companion d1 file
    for right in get_all_files(d2):
        left = output_file_from_input_file(d2, d1, right)
        if not filecmp.cmp(right, left, shallow=False):
            return False
    return True
