# Contact Book 2.0

A responsive Django contact manager with category-based profile themes and birthday countdown illustrations.

## Features
- Contact List is the default page (`/`).
- Add, view, edit and delete contacts.
- Search by first/middle/last name, phone or company.
- Contact categories: Favourite (gold), Professional (blue), Personal (pastel).
- Birthday countdown appears only on the individual contact details page.
- Birthday artwork thresholds:
  - 100 days or more: hero-themed green illustration (`ben10.svg` placeholder artwork).
  - 31–99 days: anime-style illustration.
  - 0–30 days: celebration illustration.
- Handles birthdays that have passed this year and February 29 birthdays.
- SQLite database; Django admin support.

## Requirements
- Python 3.10+
- pip

## Run on Windows
Open Command Prompt or the VS Code terminal in this project folder:

```bash
py -m venv venv
venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Run on macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Optional admin account
```bash
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/

## Birthday artwork note
The bundled `ben10.svg` is an original green hero-themed placeholder illustration, not official Ben 10 artwork. Replace it with a PNG image you have permission to use by placing it at `static/images/birthdays/ben10.png` and changing the image path in `contacts/birthday.py` to `birthdays/ben10.png`. Anime and celebration illustrations are original SVG artwork included in this project.

## Important before deployment
- Set `DEBUG = False`.
- Replace `SECRET_KEY` with an environment variable.
- Set `ALLOWED_HOSTS` to your real domain.
- Configure HTTPS and a production database if deploying publicly.
