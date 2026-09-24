# MyBlog

*A Django blog built for a university programming course.*

![Python](https://img.shields.io/badge/Python-Blog-3776AB?logo=python&logoColor=white) ![Django 5.2](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white) ![Status](https://img.shields.io/badge/Status-Course%20Project-586069)

**Guide:** [Status](#project-status) · [Run locally](#run-locally) · [Repository contents](#repository-contents)

[English](README.md) | [简体中文](README.zh-CN.md)

MyBlog is a Django 5.2.8 blog project created for a university programming course.

## Project status

Course project. The repository preserves the application source, local settings and data scripts.

## Run locally

Use a Python virtual environment, install the packages listed in requirements.txt, and start the Django development server from the repository root:

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py runserver
~~~

The project has local settings and data scripts. Review them before running the app, and keep passwords, database contents and machine-specific settings private.

## Repository contents

- manage.py — Django command-line entry point
- myblog/ and core/ — application code
- requirements.txt — Python dependencies
