# Nidhan Jain · Computer Science Portfolio

A responsive, developer-focused portfolio for Nidhan Jain, a computer science student at VIT Bhopal University. It uses plain HTML, CSS, and JavaScript for the frontend, Flask for the Python backend, and SQLite to store contact form submissions. The project cards use custom CSS interface previews instead of generic stock-image tiles.

## Features

- Responsive portfolio sections for an introduction, software project concepts, background, and contact.
- Mobile navigation and scroll reveal effects, with reduced-motion support.
- Contact API at `POST /api/contact` with input validation and a honeypot field.
- SQLite storage for submitted messages; the database is created automatically.
- Health check at `GET /api/health`.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://localhost:5000>.

Contact submissions are saved to `instance/contact_messages.sqlite3`. Messages are stored locally and are not forwarded by email. Do not use Flask's built-in development server for production deployment.

## Customize

- Update the bio and replace the project concepts and their preview markup in `index.html` with your completed projects, technologies, and repository or live-demo links.
- Adjust the theme, typography, layout, and project preview styles in `styles.css`.
- Connect an email provider or deployment-specific database if you want messages delivered to an inbox or stored remotely.

## Test

```bash
python3 -m unittest discover -s tests
```
