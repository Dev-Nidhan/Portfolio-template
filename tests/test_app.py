import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app


class PortfolioAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "messages.sqlite3"
        self.app = create_app({"TESTING": True, "DATABASE": self.database_path})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_homepage_displays_nidhan_and_university(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Nidhan Jain", response.data)
        self.assertIn(b"computer science student", response.data)
        self.assertIn(b"VIT Bhopal University", response.data)
        response.close()

    def test_contact_message_is_saved(self):
        response = self.client.post(
            "/api/contact",
            json={
                "name": "Aarav Shah",
                "email": "aarav@example.com",
                "message": "I would like to discuss a project.",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(b"received", response.data)
        with sqlite3.connect(self.database_path) as connection:
            saved_message = connection.execute(
                "SELECT name, email, message FROM contact_messages"
            ).fetchone()
        self.assertEqual(
            saved_message,
            ("Aarav Shah", "aarav@example.com", "I would like to discuss a project."),
        )

    def test_invalid_contact_data_is_rejected(self):
        response = self.client.post(
            "/api/contact",
            json={"name": "A", "email": "not-an-email", "message": "Short"},
        )

        self.assertEqual(response.status_code, 400)
        with sqlite3.connect(self.database_path) as connection:
            message_count = connection.execute(
                "SELECT COUNT(*) FROM contact_messages"
            ).fetchone()[0]
        self.assertEqual(message_count, 0)


if __name__ == "__main__":
    unittest.main()