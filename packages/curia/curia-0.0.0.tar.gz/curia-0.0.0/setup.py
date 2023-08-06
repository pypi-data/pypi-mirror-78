import os.path
from glob import glob

from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup_packages = [
    'Cython',
    'pytest-runner'
]

required_packages = [
    'importlib-metadata',
    'ipykernel',
    'numpy',
    'pandas',
    'requests',
    'dynaconf',
    'validation_decorators',
    'scikit-learn',
    'logzero',
    'docutils',
    'importlib-metadata',
    'packaging'
]

test_packages = [
    'click',
    'freezegun',
]

extras = {
    'testing': {
        'pytest-cov',
        'pytest-pylint',
        'pytest-mock',
        'flake8',
    },
    'docs': {
        'sphinx',
        'sphinx_rtd_theme',
        'sphinxcontrib-apidoc'
    }
}

name = "curia"

setup(
    name=name,
    description="A library for training and using risk & impactability models on Curia",
    packages=['curia', 'swagger_client'],
    package_dir={
        "": "src",
        # 'curia': 'src/curia',
        # 'curia.api': 'src/curia/api',
        'swagger_client': 'src/curia/api/swagger_client'
    },
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="Curia.ai",
    url="https://github.com/FoundryAI/curia-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    setup_requires=setup_packages,
    install_requires=required_packages,
    tests_require=test_packages,
    extras_require=extras,
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'source_dir': ('setup.py', 'doc'),
            'build_dir': ('setup.py', 'doc/_build')
        }
    },
)
