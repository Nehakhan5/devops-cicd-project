
import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

VERSION = "2.0.0"
WELCOME_MESSAGE = "Successfully Deployed Using CI/CD!"



@app.route("/")
def home():
    return render_template(
        "index.html",
        version=VERSION,
        message=WELCOME_MESSAGE,
        environment=os.getenv("APP_ENV", "Development")
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": VERSION
    }), 200


@app.route("/api/version")
def version():
    return jsonify({"version": VERSION})


if __name__ == "__main__":
    app.run()
