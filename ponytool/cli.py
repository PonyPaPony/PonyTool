import argparse
import sys

from ponytool.utils.ui import error, info
from ponytool.cli_config import PARSER_TABLE, DISPATCH_TABLE

def main():
    """
    Точка входа CLI.

    Изначально тут буквально было все, теперь оптимизировано.
    """
    parser = argparse.ArgumentParser(
        prog='pony',
        description='PonyTool CLI (в процессе разработки)'
    )
    # argparse иногда ведёт себя странно,
    # если не указать dest явно
    subparsers = parser.add_subparsers(dest='command')

    for section, actions in DISPATCH_TABLE.items():
        # TODO: iternal-секции тут могут быть лишними
        section_parser = subparsers.add_parser(section)

        # Некоторые секции не имеют action
        if not actions:
            continue

        section_subparsers = section_parser.add_subparsers(dest='action')

        # После диеты
        action_check(section, actions, section_subparsers)


    args = parser.parse_args()

    # ВАЖНО: dispatch не кидает исключения наружу
    dispatch(args)

def dispatch(args):
    """
    Роутинг Команд

    И что, что некрасивый за то рабочий
    """
    # args.command может отсутствовать при странных вызовах
    if not hasattr(args, 'command') or args.command is None:
        run_interactive_menu()
        return

    # Мама, пожалуйста, ударь, тапком, того кто придумал, что C и С должны быть похожи (да они разные)
    if args.command not in DISPATCH_TABLE:
        error(f"Неизвестная команда: {args.command}")
        print_available_sections()
        return

    # command есть, но action нет
    if not getattr(args, 'action', None):
        print_section_help(args.command)
        return

    handler = DISPATCH_TABLE[args.command].get(args.action)

    if handler is None:
        error(f"Неизвестное действие: {args.action}")
        print_section_help(args.command)
        return

    try:
        handler(args)
    except KeyboardInterrupt:
        info("\nОперация отменена пользователем")
    except Exception as err:
        # CLI Хэш-тэг живи, ЖИВИ
        error("Произошла ошибка при выполнении команды")
        error(str(err))

def print_available_sections():
    info("\nДоступные разделы:")
    for section in DISPATCH_TABLE.keys():
        info(f"  - {section}")


def print_section_help(section):
    info("")
    info(f"Доступные действия для '{section}':")

    actions = DISPATCH_TABLE.get(section)
    if not actions:
        info("  (действий нет)")
        return

    for action in actions:
        info(f"  - {action}")

    info("\nПример:")
    info(f"  pony {section} <action>")


# Сколько раз я при отладке забывал команды...
def run_interactive_menu():
    """
    Интерактивный режим.

    Используется как fallback,
    когда CLI запущен без аргументов.
    """

    info("\nPonyTool — интерактивный режим\n")

    for section, actions in DISPATCH_TABLE.items():
        info(section)

        if not actions:
            info("  (нет действий)")
            continue

        for action in actions:
            info(f"  - {action}")

    info("\nПример использования:")
    info("  pony git push")

def action_check(section, actions, section_subparsers):
    """
    Main был слишком перегружен,
    всучил ему диету
    """
    for action in actions:
        action_parser = section_subparsers.add_parser(action)

        parser_func = PARSER_TABLE.get((section, action))
        if parser_func is None:
            # Христа ради заклинаю не падай
            continue

        try:
            parser_func(action_parser)
        except Exception as e:
            # Парсеры порой ломают CLI
            error(f"Ошибка инициализации парсера {section}:{action}")
            error(str(e))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        info("\nВыход")
        sys.exit(130)
