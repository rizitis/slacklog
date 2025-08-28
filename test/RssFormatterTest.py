# coding=utf-8
import unittest
import os
import filecmp
import shutil
from slacklog.scripts import read, write
from slacklog.parsers import SlackLogParser
from slacklog.formatters import SlackLogRssFormatter


class RssFormatterTest(unittest.TestCase):

    def setUp(self):
        self.input = './test/changelogs/'
        self.output = './test/rss-tmp/'
        self.baseline = './test/rss/'
        self.encoding = 'iso-8859-1'
        self.parser = SlackLogParser()
        self.formatter = SlackLogRssFormatter()
        self.lastBuildDate = self.parser.parse_date(read('./test/rss-timestamp', 'ascii'))
        # Ensure clean output dir
        shutil.rmtree(self.output, ignore_errors=True)
        os.mkdir(self.output)

    def tearDown(self):
        shutil.rmtree(self.output, ignore_errors=True)

    def test(self):
        self.update_rss("slackware",   "12.0",    'Wed Oct 25 15:45:46 CDT 2006')
        self.update_rss("slackware",   "12.1",    'Thu Jul 19 12:50:36 CDT 2007')
        self.update_rss("slackware",   "13.0",    'Wed May  7 16:13:31 CDT 2008')
        self.update_rss("slackware64", "13.0",    'Tue May 19 15:36:49 CDT 2009')
        self.update_rss("slackware",   "13.1",    'Mon Sep  7 20:58:42 CDT 2009')
        self.update_rss("slackware64", "13.1",    'Mon Sep  7 20:58:42 CDT 2009')
        self.update_rss("slackware",   "13.37",   'Fri Jun 18 18:12:04 UTC 2010')
        self.update_rss("slackware64", "13.37",   'Fri Jun 18 18:12:04 UTC 2010')
        self.update_rss("slackware",   "14.0",    'Wed Oct 10 03:06:03 UTC 2012')
        self.update_rss("slackware64", "14.0",    'Wed Oct 10 03:06:03 UTC 2012')
        self.update_rss("slackware",   "14.1",    'Mon Nov 18 20:52:16 UTC 2013')
        self.update_rss("slackware64", "14.1",    'Mon Nov 18 20:52:16 UTC 2013')
        self.update_rss("slackware",   "14.2",    'Tue Jul  5 04:52:45 UTC 2016')
        self.update_rss("slackware64", "14.2",    'Tue Jul  5 04:52:45 UTC 2016')
        self.update_rss("slackware",   "current", 'Thu Jan  1 00:00:00 UTC 1970')
        self.update_rss("slackware64", "current", 'Thu Jan  1 00:00:00 UTC 1970')

        base_rss = os.listdir(self.baseline)
        match, mismatch, errors = filecmp.cmpfiles(self.baseline, self.output, base_rss, shallow=False)

        self.assertEqual(len(base_rss), len(match))
        self.assertEqual(0, len(mismatch))
        self.assertEqual(0, len(errors))

    def update_rss(self, slackware, version, min_date):
        self.parser.min_date = self.parser.parse_date(min_date)

        self.formatter.slackware = f"{slackware} {version}"
        self.formatter.rssLink = f"http://linuxbox.fi/~vmj/slacklog/{slackware}-{version}.rss"
        self.formatter.description = f"Recent changes in {slackware} {version}"
        self.formatter.managingEditor = "vmj@linuxbox.fi (Mikko Värri)"
        self.formatter.webMaster = "vmj@linuxbox.fi (Mikko Värri)"
        self.formatter.language = "en"
        self.formatter.lastBuildDate = self.lastBuildDate

        slacklog = self.parser.parse(read(f"{self.input}{slackware}-{version}.txt", self.encoding))
        text = self.formatter.format(slacklog)
        write(f"{self.output}{slackware}-{version}.rss", text)
