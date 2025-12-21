import sys
from ponytool.utils.ui import info
from ponytool.utils.shell import run


# Задача: Написать функцию для запуска pytest с покрытием -cov
def run_coverage_test(args):
    info("Запуск тестов проекта с покрытием.")

    python = sys.executable  # используем текущий интерпретатор (venv)

    cmd = [python, '-m', 'pytest', '--cov']

    if args.rootdir:
        cmd.extend(['--rootdir', args.rootdir])

    if args.html:
        cmd.append("--cov-report=html")
    else:
        # текстовый отчёт используется по умолчанию,
        # потому что HTML генерируется отдельно в release-сценарии
        cmd.append("--cov=report=term")

    run(cmd)