from setuptools import setup
from setuptools.extension import Extension
import numpy
import sys
import os.path
from pycx4.aux import cx_installpath
from pycx4.version import __version__

cxdir = cx_installpath()
if cxdir is None:
    print('Error: Unable to locate CX')
    sys.exit(1)
else:
    print('Using cx installed in:', cxdir)

cx_include = cxdir + '/include'
cx_lib = cxdir + '/lib'

USE_CYTHON = False
ext = '.c'
if os.path.isfile('./pycx4/pycda.pyx'):
    USE_CYTHON = True
    ext = '.pyx'

extensions = [
    Extension('pycx4.pycda', ['./pycx4/pycda' + ext],
              include_dirs=[numpy.get_include(), cx_include],
              libraries=['cda', 'cx_async', 'useful', 'misc', 'cxscheduler'],
              library_dirs=[cx_lib]
              )]

try:
    import PyQt4

    extensions.append(Extension('pycx4.q4cda', ['./pycx4/q4cda' + ext],
          include_dirs=[numpy.get_include(), cx_include, '/usr/include/x86_64-linux-gnu/qt4/QtCore',],
          libraries=['cda', 'cx_async', 'useful', 'misc', 'Qt4cxscheduler', 'QtCore'],
          library_dirs=[cx_lib]
         ))
except ImportError:
    pass

try:
    import PyQt5

    extensions.append(Extension('pycx4.q5cda', ['./pycx4/q5cda' + ext],
              include_dirs=[numpy.get_include(), cx_include, '/usr/include/x86_64-linux-gnu/qt5/QtCore', ],
              libraries=['cda', 'cx_async', 'useful', 'misc', 'Qt5cxscheduler', 'Qt5Core'],
              library_dirs=[cx_lib]
              ))
except ImportError:
    pass


# Cython directives
directives = {
    'language_level': 3,
    'profile':   False,
    'linetrace': False,
    'c_string_type': 'bytes',
    'c_string_encoding': 'ascii',
    'boundscheck': False,
    'wraparound': False,
    'cdivision': True,
    'always_allow_keywords': False,
    'initializedcheck': False
}

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions, compiler_directives=directives)

setup(
    name='pycx4',
    version=__version__,
    url='https://github.com/femanov/pycx4/wiki',
    download_url='https://github.com/femanov/pycx4',
    author='Fedor Emanov',
    author_email='femanov@gmail.com',
    license='GPL',
    description='CXv4 control system framework Python bindings',
    long_description='CXv4 control system framework Python bindings, pycda and qcda modules',
    install_requires=["numpy >= 1.7", ],
    packages=['pycx4'],
    platforms='Linux',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Cython",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],

    ext_modules=extensions
)

