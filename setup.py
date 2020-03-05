##############################################################################
#  This file is part of the UncleBench benchmarking tool.                    #
#        Copyright (C) 2019 EDF SA                                           #
#                                                                            #
#  UncleBench is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  UncleBench is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with UncleBench.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                            #
##############################################################################

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='mobylette',
      version='2.5',
      description="mobylette is a python script for counting the number of modules loaded via Lmod",
      url='https://github.com/edf-hpc/mobylette',
      author='EDF CCN HPC',
      author_email='dsp-cspito-ccn-hpc@edf.fr',
      scripts=['bin/mobylette'],
      packages=['mobylette'],
      license='GPLv3',
      zip_safe=False)
