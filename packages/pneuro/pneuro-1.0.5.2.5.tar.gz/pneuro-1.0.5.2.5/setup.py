import pathlib
from setuptools import setup, find_packages

# This call to setup() does all the work

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


PACKAGE_NAME = 'pneuro'

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name=PACKAGE_NAME,
    author="iNeuron",
    author_email="",
    maintainer="iNeuron",
    maintainer_email="support@iNeuron.com",
    description="Python API for Automated ML",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://autoneuro.ml",
    project_urls={
        "Documentation": "https://github.com/nabeelfahmi12/AutoNeuro-Documentation",
        "Source Code": "https://github.com/viratsagar/Autoneuro",
    },
    version="1.0.5.2.5",
    # Make sure to remove stale files such as the egg-info before updating this:
    # https://stackoverflow.com/a/26547314
    package_data={"": ["*.txt", "*.md"]},
    python_requires=">=3.6",
    extras_require={
        "test": [
            "matplotlib",
            "pytest",
            "pytest-xdist",
        ],
        "examples": [
            "matplotlib",
            "jupyter",
            "notebook",
            "ipykernel",
            "seaborn",
        ],
        "examples_unix": ["fanova",],
    },
    #version="1.2.5", #Most Stable Version
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['pneuro = pneuro.__main__:main']},
    classifiers=[
        "Intended Audience :: Developers ",
        'Intended Audience :: End Users/Desktop',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development ",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",

    ],
    install_requires=requirements
)