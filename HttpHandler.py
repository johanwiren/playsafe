from SimpleHTTPServer import SimpleHTTPRequestHandler
try:
    from guppy import hpy
except:
    pass
import json
import re
import sys


class HttpHandler(SimpleHTTPRequestHandler):

    def do_GET(s):
        job = re.compile('^/jobs/[0-9]+$')
        joblist = re.compile('^/jobs/?$')
        if (s.path == '/stats/heap' and 'guppy' in sys.modules):
            s.send_response(200)
            s.send_header('Content-Type:', 'text/plain')
            s.end_headers()
            s.wfile.write(hpy().heap())
        elif job.match(s.path):
            s.send_response(200)
            s.send_header('Content-Type:', 'application/json')
            s.end_headers()
            id = int(s.path.split('/')[2])
            result = dict()
            result['command'] = s.server.playsafe.commands[id].args
            result['status'] = s.server.playsafe.commands[id].status
            result['stdout'] = s.server.playsafe.commands[id].stdout
            s.wfile.write(json.dumps(result))
        elif joblist.match(s.path):
            s.send_response(200)
            s.send_header('Content-Type:', 'application/json')
            s.end_headers()
            result = dict()
            for i, cmd in enumerate([[x.args, x.status]
                                    for x in s.server.playsafe.commands]):
                result[i] = dict(command=" ".join(cmd[0]), status=cmd[1])
            s.wfile.write(json.dumps(result))
        else:
            SimpleHTTPRequestHandler.do_GET(s)

    def do_POST(s):
        url = s.rfile.read(int(s.headers['Content-Length']))
        try:
            s.server.playsafe.add(url.rstrip().replace('url=', ''))
        except Exception, e:
            s.send_response(500)
            s.end_headers()
            s.wfile.write(e)
            return
        s.send_response(200)
