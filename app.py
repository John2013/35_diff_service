from flask import Flask, render_template, request, abort, jsonify
from os import remove
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler

from diff import text_diff

app = Flask(__name__)
# app.config.from_object('config')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route("/api")
@app.route("/api/help")
def api_help():
    return render_template("help.html")


@app.route("/api/v1.0/diff", methods=["POST"])
def api_diff():
    if not request.json:
        abort(400)

    try:
        return jsonify({
            "result": text_diff(
                request.json["doc1"],
                request.json["doc2"],
                request.json["config"]
            )
        }), 200
    except KeyError:
        return jsonify({
            "result": text_diff(
                request.json["doc1"],
                request.json["doc2"]
            )
        }), 200


@app.route("/api/v1.0/get_file_text", methods=["POST"])
def get_file_text():
    # return "111", 200
    app.logger.info('111')
    app.logger.info(request.files)
    if "file" not in request.files:
        app.logger.info('"file" not in request.files')
        abort(400)
    file = request.files['file']
    app.logger.info('222')
    filename = secure_filename(file.filename)
    app.logger.info('333')
    with open(filename) as file:
        app.logger.info('444')
        text = file.read()
    app.logger.info('555')
    remove(filename)
    return text, 200


if __name__ == '__main__':
    handler = RotatingFileHandler('log.txt', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
