from itertools import islice

from setuptools import setup

with open("requirements.txt", mode="r", encoding="utf-8") as f:
    install_reqs = [
        s for s in [line.split("#", 1)[0].strip(" \t\n") for line in islice(f, 2, None)] if s != ""
    ]

setup(install_requires=install_reqs)
