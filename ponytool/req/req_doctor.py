import json

from ponytool.utils.ui import (info, warning, error, success)
from ponytool.req.doctor_core import run_doctor


def doctor_for_requirements(args):
    result = run_doctor()

    if args.json:
        print(json.dumps(_jsonable(result), ensure_ascii=False, indent=2))
        return

    _print_human(result, verbose=args.verbose)

def _line_ok(ok_value, title: str, value: str):
    if ok_value:
        success(f"{title}: {value}")
    else:
        warning(f"{title}: {value}")

def _jsonable(r: dict) -> dict:
    # Приведение Path к str для JSON-сериализации
    out = dict(r)
    out['python'] = str(out['python']) if out['python'] else None
    out['venv'] = str(out['venv']) if out['venv'] else None
    out['site_packages'] =  [str(p) for p in out.get('site_packages', [])]
    return out

def unmatched_msg(r):
    if r['unmatched_imports']:
        warning("\nИмпорты без пакетов:")
        for i in r['unmatched_imports']:
            warning(f"  - {i}")

    if r['unused_packages']:
        info("\nНеиспользуемые пакеты:")
        for p in r['unused_packages']:
            info(f"  - {p}")

def problems_and_hints(r):
    if r['problems']:
        warning("\nПроблемы:")
        for p in r['problems']:
            warning(f"  - {p}")

    if r['hints']:
        info("\nПодсказки:")
        for h in r['hints']:
            info(f"  - {h}")


def _print_human(r: dict, verbose: bool):
    if r['ok']:
        success("Doctor: окружение выглядит нормально")
    else:
        error("Doctor: обнаружены проблемы")

    _line_ok(r['python_ok'], "Python", str(r['python']))
    _line_ok(r['venv_ok'], "Venv", str(r['venv']))

    if verbose:
        info(f"Site-packages: {len(r['site_packages'])}")
    info(f"Установлено пакетов: {r['installed_packages']}")
    info(f"Импортов найдено: {r['imports_count']}")
    info(f"Матчей: {r['matched_count']}")

    unmatched_msg(r)
    problems_and_hints(r)
