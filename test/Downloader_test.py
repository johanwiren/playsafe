from Downloader import *
from nose.tools import with_setup
from SvtStream import SvtStream
import json
import time

config = dict(output_dir='/tmp')

dl = None

def setup():
    global dl
    dl = Downloader()

def teardown():
    global dl
    dl.stop()
    
@with_setup(setup, teardown)
def downloader_test():
    global dl

    ss = SvtStream(json.load(open('test/episode.json')))
    ss.downloadcommand="/usr/bin/echo %s %s"

    dl = Downloader()
    di = DownloadItem(ss, config['output_dir'])
    assert di.command.args == [ u'/usr/bin/echo', u'http://svtplay3q-f.akamaihd.net/i/world/open/20140210/1322836-005A/LABYRINT-005A-b6149effda4e5c1d_,900,348,564,1680,2800,.mp4.csmil/index_4_av.m3u8?null=', u'/tmp/labyrint-del-5-av-10.mp4' ]

    dl.add(di)
    assert di.command.status == "Queued"
    time.sleep(1)
    assert di.command.status == "Completed"
    assert di.command.stdout.rstrip() == "http://svtplay3q-f.akamaihd.net/i/world/open/20140210/1322836-005A/LABYRINT-005A-b6149effda4e5c1d_,900,348,564,1680,2800,.mp4.csmil/index_4_av.m3u8?null= /tmp/labyrint-del-5-av-10.mp4"
