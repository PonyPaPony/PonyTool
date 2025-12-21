import json
import sys
from ponytool.utils.ui import error, success, info, warning
from ponytool.project.project_status import project_status

LABELS = {
    "pyproject": "pyproject.toml",
    "requirements": "requirements.txt",
    "tests": "tests/",
}

def print_project_status(status: dict, verbose: bool = False):
    info("Статус проекта")

    _print_python(status["python"], status["venv"])
    _print_git(status["git"])
    _print_files(status["files"])
    _print_tests(status.get("tests"), verbose)

def _print_python(python: str, venv: dict):
    if not python:
        error("Python не найден")
        return

    if venv["active"] and venv["project_venv"]:
        success(f"Python: {python} (venv проекта)")
    elif venv["active"]:
        warning(f"Python: {python} (venv не проекта)")
    else:
        warning(f"Python: {python} (без venv)")

def _print_git(git: dict):
    if not git.get("ok"):
        warning("Git: есть проблемы")
        for p in git.get("problems", []):
            warning(f"  - {p}")
    else:
        success("Git: в порядке")

def _print_files(status: dict):
    info("Файлы проекта:")

    for name, exists in status.items():
        if exists:
            label = LABELS.get(name, name)
            success(f"{label}: найден")
        else:
            warning(f"{name}: не найден")

def _print_tests(status: dict | None, verbose: bool):
    if not status:
        warning("Tests: информация отсутствует")
        return

    if not status["exists"]:
        warning("Tests: папка tests/ не найдена")
        return

    if not status["found"]:
        warning("Tests: test_*.py не найдены")
        return

    if status["passed"] is True:
        success("Tests: последний запуск успешен")
    elif status["passed"] is False:
        error("Tests: последний запуск завершился с ошибками")
    else:
        info("Tests: найдены, но ещё не запускались")

def _print_short(status: dict):
    flags = []

    flags.append("PY✓" if status["python"] else "PY✗")
    flags.append("VENV✓" if status["venv"]["active"] else "VENV✗")
    git = status.get("git") or {}
    flags.append("GIT✓" if git.get("ok") else "GIT✗")

    print(" ".join(flags))

def _status_for_json(status: dict) -> dict:
    out = dict(status)

    # Python / venv приводим к строкам
    out["python"] = str(out["python"]) if out.get("python") else None

    venv = out.get("venv", {})
    if venv:
        out["venv"] = {
            "active": venv.get("active"),
            "project_venv": venv.get("project_venv"),
            "path": str(venv["path"]) if venv.get("path") else None,
        }

    return out

def _print_json(status: dict) -> None:
    print(json.dumps(
        _status_for_json(status),
        ensure_ascii=False,
        indent=2
    ))

def get_project_status(args):
    status = project_status()
    if args.short:
        _print_short(status)
    elif args.json:
        _print_json(status)
        sys.exit(0 if status["ok"] else 1)
    else:
        print_project_status(status, verbose=args.verbose)
