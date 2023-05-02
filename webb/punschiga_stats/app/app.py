import os
import sqlite3
import base64
from flask import g, Flask, url_for, render_template, request, make_response
import gevent
from gevent import select
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

FLAG = "undut{FzLi4gRGV0IHZhciBuw6RyYSBlbiBrYXRhc3Ryb2YhIEx1Z25ldCBsw6RnZ2VyIHNp}"
DATABASE = './database.db' 
db = sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/stats/<path:subpath>', methods=['GET'])
def api_stats(subpath):
    if len(subpath) > 6:
        return 'error: too long'
        
    base_dir = '/proc/self/'
    path = os.path.abspath(os.path.join(base_dir, subpath))

    if not path.startswith(base_dir):
        return 'error: path not allowed'

    with open(path, 'rb') as f:
        rlist, wlist, elist = select.select([f.fileno()], [], [], 0.3)
        if rlist:
            size = os.stat(path).st_size
            if size == 0:
                size = 1024
            return os.read(rlist[0], size)
        return 'error'

@app.route('/dev-admin-sida', methods=['GET'])
def admin():
    access = False
    for k, v in request.headers.items():
        if k == 'Authorization':
            auth = v.split(" ")[1]
            username, password = base64.b64decode(auth).split(b":")
            if username and password:
                user = query_db('select * from users where username = ?', [username.decode("utf-8")], one=True)
                if user and user[2] == password.decode('utf-8'):
                    return 'En bagare av rang förtjänar en flagga för sitt jobb: {}'.format(FLAG)

    resp = make_response('Access denied!', 401)
    resp.headers['WWW-Authenticate'] = 'Basic realm="StatServer"'
    return resp

@app.route('/testar-123-2023', methods=['GET'])
def testar():
    return 'testar 123'

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
