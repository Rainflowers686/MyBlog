<div align="center">

# **MyBlog**

A Django blog built for a university programming course.

Write rich-text posts, organize them with categories and tags, and add profiles, comments and notifications.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](requirements.txt) [![Django](https://img.shields.io/badge/Django-5.2.8-092E20?logo=django&logoColor=white)](requirements.txt) [![MySQL](https://img.shields.io/badge/database-MySQL-4479A1)](#configuration)

[English](README.md) · [简体中文](README.zh-CN.md)

[Features](#features) · [Run locally](#run-locally) · [Configuration](#configuration) · [Repository contents](#repository-contents) · [Contributing](#contributing)

</div>

## Project status

This course project preserves the Django 5.2.8 application, site settings and
data scripts. It is intended for local study and demonstration. Review the
authentication, upload handling and deployment settings before exposing it
to the internet.

The current rich-text dependency bundles CKEditor 4.22.1, which is no longer
maintained and produces Django warning `ckeditor.W001`. Replace that editor
or choose a supported distribution before a production deployment.

## Features

- Rich-text posts with drafts, categories, tags, search and pagination.
- User profiles with avatars, a blog title, background and theme selection.
- Comments and replies, likes, notifications and author pages.
- Django administration, django-allauth account routes and a read-only posts API.

The source configures GitHub and Google account providers. Using either one
requires your own application credentials and site configuration.

## Run locally

Use Python 3.10 or newer and a local MySQL server. Create a virtual environment
from the repository root:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
~~~

Set the configuration in the same shell. This creates a fresh development
key and prompts for the password of a local database account:

~~~powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"
$env:DJANGO_DEBUG = "1"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:DB_NAME = "my_blog_db"
$env:DB_USER = "myblog"
$env:DB_PASSWORD = [System.Net.NetworkCredential]::new("", (Read-Host "MySQL password" -AsSecureString)).Password
~~~

Create the database and grant that account access using your MySQL
administration tool. Then run:

~~~powershell
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

Open `http://127.0.0.1:8000/`. The blog is under `/blog/`, administration under
`/admin/` and the posts API under `/api/posts/`.

The original course dependency list omitted packages imported by the source.
Those package names are now included; their original versions were not
recorded. Validate the environment you restore and save its resolved versions
before treating it as a reproducible course environment.

## Configuration

[.env.example](.env.example) lists the available variables without secrets.
It is a reference file; the application reads process environment variables
and does not automatically load `.env`.

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required fresh key, at least 50 characters; the old development key is rejected |
| `DJANGO_DEBUG` | Defaults to `0`; set `1` only for local development |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts; defaults to local loopback names |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Database name, account and required password |
| `DB_HOST`, `DB_PORT` | MySQL address; defaults to `127.0.0.1:3306` |
| `EMAIL_*`, `DEFAULT_FROM_EMAIL` | Mail configuration; the default backend writes to the console |
| `MYBLOG_DEMO_PASSWORD_RESET` | Defaults to `0`; direct reset-link demonstrations also require `DJANGO_DEBUG=1` |

Keep the demonstration reset option disabled for real users. It deliberately
reveals a reset link in the browser for an isolated classroom demonstration.
Normal password resets use the mail flow; console mail is only useful locally.

The repository previously included a development secret key and database
password in source, and tracked compiled Python files that can retain old
configuration. If those values were used, replace them. Current-file cleanup does not revoke a credential or remove Git
history. See [SECURITY.md](SECURITY.md).

## Data scripts

Review these scripts before running them against any database:

- `myblog/setup_db.py` creates the configured database when run explicitly and
  requires an account with database-creation permission.
- `populate_db.py` adds demonstration records. New demonstration users have
  unusable passwords; existing users are not reset by this change.
- `fix_site.py` changes the Django Site record and clears social-application
  associations. It is a maintenance operation, not a normal startup step.
- `local_settings.py` holds site presentation strings, separate from the
  credentials supplied through environment variables.

## Repository contents

| Path | Contents |
| --- | --- |
| `manage.py` | Django command-line entry point |
| `myblog/` | Settings, URLs, application entry points and database helper |
| `core/` | Models, views, templates and migrations |
| `requirements.txt` | Python dependency declarations |
| `.env.example` | Secret-free configuration reference |

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) describes local checks and data-handling
rules. Report ordinary bugs through Issues with reproduction steps and a
redacted error message. Follow [SECURITY.md](SECURITY.md) for sensitive reports.

## License

No repository-wide license is currently declared. Dependencies and external
resources retain their own terms; clarify reuse rights before redistribution.
