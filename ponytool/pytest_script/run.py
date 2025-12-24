import sys
import subprocess
from ponytool.utils.shell import run
from ponytool.utils.ui import info
from ponytool.pytest_script.report_test import save_test_report


def run_tests(args):
    info("Запуск тестов проекта")

    python = sys.executable # используем текущий интерпретатор (venv)

    cmd = [python, '-m', 'pytest']

    if args.k:
        cmd.extend(['-k', args.k])

    if args.rootdir:
        cmd.extend(['--rootdir', args.rootdir])

    # pytest запускается без флагов по умолчанию,
    # чтобы соответствовать локальному workflow проекта

    if not args.k and not args.rootdir:
        info("Запуск всех тестов")

    try:
        run(cmd)   # check=True по умолчанию
        save_test_report(passed=True)
    except subprocess.CalledProcessError:
        save_test_report(passed=False)