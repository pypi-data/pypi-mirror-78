#!/usr/bin/env bash

# pypi.org release tool

#https://developer.github.com/v3/repos/releases/#create-a-release

# https://github.com/PyGithub/PyGithub

githubapi.py release

python3 setup.py sdist

package=$(ls -rt dist/*.tar.gz | tail -1)

echo $package

username='eddo888'
password=$(squirrel.py get eddo888@pypi.org)

twine upload -u "$username" -p "$password" "$package"

