.. image:: https://img.shields.io/pypi/v/slacklog.svg?style=plastic
   :target: https://pypi.python.org/pypi/slacklog
   :alt: Download
.. image:: https://travis-ci.org/vmj/slacklog.svg?branch=master
   :target: https://travis-ci.org/vmj/slacklog
   :alt: Build Status
.. image:: https://readthedocs.org/projects/slacklog/badge/?version=latest
   :target: https://slacklog.readthedocs.io/en/latest/?badge=latest
   :alt: Docs

slacklog -- Convert Slackware Changelog to various formats
**********************************************************

slacklog provides programs and a library to convert a Slackware
ChangeLogs into other formats.  Currently, RSS, Atom, JSON, and PyBlosxom
formats are supported.

| Source code: https://github.com/rizitis/slacklog 
| Documentation: https://slacklog.readthedocs.org

.. contents::


Basic usage
===========

Typical usage of the program looks like this::

    $ slacklog2rss --changelog slackware-current/ChangeLog.txt \
                   --encoding iso8859-1 \
                   --out ~/public_html/slackware-current.rss \
                   --slackware "Slackware current" \
                   --rssLink "http://linuxbox.fi/~vmj/slackware-current.rss" \
                   --description "Slackware current activity" \
                   --managingEditor "vmj@linuxbox.fi (Mikko Värri)" \
                   --webMaster "vmj@linuxbox.fi (Mikko Värri)"


Requirements
============

In addition to Python, `python3-dateutil
from SBo is required.

Python versions 3.12 are tested, together with python3-dateutil-2.9.0


Installation
============

Download the source archive and
use the included SlackBuild.

The source code of this fork is available at 
`Github <https://github.com/rizitis/slacklog>`_
git repository in the python3 branch.





Authors
=======

Original author is Mikko Värri
(vmj@linuxbox.fi).

This version is a fork of [slacklog](https://github.com/vmj/slacklog).
Modifications made by Ioannis Anagnostakis (rizitis):
- Modified scripts for python3.9+
- Removed test.


License
=======

slacklog is Free Software, licensed under GNU General Public License
(GPL), version 3 or later.  See LICENSE.txt file for details.
