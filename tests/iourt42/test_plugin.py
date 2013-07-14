# -*- encoding: utf-8 -*-
import logging
from b3.config import CfgConfigParser
from headshotsurt import HeadshotsurtPlugin
from tests.iourt42 import Iourt42TestCase



class Test_plugin(Iourt42TestCase):
    def setUp(self):
        super(Test_plugin, self).setUp()
        self.conf = CfgConfigParser()
        logging.getLogger('output').setLevel(logging.DEBUG)
        self.p = HeadshotsurtPlugin(self.console, self.conf)
        self.p.onStartup()


    def test_is_headshot(self):
        self.assertFalse(self.p.is_headshot('0'))
        self.assertTrue(self.p.is_headshot('1'))
        self.assertTrue(self.p.is_headshot('2'))
        self.assertFalse(self.p.is_headshot('3'))
        self.assertFalse(self.p.is_headshot('4'))
        self.assertFalse(self.p.is_headshot('5'))
        self.assertFalse(self.p.is_headshot('6'))
        self.assertFalse(self.p.is_headshot('7'))
        self.assertFalse(self.p.is_headshot(None))
        self.assertFalse(self.p.is_headshot(''))


