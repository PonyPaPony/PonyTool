from pathlib import Path

from ponytool.utils.ui import info, warning, error, success
from ponytool.utils.io import ask_confirm
from ponytool.utils.shell import run
from ponytool.project.git_ignore_cfg import PROJECT_STRUCTURE, GITIGNORE_TEMPLATE, FOLDER_STRUCTURE


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

    structure = choice_mode(PROJECT_STRUCTURE)
    creating_structure(root, args, structure)

def creating_structure(root, args, structure):
    for folder in structure:
        path = root / folder
        if path.exists():
            warning(f"{folder}/ уже существует — пропускаем")
        else:
            ensure_path(path)
            success(f"Создана папка {path.relative_to(root)}")

    create_readme(root)
    create_git_ignore(root)

    if args.no_git:
        warning("Git инициализация отключена (--no-git)")
    else:
        check_repo(root)

def check_repo(root: Path):
    """
    Проверяем есть ли уже активный Git-Репо,
    Спрашиваем подключить ли проект к Репо
    """
    if (root / ".git").exists():
        warning("Git-репозиторий уже существует — пропускаем")
        return

    if ask_confirm("Инициализировать git-репозиторий?"):
        run(['git', 'init'], cwd=root)
        success("Git-репозиторий инициализирован")

def create_readme(root):
    readme = root / "README.md"
    if readme.exists():
        warning("README.md уже существует — пропускаем")
        return

    # Первая запись в README
    readme.write_text("# Project\n\nОписание проекта.\n", encoding="utf-8")
    success("Создан README.md")

def create_git_ignore(root: Path):
    ignore = root / ".gitignore"
    if ignore.exists():
        warning(".gitignore уже существует — пропускаем")
        return

    ignore.write_text(
        GITIGNORE_TEMPLATE,
        encoding="utf-8",
    )
    success("Создан .gitignore")

def choice_mode(default_structure):
    raw = input(FOLDER_STRUCTURE).strip()

    if not raw:
        return [Path(p) for p in default_structure]

    result = []

    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue

        # Фиксим частые проблемы с интерпретациями путей
        path = normalize_path(part)

        if path.is_absolute() or path.parts[0] in (".", ".."):
            warning(f"Пропущен некорректный путь: {path}")
            continue

        result.append(path)

    return result

def normalize_path(part: str) -> Path:
    return Path(part.replace('\\', '/'))

def normalise_py_file(path: Path) -> Path:
    if path.suffix != '.py':
        path = path.with_suffix(".py")
    return path

def ensure_path(path: Path) -> Path:
    if path.suffix == '.py':
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        return path

    path.mkdir(parents=True, exist_ok=True)
    return path