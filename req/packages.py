def match_packages(imports: set[str], installed: dict[str, str]) -> dict[str, str]:
    """
    imports   — имена модулей из кода
    installed — пакеты из venv (name -> version)
    """
    result = {}

    for imp in imports:
        for package, version in installed.items():
            if matches(imp, package):
                result[package] = version

    return result

def matches(imp: str, package: str) -> bool:
    imp_n = normalize(imp)
    pkg_n = normalize(package)

    if imp_n == pkg_n:
        return True

    if imp_n == pkg_n.replace("-", "_"):
        return True

    if imp_n.replace("_", "-") == pkg_n:
        return True

    return False

def normalize(name: str) -> str:
    return name.lower().replace("-", "_")