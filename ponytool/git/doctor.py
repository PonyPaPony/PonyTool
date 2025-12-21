from ponytool.utils.shell import check, run_output
from ponytool.utils.fs import has_git_repo
from ponytool.utils.ui import success, warning, error

CHECKS = []  # накапливаем найденные проблемы для финального отчёта

def git_doctor(args=None):
    CHECKS.clear()

    if not check_git():
        return
    if not check_repo():
        return

    check_all(CHECKS)
    print_result()

def check_git() -> bool:
    if check(['git', '--version']):
        success("Git установлен")
        return True
    error("Git не установлен")
    return False

def check_repo() -> bool:
    if has_git_repo():
        success("Git-репозиторий найден")
        return True
    error("Текущая директория не является git-репозиторием")
    return False

def check_remote():
    remotes = run_output(['git', 'remote'], check=False).strip()
    if remotes:
        success("Remote origin настроен")
    else:
        warning("Remote не настроен")

    return 'remote'

def check_upstream():
    upstream = run_output(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        check=False
    ).strip()

    if upstream:
        success(f"Upstream: {upstream}")
    else:
        warning("Upstream не найден")

    return 'upstream'

def check_dirty():
    dirty = run_output(["git", "status", "--porcelain"], check=False).strip()
    if dirty:
        warning("Есть незакоммиченные изменения")
        return 'dirty'

    success("Рабочая директория чистая")
    return None

def check_branch():
    branch = run_output(
        ["git", "branch", "--show-current"],
        check=False
    ).strip()

    if branch == "main":
        success("Ветка: main")
    else:
        warning(f"Текущая ветка: {branch}")

    return 'branch'

def check_all(checks):
    checks.append(check_remote())
    checks.append(check_upstream())
    checks.append(check_dirty())
    checks.append(check_branch())

# ключи возвращаются check_* функциями и используются для рекомендаций
RECOMMENDATIONS = {
    "remote": "Добавьте remote: pony git init",
    "upstream": "Настройте upstream: git push -u origin main",
    "dirty": "Закоммитьте изменения перед push",
    "branch": "Рекомендуется использовать ветку main",
}

def print_result():
    print()
    if not CHECKS:
        success("Git-конфигурация в порядке 🎉")
        return

    warning("Обнаружены проблемы:")
    for key in CHECKS:
        print(f"  - {RECOMMENDATIONS[key]}")
