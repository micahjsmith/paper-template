#!/usr/bin/env bash

git init
git add .
git commit -m "Automatically generated files from micahjsmith/paper-template"
git remote add origin "https://git.overleaf.com/{{ cookiecutter.overleaf_id }}"
