from distutils.core import setup

setup(
    name = 'filegm',
    version = '4.1',
    description = 'File searching',
    long_description = open('README').read(),
    scripts = ['filegm.py'],
    author = 'Carlo Capobianchi',
    author_email = "degnucs@gmail.com",
    url = 'https://pypi.org/',
    platforms = 'linux',
    classifiers = [
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Documentation',
        'Topic :: Utilities'
        ],
    )
