#!/usr/bin/env python
from flask import *
from PlaySafe import *
import daemon
import simplejson
import subprocess
import sys
import yaml

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('static', filename='app/index.html'))

@app.route('/jobs', methods=['GET', 'PUT'])
def list_jobs():
    if request.method == 'GET':
        return json.dumps([x.simple_dict() for x in playsafe.commands])
    if request.method == 'PUT':
        try:
            playsafe.add(request.data)
            return make_response('', 201)
        except Exception as e:
            return make_response(e.message, 500)

@app.route('/jobs/<int:jobId>')
def show_job(jobId):
    result = dict()
    try:
        return json.dumps(playsafe.commands[jobId].simple_dict())
    except:
        return make_response('', 404)



try:
    config = yaml.load(open('config.yml'))
except:
    print "Could not load config.yml"
    sys.exit(1)
    
with daemon.DaemonContext():
    playsafe = PlaySafe(config=config)
    playsafe.run_server()
    app.debug = True
    app.run(host='0.0.0.0', port=config['port'])
    playsafe.stop()
