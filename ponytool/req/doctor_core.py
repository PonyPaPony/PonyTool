from pathlib import Path

from ponytool.req.scan.venv import find_active_venv, find_venv
from ponytool.req.scan.python import get_python
from ponytool.req.scan.site_packages import get_site_packages
from ponytool.req.scan.collector import collect_installed_packages
from ponytool.req.imports import collect_imports
from ponytool.req.packages import (match_packages, find_unused_packages, find_unmatched_imports)


def run_doctor():
    # Диагностирует окружение и зависимости проекта
    python, _ = get_python()
    venv = find_active_venv() or find_venv(Path.cwd())
    site_packages = get_site_packages(python) if venv else []

    installed = collect_installed_packages(site_packages)
    imports = collect_imports(Path.cwd())

    matched = match_packages(imports, installed)
    unused = find_unused_packages(installed, matched)
    unmatched = find_unmatched_imports(set(imports), matched)

    problems, hints = get_problems(
        python, venv, site_packages, imports, matched, unused, unmatched
    )

    # ok означает, что окружение пригодно для работы,
    # даже если есть предупреждения
    ok = python is not None and venv is not None

    return _result(
        ok=ok,
        python=python,
        venv=venv,
        site_packages=site_packages,
        installed=len(installed),
        imports=len(imports),
        matched=len(matched),
        problems=problems,
        hints=hints,
        unused_packages=unused,
        unmatched_imports=unmatched,
    )

def get_problems(
    python,
    venv,
    site_packages,
    imports,
    matched,
    unused_packages,
    unmatched_imports,
):
    # Список проблем и подсказок собирается независимо,
    # чтобы CLI мог решать, как их отображать
    problems = []
    hints = []

    if not python:
        problems.append("Python интерпретатор не найден")

    if not venv:
        problems.append("Виртуальное окружение не найдено")
        hints.append("Создайте venv: python -m venv .venv")

    if not site_packages:
        problems.append("site-packages не найдены")

    if imports and not matched:
        problems.append("Ни один импорт не сопоставлен с установленными пакетами")

    if unmatched_imports:
        problems.append("Есть импорты без соответствующих пакетов")

    if unused_packages:
        problems.append("Есть неиспользуемые пакеты в окружении")

    return problems, hints



def _result(
        ok,
        python,
        venv,
        site_packages,
        installed,
        imports,
        matched,
        problems,
        hints,
        unused_packages,
        unmatched_imports,
):
    return {
        'ok': ok,

        'python': python,
        "python_ok": python is not None,

        'venv': venv,
        'venv_ok': venv is not None,

        'site_packages': len(site_packages),

        "installed_packages": installed,
        'imports_count': imports,
        'matched_count': matched,

        'unused_packages': list(unused_packages),
        'unmatched_imports': list(unmatched_imports),

        'problems': problems,
        'hints': hints,

    }
