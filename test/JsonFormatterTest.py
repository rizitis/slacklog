import unittest
import os
import filecmp
import shutil
from slacklog.scripts import read, write
from slacklog.parsers import SlackLogParser
from slacklog.formatters import SlackLogJsonFormatter


class JsonFormatterTest(unittest.TestCase):

    def setUp(self):
        self.input = './test/changelogs/'
        self.output = './test/json-tmp/'
        self.baseline = './test/json/'
        self.encoding = 'iso-8859-1'
        self.out_encoding = 'utf-8'
        self.parser = SlackLogParser()
        self.formatter = SlackLogJsonFormatter()
        # Ensure clean output dir
        shutil.rmtree(self.output, ignore_errors=True)
        os.mkdir(self.output)

    def tearDown(self):
        shutil.rmtree(self.output, ignore_errors=True)

    def test(self):
        self.update_json("slackware",   "12.0")
        self.update_json("slackware",   "12.1")
        self.update_json("slackware",   "13.0")
        self.update_json("slackware64", "13.0")
        self.update_json("slackware",   "13.1")
        self.update_json("slackware64", "13.1")
        self.update_json("slackware",   "13.37")
        self.update_json("slackware64", "13.37")
        self.update_json("slackware",   "14.0")
        self.update_json("slackware64", "14.0")
        self.update_json("slackware",   "14.1")
        self.update_json("slackware64", "14.1")
        self.update_json("slackware",   "14.2")
        self.update_json("slackware64", "14.2")
        self.update_json("slackware",   "15.0")
        self.update_json("slackware64", "15.0")
        self.update_json("slackware",   "current")
        self.update_json("slackware64", "current")

        base_files = os.listdir(self.baseline)
        match, mismatch, error = filecmp.cmpfiles(self.baseline, self.output, base_files, shallow=False)

        self.assertEqual(len(base_files), len(match))
        self.assertEqual(0, len(mismatch))
        self.assertEqual(0, len(error))

    def update_json(self, slackware, version):
        self.formatter.indent = 4

        slacklog = self.parser.parse(read(f"{self.input}{slackware}-{version}.txt", self.encoding))
        json_text = self.formatter.format(slacklog)
        write(f"{self.output}{slackware}-{version}.json", json_text)
