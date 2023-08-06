import argparse

import kenlm

model = None

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def index_page():
    return "Hello, World!"


@app.route("/parse")
def parse_service():
    global model

    raw_text = request.args.get("q")

    if not raw_text:
        raise ValueError("missing q")

    text = " ".join(raw_text)

    result = model.score(text, bos=True, eos=True)

    return jsonify(result)


def load_model(model_file: str):
    return kenlm.Model(model_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_file", help="KenLM model file")

    config = vars(parser.parse_args())

    model = load_model(config["model_file"])

    app.run(host="0.0.0.0")
