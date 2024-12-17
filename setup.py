# -*- coding: utf-8 -*-
# Copyright 2024, bitcreed LLC. All rights reserved.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BITCREED
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import os
from setuptools import setup, find_packages
from simple_cmd_scan import __version__, __app_name__, __author__


# Utility function to read the README.md file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    'python-decouple~=3.8',
    'pypdf~=4.3.1',
    'Pillow~=10.4.0',
    'python-sane~=2.9.1',
]

extras_require = {
    'dev': [
        'pytest~=8.3.2',
        'pytest-mock~=3.14.0',
    ],
    'deploy': [
        'PyInstaller==6.10',
        'setuptools~=72.2.0',
    ]
}

setup(
    name=__app_name__,
    version=__version__,
    author=__author__,
    author_email='info@bitcreed.us',
    license='GPL-3.0',
    keywords='',
    url='https://www.github.com/bitcreed/',
    packages=find_packages(exclude=['tests', 'tests.*']),
    long_description=read('README.rst'),
    install_requires=requirements,
    python_requires='>=3.5,<4',
    include_package_data=True,
    extras_require=extras_require,
    # test_suite='pytest',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'simple-cmd-scan=simple_cmd_scan.__main__:main',
        ],
    }
)
