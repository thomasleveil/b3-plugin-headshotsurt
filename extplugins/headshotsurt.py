# headshotsurt Plugin for Big Brother Bot
# Copyright (C) 2008 Courgette
# Inspired by the spree plugin from Walker
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Requirements : B3 v1.1.3+
#
# Changelog :
# 0.0.1 : initial release
# 13/09/2008 - v0.2.0
# - Refactoring
# - Add award messages at end of game


__version__ = '0.2.0'
__author__  = 'Courgette'


import b3
import b3.events

### kill modes constants ###
MOD_WATER='1'
MOD_LAVA='3'
MOD_TELEFRAG='5'
MOD_FALLING='6'
MOD_SUICIDE='7'
MOD_TRIGGER_HURT='9'
MOD_CHANGE_TEAM='10'
UT_MOD_KNIFE='12'
UT_MOD_KNIFE_THROWN='13'
UT_MOD_BERETTA='14'
UT_MOD_DEAGLE='15'
UT_MOD_SPAS='16'
UT_MOD_UMP45='17'
UT_MOD_MP5K='18'
UT_MOD_LR300='19'
UT_MOD_G36='20'
UT_MOD_PSG1='21'
UT_MOD_HK69='22'
UT_MOD_BLED='23'
UT_MOD_KICKED='24'
UT_MOD_HEGRENADE='25'
UT_MOD_SR8='28'
UT_MOD_AK103='30'
UT_MOD_SPLODED='31'
UT_MOD_SLAPPED='32'
UT_MOD_BOMBED='33'
UT_MOD_NUKED='34'
UT_MOD_NEGEV='35'
UT_MOD_HK69_HIT='37'
UT_MOD_M4='38'
UT_MOD_FLAG='39'
UT_MOD_GOOMBA='40'

### hit location constants ###
HL_HEAD='0'
HL_HELMET='1'
HL_TORSO='2'
HL_KEVLAR='3'
HL_ARMS='4'
HL_LEGS='5'
HL_BODY='6'


class HeadShotsStats:
    headshots = 0
    kills = 0
    
#--------------------------------------------------------------------------------------------------
class HeadshotsurtPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    _reset_headshots_stats = None
    _min_level_headshots_cmd = None
    _clientvar_name = 'headshots_info'
    _show_awards = None

    
    def onLoadConfig(self):

        try:
            if self.config.get('settings', 'reset_headshots') == '1':
                self._reset_headshots_stats = True
        except:
            self._reset_headshots_stats = False
        self.debug('reset hs stats : %s' % self._reset_headshots_stats)
            
            
        try:
            if self.config.get('settings', 'show_awards') == '1':
                self._show_awards = True
        except:
            self._show_awards = False
        self.debug('show awards : %s' % self._show_awards)            
        
        
        try:
              self._min_level_headshots_cmd = self.config.getint('settings', 'min_level_headshots_cmd')
        except:
            self._min_level_headshots_cmd = 0
        self.debug('min level for hs cmd : %s' % self._min_level_headshots_cmd)
        
        
        
        # get the plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
        else:
            self._adminPlugin.registerCommand(self, 'headshots', self._min_level_headshots_cmd, self.cmd_headshots, 'hs')
        
        
        
    def onStartup(self):
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_GAME_EXIT)



    def onEvent(self, event):
        """\
        Handle intercepted events
        """
        if event.type == b3.events.EVT_CLIENT_KILL:
            self.handle_kills(event)
        elif event.type == b3.events.EVT_GAME_EXIT:
            self.handle_gameexit(event)
              

    def init_headshots_stats(self, client):
        # initialize the clients spree stats
        client.setvar(self, self._clientvar_name, HeadShotsStats())
    
    def get_headshots_stats(self, client):
        
        if not client.isvar(self, self._clientvar_name):
            client.setvar(self, self._clientvar_name, HeadShotsStats())
            
        return client.var(self, self._clientvar_name).value
    
    def handle_kills(self, event):
        """\
        A kill was made. 
        """
        client = event.client
        if client:
            weapon = event.data[1]
            hitlocation = event.data[2]
            stats = self.get_headshots_stats(client)
            
            stats.kills += 1
            
            if weapon not in (UT_MOD_BLED, UT_MOD_HEGRENADE) and hitlocation == HL_HEAD or hitlocation == HL_HELMET:
                stats.headshots += 1
                self.show_message( client )
                
            # if stats.kills>0:
              # self.debug("[%s] HS:%s K:%s ratio:%.2f" % (client.name, stats.headshots, stats.kills, (float(stats.headshots) / stats.kills)))
            # else:
              # self.debug("[%s] HS:%s K:%s" % (client.name, stats.headshots, stats.kills))

    def show_message(self, client):
        """\
        display the message
        """

        headshotsStats = self.get_headshots_stats(client)
        self.console.write('%s^3 made ^6%s^3 headshots'%(self.coloredClientName(client),headshotsStats.headshots))        
    
    
    def cmd_headshots(self, data, client, cmd=None):
        """\
        [player] - Show a players number of headshots
        """        
        if data is None or data=='':
            if client is not None:
                headshotsStats = self.get_headshots_stats(client)
                if headshotsStats.headshots > 0:
                    cmd.sayLoudOrPM(client, '^7You made ^2%s^7 headshots' % headshotsStats.headshots)
                else:
                    cmd.sayLoudOrPM(client, '^7You made no headshot')
        else:
            input = self._adminPlugin.parseUserCmd(data)
            if input:
                # input[0] is the player id
                sclient = self._adminPlugin.findClientPrompt(input[0], client)
                if not sclient:
                    # a player matchin the name was not found, a list of closest matches will be displayed
                    # we can exit here and the user will retry with a more specific player
                    client.message('^7Invalid data, can\t find player %s'%data)
                    return False
            else:
                client.message('^7Invalid data, try !help headshots')
                return False
            
            headshotsStats = self.get_headshots_stats(sclient)
            if headshotsStats.headshots > 0:
                client.message('^7%s made ^2%s^7 headshots' % (sclient.name, headshotsStats.headshots))
            else:
                client.message('^7%s made no headshot'%sclient.name)
       
       

    def handle_gameexit(self, event):
        if self._show_awards:
            maxHs = 0
            maxHsClients = []
            
            for c in self.console.clients.getList():
                stats = self.get_headshots_stats(c)
                # self.debug("[%s] HS:%s K:%s" % (c.name, stats.headshots, stats.kills))
                
                if stats.headshots > maxHs:
                    maxHs = stats.headshots
                    ratio = None
                    if stats.kills > 0:
                        ratio = float(stats.headshots) / stats.kills
                    maxHsClients = [(c, ratio)]
                elif stats.headshots>0 and stats.headshots == maxHs:
                    ratio = None
                    if stats.kills > 0:
                        ratio = float(stats.headshots) / stats.kills
                    maxHsClients.append((c, ratio))
                    
                if stats.kills > 0:
                    ratio = float(stats.headshots) / stats.kills
                    self.debug("[%s] HS:%s K:%s => ratio %.2f" % (c.name, stats.headshots, stats.kills, ratio))
        
            
            for c, ratio in maxHsClients:
                
                #self.debug("Most HS found : %s (%s)" % (c.name, maxHs))
                self.console.say('^2Most HS Award : %s^3 (^6%s^3 HS, ratio: %.2f)'%(self.coloredClientName(c), maxHs, ratio))

                
        if self._reset_headshots_stats:
            for c in self.console.clients.getList():
                self.init_headshots_stats(c)
                
                
                
    def coloredClientName(self, client):
        # color name with team color
        clientName = client.name
        if (client.team==b3.TEAM_RED):
            clientName = '^1%s^7'%client.name
        elif (client.team==b3.TEAM_BLUE):
            clientName = '^4%s^7'%client.name
        elif (client.team==b3.TEAM_UNKNOWN):
            clientName = '^3%s^7'%client.name
        return clientName