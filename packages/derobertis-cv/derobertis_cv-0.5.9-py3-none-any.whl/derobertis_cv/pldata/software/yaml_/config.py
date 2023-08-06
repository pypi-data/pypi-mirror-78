
# Modify configs
import os
import pathlib

from projectreport.config import DEFAULT_IGNORE_PATHS

DISPLAY_TITLES = {
    'project-report': 'Project Report',
    'py-mixins': 'Python Mixin Classes',
    'capiq-excel-downloader-py': 'Capital IQ Excel Downloader',
    'mendeley-python-sdk': 'Mendeley Python SDK',
    'py-edgar-api': 'Python SEC EDGAR API',
    'pl-builder': 'Py-ex-latex Builder',
    'py-excel-driver': 'Python Excel Driver',
    'py-ex-latex': 'Python Extends LaTeX',
    'py-process-files': 'Python File Processor',
    'datastream-excel-downloader-py': 'Datastream Excel Downloader',
    'data': 'Financial Data Functions',
    'modeler': 'Modeling Framework',
    'ml': 'Machine Learning Framework',
    'manager': 'Flow Manager',
    'db': 'Result Cache',
    'variables': 'Variables Framework',
    'data-code': 'Python Tools for Working with Data',
    'regtools': 'Python Regression Framework',
    'sensitivity': 'Python Sensitivity Analysis',
    'py-finstmt': 'Python Financial Statement Tools',
    'cryptocompare-py': 'Cryptoasset Data Downloader',
    'py-file-conf': 'Python Configuration Manager',
    'fin-model-course': 'Financial Modeling Course',
    'py-research-workflows': 'Python Research Workflows Website',
    'repo-splitter': 'Repository Splitter',
    'cookiecutter-pypi-sphinx': 'Python Project Template',
    'transforms-fin': 'Financial Data Transforms',
    'check-if-issue-exists-action': 'Github Actions Check Issue Existence',
    'pd-utils': 'Python Pandas Functions',
    'bibtex-gen': 'LaTeX Bibliography Generator',
    'pypi-latest-version-action': 'Github Actions Python Project Version',
    'obj-cache': 'Python Object Cache',
    'py-gh-archive': 'Python Github Archive Downloader',
    'pyfileconf-datacode': 'Integration between pyfileconf and datacode',
    'nick-derobertis-site': 'Personal Website',
    'derobertis-project-logo': 'Logo Generator',
    'py-file-conf-gui': 'GUI for pyfileconf',
    'pysentiment': 'Python Dictionary-Based Sentiment Analysis',
}

RENAME_MAP = {
    'db': 'result-cache',
    'manager': 'flow-manager'
}

REPLACE_DESCRIPTIONS = {
    'cookiecutter-pypi-sphinx': """
    A template to use for starting a new Python package
    which is hosted on PyPi and uses Sphinx for documentation
    hosted on Github pages. It has a built-in CI/CD system using Github Actions.
    """,
    'py-research-workflows': """
    A website containing examples of data munging, analysis, and presentation in Python.
    """,
    'check-if-issue-exists-action': """
    Github Action for checking whether a Github issue already exists.
    """,
    'pypi-latest-version-action': """
    Github Action for getting the latest version of a PyPI package.
    """,
    'fin-model-course': """
    Financial modeling course using Python and Excel.
    """
}

ADD_DESCRIPTIONS = {
    'py-ex-latex': ' All my papers, presentations, and even my CV are generated using py-ex-latex.',
    'project-report': ' This package helped generate this list of software projects.'
}

REPLACE_URLS = {
    'py-research-workflows': 'https://nickderobertis.github.io/py-research-workflows/'
}

REPLACE_LOGO_URLS = {
    'py-gh-archive': 'https://www.gharchive.org/assets/img/github.png',
    'pl-builder': 'https://nickderobertis.github.io/derobertis-project-logo/_images/pyexlatex.svg',
    'py-file-conf-gui': 'https://nickderobertis.github.io/derobertis-project-logo/_images/pyfileconf.svg'
}

REPLACE_LOGO_FILES = {
    'cryptocompare-py': 'cryptocompare.png',
    'datastream-excel-downloader-py': 'datastream.png',
    'py-edgar-api': 'sec-logo.png',
    'capiq-excel-downloader-py': 'sp-capital-iq.png',
    'py-excel-driver': 'excel.png',
}

REPLACE_LOGO_FA_CLASS_STRS = {
    'fin-model-course': 'fas fa-graduation-cap'
}

# Create YAML configs

PROJECT_DIRECTORIES = [
    os.path.expanduser('~/Dropbox/Python'),
    os.path.expanduser('~/Dropbox/UF')
]

IGNORE_DIRECTORIES = DEFAULT_IGNORE_PATHS + (
    'git backups',
    'scikit-learn-master',
    'Testing',
    'Dero*',
    'ftfy dev',
    'edgar-test',
    'xlwings',
    'Ticker Screenshots',
    'Django',
    'temp',
    'Temp',
    'tradingWithPython-0.0.14.0',
    'IbPy-master',
    'google-master',
    'datastream-excel-downloader-py (copy)',
    'lib',
    'MonkeyType',
    'todo-actions',
    'lexisnexis',
    'automerge-action',
    'tests',
    'examples',
    'directives',
    'mendeley-python-sdk',
    'personal-budget',
    'semopy',
)

YAML_OUT_PATH = str(pathlib.Path(__file__).parent / 'projects.yaml')
