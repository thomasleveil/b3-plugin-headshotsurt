heashotsurt plugin for Big Brother Bot (www.bigbrotherbot.net)
==============================================================

http://www.bigbrotherbot.net

Inspired from the spree plugin by Walker.


Description
-----------

When a player makes a headshot (ie: a kill with last bullet in head or helmet), display in console how many headshots the killer made so far.



Requirements
------------

This plugin will only work with B3 parsers iourt41 and iourt42. Other games won't work.



Installation
------------

- copy headshotsurt.py into b3/extplugins
- copy plugin_headshotsurt.ini in same directory as your b3.xml
- update your main b3 config file with::

    <plugin name="headshotsurt" config="@conf/plugin_headshotsurt.ini"/>

**Note:** for Urban Terror 4.2, you have to use the iourt42 B3 parser for this plugin to detect headshots correctly



Commands
--------

!headshots (or !hs)
  Tells you how many headshots kills you made so far

!headshots (or !hs) <player>
  Tells you how many headshots kills a given player made so far





Contrib
-------

- *features* can be discussed on the `B3 forums <http://forum.bigbrotherbot.net/plugins-by-courgette/heashotsurt-plugin-v0-2-0-%28urt4-1%29/>`_
- documented and reproducible *bugs* can be reported on the `issue tracker <https://github.com/courgette/b3-plugin-headshotsurt/issues>`_
- *patches* are welcome. Send me a `pull request <http://help.github.com/send-pull-requests/>`_.

.. image:: https://secure.travis-ci.org/courgette/b3-plugin-headshotsurt.png?branch=master
   :alt: Build Status
   :target: http://travis-ci.org/courgette/b3-plugin-headshotsurt