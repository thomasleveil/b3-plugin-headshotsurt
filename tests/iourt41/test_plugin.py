# -*- encoding: utf-8 -*-
from b3.config import CfgConfigParser
from headshotsurt import HeadshotsurtPlugin
from tests.iourt41 import Iourt41TestCase

class Test_plugin(Iourt41TestCase):
    def setUp(self):
        super(Test_plugin, self).setUp()
        self.conf = CfgConfigParser()
        self.p = HeadshotsurtPlugin(self.console, self.conf)
        self.p.onStartup()


    def test_is_headshot(self):
        self.assertTrue(self.p.is_headshot('0'))
        self.assertTrue(self.p.is_headshot('1'))
        self.assertFalse(self.p.is_headshot('3'))
        self.assertFalse(self.p.is_headshot('4'))
        self.assertFalse(self.p.is_headshot('5'))
        self.assertFalse(self.p.is_headshot('6'))
        self.assertFalse(self.p.is_headshot('7'))
        self.assertFalse(self.p.is_headshot(None))
        self.assertFalse(self.p.is_headshot(''))


