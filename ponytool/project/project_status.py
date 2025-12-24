import sys
from pathlib import Path

from ponytool.req.scan.venv import find_active_venv, find_venv
from ponytool.pytest_script.doctor_test_core import run_doctor_for_tests
from ponytool.pytest_script.report_test import load_test_report
from ponytool.utils.fs import has_git_repo
from ponytool.utils.shell import check

FILES = {
    "pyproject": "pyproject.toml",
    "setup": "setup.py",
    "requirements": "requirements.txt",
    "tests_cache": ".pytest_cache",
 }


def project_status():
    python = python_status()
    venv = venv_status()
    git = git_status()
    files = file_status()
    tests = status_test()

    ok = bool(python) and venv["active"]

    if git and not git.get("ok", False):
        ok = False

    return {
        "ok": ok,
        "python": python,
        "venv": venv,
        "git": git,
        "files": files,
        "tests": tests,
    }

def git_status():
    if not check(['git', '--version']):
        return {
            "ok": False,
            "problems": ["Git не установлен"],
        }

    if not has_git_repo():
        return {
            "ok": False,
            "problems": ["Не является git-репозиторием"],
        }

    return {
        "ok": True,
        "problems": [],
    }

def venv_status():
    active = sys.prefix != sys.base_prefix
    venv = find_active_venv() or find_venv(Path.cwd())

    return {
        "active": active,
        "path": venv,
        "project_venv": bool(venv and venv.exists()),
    }

def python_status():
    v = sys.version_info
    return f"{v.major}.{v.minor}.{v.micro}"

def file_status():
    status = {}
    for key, name in FILES.items():
        status[key] = (Path.cwd() / name).exists()
    return status

def status_test():
    tests = run_doctor_for_tests()
    report = load_test_report()

    return {
        "exists": bool(tests["tests_dir"]),
        "found": tests["tests_found"],
        "passed": report["passed"] if report else None,
        "last_run": report["last_run"] if report else None,
    }
