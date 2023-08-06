import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = sourcedir

class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.sourcedir)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        print("cmake call:\n", ['cmake', os.path.abspath(ext.sourcedir)] + cmake_args)
        subprocess.check_call(['cmake', os.path.abspath(ext.sourcedir)] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

binding_ext = CMakeExtension(name="binding",
                             sourcedir="persty/cpp/")

#===========================================================

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "persty",
    version = "2.0.1",
    author="Gabriele Beltramo",
    description = "Implementation of Minibox and Delauany edges algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("."),
    ext_modules = [binding_ext],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    url="https://github.com/gbeltramo/persty",
    license='GPLv3',
    install_requires=['numpy', 'scipy'],
    keywords='topology data analysis, minibox graph, delaunay graph'
)
