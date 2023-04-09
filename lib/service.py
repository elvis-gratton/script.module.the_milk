# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

import xbmc
from the_milk.modules import control

window = control.homeWindow
LOGINFO = 1  # (LOGNOTICE(2) deprecated in 19, use LOGINFO(1))


class CheckSettingsFile:
    def run(self):
        try:
            xbmc.log('[ script.module.the_milk ]  CheckSettingsFile Service Starting...', LOGINFO)
            window.clearProperty('the_milk')
            profile_dir = control.dataPath

            if not control.existsPath(profile_dir):
                success = control.makeDirs(profile_dir)
                if success:
                    xbmc.log('%s : created successfully' % profile_dir, LOGINFO)
            else:
                xbmc.log('%s : already exists' % profile_dir, LOGINFO)

            settings_xml = control.joinPath(profile_dir, 'settings.xml')
            if not control.existsPath(settings_xml):
                control.setSetting('module.provider', 'the_milk')
                xbmc.log('%s : created successfully' % settings_xml, LOGINFO)
            else:
                xbmc.log('%s : already exists' % settings_xml, LOGINFO)

            return xbmc.log('[ script.module.the_milk ]  Finished CheckSettingsFile Service', LOGINFO)
        except:
            import traceback
            traceback.print_exc()


class SettingsMonitor(control.monitor_class):
    def __init__(self):
        control.monitor_class.__init__(self)
        window.setProperty('the_milk.debug.reversed', control.setting('debug.reversed'))
        xbmc.log('[ script.module.the_milk ]  Settings Monitor Service Starting...', LOGINFO)

    def onSettingsChanged(self):  # Kodi callback when the addon settings are changed
        window.clearProperty('the_milk')
        control.sleep(50)
        refreshed = control.make_settings_dict()
        control.refresh_debugReversed()


class CheckUndesirablesDatabase:
    def run(self):
        xbmc.log('[ script.module.the_milk ]  "CheckUndesirablesDatabase" Service Starting...', LOGINFO)
        from the_milk.modules import undesirables
        try:
            old_database = undesirables.Undesirables().check_database()
            if old_database:
                undesirables.add_new_default_keywords()
        except:
            import traceback
            traceback.print_exc()

        return xbmc.log('[ script.module.the_milk ]  Finished "CheckUndesirablesDatabase" Service', LOGINFO)


def main():
    while not control.monitor.abortRequested():
        xbmc.log('[ script.module.the_milk ]  Service Started', LOGINFO)
        CheckSettingsFile().run()
        CheckUndesirablesDatabase().run()

        if control.isVersionUpdate():
            control.clean_settings()
            xbmc.log('[ script.module.the_milk ]  Settings file cleaned complete', LOGINFO)
        break
    SettingsMonitor().waitForAbort()
    xbmc.log('[ script.module.the_milk ]  Service Stopped', LOGINFO)


main()
