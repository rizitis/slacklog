# -*- coding: utf-8 -*-
"""
SlackLog scripts
================

SlackLog scripts provides CLI (command line interface) for the SlackLog parsers and formatters.
"""

import locale
from optparse import OptionParser
import slacklog
from slacklog.parsers import SlackLogParser
from slacklog.formatters import (
    SlackLogAtomFormatter,
    SlackLogRssFormatter,
    SlackLogTxtFormatter,
    SlackLogPyblosxomFormatter,
    SlackLogJsonFormatter
)
import sys
import codecs

def u(s):
    """Ensure that a command line option argument is str (Unicode in Python 3)."""
    return s

def i(s):
    """Ensure that a command line option argument is int."""
    return int(s) if s else None

def read(changelog, encoding):
    """Reads the ChangeLog.txt and returns text as a string."""
    try:
        with codecs.open(changelog, 'r', encoding) as f:
            return f.read()
    except IOError as e:
        print(f"{e.filename}: {e.strerror}", file=sys.stderr)
        sys.exit(e.errno)
    except UnicodeDecodeError as e:
        print(f"{changelog}: {e.start}-{e.end}: {e.encoding}: {e.reason}", file=sys.stderr)
        sys.exit(-1)

def write(out, data, encoding='utf-8'):
    """Writes data to a file using UTF-8 encoding by default."""
    try:
        with codecs.open(out, 'w', encoding) as f:
            f.write(data)
    except UnicodeEncodeError as e:
        print(f"{out}: {e.start}-{e.end}: {data[e.start:e.end]}: {e.reason}", file=sys.stderr)
        sys.exit(-1)

def main(**kwargs):
    """Common CLI handling for SlackLog scripts."""
    kwargs['usage'] = ''
    kwargs['version'] = f"%prog {slacklog.__version__}"
    kwargs['epilog'] = ('Bug reports, suggestions, and patches should be sent to vmj@linuxbox.fi. '
                        'This software is Free Software, released under GPLv3.')

    options = kwargs.pop('options', {})
    mandatory = []

    for option, optionSpec in options.items():
        if optionSpec.pop('mandatory', False):
            kwargs['usage'] += f" --{option} {optionSpec['metavar']}"
            mandatory.append(option)

    kwargs['usage'] = f"USAGE: %prog [options]{kwargs['usage']}"
    parser = OptionParser(**kwargs)

    for option, optionSpec in options.items():
        parser.add_option(f"--{option}", **optionSpec)

    opts, args = parser.parse_args()

    missing = [option for option in mandatory if getattr(opts, option, None) is None]
    if missing:
        parser.error(f"Missing required option(s): {', '.join(missing)}")

    return opts, args

# Example: slacklog2atom
def slacklog2atom():
    opts, args = main(
        description='Convert Slackware ChangeLog to Atom',
        options={
            'changelog': {'help': 'Read input from FILE', 'metavar': 'FILE', 'mandatory': True},
            'encoding': {'help': 'ChangeLog encoding [default: iso8859-1]', 'default': 'iso8859-1'},
            'min_date': {'help': 'Last date to include [default: include all]', 'metavar': 'DATE'},
            'out': {'help': 'Write output to FILE', 'metavar': 'FILE', 'mandatory': True},
            'quiet': {'help': 'Do not print warnings', 'action': 'store_true'},
            'max_entries': {'help': 'Max number of Atom entries [default: infinity]', 'metavar': 'NUM'},
            'slackware': {'help': 'Slackware version [default: Slackware 13.1]', 'default': 'Slackware 13.1'},
            'link': {'help': 'Full URL of the Atom feed', 'metavar': 'URL', 'mandatory': True},
            'webLink': {'help': 'Full URL of the HTML version', 'metavar': 'URL'},
            'name': {'help': 'NAME of the feed author', 'metavar': 'NAME'},
            'email': {'help': 'EMAIL of the feed author', 'metavar': 'EMAIL'},
            'updated': {'help': 'Timestamp when this feed was last generated', 'metavar': 'DATE'}
        }
    )

    parser = SlackLogParser()
    parser.quiet = opts.quiet
    parser.min_date = parser.parse_date(u(opts.min_date))

    formatter = SlackLogAtomFormatter()
    formatter.max_entries = i(opts.max_entries)
    formatter.slackware = u(opts.slackware)
    formatter.link = u(opts.link)
    formatter.webLink = u(opts.webLink)
    formatter.name = u(opts.name)
    formatter.email = u(opts.email)
    formatter.updated = parser.parse_date(u(opts.updated))

    txt = read(opts.changelog, opts.encoding)
    atom = formatter.format(parser.parse(txt))
    write(opts.out, atom)
