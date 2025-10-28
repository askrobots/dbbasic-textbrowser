"""
Setup script for DBBasic TextBrowser
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dbbasic-textbrowser",
    version="0.1.0",
    author="DBBasic TextBrowser Contributors",
    description="A text-mode web browser with AI assistance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askrobots/dbbasic-textbrowser",
    packages=find_packages(),
    py_modules=["browser"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: Console :: Curses",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dbbasic-textbrowser=browser:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.md"],
    },
    keywords="browser text terminal curses ai lynx web accessibility",
    project_urls={
        "Bug Reports": "https://github.com/askrobots/dbbasic-textbrowser/issues",
        "Source": "https://github.com/askrobots/dbbasic-textbrowser",
    },
)
