from flask import Flask, request

app = Flask(__name__)

d = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        s = ''
        for x in d:
            s += f'{x[0]}: {x[1]}\n'
        return s
    elif request.method == 'POST':
        d.append((request.remote_addr, request.form['msg']))
        print(f'{d[-1][0]}: {d[-1][1]}')
        return 'OK'

if __name__ == '__main__':
    app.debug=True
    app.run('0.0.0.0', 1337)
