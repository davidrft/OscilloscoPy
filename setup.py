try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyoscilloscope',
    version='1.0.0',
    description='High level interface for USBTMC instruments',
    long_description='''Library that implements a high level interface in python to control USBTMC oscilloscopes and wave generators''',

    url='https://github.com/davidrft/PyOscilloscope',

    author='David Riff',
    author_email='davidriff@outlook.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='usbtmc',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    #install_requires=['peppercorn'],
) 
