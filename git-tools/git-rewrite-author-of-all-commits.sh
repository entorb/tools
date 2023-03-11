#!/bin/sh
git rebase -r --root --exec "git commit --amend --no-edit --reset-author"

