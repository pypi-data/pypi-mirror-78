# coding: utf-8
import os
import sys

from setuptools import setup


__author__ = 'PyLab <yeongbin.jo@pylab.co>'


with open('README.md') as readme_file:
    long_description = readme_file.read()


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
elif sys.argv[-1] == 'clean':
    import shutil
    if os.path.isdir('build'):
        shutil.rmtree('build')
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('pylab_crawler_sdk.egg-info'):
        shutil.rmtree('pylab_crawler_sdk.egg-info')


setup(
    name="pylab-crawler-sdk",
    version="1.0.1",
    author="PyLab",
    author_email="yeongbin.jo@pylab.co",
    description="SDK for https://crawler.pylab.co",
    license="MIT",
    keywords="sdk",
    url="https://github.com/PyLabCo/pylab-crawler-sdk",
    packages=['pylab_crawler_sdk'],
    entry_points={},
    long_description_content_type='text/markdown',
    long_description=long_description,
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Installation/Setup',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'requests',
    ],
)
