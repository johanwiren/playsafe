from PlaySafe import PlaySafe
import json

def playsafe_test():
    ps = PlaySafe(config=None)

    jsondata = json.loads(open('test/episode.json').read())
    assert ps.get_filename(jsondata) == 'kommissarie-montalbano-del-2-av-4-il-gioco-degli-specchi'

    assert ps.get_streamurl(jsondata) == 'http://svtplay3l-f.akamaihd.net/i/se/open/20130728/1342328-002A/MONTALBANO_SER-002A-80cb52e1ba20c889_,900,348,564,1680,2800,.mp4.csmil/master.m3u8'

    m3u = open('test/episode.m3u8').read()
    assert ps.get_stream_from_m3u8(m3u) == 'http://svtplay3l-f.akamaihd.net/i/se/open/20130728/1342328-002A/MONTALBANO_SER-002A-80cb52e1ba20c889_,900,348,564,1680,2800,.mp4.csmil/index_4_av.m3u8?null=&id='

