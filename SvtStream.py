#!/usr/bin/env python

import json
import os
import re
import sys
import urllib

RESOLUTION = '1280x720'
EXTENSION = 'mp4'
DOWNLOADCOMMAND = "ffmpeg -i %(url)s -y -vcodec copy -strict experimental -acodec copy -absf aac_adtstoasc %(output)s"

class SvtStream(object):

    def __init__(self, source):
        self.downloadcommand = DOWNLOADCOMMAND
        if type(source) == dict:
            self.__from_dict(source)
        else:
            self.__from_url(source)

    def __get_filename(self, source):
        filename = source['statistics']['folderStructure'].split('.')[0]
        filename += '-'
        filename += ''.join(source['statistics']['title'].split(':')[0:2])
        return filename

    def __get_streamurl(self, source):
        for vref in source['video']['videoReferences']:
            if vref['playerType'] == 'ios':
                return vref['url']
        # TODO: Raise exception
        return None

    def __get_stream_from_m3u8(self, m3u8):
        resolution_re = re.compile(r'.*RESOLUTION=' + RESOLUTION + r'.*')
        lines = m3u8.splitlines()
        # Get next row if resolution matches
        stream = [lines[i+1] for i, line in enumerate(lines)
                if resolution_re.match(line)]
        if stream:
            return stream[0]
        else:
            # TODO: Raise exception
            return None

    def __from_dict(self, source):
        # Ugly hack to work with testing
        self.m3u8 = open(self.__get_streamurl(source)).read()
        self.streamurl = self.__get_stream_from_m3u8(self.m3u8)
        self.filename = "%s.%s" % (self.__get_filename(source), EXTENSION)

    # TODO: Refactor, remove code duplication
    def __from_url(self, url):
        source = json.loads(urllib.urlopen(urllib.unquote(url) + "?output=json").read())
        self.m3u8 = urllib.urlopen(self.__get_streamurl(source)).read()
        self.streamurl = self.__get_stream_from_m3u8(self.m3u8)
        self.filename = "%s.%s" % (self.__get_filename(source), EXTENSION)

