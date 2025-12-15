from pathlib import Path
from ponytool.utils.ui import info, success, warn


def format_requirements(packages: dict[str, str]) -> list[str]:
    lines = []

    for name in sorted(packages):
        version = packages[name]
        lines.append(f"{name}=={version}")

    return lines

def print_requirements(lines: list[str]):
    info("requirements.txt (dry-run):")
    for line in lines:
        print(line)

def write_requirements(lines: list[str], path: Path, overwrite: bool = False):
    if path.exists() and not overwrite:
        warn(f"{path} уже существует — используйте --force")
        return False

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    success(f"Создан {path}")
    return True

def write(packages: dict[str, str], path: Path, dry_run: bool, force: bool):
    if not packages:
        warn("Пакеты не найдены — requirements.txt пуст")
        return

    lines = format_requirements(packages)

    if dry_run:
        print_requirements(lines)
        return

    write_requirements(lines, path, overwrite=force)
