import json
import sys
from pathlib import Path

from ponytool.utils.shell import run
from ponytool.utils.ui import (info, success, warning, error)
from ponytool.req.scanner import scan
from ponytool.req.imports import collect_imports
from ponytool.req.writer import write
from ponytool.req.analyzer import analyze

IGNORED_PACKAGES = {
    "pip",
    "setuptools",
    "wheel"
}

REQ_PATH = Path("requirements.txt")


def freeze_requirements(args):
    info("Генерация requirements.txt")

    py = sys.executable

    result = run(
        [py, '-m', 'pip', 'list', '--format=json'],
        capture=True
    )

    pkg = json.loads(result)

    pkg = {
        item["name"].lower(): {
            "version": item["version"],
            "imports": set(),
            "files": set(),
        }
        for item in pkg
        if item["name"].lower() not in IGNORED_PACKAGES
    }

    write(
        packages=pkg,
        path=REQ_PATH,
        dry_run=args.dry_run,
        force=args.yes,
    )

def generate_requirements(args):
    info("Анализ проекта и генерация requirements.txt")

    info("Сканирование окружения…")
    scan_results = get_scan_result()
    if not scan_results:
        return

    info("Поиск импортов в проекте…")
    imp = get_imports()
    info("Сопоставление пакетов…")

    analysis = analyze(
        imports=imp,
        installed=scan_results["packages"]
    )

    pkg = analysis["matched"]
    unmatched = analysis["unmatched_imports"]
    unused = analysis["unused_packages"]

    if args.strict and (unused or unmatched):
        report_unused_unmatched(unused, unmatched)
        return

    write(
        packages=pkg,
        path=REQ_PATH,
        dry_run=args.dry_run,
        force=args.force,
    )

def get_scan_result():
    result = scan()
    status = result['status']
    if status != 'ok':
        if status == 'no-venv':
            error("Виртуальное окружение не найдено. Создайте venv.")
        else:
            error("Ошибка анализа окружения")
        return None
    return result

def get_imports():
    imports = collect_imports(Path.cwd())
    if not imports:
        warning("В проекте нет Python-импортов")
        return {}  # Если возвращать None, может падать с ошибкой
    return imports

def report_unused_unmatched(unused, unmatched):
    error("Strict mode: обнаружены проблемы")
    if unmatched:
        warning("Импорты без пакетов:")
        for i in unmatched:
            warning(f"  - {i}")
    if unused:
        warning("Неиспользуемые пакеты:")
        for p in unused:
            warning(f"  - {p}")

def clean_requirements(args):
    scan_result = get_scan_result()
    if not scan_result:
        return

    imports = get_imports()
    analysis = analyze(imports, scan_result["packages"])
    unused = analysis["unused_packages"]

    if not unused:
        success("Неиспользуемых пакетов нет")
        return

    warning("Эта команда удалит все неиспользуемые пакеты из текущего venv")
    warning("Включая pytest, pip-tools и т.д.")

    mode = resolve_clean_mode(args)

    if mode == "dry-run":
        info("DRY-RUN: пакеты, которые будут удалены:")
        for pkg in sorted(unused):
            print(f"  - {pkg}")
        return

    if not confirm_clean(mode, unused, args.yes):
        warning("Отменено")
        return

    py = sys.executable
    for pkg in unused:
        info("Удаление пакетов…")
        run([py, '-m', 'pip', 'uninstall', '-y', pkg])

    success("Очистка завершена")

def resolve_clean_mode(args) -> str:
    """
    Возвращает режим очистки:
    - "dry-run"
    - "project-only"
    - "all"
    """
    if args.dry_run:
        return "dry-run"
    if args.all:
        return "all"
    return "project-only"

def confirm_clean(mode: str, packages: set[str], force: bool) -> bool:
    if force:
        return True

    warning("Эта команда изменит текущее виртуальное окружение")

    if mode == "all":
        warning("Будут удалены ВСЕ неиспользуемые пакеты")
    elif mode == "project-only":
        warning("Будут удалены пакеты, не используемые в проекте")

    warning("Пакеты к удалению:")
    for pkg in sorted(packages):
        warning(f"  - {pkg}")

    from ponytool.utils.io import ask_confirm
    return ask_confirm("Продолжить?")
