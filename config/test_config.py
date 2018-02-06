# Copyright 2004-2006 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Test harness for the configuration module 'config' for Python.
"""

import unittest
from test import test_support
import config
from config import Config, ConfigMerger, ConfigList
from config import ConfigError, ConfigFormatError, ConfigResolutionError
from StringIO import StringIO

STREAMS = {
    "simple_1" :
"""
message: 'Hello, world!'
""",
    "malformed_1" :
"""
123
""",
    "malformed_2" :
"""
[ 123, 'abc' ]
""",
    "malformed_3" :
"""
{ a : 7, b : 1.3, c : 'test' }
""",
    "malformed_4" :
"""
test: $a [7] # note space before bracket
""",
    "malformed_5" :
"""
test: 'abc'
test: 'def'
""",
    "wellformed_1" :
"""
test: $a[7] # note no space before bracket
""",
    "boolean_1":
"""
test : False
another_test: True
""",
    "boolean_2":
"""
test : false
another_test: true
""",
    "none_1":
"""
test : None
""",
    "none_2":
"""
test : none
""",
    "number_1":
"""
root: 1
stream: 1.7
""",
    "include_1":
"""
included: @'include_2'
""",
    "include_2":
"""
test: 123
another_test: 'abc'
""",
    "expr_1":
"""
value1 : 10
value2 : 5
value3 : 'abc'
value4 : 'ghi'
value5 : 0
value6 : { 'a' : $value1, 'b': $value2 }
derived1 : $value1 + $value2
derived2 : $value1 - $value2
derived3 : $value1 * $value2
derived4 : $value1 / $value2
derived5 : $value1 % $value2
derived6 : $value3 + $value4
derived7 : $value3 + 'def' + $value4
derived8 : $value3 - $value4 # meaningless
derived9 : $value1 / $value5    # div by zero
derived10 : $value1 % $value5   # div by zero
derived11 : $value17    # doesn't exist
derived12 : $value6.a + $value6.b
""",
    "eval_1":
"""
stderr : `sys.stderr`
stdout : `sys.stdout`
stdin : `sys.stdin`
debug : `debug`
DEBUG : `DEBUG`
derived: $DEBUG * 10
""",
    "merge_1":
"""
value1: True
value3: [1, 2, 3]
value5: [ 7 ]
value6: { 'a' : 1, 'c' : 3 }
""",
    "merge_2":
"""
value2: False
value4: [4, 5, 6]
value5: ['abc']
value6: { 'b' : 2, 'd' : 4 }
""",
    "merge_3":
"""
value1: True
value2: 3
value3: [1, 3, 5]
value4: [1, 3, 5]
""",
    "merge_4":
"""
value1: False
value2: 4
value3: [2, 4, 6]
value4: [2, 4, 6]
""",
    "list_1":
"""
verbosity : 1
""",
    "list_2":
"""
verbosity : 2
program_value: 4
""",
    "list_3":
"""
verbosity : 3
suite_value: 5
""",
    "get_1":
"""
value1 : 123
value2 : 'abcd'
value3 : True
value4 : None
value5:
{
    value1 : 123
    value2 : 'abcd'
    value3 : True
    value4 : None
}
""",
    "multiline_1":
"""
value1: '''Value One
Value Two
'''
value2: \"\"\"Value Three
Value Four\"\"\"
"""
}

def makeStream(name):
    s = StringIO(STREAMS[name])
    s.name = name
    return s

class OutStream(StringIO):
    def close(self):
        self.value = self.getvalue()
        StringIO.close(self)

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.cfg = Config(None)

    def tearDown(self):
        del self.cfg

    def testCreation(self):
        self.assertEqual(0, len(self.cfg))  # should be empty

    def testSimple(self):
        self.cfg.load(makeStream("simple_1"))
        self.failUnless('message' in self.cfg)
        self.failIf('root' in self.cfg)
        self.failIf('stream' in self.cfg)
        self.failIf('load' in self.cfg)
        self.failIf('save' in self.cfg)

    def testValueOnly(self):
        self.assertRaises(ConfigError, self.cfg.load,
           makeStream("malformed_1"))
        self.assertRaises(ConfigError, self.cfg.load,
           makeStream("malformed_2"))
        self.assertRaises(ConfigError, self.cfg.load,
           makeStream("malformed_3"))

    def testBadBracket(self):
        self.assertRaises(ConfigError, self.cfg.load,
           makeStream("malformed_4"))

    def testDuplicate(self):
        self.assertRaises(ConfigError, self.cfg.load,
           makeStream("malformed_5"))

    def testGoodBracket(self):
        self.cfg.load(makeStream("wellformed_1"))

    def testBoolean(self):
        self.cfg.load(makeStream("boolean_1"))
        self.assertEqual(True, self.cfg.another_test)
        self.assertEqual(False, self.cfg.test)

    def testNotBoolean(self):
        self.cfg.load(makeStream("boolean_2"))
        self.assertEqual('true', self.cfg.another_test)
        self.assertEqual('false', self.cfg.test)

    def testNone(self):
        self.cfg.load(makeStream("none_1"))
        self.assertEqual(None, self.cfg.test)

    def testNotNone(self):
        self.cfg.load(makeStream("none_2"))
        self.assertEqual('none', self.cfg.test)

    def testNumber(self):
        self.cfg.load(makeStream("number_1"))
        self.assertEqual(1, self.cfg.root)
        self.assertEqual(1.7, self.cfg.stream)

    def testChange(self):
        self.cfg.load(makeStream("simple_1"))
        self.cfg.message = 'Goodbye, cruel world!'
        self.assertEqual('Goodbye, cruel world!', self.cfg.message)

    def testSave(self):
        self.cfg.load(makeStream("simple_1"))
        self.cfg.message = 'Goodbye, cruel world!'
        out = OutStream()
        self.cfg.save(out)
        self.assertEqual("message : 'Goodbye, cruel world!'" + config.NEWLINE,
           out.value)

    def testInclude(self):
        config.streamOpener = makeStream
        self.cfg = Config("include_1")
        config.streamOpener = config.defaultStreamOpener
        out = OutStream()
        self.cfg.save(out)
        s = "included :%s{%s  test : 123%s  another_test : 'abc'%s}%s" % (5 *
           (config.NEWLINE,))
        self.assertEqual(s, out.value)

    def testExpression(self):
        self.cfg.load(makeStream("expr_1"))
        self.assertEqual(15, self.cfg.derived1)
        self.assertEqual(5, self.cfg.derived2)
        self.assertEqual(50, self.cfg.derived3)
        self.assertEqual(2, self.cfg.derived4)
        self.assertEqual(0, self.cfg.derived5)
        self.assertEqual('abcghi', self.cfg.derived6)
        self.assertEqual('abcdefghi', self.cfg.derived7)
        self.assertRaises(TypeError, lambda x: x.derived8, self.cfg)
        self.assertRaises(ZeroDivisionError, lambda x: x.derived9, self.cfg)
        self.assertRaises(ZeroDivisionError, lambda x: x.derived10, self.cfg)
        self.assertRaises(ConfigResolutionError,
           lambda x: x.derived11, self.cfg)
        self.assertEqual(15, self.cfg.derived12)

    def testEval(self):
        import sys, logging
        self.cfg.load(makeStream("eval_1"))
        self.assertEqual(sys.stderr, self.cfg.stderr)
        self.assertEqual(sys.stdout, self.cfg.stdout)
        self.assertEqual(sys.stdin, self.cfg.stdin)
        self.assertRaises(ConfigResolutionError, lambda x: x.debug, self.cfg)
        self.cfg.addNamespace(logging.Logger)
        self.assertEqual(logging.Logger.debug.im_func, self.cfg.debug)
        self.assertRaises(ConfigResolutionError, lambda x: x.DEBUG, self.cfg)
        self.cfg.addNamespace(logging)
        self.assertEqual(logging.DEBUG, self.cfg.DEBUG)
        self.cfg.removeNamespace(logging.Logger)
        self.assertEqual(logging.debug, self.cfg.debug)
        self.assertEqual(logging.DEBUG * 10, self.cfg.derived)

    def testFunctions(self):
        makePath = config.makePath
        isWord = config.isWord
        self.assertEqual('suffix', makePath('', 'suffix'))
        self.assertEqual('suffix', makePath(None, 'suffix'))
        self.assertEqual('prefix.suffix', makePath('prefix', 'suffix'))
        self.assertEqual('prefix[1]', makePath('prefix', '[1]'))
        self.failUnless(isWord('a9'))
        self.failUnless(isWord('9a'))    #perverse, but there you go
        self.failIf(isWord(9))
        self.failIf(isWord(None))
        self.failIf(isWord(self))
        self.failIf(isWord(''))

    def testMerge(self):
        cfg1 = Config()
        cfg1.load(makeStream("merge_1"))
        cfg2 = Config(makeStream("merge_2"))
        ConfigMerger().merge(cfg1, cfg2)
        merged = cfg1
        cfg1 = Config()
        cfg1.load(makeStream("merge_1"))
        for i in xrange(0, 5):
            key = 'value%d' % (i + 1,)
            self.failUnless(key in merged)
        self.assertEqual(len(cfg1.value5) + len(cfg2.value5),
           len(merged.value5))
        cfg3 = Config()
        cfg3.load(makeStream("merge_3"))
        cfg4 = Config(makeStream("merge_4"))
        merger = ConfigMerger()
        self.assertRaises(ConfigError, merger.merge, cfg3, cfg4)

        cfg3 = Config(makeStream("merge_3"))
        cfg4 = Config(makeStream("merge_4"))
        merger = ConfigMerger(config.overwriteMergeResolve)
        merger.merge(cfg3, cfg4)
        self.assertEqual(False, cfg3['value1'])
        self.assertEqual(4, cfg3['value2'])

        def customMergeResolve(map1, map2, key):
            if key == "value3":
                rv = "overwrite"
            else:
                rv = config.overwriteMergeResolve(map1, map2, key)
            return rv

        cfg3 = Config(makeStream("merge_3"))
        cfg4 = Config(makeStream("merge_4"))
        merger = ConfigMerger(customMergeResolve)
        merger.merge(cfg3, cfg4)
        self.assertEqual("[2, 4, 6]", str(cfg3.value3))
        self.assertEqual("[1, 3, 5, 2, 4, 6]", str(cfg3.value4))

    def testList(self):
        list = ConfigList()
        list.append(Config(makeStream("list_1")))
        list.append(Config(makeStream("list_2")))
        list.append(Config(makeStream("list_3")))
        self.assertEqual(1, list.getByPath('verbosity'))
        self.assertEqual(4, list.getByPath('program_value'))
        self.assertEqual(5, list.getByPath('suite_value'))
        self.assertRaises(ConfigError, list.getByPath, 'nonexistent_value')

    def testGet(self):
        cfg = self.cfg
        cfg.load(makeStream("get_1"))
        self.assertEqual(123, cfg.get('value1'))
        self.assertEqual(123, cfg.get('value1', -123))
        self.assertEqual(-123, cfg.get('value11', -123))
        self.assertEqual('abcd', cfg.get('value2'))
        self.failUnless(cfg.get('value3'))
        self.failIf(cfg.get('value4') is not None)
        self.assertEqual(123, cfg.value5.get('value1'))
        self.assertEqual(123, cfg.value5.get('value1', -123))
        self.assertEqual(-123, cfg.value5.get('value11', -123))
        self.assertEqual('abcd', cfg.value5.get('value2'))
        self.failUnless(cfg.value5.get('value3'))
        self.failIf(cfg.value5.get('value4') is not None)

    def testMultiline(self):
        cfg = self.cfg
        cfg.load(makeStream("multiline_1"))
        self.assertEqual("Value One\nValue Two\n", cfg.get('value1'))
        self.assertEqual("Value Three\nValue Four", cfg.get('value2'))

def test_main():
    #unittest.main()
    test_support.run_unittest(TestConfig)

if __name__ == "__main__":
    test_main()
