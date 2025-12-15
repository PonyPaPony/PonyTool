import json
import sys
from pathlib import Path

from ponytool.utils.shell import run
from ponytool.utils.ui import info, success, warn, error
from ponytool.utils.io import ask_confirm

from ponytool.req.scanner import scan
from ponytool.req.imports import collect_imports
from ponytool.req.packages import match_packages
from ponytool.req.writer import write

IGNORED_PACKAGES = {
    "pip",
    "setuptools",
    "wheel"
}


def req_freeze(args):
    info("Генерация requirements.txt")

    python = sys.executable

    # получаем список пакетов
    result = run(
        [python, "-m", "pip", "list", "--format=json"],
        capture=True
    )

    packages = json.loads(result)

    packages = {
        pkg["name"].lower(): pkg["version"]
        for pkg in packages
        if pkg["name"].lower() not in IGNORED_PACKAGES
    }

    write(
        packages=packages,
        path=Path("requirements.txt"),
        dry_run=args.dry_run,
        force=args.yes,
    )

def req_generate(args):
    info("Анализ проекта и генерация requirements.txt")

    scan_result = get_scan_result()
    if not scan_result:
        return
    imports = get_imports()
    packages = get_packages(imports, scan_result["packages"])

    write(
        packages=packages,
        path=Path("requirements.txt"),
        dry_run=args.dry_run,
        force=args.force,
    )

def get_scan_result():
    result = scan()
    status = result["status"]
    if status != "ok":
        if status == 'no-venv':
            error("Виртуальное окружение не найдено. Создайте venv.")
        else:
            error("Ошибка анализа окружения")
        return None
    return result

def get_imports():
    imports = collect_imports(Path.cwd())
    if not imports:
        warn("Импорты не найдены — requirements.txt будет пустым")
    return imports

def get_packages(imports, installed_packages):
    packages = match_packages(imports, installed_packages)
    if not packages:
        warn("Ни один импорт не сопоставлен с установленными пакетами")
    return packages
