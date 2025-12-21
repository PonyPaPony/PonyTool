#! ВАЖНО:
#! Имена аргументов в argparse должны точно соответствовать
#! использованию в handler-функциях (args.<name>).
#! Несоответствие приводит к runtime-ошибкам.

# TODO: подумать над унификацией общих аргументов (--yes, --rootdir)

# --- Парсеры для Project --- #
def project_init_parser(parser):
    parser.add_argument(
        '--no-git',
        action='store_true',
        help="Не инициализировать git-репозиторий"
    )
    parser.add_argument(
        '--name',
        help="Имя проекта (будет создана папка)"
    )

def project_clear_parser(parser):
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать, что будет удалено, без удаления"
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Не спрашивать подтверждение"
    )

def project_status_parser(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--short",
        action="store_true",
        help="Краткий вывод"
    )
    group.add_argument(
        "--json",
        action="store_true",
        help="Вывести в JSON"
    )
    group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Подробный вывод"
    )

# --- Парсеры для Git --- #

def git_info_parser(parser):
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help='Показать подробную информацию'
    )
    parser.add_argument(
        '--short',
        action='store_true',
        help="Краткий вывод (для скриптов)"
    )

def git_init_parser(parser):
    parser.add_argument("--remote", help="URL git-репозитория")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("-y", "--yes", action="store_true")

def git_push_parser(parser):
    parser.add_argument("-m", '--message', help='Commit сообщение')
    parser.add_argument('--dry-run', action="store_true", help="Покажи что будет сделано без выполнения операции")
    parser.add_argument("-y", "--yes", action="store_true", help='Пропуск подтверждения')

def git_rollback_parser(parser):
    parser.add_argument("-y", "--yes", action="store_true", help="Без подтверждения")

# ----- Парсеры для tests ----- #
def run_py_test_parser(parser):
    parser.add_argument("-k", help="Фильтр тестов pytest (-k)")
    parser.add_argument("--rootdir", help="Путь к тестам")

def cov_py_test_parser(parser):
    parser.add_argument("-html", action="store_true", help="HTML отчёт покрытия")
    parser.add_argument("--rootdir", help="Путь к тестам")

def doc_py_test_parser(parser):
    parser.add_argument("--json", action="store_true", help="Вывести результат в JSON")
    parser.add_argument("-v", "--verbose", action="store_true", help="Показать подробности")

# ----- Парсеры для requirements Script ----- #
def req_gen_parser(parser):
    parser.add_argument("--dry-run", action="store_true", help="Показать requirements.txt без записи")
    parser.add_argument("--force", action="store_true", help="Перезаписать requirements.txt")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Ошибка, если есть не сопоставленные импорты или лишние пакеты"
    )

def req_freeze_parser(parser):
    parser.add_argument('-y', '--yes', action="store_true", help="Не спрашивать подтверждения")
    parser.add_argument("--dry-run", action="store_true", help="Показать requirements.txt без записи")

def req_clean_parser(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--all",
        action="store_true",
        help="Удалить все неиспользуемые пакеты из venv"
    )
    group.add_argument(
        "-p",
        "--project-only",
        action="store_true",
        help="Удалить пакеты, не используемые проектом (по умолчанию)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать, что будет удалено, без выполнения"
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Не спрашивать подтверждение"
    )

def req_doctor_parser(parser):
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывести результат в JSON"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Показать подробности"
    )