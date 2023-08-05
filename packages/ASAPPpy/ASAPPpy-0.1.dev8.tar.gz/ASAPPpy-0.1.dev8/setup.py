#! /usr/bin/env python
#
# Copyright (c) 2020 José Santos
# License: MIT License
from setuptools import setup, find_packages
from setuptools.command.install import install

import ASAPPpy
# from download_models import download_from_google_drive

# class DownloadModels(install):
#     """Customized setuptools install command - Downloads STS models from Google Drive."""

#     def run(self):
#         install.run(self)
#         download_from_google_drive('1VmCflR_ULeyQx38u6kKIVgoMBAtCc4jd', 'ASAPPpy')

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='ASAPPpy',
    version=ASAPPpy.__version__,
    description='Semantic Textual Similarity and Dialogue System package for Python',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    
    packages=find_packages(),
    include_package_data=True,
    # cmdclass={
    #     'install': DownloadModels,
    # },

    author=u'José Santos',
    author_email='santos@student.dei.uc.pt',

    license='MIT License',

    keywords='Natural Language Processing, NLP,'
        'Sentence Similarity, Semantic Textual Similarity, STS,'
        'Dialogue Agents, Chatbot Framework, Chatbot',

    platforms='any',

    zip_safe=False,

    classifiers=[  # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],

    python_requires='>=3.6.1',
)