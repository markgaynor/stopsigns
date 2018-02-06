from distutils.core import setup

setup(name = "config",
   description="A hierarchical, easy-to-use, powerful configuration module for Python",
   long_description = """This module allows a hierarchical configuration scheme with support for mappings
and sequences, cross-references between one part of the configuration and
another, the ability to flexibly access real Python objects without full-blown
eval(), an include facility, simple expression evaluation and the ability to
change, save, cascade and merge configurations. Interfaces easily with
environment variables and command-line options. It has been developed on python
2.3 but should work on version 2.2 or greater.""",
   license="""Copyright (C) 2004-2007 by Vinay Sajip. All Rights Reserved. See LICENSE for license.""",
            version = "0.3.7",
            author = "Vinay Sajip",
            author_email = "vinay_sajip@red-dove.com",
            maintainer = "Vinay Sajip",
            maintainer_email = "vinay_sajip@red-dove.com",
            url = "http://www.red-dove.com/python_config.html",
            py_modules = ["config"],
            )
