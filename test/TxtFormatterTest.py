# coding=utf-8
import unittest
import os
import filecmp
import shutil
from slacklog.scripts import read
from slacklog.parsers import SlackLogParser
from slacklog.formatters import SlackLogTxtFormatter


class TxtFormatterTest(unittest.TestCase):

    def setUp(self):
        self.input = './test/changelogs/'
        self.output = './test/txt/'
        self.encoding = 'iso-8859-1'
        # Try to ensure clean output dir
        shutil.rmtree(self.output, True)
        os.mkdir(self.output)

    def tearDown(self):
        shutil.rmtree(self.output, True)

    def test(self):
        parser = SlackLogParser()
        formatter = SlackLogTxtFormatter()

        changelogs = os.listdir(self.input)

        for changelog in changelogs:
            slacklog = parser.parse(read(self.input + changelog, self.encoding))
            text = formatter.format(slacklog)

            with open(self.output + changelog, 'w', encoding=self.encoding) as f:
                f.write(text)

        match, mismatch, errors = filecmp.cmpfiles(self.input, self.output, changelogs, shallow=False)

        self.assertEqual(len(changelogs), len(match))
