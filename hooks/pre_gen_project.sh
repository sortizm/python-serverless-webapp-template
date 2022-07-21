#!/bin/bash

if [ '{{ cookiecutter.app_name }}' == "" ]; then
  echo "ERROR: The app name can't be empty"
  exit 1
elif [ '{{ cookiecutter.app_description }}' == "" ]; then
  echo "ERROR: The app description can't be empty"
  exit 1
fi