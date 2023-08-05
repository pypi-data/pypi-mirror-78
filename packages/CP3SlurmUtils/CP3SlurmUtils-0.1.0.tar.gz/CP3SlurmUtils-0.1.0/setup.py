""" Setuptools-based setup module for CP3SlurmUtils """

from setuptools import setup, find_packages
import os, os.path

from io import open
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

from CP3SlurmUtils import __version__ as version

pkgName = "CP3SlurmUtils"

setup(
    name=pkgName,
    version=version,

    description="Utilities package to submit jobs to SLURM using as input a python sbatch configuration file.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    url="https://gitlab.cern.ch/cp3-cms/CP3SlurmUtils",

    author="Andres Tanasijczuk (Université catholique de Louvain)",
    author_email="cp3-support@listes.uclouvain.be",
    license="GPL-3.0-or-later",

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='slurm',

    package_dir={'' : os.path.join('src', 'python')},
    packages=find_packages(os.path.join('src', 'python')),
    scripts=[os.path.join(root, item) for root, subFolder, files in os.walk('bin') for item in files],
    package_data={pkgName: ['examples/*']},
    data_files=[(os.path.join('etc', pkgName), [os.path.join('etc', 'defaults.cfg.example')])],
)
