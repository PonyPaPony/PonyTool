import json
from ponytool.utils.ui import info, success, warning, error
from ponytool.pytest_script.doctor_test_core import run_doctor_for_tests


def doctor_for_tests(args):
    result = run_doctor_for_tests()

    if args.json:
        _print_json(result)
        return

    _print_human(result, verbose=args.verbose)


def _print_human(r: dict, verbose: bool = False):
    info("Доктор: tests")

    if not r:
        warning("Нет данных для анализа тестов")
        return

    _print_pytest(r)
    has_dir = _print_tests_dir(r)
    if not has_dir:
        return
    if has_dir:
        _print_tests_file(r)
    _print_pycache(r, verbose)

def _print_json(result: dict):
    print(json.dumps(result, ensure_ascii=False, indent=2))

def _print_pytest(r: dict):
    if r["pytest_installed"]:
        success("Pytest: установлен")
    else:
        error("Pytest: не установлен")

def _print_tests_dir(r: dict):
    if not r["tests_dir"]:
        warning("Доктор: папка tests/ не найдена")
        return False

    success(f"Доктор: найдена папка {r['tests_dir']}")
    return True

def _print_tests_file(r: dict):
    if not r["tests_found"]:
        warning("Доктор: файлы test_*.py не найдены")
    else:
        success("Доктор: файлы test_*.py найдены")

def _print_pycache(r: dict, verbose: bool = False):
    if verbose:
        if r["pytest_cache"]:
            info("Pytest cache: найден (.pytest_cache)")
        else:
            info("Pytest cache: отсутствует")
