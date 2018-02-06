This module is intended to provide configuration functionality for Python
programs.

Change History
--------------

Version   Date        Description
=============================================================================
0.3.7     05 Oct 2007 Added Mapping.__delitem__ (patch by John Drummond).
                      Mapping.__getattribute__ no longer returns "" when
                      asked for "__class__" - doing so causes pickle to
                      crash (reported by Jamila Gunawardena).
                      Allow negative numbers (reported by Gary Schoep; had
                      already been fixed but not yet released).
-----------------------------------------------------------------------------
0.3.6     09 Mar 2006 Made classes derive from object (previously they were
                      old-style classes).
                      Changed ConfigMerger to use a more flexible merge
                      strategy.
                      Multiline strings (using """ or ''') are now supported.
                      A typo involving raising a ConfigError was fixed.
                      Patches received with thanks from David Janes & Tim
                      Desjardins (BlogMatrix) and Erick Tryzelaar.
-----------------------------------------------------------------------------
0.3.5     27 Dec 2004 Added ConfigOutputStream to provide better Unicode
                      output support. Altered save code to put platform-
                      dependent newlines for Unicode.
-----------------------------------------------------------------------------
0.3.4     11 Nov 2004 Added ConfigInputStream to provide better Unicode
                      support.
                      Added ConfigReader.setStream().
-----------------------------------------------------------------------------
0.3.3     09 Nov 2004 Renamed config.get() to getByPath(), and likewise for
                      ConfigList.
                      Added Mapping.get() to work like dict.get().
                      Added logconfig.py and logconfig.cfg to distribution.
-----------------------------------------------------------------------------
0.3.2     04 Nov 2004 Simplified parseMapping().
                      Allowed Config.__init__ to accept a string as well as a
                      stream. If a string is passed in, streamOpener is used
                      to obtain the stream to be used.
-----------------------------------------------------------------------------
0.3.1     04 Nov 2004 Changed addNamespace/removeNamespace to make name
                      specification easier.
                      Refactored save(), added Container.writeToStream and
                      Container.writeValue() to help with this.
-----------------------------------------------------------------------------
0.3       03 Nov 2004 Added test harness (test_config.py)
                      Fixed bugs in bracket parsing.
                      Refactored internal classes.
                      Added merging functionality.
-----------------------------------------------------------------------------
0.2       01 Nov 2004 Added support for None.
                      Stream closed in load() and save().
                      Added support for changing configuration.
                      Fixed bugs in identifier parsing and isword().
-----------------------------------------------------------------------------
0.1       31 Oct 2004 Initial implementation (for community feedback)
-----------------------------------------------------------------------------

-----------------------------------------------------------------------------
COPYRIGHT
-----------------------------------------------------------------------------
Copyright 2004-2006 by Vinay Sajip. All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Vinay Sajip
not be used in advertising or publicity pertaining to distribution
of the software without specific, written prior permission.
VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
