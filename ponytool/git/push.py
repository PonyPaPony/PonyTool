from ponytool.utils.shell import run
from ponytool.utils.fs import has_git_repo, working_tree_has_changes as changes
from ponytool.utils.ui import info, success, error, help
from ponytool.utils.io import ask_confirm


def push_to_git(args):
    if not has_git_repo():
        error("Текущая директория не является git-репозиторием")
        return

    run(['git', 'status'])

    if not changes():
        info("Нет изменений для коммита. Push отменён.")
        return

    #! interactive-режим нужен, чтобы можно было остановить push перед коммитом
    interactive = not (args.yes or args.message or args.dry_run)

    if interactive and not ask_confirm("Продолжить коммит и push?"):
        info("Отменено пользователем.")
        return

    # Дефолтное значение для commit -m
    message = args.message or 'Update project files'

    if args.dry_run:
        info("DRY-RUN (ничего не выполняется):")
        help("> git add .")
        help(f'> git commit -m "{message}"')
        help("> git push")
        return

    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', message])
    run(['git', 'push'])

    success("Push выполнен успешно")
