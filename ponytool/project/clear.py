from pathlib import Path
import shutil

from ponytool.utils.ui import info, warning, success
from ponytool.utils.io import ask_confirm
from ponytool.utils.config import load_project_config

def load_trash_list():
    config = load_project_config()
    trash = (
        config
        .get('project', {})
        .get('clean', {})
        .get('trash', [])
    )
    # список путей берётся из конфига, чтобы не хардкодить очистку

    if not trash:
        warning("Список очистки пуст — проверь конфигурацию")

    return trash

def problem_check(args, found):
    if not found:
        info("Нечего очищать — проект чистый")
        return

    info("Будут удалены следующие элементы:")
    for path in found:
        warning(f"  - {path.name}")

    if args.dry_run:
        info("DRY-RUN: удаление не выполняется")
        return # важно для проверки конфига без риска

    if not args.yes:
        if not ask_confirm("Продолжить очистку?"):
            info("Очистка отменена")
            return

def project_clean(args):
    root = Path.cwd()
    found = []
    trash = load_trash_list()

    for item in trash:
        path = root / item
        if path.exists():
            found.append(path)

    problem_check(args, found)

    for path in found:
        if path.is_dir():
            shutil.rmtree(path)
            success(f"Удалена папка {path.name}")
        else:
            path.unlink()
            success(f"Удалён файл {path.name}")
