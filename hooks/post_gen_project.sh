#!/bin/bash

poetry install
npm install

git init
poetry run pre-commit install