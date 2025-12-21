from ponytool.utils.shell import run
from ponytool.utils.io import ask_confirm, ask_input
from ponytool.utils.fs import has_git_repo
from ponytool.utils.ui import info, error


def remove_git_data(args):
    if not has_git_repo():
        error("❌ Не git-репозиторий")
        return

    if not ask_confirm("Ты уверен, что хочешь удалить данные git?"):
        info("Отменено")
        return

    choice = ask_input(
        "Что удалить? (branch / repo / file)",
        default="branch"
    )

    choice = choice.lower().strip()

    ensure_choice(choice)


def ensure_choice(choice):
    if choice == "branch":
        branch_choice()
    elif choice == "repo":
        repo_choice()
    elif choice == "file":
        file_choice()
    else:
        error("Неизвестный вариант. Используй: branch / repo / file")

def branch_choice():
    branch = ask_input("Имя ветки")
    if not branch:
        error("Имя ветки не задано")
        return
    run(["git", "branch", "-D", branch])  # удаляем только ветку, рабочее дерево не трогаем
    info(f"Ветка '{branch}' удалена")

def repo_choice():
    if not ask_confirm("Это удалит ВСЕ незакоммиченные изменения. Продолжить?"):
        return
    run(["git", "clean", "-fd"])
    run(["git", "reset", "--hard"])
    info("Рабочее дерево очищено")

def file_choice():
    file = ask_input("Название файла")
    if not file:
        error("Имя файла не задано")
        return
    run(['git', 'rm', '--cached', file])
    info(f"Файл '{file}' удалён из индекса")
