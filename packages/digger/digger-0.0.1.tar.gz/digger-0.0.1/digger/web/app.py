import os

try:
    from flask import Flask, render_template, request, jsonify
except ImportError as exc:
    raise ImportError('Digger webserver requires "flask" installed') from exc

from digger import Digger

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@app.route('/')
def index():
    return render_template("index.html")


digger = Digger()


@app.route('/api/result', methods=['post'])
def result():
    urls = request.form.getlist('url')
    return jsonify(digger(urls, merge_result=True))


if __name__ == '__main__':
    app.run(debug=True)
