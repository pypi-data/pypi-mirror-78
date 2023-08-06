import pathlib
import re

import setuptools


def version():
    """Extract version from __init__.py"""
    here = pathlib.Path(__file__).parent.resolve()
    with open(str(here / "tutti_product_tagger" / "__init__.py"), "r") as fd:
        for line in fd:
            if re.match("^__version__ = ", line):
                version_string = re.search(r"[0-9]+\.[0-9]+\.[0-9]+", line).group(0).strip()
                return version_string


if __name__ == "__main__":
    print(version())


def requirements():
    """Extract requirements from requirements.txt"""
    here = pathlib.Path(__file__).parent.resolve()
    with open(str(here / "requirements.txt"), "r") as fd:
        reqs = [line.strip() for line in fd if not re.match(r"^#", line)]
        return reqs


setuptools.setup(
    name="tutti_product_tagger",
    version=version(),
    description="A tutti.ch automatic product tagger.",
    long_description="Very simple logic to tag furniture products from Swiss-German text ads.",
    author="Oscar Saleta",
    author_email="oscar@tutti.ch",
    license="Proprietary",
    keywords=["product", "tagging"],
    packages=setuptools.find_packages(exclude=["contrib", "docs", "*test*", "*venv*", ".gitlab-ci.yml"]),
    python_requires=">=3.5.2",
    install_requires=requirements(),
    zip_safe=True,
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
    include_package_data=False,
)
