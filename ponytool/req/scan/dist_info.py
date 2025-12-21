from pathlib import Path

from ponytool.req.scan import metadata


def collect_dist_info(site_packages: Path) -> dict[str, str]:
    packages: dict[str, str] = {}  # Защита от некорректного вывода

    for item in site_packages.iterdir():
        if not item.is_dir() or not item.name.endswith(".dist-info"):
            continue

        info = metadata.read_metadata(item)
        if not info:
            continue

        packages[info["name"]] = info["version"]

    return packages