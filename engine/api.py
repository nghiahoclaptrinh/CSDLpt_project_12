from flask import Flask
from flask import request
from flask import jsonify

from localizer import execute_localized_query

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():

    data = request.json

    sql = data["query"]

    result = execute_localized_query(sql)

    return jsonify(
        result.to_dict(orient="records")
    )

app.run(
    host="0.0.0.0",
    port=5000
)