from ponytool.req.scan.venv import find_venv
from ponytool.req.scan.python import get_python
from ponytool.req.scan.site_packages import get_site_packages
from ponytool.req.scan.collector import collect_installed_packages


def scan():
    # Пошаговый pipeline: каждая стадия валидирует окружение
    # и возвращает ctx со статусом выполнения
    ctx = check_venv()
    if ctx["status"] != "ok":
        return ctx

    ctx = check_python(ctx)
    if ctx["status"] != "ok":
        return ctx

    ctx = check_site_packages(ctx)
    if ctx["status"] != "ok":
        return ctx

    ctx["packages"] = collect_installed_packages(ctx["site_packages"])
    return ctx

def check_venv():
    venv = find_venv()
    if not venv:
        return {
            "status": "no-venv",
            "python": None,
            "venv": None,
            "site_packages": [],
            "packages": {},
        }

    return {
        "status": "ok",
        "python": None,
        "venv": venv,
        "site_packages": [],
        "packages": {},
    }


def check_python(ctx: dict):
    # Отсутствие venv — не ошибка, а валидный сценарий
    py = get_python()
    python = py["python"]

    if not python:
        ctx["status"] = "error"
        return ctx

    # python и venv могут отличаться от найденного ранее окружения
    ctx["python"] = python
    ctx["venv"] = py["venv"]
    return ctx


def check_site_packages(ctx: dict):
    # site-packages нужны для дальнейшего сбора зависимостей
    site_packages = get_site_packages(ctx["python"])
    if not site_packages:
        ctx["status"] = "error"
        return ctx

    ctx["site_packages"] = site_packages
    return ctx
