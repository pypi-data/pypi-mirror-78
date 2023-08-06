import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

with open("../version.txt", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="case_convert",
    version=version,
    author="SECRET Olivier",
    author_email="pypi-package-case_convert@devo.live",
    description="Case converter with permissive input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/olive007/case-convert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'
)
