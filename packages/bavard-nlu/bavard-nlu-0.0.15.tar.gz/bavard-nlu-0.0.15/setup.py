import os
import sys
import setuptools
from setuptools.command.install import install

# The version of this package
VERSION = "0.0.15"


class VerifyVersionCommand(install):
    """
    Custom command to verify that the git tag matches the package version.
    Source: https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
    """

    description = 'verify that the git tag matches the package version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = f"Git tag: {tag} does not match the version of this package: {VERSION}"
            sys.exit(info)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bavard-nlu",
    version=VERSION,
    author="Bavard AI, LLC",
    author_email="dev@bavard.ai",
    description="A library and CLI for NLP tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bavard-ai/bavard-nlu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['bavard-nlu=bavard_nlu.cli.main:main'],
    },
    install_requires=[
        'tensorflow>=2.2',
        'tf-models-official',
        'tensorflow-hub>=0.7.0',
        'sentencepiece==0.1.85',
        'google-api-python-client>=1.8.0',
        'nltk>=3.5',
        'scikit-learn>=0.23.1',
    ],
    cmdclass={
        "verify": VerifyVersionCommand
    }
)
