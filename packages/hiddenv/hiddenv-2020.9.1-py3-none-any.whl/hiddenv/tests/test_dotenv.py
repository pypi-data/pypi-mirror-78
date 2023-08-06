import os
from contextlib import suppress
from tempfile import NamedTemporaryFile
from unittest import TestCase
from hiddenv import dotenv


test_file_content = """
FOO=foo
BAR=bar
NORMAL=bar
BEFORE_SPACE =bar
AFTER_SPACE= bar
BOTH_SPACE = bar
DOUBLE_QUOTE="bar"
SINGLE_QUOTE='bar'
ESCAPED="escaped\\"bar"
EMPTY=
EMPTY1=$EMPTY

NORMAL_BAR=${NORMAL}bar
NORMAL_EVALUATED=$NORMAL

EVALUATED_COMMENT=$NORMAL ## ''

QUOTE_CONCAT_ESCAPE=\\"quote $FOO\\"



QUOTE_CONCAT='quote $FOO'
QUOTE_ESCAPE_DOLLAR="foo\\${BAR}"
#QUOTE_ESCAPE_DOLLAR_DUPLICATE="foo\\${BAR}${BAR}"  # ToDo
export EXPORTED_BAR=bar
lowercase_bar=bar

""" + "\t  " + """


lowercase_bar_comments=bar # this is foo

CONCATENATED_BAR_BAZ_COMMENTED="bar#baz" # comment""" + " " + """



# HERE GOES FOO


#foo="ba#r"


# wrong
# lol$wut

"""


class DotEnvTest(TestCase):
    expected = dict(
        FOO="foo",
        BAR="bar",
        NORMAL="bar",
        BEFORE_SPACE="bar",
        AFTER_SPACE="bar",
        BOTH_SPACE="bar",
        DOUBLE_QUOTE="bar",
        SINGLE_QUOTE="bar",
        ESCAPED="escaped\"bar",
        EMPTY="",
        EMPTY1="",
        NORMAL_BAR="barbar",
        NORMAL_EVALUATED="bar",
        EVALUATED_COMMENT="bar",
        QUOTE_CONCAT_ESCAPE="\"quote foo\"",
        QUOTE_CONCAT="quote foo",
        QUOTE_ESCAPE_DOLLAR="foo${BAR}",
        EXPORTED_BAR="bar",
        lowercase_bar="bar",
        lowercase_bar_comments="bar",
        CONCATENATED_BAR_BAZ_COMMENTED="bar#baz",
        # QUOTE_ESCAPE_DOLLAR_DUPLICATE="foo${BAR}bar"  # ToDo
    )

    @classmethod
    def tearDownClass(cls) -> None:
        with suppress(FileNotFoundError):
            os.remove("test.env")

    @staticmethod
    def temporary_dotenv_file(dotenv_string):
        file_descriptor = NamedTemporaryFile()
        file_descriptor.write(dotenv_string.encode("utf-8"))
        file_descriptor.seek(0)
        return file_descriptor

    @staticmethod
    def dotenv_file(dotenv_string):
        file_descriptor = NamedTemporaryFile()
        file_descriptor.write(dotenv_string.encode("utf-8"))
        file_descriptor.seek(0)
        return file_descriptor

    def _test(self, data, expected):
        self.assertEqual(set(), {*data}.difference({*expected}))
        self.assertEqual(set(), {*expected}.difference({*data}))
        for key, value in expected.items():
            self.assertEqual(value, data[key])

    def test_values(self):
        data = dotenv.parse(test_file_content)
        self._test(data, self.expected)

    def test_file(self):
        file = self.temporary_dotenv_file(test_file_content)
        data = dotenv.read_dotenv(file.name)
        self._test(data, self.expected)

    def test_real_file(self):
        with open("test.env", "w") as f:
            f.write(test_file_content)
        file_path = dotenv.find_dotenv(filename="test.env")
        self.assertEqual(dotenv.find_dotenv(find=False, filename="test.env"), file_path)
        os.environ.update(DOTENV_PATH=file_path)
        self.assertEqual(dotenv.find_dotenv(), file_path)
        data = dotenv.read_dotenv(dotenv.find_dotenv(filename="test.env"))
        self._test(data, self.expected)
        os.remove("test.env")

    def test_file_not_found(self):
        self.assertEqual(dotenv.find_dotenv(filename="nothing.env"), None)
        self.assertEqual(dotenv.find_dotenv(filename="nothing.env", find=False), None)
        self.assertEqual(dotenv.read_dotenv(None), None)
        self.assertEqual(dotenv.read_dotenv("nothing.env"), None)
