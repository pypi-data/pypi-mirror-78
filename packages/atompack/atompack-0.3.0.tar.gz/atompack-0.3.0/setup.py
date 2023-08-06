from setuptools import setup

import numpy as np

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="atompack",
      version="0.3.0",
      description="A flexible Python library for atomic structure generation.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Seaton Ullberg",
      author_email="seatonullberg@gmail.com",
      url="https://github.com/seatonullberg/atompack",
      license="MIT License",
      packages=["atompack"],
      install_requires=["numpy", "scipy", "python-igraph"],
      extras_require={"dev": [
          "pytest",
          "pytest-benchmark",
          "pdoc3",
          "isort",
          "yapf",
          "mypy",
          "pyflakes",
      ]})
