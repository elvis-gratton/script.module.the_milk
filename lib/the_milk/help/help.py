# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from the_milk.modules.control import addonPath, addonVersion, joinPath
from the_milk.windows.textviewer import TextViewerXML


def get(file):
    the_milk_path = addonPath()
    the_milk_version = addonVersion()
    helpFile = joinPath(the_milk_path, 'lib', 'the_milk', 'help', file + '.txt')
    r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
    text = r.read()
    r.close()
    heading = '[B]The Milk -  v%s - %s[/B]' % (the_milk_version, file)
    windows = TextViewerXML('textviewer.xml', the_milk_path, heading=heading, text=text)
    windows.run()
    del windows
