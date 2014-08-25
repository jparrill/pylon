import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pylon",
    version = "0.0.1",
    author = "Juan Manuel Parrilla Madrid",
    author_email = "padajuan@gmail.com",
    description = ("Use psutils to send data to Graphite Backend"),
    license = "GPLv2",
    keywords = "psutil pylon monitoring graphite",
    url = "http://packages.python.org/pylon",
    packages=['pylon'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: DevOps',
        'License :: OSI Approved :: GPLv2 License',
        'Operating System :: Redhat/CentOS/Fedora',
        'Programming Language :: Python',
        "Topic :: Monitoring",
    ],
)