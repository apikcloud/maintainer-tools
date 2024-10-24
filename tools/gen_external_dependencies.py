#!/usr/bin/env python3
"""Generate requirements.txt with external dependencies of Odoo addons."""

import os
import subprocess
import sys
from pathlib import Path

import click

@click.command(help=__doc__)
@click.option("--empty-requirement",default="No", help="Can have a empty file requiement.txt")
def main(empty_requirement) -> int:
    if sys.version_info < (3, 7):
        raise SystemExit("Python 3.7+ is required.")

    projects = [
        *Path.glob(Path.cwd(), "*/pyproject.toml"),
        *Path.glob(Path.cwd(), "setup/*/setup.py"),
    ]

    # if not projects:
    #     return 1

    env = os.environ.copy()
    env.update(
        {
            # for better performance, since we are not interested in precise versions
            "WHOOL_POST_VERSION_STRATEGY_OVERRIDE": "none",
            "SETUPTOOLS_ODOO_POST_VERSION_STRATEGY_OVERRIDE": "none",
        }
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyproject_dependencies",
            "--no-isolation",  # whool and setuptools Odoo must be preinstalled
            "--ignore-build-errors",  # ignore uninstallable addons
            "--name-filter",
            r"^(odoo$|odoo\d*-addon-)",  # filter out odoo and odoo addons
            *projects,
        ],
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        text=True,
    )

    with open("test.md","w") as f:
        f.write("# Test of hook\n")
        f.write(f'{Path("requirements.txt")} -- {Path("requirements.txt").exists()} -- {empty_requirement}\n')
        f.write(f"projects: {projects}\n")    
        f.write(f"result: {result.stdout}\n")    

    if result.returncode != 0:
        return result.returncode

    requirements = result.stdout

    requirements_path = Path("requirements.txt")
    if requirements:
        with requirements_path.open("w") as f:
            f.write("# generated from manifests external_dependencies\n")
            f.write(requirements)

    if requirements_path.exists() and empty_requirement == "No":
        requirements_path.unlink()

    return 0


if __name__ == "__main__":
    sys.exit(main())
