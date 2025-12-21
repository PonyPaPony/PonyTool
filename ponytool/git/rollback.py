import shutil
from pathlib import Path

from ponytool.utils.fs import has_git_repo
from ponytool.utils.ui import warning, success, info, error
from ponytool.utils.io import ask_confirm


def git_rollback(args):
    if not has_git_repo():
        warning("Текущая директория не является git-репозиторием")
        return

    git_dir = Path.cwd() / '.git'

    info("Будет удалён git-репозиторий (.git)")
    warning("Файлы проекта затронуты не будут")

    if not args.yes:
        if not ask_confirm("Продолжить откат?"):
            info("Откат отменён")
            return

    try:
        shutil.rmtree(git_dir)
        success("Git-репозиторий успешно удалён")
    except FileNotFoundError:
        error("Git-репозиторий не найден!")