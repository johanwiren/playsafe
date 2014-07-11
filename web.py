#!/usr/bin/env python
from Downloader import *
from flask import *
from SvtStream import *
import daemon
import sys
import yaml

app = Flask(__name__)

CONFIG_DEFAULT = dict(debug=False, host='127.0.0.1')

@app.route('/')
def index():
    return redirect(url_for('static', filename='app/index.html'))

@app.route('/jobs', methods=['GET', 'PUT'])
def list_jobs():
    if request.method == 'GET':
        return json.dumps([x.command.simple_dict() for x in downloader.downloaditems])
    if request.method == 'PUT':
        try:
            app.logger.debug(request.data)
            svtstream = SvtStream(request.data)
            downloaditem = DownloadItem(svtstream, config['output_dir'])
            downloader.add(downloaditem)
            return make_response('', 201)
        except Exception as e:
            app.logger.debug(e.message)
            return make_response(e.message, 500)

@app.route('/jobs/<int:jobId>')
def show_job(jobId):
    result = dict()
    try:
        return json.dumps(downloader.downloaditems[jobId].command.simple_dict())
    except Exception as e:
        app.logger.debug(e.message)
        return make_response(e.message, 404)

try:
    config = dict(CONFIG_DEFAULT.items() + yaml.load(open('config.yml')).items())
except:
    print "Could not load config.yml"
    sys.exit(1)
    
if config['debug']:
    downloader = Downloader()
    app.debug = True
    app.run(host=config['host'], port=config['port'])
    downloader.stop()
else:
    stdout = open("server.out", "w")
    stderr = open("server.err", "w")
    stdin = open("/dev/null", "r")
    with daemon.DaemonContext(stdout=stdout, stderr=stderr, stdin=stdin,
            working_directory='.'):
        downloader = Downloader()
        app.run(host=config['host'], port=config['port'])
        downloader.stop()
