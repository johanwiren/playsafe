#!/usr/bin/env python

import json
import os
import re
import sys
import urllib

FFMPEGARGS = [ "-vcodec", "copy", "-strict", "experimental", "-acodec", "copy", "-absf", "aac_adtstoasc" ]
RESOLUTION = '1280x720'
EXTENSION = 'mp4'


class SvtStream(object):

    def __init__(self, config=None, url=url):
        self.ffmpegargs = FFMPEGARGS
        self.config = config
        self.output_dir = config['output_dir']
        self.__from_url(url)

    def __get_filename(self, jsondata):
        filename = jsondata['statistics']['folderStructure'].split('.')[0]
        filename += '-'
        filename += ''.join(jsondata['statistics']['title'].split(':')[0:2])
        return filename

    def __get_streamurl(self, jsondata):
        for vref in jsondata['video']['videoReferences']:
            if vref['playerType'] == 'ios':
                return vref['url']
        # TODO: Raise exception
        return None

    def __get_stream_from_m3u8(self, m3u):
        resolution_re = re.compile(r'.*RESOLUTION=' + RESOLUTION + r'.*')
        lines = m3u.splitlines()
        # Get next row if resolution matches
        stream = [lines[i+1] for i, line in enumerate(lines)
                if resolution_re.match(line)]
        if stream:
            return stream[0]
        else:
            # TODO: Raise exception
            return None

    def __from_url(self, url):
        jsondata = json.loads(urllib.urlopen(urllib.unquote(url) + "?output=json").read())
        self.m3u = urllib.urlopen(self.__get_streamurl(jsondata)).read()
        self.streamurl = self.__get_stream_from_m3u8(m3u)
        self.filename = "%s.%s" % (self.__get_filename(jsondata), EXTENSION)
