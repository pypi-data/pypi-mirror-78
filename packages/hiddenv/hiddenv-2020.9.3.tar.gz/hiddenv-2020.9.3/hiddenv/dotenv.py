import os
import re

# https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_10_02
flags = re.VERBOSE | re.MULTILINE
_pattern_key = "(?P<key>[a-zA-Z_]+[a-zA-Z0-9_]*)"
_pattern_value = "(?P<value>.*)"
KEY_VALUE_RE = re.compile(f"^.*?[ ]*{_pattern_key}[ ]*=[ ]*{_pattern_value}$", flags)
COMMENTS_RE = re.compile(r"[ ][#]+.*$|^[ ]*[#]+.*$", flags)  # Match commented line or end of line comment
WHITESPACE_RE = re.compile(r"\s*$", flags)  # Match from whitespace to end of line
EXPAND_VARS_RE = re.compile(r"[^\\]\$(\w+)+")  # Match e.g. "$BAR"
EXPAND_VARS_RE_F = re.compile(r"[^\\]\${([^}]*)")  # Match e.g. "${BAR}"


def find_dotenv(
    *, variable="DOTENV_PATH",
    filename=".env",
    path=None,
    find=True
):
    """Finds path to dotenv file if it exists.

    Defaults to path in given system environment variable, then
    searches for file name in the directory path and its parents.

    To disable searching in parent directories, set find to False.

    Keyword Args:
        variable: Environment variable for dotenv file path
        filename: Name of dotenv file
        path: Directory path to search in, defaults to current directory
        find: Whether to search in parent directories, default True

    Returns:
        File path of existing dotenv file or None.
    """

    def _file_or_none(dotenv_file_path):
        if os.path.isfile(dotenv_file_path):
            return dotenv_file_path
        return None

    if isinstance(variable, str) and variable in os.environ:
        return _file_or_none(os.environ[variable])

    path = os.getcwd() if path is None else os.path.abspath(path)
    file_path = _file_or_none(os.path.join(path, filename))
    while (
        find and file_path is None and
        path != os.path.dirname(path)
    ):
        path = os.path.dirname(path)
        file_path = _file_or_none(os.path.join(path, filename))
    return file_path


def read_dotenv(file_path):
    """Reads dotenv file.

    Args:
        file_path: Path to dotenv file.

    Returns:
        Parsed data from existing dotenv file or None.
    """

    if file_path is None:
        return None
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r") as file_descriptor:
        return parse(file_descriptor.read())


def parse(dotenv):
    """Parses dotenv data.

    Args:
        dotenv: Data to parse

    Returns:
        Parsed data.
    """

    dotenv = COMMENTS_RE.sub(repl="", string=dotenv)
    dotenv = WHITESPACE_RE.sub(repl="", string=dotenv)
    parsed = {}
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
