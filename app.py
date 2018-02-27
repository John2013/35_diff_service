from flask import Flask, render_template, request, abort, jsonify
from logging.handlers import RotatingFileHandler

from werkzeug.contrib.fixers import ProxyFix

from diff import text_diff

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/api")
@app.route("/api/help")
def api_help():
    return render_template("help.html")


@app.route("/api/v1.0/diff", methods=["POST"])
def api_diff():
    status_ok, status_bad_request = 200, 400
    if not request.json:
        abort(status_bad_request)

    try:
        return jsonify({
            "result": text_diff(
                request.json["doc1"],
                request.json["doc2"],
                request.json["config"]
            )
        }), status_ok
    except KeyError:
        return jsonify({
            "result": text_diff(
                request.json["doc1"],
                request.json["doc2"]
            )
        }), status_ok


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    log_size = 10000
    handler = RotatingFileHandler("log.txt", maxBytes=log_size, backupCount=1)
    app.logger.addHandler(handler)
    app.run()
