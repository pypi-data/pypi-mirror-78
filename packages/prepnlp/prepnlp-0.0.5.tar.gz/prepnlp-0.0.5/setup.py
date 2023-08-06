import pathlib
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

HERE = pathlib.Path(__file__).parent
TESTS_REQUIRE = (HERE / "test-requirements.txt").read_text().splitlines()[1:]
setup(
    name='prepnlp',
    version='0.0.5',
    description='Lightweight utilities to train nlp tasks for deep learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Arie Pratama Sutiono',
    packages=find_packages(),
    url='https://github.com/ariepratama/prepnlp',
    tests_require=TESTS_REQUIRE,
    python_requires='>=3.5'
)
