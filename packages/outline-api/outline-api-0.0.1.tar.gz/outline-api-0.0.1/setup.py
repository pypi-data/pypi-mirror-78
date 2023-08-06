from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

with open(path.join(here, 'CHANGES.txt'), encoding='utf-8') as f:
    CHANGES = f.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    VERSION = f.read()

setup(
    name="outline-api",
    version=VERSION,
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='GPLv3',
    author="ASL19 Software Development Team",
    author_email="dev@asl19.org",
    description="A wrapper library to facilitate the access to Outline VPN as well as its Prometheus APIs on Outline VPN Servers.",
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type="text/markdown",
    # Provide either the link to your github or to your website
    url="https://github.com/ASL-19/outline-api",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Keywords that define your package best
    keywords=['Outline', 'Outline Manager', 'Outline VPN', 'Outline API'],
    install_requires=[
        'requests'],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
