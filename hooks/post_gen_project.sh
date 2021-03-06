#!/usr/bin/env bash

git init
git add .
git commit -m "Automatically generated files from micahjsmith/paper-template"
git remote add origin "https://git.overleaf.com/{{ cookiecutter.overleaf_id }}"

# "Merge" remote
if [[ -n "{{ cookiecutter.overleaf_id }}" ]]; then
    git fetch origin master
    git branch --set-upstream-to=origin/master master
    git merge --allow-unrelated-histories -s ours --no-edit origin/master
fi
