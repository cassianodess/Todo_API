#!/bin/bash
SHELL=/bin/bash

include .env
export

init:
	rm -rf .venv; python -m venv .venv; source .venv/bin/activate; python -m pip install -r requirements.txt;

migrate:
	export FLASK_APP=app; flask db init; flask db migrate; flask db upgrade;

run:
	source .venv/bin/activate; flask --app app run --debug --port=8080

freeze:
	source .venv/bin/activate; python -m pip freeze > requirements.txt	
