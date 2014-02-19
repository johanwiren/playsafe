from SvtStream import SvtStream
import json

config = dict(output_dir='/tmp')

def svtstream_test():
    ss = SvtStream(json.load(open('test/episode.json')))
    assert ss.filename == 'labyrint-del-5-av-10.mp4'

    assert ss.streamurl == 'http://svtplay3q-f.akamaihd.net/i/world/open/20140210/1322836-005A/LABYRINT-005A-b6149effda4e5c1d_,900,348,564,1680,2800,.mp4.csmil/index_4_av.m3u8?null='

