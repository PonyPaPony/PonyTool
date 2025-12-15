from pathlib import Path

from ponytool.req.scan.venv import find_active_venv, find_venv
from ponytool.req.scan.python import get_python
from ponytool.req.scan.site_packages import get_site_packages
from ponytool.req.scan.collector import collect_installed_packages
from ponytool.req.imports import collect_imports
from ponytool.req.packages import match_packages


def run_doctor():
    problems = []
    hints = []

    python, _ = get_python()
    if not python:
        problems.append("Python интерпретатор не найден")
        return _result(False, None, None, [], 0, 0, 0, problems, hints)

    venv = find_active_venv() or find_venv(Path.cwd())
    if not venv:
        problems.append("Виртуальное окружение не найдено")
        hints.append("Создайте venv: python -m venv .venv")

    site_packages = get_site_packages(python) if venv else []
    if not site_packages:
        problems.append("site-packages не найдены")

    packages = collect_installed_packages(site_packages)
    imports = collect_imports(Path.cwd())
    matched = match_packages(imports, packages)

    if imports and not matched:
        problems.append("Импорты не сопоставлены с установленными пакетами")

    ok = not any(p for p in problems if "не найден" in p)

    return _result(
        ok=ok,
        python=python,
        venv=venv,
        site_packages=site_packages,
        installed=len(packages),
        imports=len(imports),
        matched=len(matched),
        problems=problems,
        hints=hints,
    )


def _result(ok, python, venv, site_packages, installed, imports, matched, problems, hints):
    return {
        "ok": ok,
        "python": python,
        "venv": venv,
        "site_packages": site_packages,
        "installed_packages": installed,
        "imports": imports,
        "matched": matched,
        "problems": problems,
        "hints": hints,
    }
