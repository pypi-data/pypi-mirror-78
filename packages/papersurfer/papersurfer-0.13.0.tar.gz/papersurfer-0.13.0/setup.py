import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
VERSION = (HERE / "papersurfer/_version.txt").read_text()

# This call to setup() does all the work
setup(
    name="papersurfer",
    version=VERSION,
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Johann Jacobsohn",
    author_email="johann.jacobsohn@uni-hamburg.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        'Development Status :: 1 - Planning',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "mattermostdriver",
        "urwid",
        "configargparse",
        "tinydb",
        "dataclasses",
        "xdgappdirs",
    ],
    extras_require={
        'dev': [
            "flake8",
            "pylint==2.4.4",
            "pycodestyle",
            "pydocstyle",
            "twine",
            "pytest",
            "pytest-cov",
            "pytest-datadir",
        ]
    },
    entry_points={
        "console_scripts": [
            "papersurfer=papersurfer.papersurfer:main",
        ]
    },
)
