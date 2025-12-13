import argparse

from ponytool.utils.ui import error, info
from ponytool.cli_parsers import *

from ponytool.project.init import project_init
from ponytool.project.clean import project_clean

from ponytool.git.push import git_push
from ponytool.git.status import git_status
from ponytool.git.remove import git_remove
from ponytool.git.init import git_init
from ponytool.git.info import git_info
from ponytool.git.rollback import git_rollback

from ponytool.test.run import run_tests
from ponytool.test.coverage import run_coverage

DISPATCH_TABLE = {
    "project": {
        "init": project_init,
        "clean": project_clean,
    },
    "git": {
        'init': git_init,
        'info': git_info,
        "push": git_push,
        "status": git_status,
        "remove": git_remove,
        "rollback": git_rollback,
    },
    "test": {
        "run": run_tests,
        "coverage": run_coverage,
    },
}

PARSER_TABLE = {
    ("git", "push"): git_parser,
    ("git", 'init'): git_init_parser,
    ("git", 'rollback'): git_rollback_parser,
    ("project", "init"): project_parser,
    ("project", "clean"): project_clean_parser,
    ("test", 'run'): run_tests_parser,
    ("test", 'coverage'): cov_tests_parser,
}


def main():
    parser = argparse.ArgumentParser(prog="pony")
    subparsers = parser.add_subparsers(dest="command")

    for section, actions in DISPATCH_TABLE.items():
        section_parser = subparsers.add_parser(section)
        section_sub = section_parser.add_subparsers(dest="action")

        for action in actions:
            action_parser = section_sub.add_parser(action)

            parser_func = PARSER_TABLE.get((section, action))
            if parser_func:
                parser_func(action_parser)

    args = parser.parse_args()
    dispatch(args)

def dispatch(args):
    if not args.command:
        run_interactive_menu()
        return

    if args.command not in DISPATCH_TABLE:
        error(f"Неизвестная команда: {args.command}")
        return

    if not args.action:
        print_section_help(args.command)
        return

    handler = DISPATCH_TABLE[args.command].get(args.action)

    if not handler:
        print_action_help(args.command)
        return

    handler(args)

def print_section_help(section: str):
    info(f"\nДоступные действия для '{section}':")
    for action in DISPATCH_TABLE[section]:
        info(f"  - {action}")

def print_action_help(section: str):
    info(f"\nНеизвестное действие для '{section}'.")
    print_section_help(section)

def run_interactive_menu():
    info("\nPonyTool — интерактивный режим\n")

    for section, actions in DISPATCH_TABLE.items():
        info(section)
        for action in actions:
            info(f"  - {action}")

    info("\nПример: pony git push")

if __name__ == '__main__':
    main()