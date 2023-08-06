import os
import unittest
from hiddenv.environment import Env


class TestEnv(unittest.TestCase):
    def test(self):
        os.environ.update(STR="hello")
        env = Env(
            STR="text",
            BOOL="True",
            NUM="7",
            JSON='{"one": true}',
            LIST="one,two, three",
            TUPLE="(one, two ,three)",
            DICT=" a=3;b=asd ;"
        )
        self.assertEqual("hello", env.str("STR"))
        self.assertIs(True, env.bool("BOOL"))
        self.assertIs(7, env.int("NUM"))
        self.assertEqual(7.0, env.float("NUM"))
        self.assertIsInstance(env.float("NUM"), float)
        self.assertDictEqual(dict(one=True), env.json("JSON"))
        self.assertListEqual(["one", "two", "three"], env.list("LIST"))
        self.assertTupleEqual(("one", "two", "three"), env.tuple("TUPLE"))
        self.assertDictEqual(dict(a="3", b="asd"), env.dict("DICT"))
        with self.assertRaises(LookupError):
            env.str("DOES_NOT_EXIST")
        self.assertEqual(env.str("DOES_NOT_EXIST", default="Nope"), "Nope")
