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

    command = ["manifestoo", "-d", ".", "--exclude-core-addons", "list-external-dependencies", "python"]

    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

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
