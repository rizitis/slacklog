# -*- coding: utf-8 -*-
"""
SlackLog formatters
===================

SlackLog formatter takes an in-memory representation of a Slackware ChangeLog.txt and produces different
representations of it (TXT, RSS, Atom, JSON).
"""

import datetime
import re
from json import dumps
from dateutil import tz
from slacklog.models import SlackLog, SlackLogEntry, SlackLogPkg


def readable(d: datetime.datetime) -> str:
    return d.strftime("%a, %d %b %Y %H:%M:%S GMT")


def anchor(d: datetime.datetime) -> str:
    return d.strftime("%Y%m%dT%H%M%SZ")


class SlackLogFormatter:
    """
    Base class for SlackLog formatters.
    """

    def __init__(self):
        self.max_entries = None
        self.max_pkgs = None

    def format(self, log: SlackLog) -> str:
        data = ''
        data += self.format_log_preamble(log)
        data += self.format_list(log.entries, self.format_entry, self.max_entries)
        data += self.format_log_postamble(log)
        return data

    def format_log_preamble(self, log: SlackLog) -> str:
        return ''

    def format_log_postamble(self, log: SlackLog) -> str:
        return ''

    def format_entry(self, entry: SlackLogEntry, is_first: bool, is_last: bool) -> str:
        data = ''
        data += self.format_entry_separator(is_first, is_last)
        data += self.format_entry_preamble(entry)
        data += self.format_list(entry.pkgs, self.format_pkg, self.max_pkgs)
        data += self.format_entry_postamble(entry)
        return data

    def format_entry_separator(self, is_first: bool, is_last: bool) -> str:
        return ''

    def format_entry_preamble(self, entry: SlackLogEntry) -> str:
        return ''

    def format_entry_postamble(self, entry: SlackLogEntry) -> str:
        return ''

    def format_pkg(self, pkg: SlackLogPkg, is_first: bool, is_last: bool) -> str:
        data = ''
        data += self.format_pkg_separator(is_first, is_last)
        data += self.format_pkg_preamble(pkg)
        data += self.format_pkg_postamble(pkg)
        return data

    def format_pkg_separator(self, is_first: bool, is_last: bool) -> str:
        return ''

    def format_pkg_preamble(self, pkg: SlackLogPkg) -> str:
        return ''

    def format_pkg_postamble(self, pkg: SlackLogPkg) -> str:
        return ''

    def format_list(self, items, item_formatter, max_items=None) -> str:
        data = ''
        num_items = len(items)
        if max_items is not None:
            num_items = min(num_items, max_items)
        for i in range(num_items):
            data += item_formatter(items[i], i == 0, i == num_items - 1)
        return data


class SlackLogTxtFormatter(SlackLogFormatter):
    """Recreate original ChangeLog.txt format."""

    def format_log_preamble(self, log: SlackLog) -> str:
        return '+--------------------------+\n' if log.startsWithSeparator else ''

    def format_log_postamble(self, log: SlackLog) -> str:
        return '+--------------------------+\n' if log.endsWithSeparator else ''

    def format_entry_separator(self, is_first: bool, is_last: bool) -> str:
        return '+--------------------------+\n' if not is_first else ''

    def format_entry_preamble(self, entry: SlackLogEntry) -> str:
        timestamp = entry.timestamp
        if entry.timezone and not isinstance(entry.timezone, tz.tzutc):
            timestamp = timestamp.astimezone(entry.timezone)
        if entry.twelveHourFormat:
            data = timestamp.strftime("%a %d %b %Y %I:%M:%S %p %Z")
        else:
            data = timestamp.strftime("%a %b %d %H:%M:%S %Z %Y")
            data = re.sub(r' 0(\d) ', r'  \1 ', data)
        data += '\n'
        if entry.description:
            data += entry.description
        return data

    def format_pkg_preamble(self, pkg: SlackLogPkg) -> str:
        return f"{pkg.pkg}:{pkg.description}"


class SlackLogRssFormatter(SlackLogFormatter):
    """Generate an RSS feed from SlackLog."""

    def __init__(self):
        super().__init__()
        self.slackware = None
        self.rssLink = None
        self.webLink = None
        self.description = None
        self.language = None
        self.managingEditor = None
        self.webMaster = None
        self.lastBuildDate = None

    def format_log_preamble(self, log: SlackLog) -> str:
        data = '<?xml version="1.0"?>\n'
        data += '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        data += '  <channel>\n'
        data += f'    <atom:link href="{self.rssLink}" rel="self" type="application/rss+xml" />\n'
        data += f'    <title>{self.slackware} ChangeLog</title>\n'
        link = self.webLink or self.rssLink
        data += f'    <link>{link}</link>\n'
        if self.description:
            data += f'    <description>{self.description}</description>\n'
        data += '    <docs>http://www.rssboard.org/rss-specification</docs>\n'
        data += f'    <language>{self.language}</language>\n'
        if self.managingEditor:
            data += f'    <managingEditor>{self.managingEditor}</managingEditor>\n'
        if self.webMaster:
            data += f'    <webMaster>{self.webMaster}</webMaster>\n'
        pub_date = readable(log.entries[0].timestamp) if log.entries else readable(self.lastBuildDate or datetime.datetime.utcnow())
        data += f'    <pubDate>{pub_date}</pubDate>\n'
        last_build = readable(self.lastBuildDate or datetime.datetime.utcnow())
        data += f'    <lastBuildDate>{last_build}</lastBuildDate>\n'
        data += '    <generator>SlackLog</generator>\n'
        return data

    def format_log_postamble(self, log: SlackLog) -> str:
        return '  </channel>\n</rss>\n'

    def format_entry_preamble(self, entry: SlackLogEntry) -> str:
        data = '    <item>\n'
        link = f"{self.webLink}#{anchor(entry.timestamp)}" if self.webLink else f"{self.slackware.replace(' ', '-')}-{anchor(entry.timestamp)}"
        perma = 'true' if self.webLink else 'false'
        data += f'      <guid isPermaLink="{perma}">{link}</guid>\n'
        data += f'      <title>{self.slackware} changes for {readable(entry.timestamp)}</title>\n'
        data += f'      <pubDate>{readable(entry.timestamp)}</pubDate>\n'
        data += '      <description><![CDATA[<pre>'
        if entry.description:
            data += entry.description.replace('<', '&lt;')
        return data

    def format_entry_postamble(self, entry: SlackLogEntry) -> str:
        return '</pre>]]></description>\n    </item>\n'

    def format_pkg_preamble(self, pkg: SlackLogPkg) -> str:
        return f"{pkg.pkg}:{pkg.description.replace('<', '&lt;')}"


class SlackLogJsonFormatter(SlackLogFormatter):
    """Generate JSON output from SlackLog."""

    def format(self, log: SlackLog) -> str:
        return dumps(
            log,
            default=self.json_default,
            indent=getattr(self, 'indent', 4),
            separators=(',', ':')  # <- removes spaces after colon
        )

    def json_default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, SlackLog):
            return {
                'entries': obj.entries,
                'startsWithSeparator': obj.startsWithSeparator,
                'endsWithSeparator': obj.endsWithSeparator
            }
        if isinstance(obj, SlackLogEntry):
            tz_obj = getattr(obj, 'timezone', None)
            tz_name = tz_obj.tzname(obj.timestamp) if tz_obj else None
            return {
                'timestamp': obj.timestamp,
                'timezone': tz_name,
                'description': obj.description,
                'pkgs': obj.pkgs,
                'checksum': getattr(obj, 'checksum', None),
                'identifier': getattr(obj, 'identifier', None),
                'parent': getattr(obj, 'parent', None)
            }
        if isinstance(obj, SlackLogPkg):
            return {
                'pkg': obj.pkg,
                'description': obj.description
            }
        return str(obj)

class SlackLogAtomFormatter(SlackLogFormatter):
    """Minimal Atom feed formatter stub for compatibility."""

    def format(self, log: SlackLog) -> str:
        return "<feed></feed>"
