#!/usr/bin/env python

from Command import Command
from Queue import Queue
from threading import Thread
import json
import os
import re
import sys
import urllib
import yaml

FFMPEGARGS = [ "-vcodec", "copy", "-strict", "experimental", "-acodec", "copy", "-absf", "aac_adtstoasc" ]
RESOLUTION = '1280x720'
EXTENSION = 'mp4'

class PlaySafe(object):

    def __init__(self, config=None):
        self.files = []
        self.commands = []
        self.q = Queue()
        self.run_threads = True
        self.thread = Thread(target=self.runner)

    def runner(self):
        while self.run_threads:
            command = self.q.get()
            if command != 'stop':
                command.run()

    def get_filename(self, jsondata):
        filename = jsondata['statistics']['folderStructure'].split('.')[0]
        filename += '-'
        filename += ''.join(jsondata['statistics']['title'].split(':')[0:2])
        return filename

    def get_streamurl(self, jsondata):
        for vref in jsondata['video']['videoReferences']:
            if vref['playerType'] == 'ios':
                return vref['url']
        return None

    def get_stream_from_m3u8(self, m3u):
        resolution_re = re.compile(r'.*RESOLUTION=' + RESOLUTION + r'.*')
        lines = m3u.splitlines()
        # Get next row if resolution matches
        stream = [lines[i+1] for i, line in enumerate(lines)
                if resolution_re.match(line)]
        if stream:
            return stream[0]
        else:
            return None

    def add(self, url):
        jsondata = json.loads(urllib.urlopen(urllib.unquote(url) + "?output=json").read())
        m3u = urllib.urlopen(self.get_streamurl(jsondata)).read()
        stream = self.get_stream_from_m3u8(m3u)
        if stream is None:
            return
        filename = "%s.%s" % (self.get_filename(jsondata), EXTENSION)
        args = [ "ffmpeg", "-i", stream ]
        args += FFMPEGARGS
        args.append('/'.join([self.config["output_dir"], filename]))
        command = Command(args, name=filename)
        self.commands.append(command)
        self.q.put(command)
        return command

    def stop(self):
        self.run_threads = False
        self.q.put('stop')
        self.thread.join()

    def run_server(self):

        self.thread.start()

if __name__ == "__main__":
    try:
        config = yaml.load(open('config.yml'))
    except:
        print "Could not load config.yml"
        sys.exit(1)
    pid = os.fork()
    if not pid:
        PlaySafe(config).run_server()
