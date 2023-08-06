import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codingclash2020",
    version="0.0.5",
    author="Srikar Gouru",
    author_email="srikarg89@gmail.com",
    description="Pip package for CodingClash2020",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodingClash2020/codingclash2020",
#    packages=setuptools.find_packages('engine'),
    packages=setuptools.find_packages(),
    install_requires = [], # List all your dependencies inside the list
    license = 'MIT'
)