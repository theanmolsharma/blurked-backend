from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS, cross_origin
import filter

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/<body>')
def success(body):
    return '%s' % body


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        user = data['body']
        options = {'removeName': data['removeName'], 'removeAddress': data['removeAddress'],
                   'removeEmail': data['removeEmail'], 'removePhone': data['removePhone'],
                   'removeDate': data['removeDate'], 'removePostalCode': data['removePostalCode'],
                   'removeGender': data['removeGender'], 'removeURL': data['removeURL']}
        Filter = filter.Filter()
        data = Filter.filter(user, options)
        return redirect(url_for('success', body=data))
    else:
        return 'Hello World!'


if __name__ == '__main__':
    app.run()
