# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module changed 10-11-22 by umbrelladev
"""

import re
from the_milk.modules import log_utils


def get(title):
    try:
        if not title: return
        title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2',
                       title)  # fix html codes with missing semicolon between groups
        title = re.sub(r'&#(\d+);', '', title).lower()
        title = title.replace('&quot;', '\"').replace('&amp;', '&').replace('&nbsp;', '')
        # title = re.sub(r'[<\[({].*?[})\]>]|[^\w0-9]|[_]', '', title) #replaced with lines below to stop removing () and everything between.
        title = re.sub(r'\([^\d]*(\d+)[^\d]*\)', '', title)  # eliminate all numbers between ()
        title = re.sub(r'[<\[{].*?[}\]>]|[^\w0-9]|[_]', '', title)
        return title
    except Exception as e:
        log_utils.error('cleantitle.get Exception %s' % str(e))
        return title


def get_simple(title):
    try:
        if not title: return
        title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2',
                       title).lower()  # fix html codes with missing semicolon between groups
        title = re.sub(r'&#(\d+);', '', title)
        title = re.sub(r'(\d{4})', '', title)
        title = title.replace('&quot;', '\"').replace('&amp;', '&').replace('&nbsp;', '')
        title = re.sub(r'\n|[()[\]{}]|[:;–\-",\'!_.?~$@]|\s', '',
                       title)  # stop trying to remove alpha characters "vs" or "v", they're part of a title
        title = re.sub(r'<.*?>', '', title)  # removes tags
        return title
    except Exception as e:
        log_utils.error('cleantitle.get_simple Exception %s' % str(e))
        return title


def geturl(title):
    if not title: return
    try:
        title = title.lower().rstrip()
        try:
            title = title.translate(None, ':*?"\'\.<>|&!,')
        except:
            try:
                title = title.translate(title.maketrans('', '', ':*?"\'\.<>|&!,'))
            except:
                for c in ':*?"\'\.<>|&!,': title = title.replace(c, '')
        title = title.replace('/', '-').replace(' ', '-').replace('--', '-').replace('–', '-').replace('!', '')
        return title
    except Exception as e:
        log_utils.error('cleantitle.geturl Exception %s' % str(e))
        return title


def normalize(title):
    try:
        import unicodedata
        if not title or len(title) == 0: return ''
        txt = u'%s' % title.lower()
        txt = ''.join(c for c in unicodedata.normalize('NFKD', txt) if unicodedata.category(c) != 'Mn')
        return str(txt)
    except Exception as e:
        log_utils.error('cleantitle.normalize Exception %s' % str(e))
        return ''
