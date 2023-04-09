# -*- coding: UTF-8 -*-

from os.path import join as osPath_join, dirname as osPath_dirname
from os import walk as osWalk
from pkgutil import walk_packages
from the_milk.modules.control import setting as getSetting
from the_milk.modules import log_utils

debug = getSetting('debug.enabled') == 'true'
sourceFolder = 'sources_the_milk'

def debug_it(msg, caller=None):
    #if debug:
    log_utils.log('__init__ %s' % msg)

def sources(specified_folders=None, ret_all=False):
    try:
        sourceDict = []
        append = sourceDict.append
        sourceFolderLocation = osPath_join(osPath_dirname(__file__), sourceFolder)
        sourceSubFolders = [x[1] for x in osWalk(sourceFolderLocation)][0]

        debug_it('sourceFolderLocation = %s' % sourceFolderLocation)
        debug_it('sourceSubFolders = %s' % sourceSubFolders)

        if specified_folders:
            sourceSubFolders = specified_folders

        for i in sourceSubFolders:
            for loader, module_name, is_pkg in walk_packages([osPath_join(sourceFolderLocation, i)]):
                debug_it('loader= %s module_name= %s is_pkg= %s' % (loader, module_name, is_pkg))
                if is_pkg:
                    continue
                if ret_all or enabledCheck(module_name):
                    try:
                        module = loader.find_module(module_name).load_module(module_name)
                        append((module_name, module.source))

                    except Exception as e:
                        if debug:
                            log_utils.log('Error: Loading module: "%s": %s' % (module_name, e),
                                          level=log_utils.LOGWARNING)
        return sourceDict

    except Exception as e:
        log_utils.error('__init__.py.sources: Exception %s' % str(e))
        return []


def enabledCheck(module_name):
    try:
        if getSetting('provider.' + module_name) == 'true':
            debug_it('module_name = %s status = Enable' % module_name)
            return True
        else:
            debug_it('module_name = %s status = Enable' % module_name)
            return False

    except Exception as e:
        log_utils.error('__init__.py.enabledCheck: Exception %s' % str(e))
        return True


def pack_sources(sourceSubFolder='torrents'):
    try:
        sourceList = []
        sourceList_append = sourceList.append
        sourceFolderLocation = osPath_join(osPath_dirname(__file__), sourceFolder)

        for loader, module_name, is_pkg in walk_packages([osPath_join(sourceFolderLocation, sourceSubFolder)]):
            if is_pkg:
                continue
            module = loader.find_module(module_name).load_module(module_name)
            if module.source.pack_capable:
                sourceList_append(module_name)

        return sourceList
    except Exception as e:
        log_utils.error('__init__.py.pack_sources: Exception %s' % str(e))
    return sourceList  # return []
