import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGELOG.md')) as f:
    CHANGES = f.read()

dev_requires = [
    'pytest',
    'pytest-cov',
]


setup(
    author='tickstep',
    author_email='tickstep@outlook.com',
    name='pycloud189',
    version='0.0.3',
    keywords='cloud189',
    description='Cloud189 cloud disk utility for Python3+',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    url='https://github.com/tickstep/python-cloudpan189-api',
    packages=find_packages(),
    zip_safe=False,
    extras_require={
      'dev': dev_requires,
    },
)
