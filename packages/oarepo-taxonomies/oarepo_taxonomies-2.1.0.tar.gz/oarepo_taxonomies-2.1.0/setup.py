# -*- coding: utf-8 -*-


"""Wrapper that connect flask-taxonomies with Invenio"""
import os

from setuptools import find_packages, setup

readme = open('README.md').read()

tests_require = [
    'pytest',
    'pytest-cov',
    'oarepo[deploy-es7]>=3.2.1.2,<3.3.0.0'
]
extras_require = {
    "tests": tests_require
}

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'flask-taxonomies>=7.0.0a16',
    'flatten_json>=0.1.7,<1.0.0',
    'openpyxl>=3.0.4,<4.0.0',
    'oarepo-mapping-includes>=1.1.0,<2.0.0',
    'oarepo-references[validate]>=1.8.3,<2.0.0'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo_taxonomies', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo_taxonomies',
    version=version,
    description=__doc__,
    # long_description=readme,
    keywords='oarepo taxonomies',
    license='MIT',
    author='Daniel Kopecký',
    author_email='Daniel.Kopecky@techlib.cz',
    url='https://github.com/oarepo/oarepo-taxonomies',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'flask.commands': [
            'taxonomies = oarepo_taxonomies.cli:taxonomies',
        ],
        'invenio_base.api_apps': [
            'taxonomies = oarepo_taxonomies.ext:OarepoTaxonomies'
        ],
        'invenio_base.apps': [
            'taxonomies = oarepo_taxonomies.ext:OarepoTaxonomies'
        ],
        'invenio_jsonschemas.schemas': [
            'oarepo_taxonomies = oarepo_taxonomies.jsonschemas'
        ],
        "oarepo_mapping_includes": [
            "oarepo_taxonomies = oarepo_taxonomies.included_mappings"
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)
