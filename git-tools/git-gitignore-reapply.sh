#!/bin/bash

git status
read -p manually commit all your pending changes
# Remove everything from the git index in order to refresh your git repository:
git rm -r --cached .
# Add everything back into the repo:
git add .
# Commit these changes:
git commit -m ".gitignore re-applied"
git status
read -p "Enter to push"
git push
