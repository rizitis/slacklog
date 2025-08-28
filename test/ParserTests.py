import unittest
from slacklog.scripts import read
from slacklog.parsers import SlackLogParser
from datetime import datetime
from dateutil import tz


class ParserTests(unittest.TestCase):

    def test_slackware_leet_release_entry(self):
        log = SlackLogParser().parse(read('./test/slackware-leet-release-entry.txt', 'iso8859-1'))
        self.assertIsNotNone(log)
        self.assertEqual(len(log.entries), 1)

        e = log.entries[0]
        self.assertEqual(e.timestamp, datetime(2011, 4, 25, 13, 37, 0, tzinfo=tz.tzutc()))
        self.assertTrue(e.description.startswith('Slackware 13.37 x86 stable is released!\n\n'))
        self.assertTrue(e.description.endswith('\nHave fun!\n'))
        self.assertEqual(e.checksum, 'b69d2c808b87e4aeeecfc4a3023ed8024473e9a3337e33246ae0d357aa88abd33c78e7a0f7ffc2ba27f0205c35bbe8bffc7269b41cdc1443b5a15ab7969b2245')
        self.assertEqual(e.identifier, 'e22d108e36d622759515b5e495e0b58927bf514a8315dce9d269743826a6c0908cce7b515b3ecd76d6fadf62bb1e56aa11bd8dea1a37cb68044b27ff86c4b0c0')
        self.assertIsNone(e.parent)
        self.assertEqual(e.pkgs, [])

    def test_slackware_leet_rc3_entry(self):
        log = SlackLogParser().parse(read('./test/slackware-leet-rc3-entry.txt', 'iso8859-1'))
        self.assertIsNotNone(log)
        self.assertEqual(len(log.entries), 1)

        e = log.entries[0]
        self.assertEqual(e.timestamp, datetime(2011, 3, 27, 8, 28, 47, tzinfo=tz.tzutc()))
        self.assertEqual(e.description, (
            "There have been quite a few changes so we will have one more release\n"
            "candidate:  Slackware 13.37 RC 3.14159265358979323846264338327950288419716.\n"
            "Very close now!  But we'll likely hold out for 2.6.37.6.\n"
        ))
        self.assertEqual(len(e.pkgs), 62)
        self.assertEqual(e.pkgs[0].pkg, 'a/aaa_base-13.37-i486-3.txz')
        self.assertEqual(e.pkgs[57].pkg, 'extra/linux-2.6.37.5-nosmp-sdk/*')
        self.assertEqual(e.pkgs[58].pkg, 'isolinux/initrd.img')
        self.assertEqual(e.pkgs[59].pkg, 'kernels/*')
        self.assertEqual(e.pkgs[60].pkg, 'usb-and-pxe-installers/usbboot.img')
        self.assertEqual(e.pkgs[61].pkg, 'testing/source/linux-2.6.38.1-configs/')

    def test_good_11(self):
        log1 = SlackLogParser().parse(read('./test/good-11-slackware-13.0.txt', 'iso8859-1'))
        log2 = SlackLogParser().parse(read('./test/good-11-slackware-13.1.txt', 'iso8859-1'))

        self.assertEqual(log1.entries[1].checksum, log2.entries[1].checksum)
        self.assertNotEqual(log1.entries[1].parent, log2.entries[1].parent)
        self.assertNotEqual(log1.entries[1].identifier, log2.entries[1].identifier)

    def test_single_line_change(self):
        log = SlackLogParser().parse(
            "Thu May 11 18:09:15 UTC 2017\n"
            "l/gtk+3-3.22.14-i586-1.txz:  Upgraded.\n"
        )
        self.assertEqual(len(log.entries), 1)
        self.assertEqual(log.entries[0].description, '')
        self.assertEqual(len(log.entries[0].pkgs), 1)
        self.assertEqual(log.entries[0].pkgs[0].description, '  Upgraded.\n')

    def test_parse_separators(self):
        p = SlackLogParser()

        def check(s, a, b):
            log = p.parse(s)
            self.assertEqual(log.startsWithSeparator, a)
            self.assertEqual(log.endsWithSeparator, b)

        check('', False, False)
        check('+-+', True, False)
        check('\n+-+', False, True)
        check('\n+-+\n', False, True)
        check('+-+\n+-+', True, True)
        check('Thu May 11 18:09:15 UTC 2017\n+-+\nThu May 11 18:09:15 UTC 2017', False, False)
        check('+-+\nThu May 11 18:09:15 UTC 2017\n+-+\nThu May 11 18:09:15 UTC 2017\n+-+', True, True)
