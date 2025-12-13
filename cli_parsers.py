def git_parser(action_parser):
    action_parser.add_argument(
        "-m", "--message",
        help="Commit message"
    )
    action_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )
    action_parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmations"
    )


def project_parser(action_parser):
    action_parser.add_argument(
        "--no-git",
        action="store_true",
        help="Не инициализировать git-репозиторий"
    )
    action_parser.add_argument(
        "--name",
        help="Имя проекта (будет создана папка)"
    )

def project_clean_parser(action_parser):
    action_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать, что будет удалено, без удаления"
    )
    action_parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Не спрашивать подтверждение"
    )

def run_tests_parser(action_parser):
    action_parser.add_argument(
        "-k",
        help="Фильтр тестов pytest (-k)"
    )

def cov_tests_parser(action_parser):
    action_parser.add_argument(
        '--html',
        action='store_true',
        help="HTML отчёт покрытия"
    )

def git_init_parser(parser):
    parser.add_argument("--remote", help="URL репозитория")
    parser.add_argument("--ssh", action="store_true", help="Использовать SSH")
    parser.add_argument("-y", "--yes", action="store_true", help="Без подтверждений")

def git_rollback_parser(parser):
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Без подтверждений"
    )