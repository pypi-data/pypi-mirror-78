""" Setup for NFSyndication
 See: https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

from os.path import dirname, abspath, join, exists
from setuptools import setup, find_packages
from NFSyndication import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()
 
install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name = "NFSyndication",
    version = __version__,
    packages=find_packages(exclude=['test', 'test.*', 'testcase.py']),
    entry_points = {
        'console_scripts': [ 
            'nfsyndication-src = NFSyndication:main',
         ]
        },
    package_data = {'NFSyndication': ['templates/*.html']},
    description= "News Feed Syndication - A package that read and fetch RSS feeds from the publications.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author = "Web SRC",
    author_email = "web.system.management@gmail.com",
    install_requires=install_reqs,
    license = "GNU GPL",
    keywords = "rss, news",
    project_urls={ 
        'Source': 'https://github.com/web-sys1/NFSyndication/'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
        ]
 )
