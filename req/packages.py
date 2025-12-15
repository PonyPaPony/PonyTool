from pathlib import Path


def normalize(name: str) -> str:
    return name.lower().replace("-", "_")


def matches(import_name: str, package_name: str) -> bool:
    imp = normalize(import_name)
    pkg = normalize(package_name)

    return (
        imp == pkg
        or imp == pkg.replace("-", "_")
        or imp.replace("_", "-") == pkg
    )


def match_packages(
    imports: dict[str, set[Path]],
    installed: dict[str, str],
) -> dict[str, dict]:
    """
    Возвращает:
    {
        "aiohttp": {
            "version": "3.13.2",
            "imports": {"aiohttp"},
            "files": {Path(...)},
        }
    }
    """

    result: dict[str, dict] = {}

    for import_name, files in imports.items():
        for pkg_name, version in installed.items():
            if not matches(import_name, pkg_name):
                continue

            entry = result.setdefault(pkg_name, {
                "version": version,
                "imports": set(),
                "files": set(),
            })

            entry["imports"].add(import_name)
            entry["files"].update(files)

    return result
