"""
SlackLog parsers
================

SlackLog parser takes a string representation of a Slackware ChangeLog.txt and produces an in-memory representation
of it.

The in-memory representation is an instance of :any:`SlackLog`.
"""

import re
import hashlib
from dateutil import parser, tz
from slacklog.models import SlackLog, SlackLogEntry, SlackLogPkg
from codecs import encode
import sys

# Package name regex: starts from the beginning of line, colon + double space, must look like file name
pkg_name_re = re.compile(r'\A[-a-zA-Z0-9_]+[/.][-a-zA-Z0-9_+/.]*[*]?:  ')

# Regex to detect AM/PM (12-hour) timestamps
am_pm_re = re.compile(r' [AaPp][Mm]? ')

# Timezone mapping
tzinfos = {
    'CDT': -5 * 60 * 60,
    'CST': -6 * 60 * 60,
    'UTC': 0,
}

class SlackLogParser:
    """
    Parser for Slackware ChangeLog.txt files.
    Works for Slackware 12.x and newer.
    """

    def __init__(self):
        self.quiet = False
        """If True, warnings about date parsing are not printed."""
        self.min_date = None
        """If set to a datetime object, older log entries are ignored."""
        self.ENTRY = 0
        """Counter of entries (debugging)."""
        self.PKG = 0
        """Counter of packages (debugging)."""

    def parse(self, data):
        """Return SlackLog object representing parsed data."""
        assert isinstance(data, str)
        log = SlackLog()
        log.startsWithSeparator = bool(re.match(r'\A(\+-+\+[\n]?)', data))
        log.endsWithSeparator = bool(re.search(r'[\n](\+-+\+[\n]?)\Z', data))

        # Safely remove starting separator if present
        m_start = re.match(r'\A(\+-+\+[\n]?)', data)
        if m_start:
            data = data[m_start.end():]

        # Safely remove ending separator if present
        m_end = re.search(r'[\n](\+-+\+[\n]?)\Z', data)
        if m_end:
            data = data[:m_end.start(1)]

        for entry_data in self.split_log_to_entries(data):
            entry = self.parse_entry(entry_data, log)
            if entry:
                log.entries.insert(0, entry)
        return log

    def split_log_to_entries(self, data):
        """Split the ChangeLog into individual entries."""
        assert isinstance(data, str)
        raw_entries = re.split(r'\+-+\+', data)
        entries = [entry.lstrip() for entry in raw_entries if entry.strip()]
        entries.reverse()
        return entries

    def parse_entry(self, data, log):
        """Parse a single entry."""
        assert isinstance(data, str)
        assert isinstance(log, SlackLog)
        self.ENTRY += 1
        self.PKG = 0

        checksum = self.gen_entry_checksum(data)
        parent = log.entries[0].identifier if log.entries else None
        identifier = self.gen_entry_identifier(data, checksum, parent)

        timestamp, timezone, twelve_hour, data = self.parse_entry_timestamp(data)
        if self.min_date and self.min_date > timestamp:
            return None

        description, data = self.parse_entry_description(data)
        entry = SlackLogEntry(timestamp, description, log, checksum=checksum,
                              identifier=identifier, parent=parent,
                              timezone=timezone, twelveHourFormat=twelve_hour)

        for pkg_data in self.split_entry_to_pkgs(data):
            pkg = self.parse_pkg(pkg_data, entry)
            entry.pkgs.append(pkg)
        return entry

    def gen_entry_checksum(self, data):
        """Generate SHA512 checksum of entry."""
        assert isinstance(data, str)
        return hashlib.sha512(data.encode('utf-8')).hexdigest()

    def gen_entry_identifier(self, data, checksum, parent):
        """Generate SHA512 identifier for entry."""
        combined = (parent + checksum) if parent else checksum
        return hashlib.sha512(combined.encode('utf-8')).hexdigest()

    def parse_entry_timestamp(self, data):
        """Parse timestamp of entry and return timestamp, timezone, 12-hour flag, and remaining data."""
        assert isinstance(data, str)
        timestamp_str, data = self.get_line(data)
        timestamp, timezone = self.parse_date_with_timezone(timestamp_str)
        twelve_hour = bool(am_pm_re.search(timestamp_str))
        return timestamp, timezone, twelve_hour, data

    def parse_entry_description(self, data):
        """Parse entry description and return description + remaining data."""
        assert isinstance(data, str)
        description = ''
        while data and not pkg_name_re.match(data):
            line, data = self.get_line(data)
            description += line
        return description, data

    def split_entry_to_pkgs(self, data):
        """Split entry content into package blocks."""
        assert isinstance(data, str)
        if not data.strip():
            return []
        pkgs = []
        pkg_lines = []
        for line in data.split('\n'):
            if not pkg_name_re.match(line):
                pkg_lines.append(line)
            else:
                if pkg_lines:
                    pkgs.append('\n'.join(pkg_lines) + '\n')
                    pkg_lines = []
                if line:
                    pkg_lines.append(line)
        if pkg_lines:
            pkgs.append('\n'.join(pkg_lines))
        return pkgs

    def parse_pkg(self, data, entry):
        """Parse a package from a block of text."""
        assert isinstance(data, str)
        assert isinstance(entry, SlackLogEntry)
        self.PKG += 1
        try:
            pkg, data = self.parse_pkg_name(data)
        except ValueError:
            print(f"data: '{data[:50]}...'", file=sys.stderr)
            raise
        description = self.parse_pkg_description(data)
        return SlackLogPkg(pkg, description, entry)

    def parse_pkg_name(self, data):
        """Extract package name and description from a line."""
        assert isinstance(data, str)
        return data.split(':', 1)

    def parse_pkg_description(self, data):
        """Return package description."""
        assert isinstance(data, str)
        return data

    def get_line(self, data):
        """Consume and return first line + remainder."""
        assert isinstance(data, str)
        if '\n' in data:
            line, rest = data.split('\n', 1)
            return line + '\n', rest
        return data, ''

    def parse_date(self, data):
        """Parse date string to datetime in UTC."""
        if data is None:
            return None
        timestamp, _ = self.parse_date_with_timezone(data)
        return timestamp

    def parse_date_with_timezone(self, data):
        """Parse date string to datetime + original tzinfo."""
        if data is None:
            return None
        assert isinstance(data, str)
        timestamp = parser.parse(data, tzinfos=tzinfos)
        timezone = timestamp.tzinfo

        if timezone is None:
            if not self.quiet:
                sys.stderr.write(f"Warning: Assuming UTC, input was '{data}'\n")
            timestamp = timestamp.replace(tzinfo=tz.tzutc())
        elif timestamp.tzinfo.utcoffset(timestamp).total_seconds() != 0:
            tzname = timezone.tzname(timestamp)
            if not self.quiet and tzname not in tzinfos:
                sys.stderr.write(f"Warning: Converting '{tzname}' to UTC\n")
            timestamp = timestamp.astimezone(tz.tzutc())
        return timestamp, timezone
