import unittest
from datetime import date, datetime
from typing import Callable

from pyrdfj2.j2_functions import Functions, ValueMapper

ttl_fmt = Functions.all()["ttl_fmt"]
uritexpand_fmt = Functions.all()["uritexpand"]
regexreplace_fmt = Functions.all()["regexreplace"]
map_build_fmt = Functions.all()["map"]


class TestTTLFormatting(unittest.TestCase):
    def test_fn(self):
        self.assertIsNotNone(ttl_fmt, "function not found")
        self.assertTrue(isinstance(ttl_fmt, Callable), "function not callable")

    def test_bool(self):
        type_name = "xsd:boolean"
        self.assertEqual(
            ttl_fmt(True, type_name),
            "'true'^^xsd:boolean",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt("anything", type_name, '"'),
            '"true"^^xsd:boolean',
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(False, type_name, '"'),
            '"false"^^xsd:boolean',
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(0, type_name),
            "'false'^^xsd:boolean",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(None, type_name),
            "'false'^^xsd:boolean",
            "bad %s format" % type_name,
        )

    def test_int(self):
        type_name = "xsd:integer"
        self.assertEqual(
            ttl_fmt(1, type_name),
            "'1'^^xsd:integer",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(-10, type_name, '"'),
            '"-10"^^xsd:integer',
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(0, type_name, '"'),
            '"0"^^xsd:integer',
            "bad %s format" % type_name,
        )

        with self.assertRaises(
            AssertionError,
            msg="leading zero's should be dealth with before formatting",
        ):
            ttl_fmt(
                "001", type_name
            )  # you should not simply assume this to become 1
        # in stead -- force int casting:
        self.assertEqual(
            ttl_fmt(int("001"), type_name),
            "'1'^^xsd:integer",
            "bad %s format" % type_name,
        )

    def test_double(self):
        type_name = "xsd:double"
        self.assertEqual(
            ttl_fmt(1.0, type_name),
            "'1.0'^^xsd:double",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt("1", type_name),
            "'1.0'^^xsd:double",
            "bad %s format" % type_name,
        )  # automatic to float
        self.assertEqual(
            ttl_fmt(1, type_name),
            "'1.0'^^xsd:double",
            "bad %s format" % type_name,
        )  # automatic to float
        self.assertEqual(
            ttl_fmt(1.00, type_name),
            "'1.0'^^xsd:double",
            "bad %s format" % type_name,
        )  # reformatting sideeffect
        # so actual forced float casting is not needed any more (but works)
        self.assertEqual(
            ttl_fmt(float(1), type_name),
            "'1.0'^^xsd:double",
            "bad %s format" % type_name,
        )

    def test_date(self):
        type_name = "xsd:date"
        val = "1970-05-06"
        values = [val, date.fromisoformat(val)]
        for v in values:
            fmt = "'" + str(v) + "'^^" + type_name

            self.assertEqual(
                ttl_fmt(v, type_name), fmt, "bad %s format" % type_name
            )

    def test_datetime(self):
        type_name = "xsd:datetime"
        val = "2021-09-30T16:25:50+02:00"
        values = [val, datetime.fromisoformat(val)]

        for v in values:
            fmt = "'" + val + "'^^" + type_name
            self.assertEqual(
                ttl_fmt(v, type_name), fmt, "bad %s format" % type_name
            )

    def test_uri(self):
        type_name = "xsd:anyURI"
        val = "https://example.org/for/testing"
        fmt = "'" + val + "'^^" + type_name
        self.assertEqual(
            ttl_fmt(val, type_name), fmt, "bad %s format" % type_name
        )

    def test_string(self):
        type_name = "xsd:string"
        self.assertEqual(
            ttl_fmt("Hello!", type_name),
            "'Hello!'^^xsd:string",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt("'", type_name, quote='"'),
            '"\'"^^xsd:string',
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt('"', type_name, quote="'"),
            "'\"'^^xsd:string",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(">'<", type_name, quote="'"),
            "'''>'<'''^^xsd:string",
            "bad %s format" % type_name,
        )
        self.assertEqual(
            ttl_fmt(">\n<", type_name, quote="'"),
            "'''>\n<'''^^xsd:string",
            "bad %s format" % type_name,
        )

    def test_lang_string(self):
        self.assertEqual(
            ttl_fmt("Hello!", "@en"),
            "'Hello!'@en",
            "bad language-string format",
        )


class TestURIFormatting(unittest.TestCase):
    def test_fn(self):
        self.assertIsNotNone(uritexpand_fmt, "function not found")
        self.assertTrue(
            isinstance(uritexpand_fmt, Callable), "function not callable"
        )

    def test_all(self):
        uri = "https://vliz.be/code/pysubyt/test/item#somepath"
        fmt = uritexpand_fmt(
            "https://vliz.be/code/pysubyt/test/item{#id}", {"id": "somepath"}
        )
        self.assertEqual(fmt, uri)


class TestRegexFormatting(unittest.TestCase):
    def test_fn(self):
        self.assertIsNotNone(regexreplace_fmt, "function not found")
        self.assertTrue(
            isinstance(regexreplace_fmt, Callable), "function not callable"
        )

    def test_all(self):
        text = "is-kept"
        fmt = regexreplace_fmt("^[^:]*:", "", "all-after-semicolon:is-kept")
        self.assertEqual(fmt, text)


class TestMapFormatting(unittest.TestCase):
    key_name = "Alpha-2 code"
    val_name = "Alpha-3 code"
    key_val = str(3)
    val_val = str(4)
    map_test = [
        {key_name: key_val, val_name: val_val},
    ]
    fmt = map_build_fmt(map_test, key_name, val_name)

    # TODO: Redo this tests.
    def test_fn(self):
        self.assertIsNotNone(map_build_fmt, "function not found")
        self.assertTrue(
            isinstance(map_build_fmt, Callable), "function not callable"
        )

    def test_all(self):
        self.assertIsInstance(self.fmt, ValueMapper)
        self.assertEqual(self.fmt._map[self.key_val], self.val_val)

    def test_add(self):
        key_name = "Alpha-5 code"
        key_val = 9
        self.fmt.add(key_name, key_val)
        self.assertDictEqual(
            self.fmt._map, self.fmt._map | {key_name: key_val}
        )

    def test_apply(self):
        key_name = "Alpha-8 code"
        self.fmt.apply(self.map_test[0], self.key_name, key_name)
        assert key_name in self.map_test[0]


if __name__ == "__main__":
    unittest.main()
