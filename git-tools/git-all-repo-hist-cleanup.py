#!/usr/bin/env python3
"""Using git-filter-repo to cleanup git history."""


# RUN IN TERMINAL, not from within vscode, as that uses the python version of the repo

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

GITHUB_USER = "entorb"
CLONE_DIR = Path("/tmp/git-filter-repo-clone")  # noqa: S108
BACKUP_DIR = Path("/tmp/git-filter-repo-backup")  # noqa: S108
REPOS_DIR = Path.home() / "GitHub"
BACKUP_DIR_ZIP = REPOS_DIR / "zzz_backup"
BACKUP_DIR_ZIP.mkdir(parents=True, exist_ok=True)

# Clean up and create directories
for dir_path in [CLONE_DIR, BACKUP_DIR]:
    if dir_path.exists():
        shutil.rmtree(dir_path)
    dir_path.mkdir(parents=True)


# supports files and dirs
# for dirs: enter no trailing / (.github/workflows)
# files in subdirs are fine (app/1x1/README.md)
FILES_DOC = [
    "cspell-words.txt",
    "AGENTS.md",
    "README.md",
    "TODO.md",
    "apps/1x1/AGENTS.md",
    "apps/voc/AGENTS.md",
    "apps/lwk/AGENTS.md",
    "packages/shared/AGENTS.md",
]

FILES_TOOLS = [
    ".editorconfig",
    ".gitattributes",
    ".github",  # dir
    ".gitignore",
    ".pre-commit-config.yaml",
    ".prettierignore",
    ".prettierrc.json",
    ".ruff.toml",
    ".sonarcloud.properties",
    ".sonarlint",  # dir
    ".vscode",  # dir
    "cspell.config.yaml",
    "cspell.json",
    "eslint.config.ts",
    "ruff.toml",
    "scripts",  # dir
    "setup.cfg",
    "sonar-project.properties",
]

FILES_LOCK = [
    "package-lock.json",
    "pnpm-lock.yaml",
    "uv.lock",
]

FILE_PACKAGES = [
    "package.json",
    "apps/1x1/package.json",
    "apps/voc/package.json",
    "apps/lwk/package.json",
    "packages/shared/package.json",
    "pnpm-workspace.yaml",
    "pyproject.toml",
    "requirements-all.txt",
    "requirements-dev.txt",
    "requirements.txt",
]


def restore_and_commit(
    file_list: list[str], backup_dir: Path, commit_message: str
) -> None:
    """Restore files from backup and commit them."""
    restored_files = []
    for file in file_list:
        backup_path = backup_dir / file
        if backup_path.exists():
            dest = Path(file)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(backup_path, dest)
            restored_files.append(file)

    # Git add and commit restored files
    if restored_files:
        subprocess.run(["git", "add", *restored_files], check=True)  # noqa: S603, S607
        subprocess.run(["git", "commit", "-m", commit_message], check=True)  # noqa: S603, S607


# Get all directories (repos)
LIST_REPOS = sorted(
    [
        Path(d)
        for d in REPOS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("zzz_") and d.name != "hpmor-de"
    ]
)

# single repo
# LIST_REPOS = [Path("flashcards")]
for d in LIST_REPOS:
    repo_name = d.name

    print("===")
    print(f"=== {repo_name} ====")
    print("===")

    # Clone the repo
    clone_url = f"git@github.com:{GITHUB_USER}/{repo_name}.git"
    clone_path = CLONE_DIR / repo_name

    print(f"Cloning {clone_url}...")
    subprocess.run(["git", "clone", clone_url, str(clone_path)], check=True)  # noqa: S603, S607

    # Change to cloned repo directory
    os.chdir(clone_path)

    # Create zip backup with timestamp

    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")  # noqa: DTZ005
    backup_zip_file = BACKUP_DIR_ZIP / f"{repo_name}-{timestamp}.zip"

    print(f"Creating backup: {backup_zip_file}")
    shutil.make_archive(
        str(backup_zip_file.with_suffix("")),  # Remove .zip as make_archive adds it
        "zip",
        clone_path,
    )

    # Backup .git/config
    backup_repo_dir = BACKUP_DIR / repo_name
    backup_repo_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(".git/config", backup_repo_dir / ".git-config")

    # Merge both lists
    files = FILES_DOC + FILES_TOOLS + FILES_LOCK + FILE_PACKAGES

    # Copy all files to backup
    for file in files:
        path = Path(file)
        if path.exists():
            dest = backup_repo_dir / file
            if path.is_dir():
                shutil.copytree(path, dest, dirs_exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)

    # Build command with only existing files
    cmd = ["git-filter-repo", "--prune-empty", "always", "--invert-paths"]

    for file in files:
        # no file.exist here, as we want to clean from git history too
        path = Path(file)
        if path.is_dir():
            # For directories, match the dir and everything under it
            cmd.extend(["--path-regex", f"^{file}/"])
        else:
            # For files, exact match
            cmd.extend(["--path-regex", f"^{file}$"])

    # Run the command if we have files to filter
    subprocess.run(cmd, check=True)  # noqa: S603

    # Restore .git/config
    shutil.move(backup_repo_dir / ".git-config", ".git/config")

    # Restore and commit files
    restore_and_commit(FILES_LOCK, backup_repo_dir, "Lock")
    restore_and_commit(FILE_PACKAGES, backup_repo_dir, "Packages")
    restore_and_commit(FILES_DOC, backup_repo_dir, "Documentation")
    restore_and_commit(FILES_TOOLS, backup_repo_dir, "Tools")

    # Explicit cleanup (git-filter-repo usually does this already)
    subprocess.run(["git", "reflog", "expire", "--expire=now", "--all"], check=True)  # noqa: S607
    subprocess.run(["git", "gc", "--prune=now", "--aggressive"], check=True)  # noqa: S607

    # input(f"press Enter force push to {repo_name}")
    # Force push to remote
    subprocess.run(["git", "push", "--force", "origin", "--all"], check=True)  # noqa: S607
    subprocess.run(
        ["git", "push", "--force", "origin", "--tags"],  # noqa: S607
        check=True,
    )

    # input(f"Press Enter to reset local repo {repo_name} to remote...")
    os.chdir(Path.home() / "GitHub" / repo_name)
    subprocess.run(["git", "fetch", "origin"], check=True)  # noqa: S607
    subprocess.run(["git", "reset", "--hard", "origin/main"], check=True)  # noqa: S607
    print(f"Local repo {repo_name} reset to remote")

    shutil.rmtree(backup_repo_dir)

# Cleanup
for dir_path in [CLONE_DIR, BACKUP_DIR]:
    if dir_path.exists():
        shutil.rmtree(dir_path)
