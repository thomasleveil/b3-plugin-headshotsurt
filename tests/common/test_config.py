# -*- encoding: utf-8 -*-
import logging

from headshotsurt import HeadshotsurtPlugin
from b3.config import CfgConfigParser

from tests.iourt41 import Iourt41TestCase
from tests.iourt42 import Iourt42TestCase

class mixin_conf(object):

    def setUp(self):
        super(mixin_conf, self).setUp()
        self.conf = CfgConfigParser()
        self.p = HeadshotsurtPlugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.INFO)


    def test_empty_config(self):
        self.conf.loadFromString("""
[foo]
        """)
        self.p.onLoadConfig() # should not raise any error
        self.assertFalse(self.p._reset_headshots_stats)
        self.assertEqual(0, self.p._min_level_headshots_cmd)
        self.assertFalse(self.p._show_awards)


    # reset_headshots

    def test_reset_headshots__empty(self):
        self.conf.loadFromString("""
[settings]
reset_headshots:
        """)
        self.p.onLoadConfig()
        self.assertFalse(self.p._reset_headshots_stats)

    def test_reset_headshots__yes(self):
        self.conf.loadFromString("""
[settings]
reset_headshots: yes
        """)
        self.p.onLoadConfig()
        self.assertTrue(self.p._reset_headshots_stats)

    def test_reset_headshots__no(self):
        self.conf.loadFromString("""
[settings]
reset_headshots: no
        """)
        self.p.onLoadConfig()
        self.assertFalse(self.p._reset_headshots_stats)

    def test_reset_headshots__junk(self):
        self.conf.loadFromString("""
[settings]
reset_headshots: f00
        """)
        self.p.onLoadConfig()
        self.assertFalse(self.p._reset_headshots_stats)



    # min_level_headshots_cmd

    def test_min_level_headshots_cmd__empty(self):
        self.conf.loadFromString("""
[settings]
min_level_headshots_cmd:
        """)
        self.p.onLoadConfig()
        self.assertEqual(0, self.p._min_level_headshots_cmd)

    def test_min_level_headshots_cmd__nominal(self):
        self.conf.loadFromString("""
[settings]
min_level_headshots_cmd: 2
        """)
        self.p.onLoadConfig()
        self.assertEqual(2, self.p._min_level_headshots_cmd)

        self.conf.loadFromString("""
[settings]
min_level_headshots_cmd: 40
        """)
        self.p.onLoadConfig()
        self.assertEqual(40, self.p._min_level_headshots_cmd)

    def test_min_level_headshots_cmd__junk(self):
        self.conf.loadFromString("""
[settings]
min_level_headshots_cmd: f00
        """)
        self.p.onLoadConfig()
        self.assertEqual(0, self.p._min_level_headshots_cmd)



    # show_awards

    def test_show_awards__empty(self):
        self.conf.loadFromString("""
[settings]
show_awards:
        """)
        self.p.onLoadConfig()
        self.assertFalse(self.p._show_awards)

    def test_show_awards__yes(self):
        self.conf.loadFromString("""
[settings]
show_awards: yes
        """)
        self.p.onLoadConfig()
        self.assertTrue(self.p._show_awards)

    def test_show_awards__no(self):
        self.conf.loadFromString("""
[settings]
show_awards: no
        """)
        self.p.onLoadConfig()
        self.assertFalse(self.p._show_awards)

    def test_show_awards__junk(self):
        self.conf.loadFromString("""
[settings]
show_awards: f00
        """)
        self.p.onLoadConfig()
        self.assertFalse(self.p._show_awards)







##############################################################################
class Test_41(mixin_conf, Iourt41TestCase):
    """
    call the mixin tests using the Iourt41TestCase parent class
    """

class Test_42(mixin_conf, Iourt42TestCase):
    """
    call the mixin tests using the Iourt42TestCase parent class
    """
