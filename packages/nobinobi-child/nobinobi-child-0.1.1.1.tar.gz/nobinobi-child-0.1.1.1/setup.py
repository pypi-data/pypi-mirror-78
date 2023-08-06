#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from nobinobi_child/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("nobinobi_child", "__init__.py")

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist')
    os.system('python setup.py bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='nobinobi-child',
    version=version,
    description="""Application Child for Nobinobi""",
    long_description=readme + '\n\n' + history,
    author='Florian Alu',
    author_email='alu@prolibre.com',
    url='https://github.com/prolibre-ch/nobinobi-child',
    packages=[
        'nobinobi_child',
    ],
    include_package_data=True,
    install_requires=[
        "djangorestframework==3.11.1", "django==3.1.1", "django-model-utils==4.0.0", "django-phonenumber-field==5.0.0",
        "phonenumbers==8.12.9", "Pillow==7.2.0", "django-crispy-forms==1.9.2", "urllib3==1.25.10",
        "django-select2==7.4.2", "django-bootstrap-modal-forms==2.0.0", "django-widget-tweaks==1.4.8",
        "django-bootstrap-datepicker-plus==3.0.5", "django-simple-menu==1.2.1", "django-extensions==3.0.8",
        "djangorestframework-datatables==0.5.2", "django_weasyprint==1.0.1", "nobinobi-staff==0.1.3.1", "nobinobi-core==0.1.0"
    ],
    zip_safe=False,
    keywords='nobinobi-child',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
