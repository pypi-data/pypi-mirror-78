import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="py3adf",
    version="0.1.2",
    author="David Boddie, Toby McLaughlin",
    author_email="toby@jarpy.net",
    description="Python 3 port of ADF2INF from David Boddie's Acorn-Format-Tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jarpy/Acorn-Format-Tools",
    packages=setuptools.find_packages(),
    scripts=['bin/py3adf.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.7',
    install_requires=[
    ]
)
