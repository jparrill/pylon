import os
from setuptools import setup, find_packages
import re
import sys

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]",
        init_py, re.MULTILINE).group(1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

package = 'pylon'
version = get_version(package)

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': version}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

setup(
    name = "pyl0n",
    version = version,
    author = "Juan Manuel Parrilla Madrid",
    author_email = "padajuan@gmail.com",
    description = ("Use psutils to send data to Graphite Backend"),
    license = "GPLv2",
    keywords = "psutil pylon monitoring graphite",
    url = "https://github.com/padajuan/pylon",
    include_package_data=True,
    packages=find_packages(),
    install_requires=open('requirements.txt').read().split('\n'),
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Operating System',
    ],
)