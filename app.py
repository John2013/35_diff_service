from flask import Flask, request, abort, jsonify
from diff import text_diff

app = Flask(__name__)


@app.route("/")
def index():
    text = "<h1>Get difference of 2 html documents</h1>\n" \
        "<pre>POST http://127.0.0.1:5000/api/v1.0/diff\n" \
        "Content-Type: application/json\n" \
        "\n" \
        "Params:\n" \
        "{\n" \
        "    \"doc1\": \"text1\",\n" \
        "    \"doc2\": \"text2\",\n" \
        "    \"config\": {//any config param are not required\n" \
        "       \"deleted_element\": \"del\",\n" \
        "        \"inserted_element\": \"ins\",\n" \
        "        \"modified_class\": \"diff modified\",\n" \
        "        \"deleted_class\": \"diff deleted\",\n" \
        "        \"inserted_class\": \"diff inserted\",\n" \
        "    }\n" \
        "}</pre>\n" \
        "<h2>Example</h2>\n" \
        "<h3>Request</h3>\n" \
        "<pre>POST http://127.0.0.1:5000/api/v1.0/diff\n" \
        "Content-Type: application/json\n" \
        "\n" \
        "{\n" \
        "    \"doc1\": \"&lt;ul&gt;\n\t&lt;li&gt;Автор: Григорьев П.А." \
        "&lt;/li&gt;\n\t&lt;li&gt;Сумма: 126000 руб.&lt;/li&gt;\n\t&lt;li" \
        "&gt;Дата: 26.12.14&lt;/li&gt;\n&lt;/ul&gt;\",\n" \
        "    \"doc2\": \"&lt;ul&gt;\n\t&lt;li&gt;Сумма: 126000 руб.&lt;/li" \
        "&gt;\n\t&lt;li&gt;Автор: Петров Г.Е.&lt;/li&gt;" \
        "\n\t&lt;li&gt;Дата: 26.12.14&lt;/li&gt;\n\t484\n&lt;/ul&gt;\",\n" \
        "    \"config\": {\n" \
        "        \"modified_class\": \"diff modifieddd\",\n" \
        "        \"deleted_class\": \"diff deleteddd\",\n" \
        "        \"inserted_class\": \"diff inserteddd\"\n" \
        "    }\n" \
        "}</pre>\n" \
        "<h3>Response</h3>\n" \
        "<pre>{\n" \
        "  \"result\": \"&lt;ul&gt;&lt;del class=\&quot;diff deleteddd" \
        "\&quot;&gt;\n\t&lt;li&gt;\u0410\u0432\u0442\u043e\u0440: \u0413" \
        "\u0440\u0438\u0433\u043e\u0440\u044c\u0435\u0432 \u041f.\u0410." \
        "&lt;/li&gt;&lt;/del&gt;\n\t&lt;li&gt;\u0421\u0443\u043c\u043c\u0430" \
        ": 126000 \u0440\u0443\u0431.&lt;/li&gt;\n\t&lt;li&gt;&lt;ins " \
        "class=\&quot;diff inserteddd\&quot;&gt;\u0410\u0432\u0442\u043e" \
        "\u0440: \u041f\u0435\u0442\u0440\u043e\u0432 \u0413.\u0415.&lt;/li" \
        "&gt;\n\t&lt;li&gt;&lt;/ins&gt;\u0414\u0430\u0442\u0430: 26.12.14&l" \
        "t;/li&gt;\n&lt;ins class=\&quot;diff inserteddd\&quot;&gt;\t484\n&" \
        "lt;/ins&gt;&lt;/ul&gt;\"\n}</pre>"
    return text


@app.route("/api/v1.0/diff", methods=["POST"])
def diff():
    if not request.json:
        abort(400)

    return jsonify({
        "result": text_diff(
            request.json["doc1"],
            request.json["doc2"],
            request.json["config"]
        )
    }), 200


if __name__ == "__main__":
    app.run()
