import re
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory


ROOT = Path(__file__).resolve().parent
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=ROOT / "instance" / "contact_messages.sqlite3",
        MAX_CONTENT_LENGTH=16 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    database_path = Path(app.config["DATABASE"])
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    @app.get("/")
    def home():
        return send_from_directory(ROOT, "index.html")

    @app.get("/styles.css")
    def styles():
        return send_from_directory(ROOT, "styles.css")

    @app.get("/script.js")
    def script():
        return send_from_directory(ROOT, "script.js")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.post("/api/contact")
    def contact():
        payload = request.get_json(silent=True)
        if payload is None:
            payload = request.form
        if not hasattr(payload, "get"):
            return jsonify(error="Please send a valid contact form."), 400

        if str(payload.get("website", "")).strip():
            return jsonify(message="Thanks for reaching out. Your message has been received."), 202

        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip()
        message = str(payload.get("message", "")).strip()

        if not 2 <= len(name) <= 80:
            return jsonify(error="Name must be between 2 and 80 characters."), 400
        if len(email) > 254 or not EMAIL_PATTERN.fullmatch(email):
            return jsonify(error="Enter a valid email address."), 400
        if not 10 <= len(message) <= 3000:
            return jsonify(error="Message must be between 10 and 3000 characters."), 400

        with sqlite3.connect(app.config["DATABASE"]) as connection:
            connection.execute(
                "INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)",
                (name, email, message),
            )

        return jsonify(message="Thanks for reaching out. Your message has been received."), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)