import shutil
import re
from pathlib import Path

from ponytool.utils.shell import run, check
from ponytool.utils.fs import has_git_repo
from ponytool.utils.ui import info, success, warning, error
from ponytool.utils.io import ask_input, ask_confirm
from ponytool.utils.shell import run_output


def ensure_git_available():
    if not check(['git', '--version']):
        error("Git не установлен или недоступен в PATH")
        return False
    return True

def ensure_repo_available():
    if has_git_repo():
        warning("Git-репозиторий уже существует")

    info("Инициализация git-репозитория")
    run(['git', 'init'])

def ensure_remote_available(args):
    if get_remote():
        warning("Remote уже настроен — пропускаем")
        return None

    remote = args.remote or ask_input("Введите URL репозитория")

    if not remote:
        error("Remote URL не указан")
        return None

    if not valid_remote(remote):
        error("Remote URL выглядит некорректно")
        warning("Примеры:")
        warning("  https://github.com/user/repo.git")
        warning("  git@github.com:user/repo.git")
        return None

    info(f"Remote будет установлен как:\n  {remote}")

    if not args.yes and not ask_confirm("Продолжить?"):
        warning("Настройка remote отменена")
        return None

    return set_remote(remote)

def get_remote() -> set[str]:
    out = run_output(['git', 'remote'], check=False)
    return set(out.splitlines()) if out else set()

def valid_remote(remote):
    return bool(
        re.match(
            r"^(https://|http://|git@)[\w\.-]+[:/][\w\.-]+/[\w\.-]+(\.git)?$",
            remote
        )
    )

def set_remote(remote):
    try:
        run(["git", "remote", "add", "origin", remote])
        success("Remote origin добавлен")
        return remote
    except Exception:
        error("Не удалось добавить remote")
        warning("Вы можете исправить это командой:")
        warning("  git remote remove origin")
        return None

def initial_commit(args):
    status = run_output(['git', 'status', '--porcelain'], check=False)

    if not status.strip():
        warning("Нет файлов для коммита")
        return False

    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', 'Initial commit'])
    success("Создан первый коммит")
    return True

def initial_push():
    remotes = get_remote()

    if 'origin' not in remotes:
        error("Remote origin не найден — push невозможен")
        return

    current = run_output(
        ['git', 'branch', '--show-current'],
        check=False
    ).strip()

    if current != 'main':
        run(['git', 'branch', '-M', 'main']) # приводим ветку к main для единообразия
    run(['git', 'push', '-u', 'origin', 'main'])
    success("Репозиторий успешно опубликован 🚀")

def rollback_repository():
    """
    Для отката ошибочной установки Git или его удаления
    """
    git_dir = Path(".git")

    if not git_dir.exists():
        warning("Откат невозможен — .git не найден")
        return

    info("Будет удалён git-репозиторий (.git)")
    warning("Файлы проекта затронуты не будут")

    if not ask_confirm("Продолжить откат?"):
        warning("Откат отменён")
        return

    shutil.rmtree(git_dir)
    success("Git-репозиторий успешно удалён")

def git_init(args):
    if not ensure_git_available():
        return

    if args.rollback:
        rollback_repository()
        return

    if has_git_repo() and get_remote():
        warning("Git-репозиторий и remote уже настроены")
        return

    ensure_repo_available()

    remote = ensure_remote_available(args)
    if not remote:
        return

    committed(args)

def committed(args):
    com = initial_commit(args)

    if args.no_push:
        warning("Push пропущен (--no-push)")
        return

    if com or args.yes:
        initial_push()
    else:
        warning("Push пропущен (нет коммита)")
        info("Добавьте файлы и выполните: pony git push")
