import os
import unittest
from typing import NamedTuple
from hiddenv.conf import settings


class TestSettings(unittest.TestCase):
    def test_settings_1(self):
        settings.reset()
        os.environ["SETTINGS_MODULE"] = "hiddenv.tests.settingstest"
        settings.configure()
        self.assertEqual(settings.CONFIGURATION, "jejee")
        self.assertEqual(settings._AAAA, "B")
        self.assertEqual(settings.COMMON, "THAT")
        with self.assertRaises(KeyError):
            settings.BBB  # noqa

    def test_settings_2(self):
        settings.reset()
        os.environ["SETTINGS_MODULE"] = "hiddenv.tests.settingstest_1"
        settings.configure()
        self.assertEqual(settings.BBB, 123)
        self.assertEqual(settings.COMMON, "THIS")
        with self.assertRaises(KeyError):
            settings.CONFIGURATION  # noqa

    def test_no_settings_module_1(self):
        settings.reset()
        os.environ.pop("SETTINGS_MODULE", None)
        with self.assertRaises(KeyError):
            settings.configure()

    def test_no_settings_module_2(self):
        settings.reset()
        os.environ["SETTINGS_MODULE"] = "hiddenv.tests.settingstest_nothere"
        with self.assertRaises(ModuleNotFoundError):
            settings.configure()

    def test_settings_3(self):
        settings.reset()
        os.environ["SETTINGS_MODULE"] = "hiddenv"
        settings.configure()
        with self.assertRaises(ValueError):
            settings.configure()

    def test_load(self):
        class Test(NamedTuple):
            truthy: bool
            common: str
        settings.reset()
        os.environ["SETTINGS_MODULE"] = "hiddenv.tests.settingstest"
        settings.configure()
        self.assertEqual(settings.load(Test), Test(truthy=True, common="THAT"))
