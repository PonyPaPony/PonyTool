from pathlib import Path

from ponytool.utils.ui import info, success, warn, error
from ponytool.utils.io import ask_confirm
from ponytool.utils.fs import is_git_repo
from ponytool.utils.shell import run

PROJECT_STRUCTURE = [
    "src",
    "tests",
    "docs",
]

def project_init(args):
    base = Path.cwd()

    if args.name:
        root = base / args.name
        if root.exists():
            error(f"Папка '{args.name}' уже существует")
            return
        root.mkdir()
        success(f"Создана папка проекта: {args.name}")
    else:
        root = base

    info(f"Инициализация проекта в {root}")

    # структура проекта
    creating_process(root, args)

def creating_process(root, args):
    for folder in PROJECT_STRUCTURE:
        path = root / folder
        if path.exists():
            warn(f"{folder}/ уже существует — пропускаем")
        else:
            path.mkdir()
            success(f"Создана папка {folder}/")

    # файлы
    create_readme(root)
    create_gitignore(root)

    # git
    if args.no_git:
        warn("Git инициализация отключена (--no-git)")
    else:
        check_repo()

def check_repo():
    if is_git_repo():
        warn("Git-репозиторий уже существует — пропускаем")
        return

    if ask_confirm("Инициализировать git-репозиторий?"):
        run(["git", "init"])
        success("Git-репозиторий инициализирован")

def create_readme(root):
    readme = root / "README.md"
    if readme.exists():
        warn("README.md уже существует — пропускаем")
        return

    readme.write_text("# Project\n\nОписание проекта.\n", encoding="utf-8")
    success("Создан README.md")

def create_gitignore(root: Path):
    gitignore = root / ".gitignore"
    if gitignore.exists():
        warn(".gitignore уже существует — пропускаем")
        return

    gitignore.write_text(
        "__pycache__/\n.venv/\n.env\n",
        encoding="utf-8"
    )
    success("Создан .gitignore")
