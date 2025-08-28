"""
SlackLog models
===============

SlackLog models represent the ChangeLog.txt after parsing.
"""

from datetime import datetime, tzinfo


class SlackLog:
    """
    Container for SlackLogEntry objects.
    """

    def __init__(self):
        self.entries = []
        """List of SlackLogEntry objects."""
        self.startsWithSeparator = False
        """True if the log started with an entry separator."""
        self.endsWithSeparator = False
        """True if the log ended with an entry separator."""


class SlackLogEntry:
    """
    Represents a single entry in a SlackLog.
    """

    def __init__(self, timestamp: datetime, description: str, log: SlackLog,
                 checksum: str = None, identifier: str = None, parent: str = None,
                 timezone: tzinfo = None, twelveHourFormat: bool = None):

        assert isinstance(timestamp, datetime)
        assert timestamp.tzinfo is not None  # allow any timezone
        assert isinstance(description, str)
        assert isinstance(log, SlackLog)
        if checksum is not None:
            assert isinstance(checksum, str)
        if identifier is not None:
            assert isinstance(identifier, str)
        if parent is not None:
            assert isinstance(parent, str)
        if timezone is not None:
            assert isinstance(timezone, tzinfo)

        self.timestamp = timestamp
        """Timestamp of the entry (with timezone)."""
        self.description = description
        """Description of the entry."""
        self.log = log
        """Reference to the parent SlackLog."""
        self.checksum = checksum
        """SHA512 checksum identifying the entry."""
        self.identifier = identifier
        """SHA512 identifier including parent info."""
        self.parent = parent
        """Identifier of the parent entry."""
        self.timezone = timezone
        """Original timezone of the entry."""
        self.twelveHourFormat = twelveHourFormat
        """True if the original timestamp was 12-hour format."""
        self.pkgs = []
        """List of SlackLogPkg objects contained in this entry."""


class SlackLogPkg:
    """
    Represents a single package in a SlackLogEntry.
    """

    def __init__(self, pkg: str, description: str, entry: SlackLogEntry):
        assert isinstance(pkg, str)
        assert isinstance(description, str)
        assert isinstance(entry, SlackLogEntry)

        self.pkg = pkg
        """Package identifier."""
        self.description = description
        """Package description."""
        self.entry = entry
        """Reference to the parent SlackLogEntry."""
