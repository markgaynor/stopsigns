#!/usr/bin/env python
#
# Copyright 2001-2004 by Vinay Sajip. All Rights Reserved.
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
#
# This file is part of the Python config distribution. See
# http://www.red-dove.com/python_config.html
#
"""
A test for the config module through seeing how to use it to configure logging.

Copyright (C) 2004 Vinay Sajip. All Rights Reserved.
"""

from config import Config
from optparse import OptionParser, get_prog_name
from whrandom import choice
import logging
import logging.handlers
import sys

class Usage(Exception):
    pass

class BaseHandler:
    def __init__(self, config):
        if 'level' in config:
            self.setLevel(config.level)
        if 'formatter' in config:
            self.setFormatter(config.formatter)

class StreamHandler(logging.StreamHandler, BaseHandler):
    def __init__(self, config):
        stream = config.get('stream')
        logging.StreamHandler.__init__(self, stream)
        BaseHandler.__init__(self, config)

class RotatingFileHandler(logging.handlers.RotatingFileHandler, BaseHandler):
    def __init__(self, config):
        name = config.get('name')
        if name is None:
            raise ValueError('RotatingFileHandler: name not specified')
        mode = config.get('mode', 'a')
        maxBytes = config.get('maxBytes', 0)
        backupCount = config.get('backupCount', 0)
        logging.handlers.RotatingFileHandler.__init__(self, name, mode, maxBytes, backupCount)
        BaseHandler.__init__(self, config)

class FileHandler(logging.FileHandler, BaseHandler):
    def __init__(self, config):
        name = config.get('name')
        if name is None:
            raise ValueError('FileHandler: name not specified')
        mode = config.get('mode', 'a')
        logging.FileHandler.__init__(self, name, mode)
        BaseHandler.__init__(self, config)

def configLogger(logger, config):
    for handler in logger.handlers:
        logger.removeHandler(handler)
    if 'level' in config:
        logger.setLevel(config.level)
    if 'handlers' in config:
        for handler in config.handlers:
            logger.addHandler(handler)

def fileConfig(fname, *args, **kwargs):
    cfg = Config(fname)
    cfg.addNamespace(logging)
    cfg.addNamespace(sys.modules[StreamHandler.__module__], 'logconfig')

    for name in cfg.formatters.keys():
        formatterConfig = cfg.formatters[name]
        fmt = formatterConfig.get('format')
        datefmt = formatterConfig.get('datefmt')
        formatter = logging.Formatter(fmt, datefmt)
        cfg.formatters[name] = formatter

    for name in cfg.handlers.keys():
        klass = cfg.handlers[name].get('class')
        config = cfg.handlers[name].get('config')
        cfg.handlers[name] = klass(config)

    for name in cfg.loggers.keys():
        loggerConfig = cfg.loggers[name]
        logger = logging.getLogger(name)
        configLogger(logger, loggerConfig)

    if 'root' in cfg:
        configLogger(logging.getLogger(''), cfg.root)

def testConfig():
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    loggers = ['', 'area1', 'area2']
    for i in xrange(1000):
        logger = logging.getLogger(choice(loggers))
        level = choice(levels)
        logger.log(level, "Message number %d", i)

def main(args=None):
    rv = 0
    if args is None:
        args = sys.argv[1:]
    parser = OptionParser(usage="usage: %prog [options] CONFIG-FILE")

    (options, args) = parser.parse_args(args)
    try:
        if len(args) == 0:
            raise Usage("No configuration file specified")
        fileConfig(args[0])
        testConfig()
    except Usage, e:
        parser.print_help()
        print "\n%s: error: %s" % (get_prog_name(), e)
        rv = 1
    except Exception, e:
        print "\n%s: error: %s" % (get_prog_name(), e)
        typ, val, tb = sys.exc_info()
        import traceback
        traceback.print_tb(tb)
        rv = 2
    return rv

if __name__ == "__main__":
    sys.exit(main())
