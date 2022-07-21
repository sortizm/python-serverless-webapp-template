# python-serverless-webapp-template
Cookiecutter template to bootstrap a new Python serverless webapp

## Requirements
To use this template, it is necessary to install cookiecutter

`pip install cookiecutter`

## Usage
It is not necessary to clone this repository to use the template, as cookiecutter supports using github repositories
as source templates.
It is not recommended to clone the repo either, as running it using the github handle will always use the latest version.

`$ cookiecutter gh:sortizm/python-serverless-webapp-template`

## Configuration
At runtime, the template will request the following values:

* app_name: the name for the app. E.g. my-web-app *REQUIRED*
* app_description: a description for the app. E.g. my first web app *REQUIRED*
* author: the author of the repository. Leave empty for default.
* email: the email of the author.
* version: the version of the app. Leave empty for default
* with_dynamodb_table: if a dynamodb table config is required (y/n). Leave empty for default
* with_s3_bucket: if a s3 bucket config is required (y/n). Leave empty for default
