from flask import Flask, request, abort, jsonify
from diff import text_diff

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1.0/diff', methods=['POST'])
def diff():
    if not request.json:
        abort(400)

    return jsonify({
        'result': text_diff(
            request.json["doc1"],
            request.json["doc2"],
            request.json['config']
        )
    }), 200


if __name__ == '__main__':
    app.run()
