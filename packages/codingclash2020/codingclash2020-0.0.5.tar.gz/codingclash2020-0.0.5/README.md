# CodingClash2020
CodingClash2020


## Updating the pip package
To update the _dist/_ folder: `python3 setup.py sdist bdist_wheel` for Linux and `python setup.py sdist bdist_wheel` for Windows.
To upload to the pip server: `python3 -m twine upload dist/*` for Linux and `python -m twine upload dist/*` for Windows.

