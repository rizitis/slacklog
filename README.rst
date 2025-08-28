slacklog -- Convert Slackware Changelog to various formats
**********************************************************

slacklog provides programs and a library to convert a Slackware
ChangeLog into other formats. Currently, RSS, Atom, JSON, and PyBlosxom
formats are supported.

- Source code: `https://github.com/rizitis/slacklog <https://github.com/rizitis/slacklog>`_
- Documentation: `https://slacklog.readthedocs.org <https://slacklog.readthedocs.org>`_

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

In addition to Python, `python3-dateutil` from SlackBuilds.org is required.

Python 3.12 is tested together with python3-dateutil-2.9.0.


Installation
============

Download the source archive and use the included SlackBuild.

The source code of this fork is available at
`GitHub <https://github.com/rizitis/slacklog>`_ (python3 branch).


Authors
=======

Original author: Mikko Värri (vmj@linuxbox.fi)

Current version is a fork by Ioannis Anagnostakis (rizitis):

- Modified scripts for Python 3.9+
- Removed Docker and tests


License
=======

slacklog is Free Software, licensed under the GNU General Public License (GPL),
version 3 or later. See LICENSE.txt file for details.
