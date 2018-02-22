from flask import Flask, render_template, request, abort, jsonify
from logging.handlers import RotatingFileHandler

from diff import text_diff

app = Flask(__name__)


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


if __name__ == '__main__':
    handler = RotatingFileHandler('log.txt', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    app.run()
