import json
from pprint import pprint
from urllib.request import urlopen
from flask import Flask, render_template, request

app = Flask(__name__)
url = 'http://api.umd.io/v0/courses/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        result = request.form
        get_classes(result['classes'])
        return result['classes']

def get_classes(classes):
    classes = classes.split(',')
    mod = list()
    for c in classes:
        c = c.strip()
        c = c.lower()
        mod.append(c)

    for c in mod:
        c_url = ''.join([url, c, '?expand=sections'])
        result = urlopen(c_url)
        pprint(json.load(result))

if __name__ == '__main__':
    app.run()
