""" test sequence

   isort:skip_file
"""
import os
import sys
import unittest
import mock

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


from ciocore.expander import Expander


class ExpanderTokensTest(unittest.TestCase):

    def setUp(self):
        self.context = {
            "Scene": "/projects/myscene",
            "RenderLayer": "masterLayer",
            "home": "/users/joebloggs/",
            "shot": "/metropolis/shot01/",
            "ct_dept": "texturing",
            "frames": 20,
            "directories": "/a/b /a/c"}

    def test_expand_value_target(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<home>_y")
        self.assertEqual(result, "x_/users/joebloggs/_y")

    def test_expand_numeric_value_target(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<frames>_y")
        self.assertEqual(result, "x_20_y")

    def test_expand_numeric_value_is_string(self):
        e = Expander(**self.context)
        result = e.evaluate("<frames>")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "20")

    def test_bad_value_raises(self):
        e = Expander(**self.context)
        with self.assertRaises(KeyError):
            e.evaluate("<bad>")

    def test_mixed_case(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<Scene>_y")
        self.assertEqual(result, "x_/projects/myscene_y")

    def test_repeated_tokens(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<Scene>_<Scene>_y")
        self.assertEqual(result, "x_/projects/myscene_/projects/myscene_y")

    # lists
    def test_expand_list_target(self):
        e = Expander(**self.context)
        result = e.evaluate(["x_<shot>_y", "x_<ct_dept>_y"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["x_/metropolis/shot01/_y", "x_texturing_y"])

    def test_expand_empty_list_target(self):
        e = Expander(**self.context)
        result = e.evaluate([])
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    def test_bad_list_value_raises(self):
        e = Expander(**self.context)
        with self.assertRaises(KeyError):
            e.evaluate(["<bad>", "directories"])

    # dicts
    def test_expand_dict_target(self):
        e = Expander(**self.context)
        result = e.evaluate({"foo": "x_<shot>_y", "bar": "x_<ct_dept>_y"})
        self.assertIsInstance(result, dict)
        self.assertEqual(
            result, {"foo": "x_/metropolis/shot01/_y", "bar": "x_texturing_y"})

    def test_expand_empty_dict_target(self):
        e = Expander(**self.context)
        result = e.evaluate({})
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_bad_dict_value_raises(self):
        e = Expander(**self.context)
        with self.assertRaises(KeyError):
            e.evaluate({"foo": "<bad>", "bar": "directories"})

    def test_bad_dict_value_does_not_raise_if_safe(self):
        e = Expander(safe=True, **self.context)
        result = e.evaluate("x_<bad>_y")
        self.assertEqual(result, "x_<bad>_y")

    def test_strip(self):
        e = Expander(**self.context)
        result = e.evaluate(" x_<home>_y ")
        self.assertEqual(result, "x_/users/joebloggs/_y")


class ExpanderEnvVarTest(unittest.TestCase):

    def setUp(self):
        self.env = {
            "HOME": "/users/joebloggs",
            "SHOT": "MT_shot01",
            "DEPT": "texturing",
        }

    def test_expand_env_vars(self):
        with mock.patch.dict("os.environ", self.env):
            e = Expander()
            result = e.evaluate({"foo": "${SHOT}_hello", "bar": "x_${DEPT}_y"})
            self.assertIsInstance(result, dict)
            self.assertEqual(
                result, {"foo": "MT_shot01_hello", "bar": "x_texturing_y"})

    def test_doesnt_expand_nonexistent_vars(self):
        with mock.patch.dict("os.environ", self.env):
            e = Expander()
            o = {"foo": "${JOB}_hello", "bar": "x_${PROD}_y"}
            result = e.evaluate(o)
            self.assertIsInstance(result, dict)
            self.assertEqual(result, o)


if __name__ == '__main__':
    unittest.main()
