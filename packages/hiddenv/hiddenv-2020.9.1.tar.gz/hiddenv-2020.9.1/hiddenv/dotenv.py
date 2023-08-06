__all__ = [
    "find_dotenv",
    "read_dotenv"
]

import os
import re
from typing import Dict, Optional, Pattern

# https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_10_02
flags = re.VERBOSE | re.MULTILINE
_pattern_key = "(?P<key>[a-zA-Z_]+[a-zA-Z0-9_]*)"
_pattern_value = "(?P<value>.*)"
KEY_VALUE_RE: Pattern = re.compile(f"^.*?[ ]*{_pattern_key}[ ]*=[ ]*{_pattern_value}$", flags)
COMMENTS_RE: Pattern = re.compile(r"[ ][#]+.*$|^[ ]*[#]+.*$", flags)  # Match commented line or end of line comment
WHITESPACE_RE: Pattern = re.compile(r"\s*$", flags)  # Match from whitespace to end of line
EXPAND_VARS_RE: Pattern = re.compile(r"[^\\]\$(\w+)+")  # Match e.g. "$BAR"
EXPAND_VARS_RE_F: Pattern = re.compile(r"[^\\]\${([^}]*)")  # Match e.g. "${BAR}"


def find_dotenv(
    *, environment_variable: Optional[str] = "DOTENV_PATH",
    path: str = os.getcwd(),
    filename: str = ".env",
    find: bool = True
) -> Optional[str]:
    """Finds dotenv file path.

    Defaults to path given in system environment if it contains
    the given `environment_variable`. Otherwise, finds the dotenv
    file by `filename` in given directory `path` (or its parent
    directories, when `find` is set to `True`).

    Keyword Args:
        environment_variable: If not set to `None` and the
            variable exists in the system environment, this
            path is used to look up dotenv file.
        path: Directory path of dotenv file, or of directory
            to start search with if `find` is set to `True`.
        filename: Name of dotenv file.
        find: Unless set to `False`, dotenv file is searched
            for starting from given parent directory `path`

    Returns:
        File path of dotenv file, if found, otherwise `None`.
    """

    file_path = None
    if environment_variable is not None and environment_variable in os.environ:
        file_path = os.environ.get(environment_variable)
    if file_path is None and not find:
        file_path = os.path.join(path, filename)

    if file_path is not None:
        if os.path.isfile(file_path):
            return file_path
        return None

    path = os.path.abspath(path)
    while True:
        # Travel to root until dotenv file is found
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            return file_path
        if os.path.dirname(path) == path:
            return None  # found root, dotenv file not found
        path = os.path.dirname(path)


def read_dotenv(file_path: Optional[str]) -> Optional[Dict[str, str]]:
    """Reads dotenv file.

    Args:
        file_path: Path to dotenv file.

    Returns:
        Parsed dotenv data if file is found, else `None`.
    """

    if file_path is None:
        return None
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r") as file_descriptor:
        return parse(file_descriptor.read())


def parse(dotenv: str) -> Dict[str, str]:
    """Parses dotenv data.

    Args:
        dotenv: Data to parse.
    """

    dotenv = COMMENTS_RE.sub(repl="", string=dotenv)
    dotenv = WHITESPACE_RE.sub(repl="", string=dotenv)
    parsed: Dict[str, str] = {}
    for k, v in KEY_VALUE_RE.findall(string=dotenv):
        if v and v[0] == v[-1] and v[0] in "'\"":
            # Clean string encapsulation
            v = v[1:-1]

        # Fix escapes, except for "\$"
        v = " " + v.replace("\\\"", "\"").replace("\\'", "'").replace("\\\\", "\\")

        # Expand non-encapsulated variables, e.g. "$BAR"
        # ToDo this will replace escaped cases if they are duplicated e.g. "\$BAR hello $BAR"
        for item in EXPAND_VARS_RE.findall(v):
            val = os.environ[item] if item in os.environ else parsed[item]
            v = re.compile(r"\$" + item).sub(repl=val, string=v)

        # Expand non-encapsulated variables, e.g. "${BAR}"
        # ToDo this will replace escaped cases if they are duplicated e.g. "\${BAR} hello ${BAR}"
        for item in EXPAND_VARS_RE_F.findall(v):
            val = os.environ[item] if item in os.environ else parsed[item]
            v = re.compile(r"\${" + item + "}").sub(val, string=v)

        # Fix $ escape "\$"
        parsed[k] = v[1:].replace("\\$", "$")
    return parsed
