# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from the_milk.modules.control import addonPath, addonVersion, joinPath
from the_milk.windows.textviewer import TextViewerXML


def get():
    the_milk_path = addonPath()
    the_milk_version = addonVersion()
    changelogfile = joinPath(the_milk_path, 'changelog.txt')
    r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
    text = r.read()
    r.close()
    heading = '[B]the_milk -  v%s - ChangeLog[/B]' % the_milk_version
    windows = TextViewerXML('textviewer.xml', the_milk_path, heading=heading, text=text)
    windows.run()
    del windows
