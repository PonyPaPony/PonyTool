from pathlib import Path
import tomllib


def load_toml(path: Path) -> dict:
    if not path.exists():
        return {} # отсутствие файла — нормальный сценарий
    with path.open('rb') as f:
        return tomllib.load(f)

def merge_config_dicts(main: dict, override: dict) -> dict:
    # merge in-place, без копирования
    for key, value in override.items():
        if (
            key in main
            and isinstance(main[key], dict)
            and isinstance(value, dict)
        ):
            merge_config_dicts(main[key], value)
        else:
            main[key] = value
    return main

def load_project_config() -> dict:
    root = Path(__file__).resolve().parent.parent

    defaults = load_toml(root / 'config' / 'defaults.toml')
    user = load_toml(root / 'config' / 'user.toml')

    return merge_config_dicts(defaults, user)
