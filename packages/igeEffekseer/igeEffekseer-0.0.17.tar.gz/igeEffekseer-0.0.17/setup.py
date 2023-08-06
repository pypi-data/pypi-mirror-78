import importlib
try:
    importlib.import_module('numpy')
except ImportError:
	from pip._internal import main as _main
	_main(['install', 'numpy'])

from setuptools import setup, Extension, find_packages
import setuptools
import numpy
import sys
import os
from distutils.sysconfig import get_python_lib
import shutil

# To use a consistent encoding
from codecs import open

from os import path
here = path.abspath(path.dirname(__file__))

# Looks for igeLibs in current project libs
igeLibsPath = 'igeLibs'

# Looks for global environment variable
if not path.exists(igeLibsPath):
    igeLibsPath = os.environ.get('IGE_LIBS')

# If not exist, then error
if not path.exists(igeLibsPath):
    print("ERROR: IGE_LIBS was not set!")
    exit(0)

json_inc_dir = path.join(igeLibsPath, 'json/include/json')
effekseer_lib =  path.join(igeLibsPath, 'igeEffekseer/libs/pc')
effekseer_include = path.join(igeLibsPath, 'igeEffekseer/include')
pyxcore_include = path.join(igeLibsPath, 'pyxCore/include')
igeVMath_include = path.join(igeLibsPath, 'igeVMath/include')

is64Bit = sys.maxsize > 2 ** 32
if is64Bit:
    effekseer_lib = effekseer_lib + '/x64'
else:
    effekseer_lib = effekseer_lib + '/x86'

sfc_module = Extension('igeEffekseer',
                    sources=[
                        'igeEffekseer.cpp',
                        'pyxieEffekseer.cpp',
                    ],
                    include_dirs=[json_inc_dir,
                                    './',
                                    path.join(effekseer_include, "ThirdParty/Effekseer/Dev/Cpp"),
                                    path.join(effekseer_include, "ThirdParty/Effekseer/Dev/Cpp/Effekseer"),
                                    path.join(effekseer_include, "ThirdParty/Effekseer/Dev/Cpp/EffekseerRendererCommon"),
                                    path.join(pyxcore_include, "ThirdParty/GLEW"),
                                    igeVMath_include,
                                    './win32'],
                    library_dirs=[effekseer_lib],
                    libraries=['Effekseer', 'EffekseerRendererGL', 'MSVCRT'])

setup(name='igeEffekseer', version='0.0.17',
        description= 'C++ extension Effekseer for 3D and 2D games.',
        author=u'Indigames',
        author_email='dev@indigames.net',
        packages=find_packages(),
        ext_modules=[sfc_module],
        long_description=open(path.join(here, 'README.md')).read(),
        long_description_content_type='text/markdown',

        # The project's main homepage.
        url='https://indigames.net/',

        license='MIT',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            #'Operating System :: MacOS :: MacOS X',
            #'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Topic :: Games/Entertainment',
        ],
        # What does your project relate to?
        keywords='Effekseer 3D game Indigames',
      )
