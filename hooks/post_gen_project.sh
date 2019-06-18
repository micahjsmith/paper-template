#!/usr/bin/env bash

git config user.name "{{ cookiecutter.full_name }}"
git config user.email "{{ cookiecutter.email }}"
git remote add origin "https://git.overleaf.com/{{ cookiecutter.overleaf_id }}"
git add .
git commit -m "Automatically generated files from micahjsmith/paper-template"
