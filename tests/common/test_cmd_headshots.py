# -*- encoding: utf-8 -*-
from mock import patch
from b3.config import CfgConfigParser
from headshotsurt import HeadshotsurtPlugin
from tests.iourt41 import Iourt41TestCase
from tests.iourt42 import Iourt42TestCase



class mixin_cmd_headshots(object):
    def setUp(self):
        super(mixin_cmd_headshots, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[settings]
reset_headshots: yes
min_level_headshots_cmd: 1
show_awards: yes
        """)
        self.p = HeadshotsurtPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.moderator.connects("2")


    def test_no_argument(self):
        self.moderator.message_history = []
        self.moderator.says("!headshots")
        self.assertEqual(['You made no headshot'], self.moderator.message_history)

    def test_unknown_player(self):
        self.moderator.message_history = []
        self.moderator.says("!headshots f00")
        self.assertEqual(['No players found matching f00'], self.moderator.message_history)

    def test_joe(self):
        self.joe.connects('3')
        self.moderator.message_history = []
        self.moderator.says("!headshots joe")
        self.assertEqual(['Joe made no headshot'], self.moderator.message_history)

    def test_alias(self):
        self.moderator.message_history = []
        self.moderator.says("!hs")
        self.assertEqual(['You made no headshot'], self.moderator.message_history)

    def test_has_1_headshots(self):
        self.joe.connects('3')
        with patch.object(self.p, "is_headshot", return_value=True):
            self.moderator.kills(self.joe)
        self.moderator.message_history = []
        self.moderator.says("!headshots")
        self.assertEqual(['You made 1 headshot'], self.moderator.message_history)

    def test_has_3_headshots(self):
        self.joe.connects('3')
        with patch.object(self.p, "is_headshot", return_value=True):
            self.moderator.kills(self.joe)
            self.moderator.kills(self.joe)
            self.moderator.kills(self.joe)
        with patch.object(self.p, "is_headshot", return_value=False):
            self.moderator.kills(self.joe)
        self.moderator.message_history = []
        self.moderator.says("!headshots")
        self.assertEqual(['You made 3 headshots'], self.moderator.message_history)



##############################################################################
class Test_41(mixin_cmd_headshots, Iourt41TestCase):
    """
    call the mixin tests using the Iourt41TestCase parent class
    """

class Test_42(mixin_cmd_headshots, Iourt42TestCase):
    """
    call the mixin tests using the Iourt42TestCase parent class
    """
