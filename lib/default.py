# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from sys import argv
from urllib.parse import parse_qsl
from the_milk import sources_the_milk
from the_milk.modules import control

params = dict(parse_qsl(argv[2].replace('?', '')))
action = params.get('action')

if action is None:
    control.openSettings('0.0', 'script.module.the_milk')

if action == "the_milkSettings":
    control.openSettings('0.0', 'script.module.the_milk')

elif action == 'ShowChangelog':
    from the_milk.modules import changelog

    changelog.get()

elif action == 'ShowHelp':
    from the_milk.help import help

    help.get(params.get('name'))

elif action == "Defaults":
    control.setProviderDefaults()

elif action == "toggleAll":
    sourceList = []
    sourceList = sources_the_milk.all_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])

elif action == "toggleAllHosters":
    sourceList = []
    sourceList = sources_the_milk.hoster_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])

elif action == "toggleAllTorrent":
    sourceList = []
    sourceList = sources_the_milk.torrent_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])

elif action == "toggleAllPackTorrent":
    control.execute('RunPlugin(plugin://script.module.the_milk/?action=toggleAllTorrent&amp;setting=false)')
    control.sleep(500)
    sourceList = []
    from the_milk import pack_sources

    sourceList = pack_sources()
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])

elif action == 'cleanSettings':
    control.clean_settings()

elif action == 'undesirablesSelect':
    from the_milk.modules.undesirables import undesirablesSelect

    undesirablesSelect()

elif action == 'undesirablesInput':
    from the_milk.modules.undesirables import undesirablesInput

    undesirablesInput()

elif action == 'undesirablesUserRemove':
    from the_milk.modules.undesirables import undesirablesUserRemove

    undesirablesUserRemove()

elif action == 'undesirablesUserRemoveAll':
    from the_milk.modules.undesirables import undesirablesUserRemoveAll

    undesirablesUserRemoveAll()

elif action == 'tools_clearLogFile':
    from the_milk.modules import log_utils

    cleared = log_utils.clear_logFile()
    if cleared == 'canceled':
        pass
    elif cleared:
        control.notification(message='Log File Successfully Cleared')
    else:
        control.notification(message='Error clearing Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
    from the_milk.modules import log_utils

    log_utils.view_LogFile(params.get('name'))

elif action == 'tools_uploadLogFile':
    from the_milk.modules import log_utils

    log_utils.upload_LogFile()

elif action == 'plexAuth':
    from the_milk.modules import plex

    plex.Plex().auth()

elif action == 'plexRevoke':
    from the_milk.modules import plex

    plex.Plex().revoke()

elif action == 'plexSelectShare':
    from the_milk.modules import plex

    plex.Plex().get_plexshare_resource()

elif action == 'plexSeeShare':
    from the_milk.modules import plex

    plex.Plex().see_active_shares()

elif action == 'ShowOKDialog':
    control.okDialog(params.get('title', 'default'), int(params.get('message', '')))
