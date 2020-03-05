# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#  This file is part of the mobylette parsing tool.                          #
#        Copyright (C) 2019 EDF SA                                           #
#                                                                            #
#  mobylette is free software: you can redistribute it and/or modify         #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  mobylette is distributed in the hope that it will be useful,              #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with mobyllette. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                            #
##############################################################################
''' Implements Config class'''

import os
import sys
import pwd
import subprocess
if sys.version_info.major == 2:
    import ConfigParser as configparser
else:
    import configparser as configparser

class Config(object):
    '''
    Reads configuration from mobylette.conf which can be found in:

      /etc/mobylette.conf
      ~/.mobylette/mobylette.conf

    More search paths can be added to conf_path. The first path where
    mobylette.conf is found will be returned.
    '''
    
    conf_path = [u'' + pwd.getpwuid(os.getuid()).pw_dir + '/.mobylette/mobylette.conf',
                 u'' + '/etc/mobylette.conf']
    config = configparser.ConfigParser()

    def __init__(self, verbose):
        self.verbose = verbose
        self.log_path = None
        self.cluster_name = None
        self.cluster_prefix = None
        self.search_pattern = None
        self.nodes_tuple = None
        self.hostname = self._read_hostname()
        self.read_configuration()

    def _read_hostname(self):
        ''' Read hostname from command line.
        hostname read from command line Will be used to match against cluster name found in mobylette.conf
        '''
        process_result = subprocess.Popen('hostname', stdout=subprocess.PIPE, shell=True)
        (output, err) = process_result.communicate() 
        result_status = process_result.wait()
        if result_status != 0:
            print('Could not read cluster name : {}'.format(err.rstrip().decode('utf8')))
        hostname = output.rstrip().decode('utf8')
        if self.verbose:
            print('hostname: {}'.format(hostname))
        return hostname

    def _config_in_location(self, location):
        ''' Returns True if configparser is able to read a file in given location '''
        f = self.config.read(location)
        result = False
        if len(f) > 0:
            result = True
            if self.verbose:
                print('found configuration file at: {}'.format(location))
        return result

    def _config_file(self):
        ''' Returns a handle to the config file '''
        j = 0
        while not self._config_in_location(self.conf_path[j]):
            j = j + 1
        return self.config.read(self.conf_path[j])

    def read_configuration(self):
        ''' Reads config file '''
        f = self._config_file()
        if len(f) > 0:
            if self.config.has_option('CLUSTER', 'name'):
                self.cluster_name = self.config.get('CLUSTER', 'name')
            if self.config.has_option('CLUSTER', 'prefix'):
                self.cluster_prefix = self.config.get('CLUSTER', 'prefix')
            if self.config.has_option('CLUSTER', 'log_path'):
                self.log_path = self.config.get('CLUSTER', 'log_path')
            if self.config.has_option('CLUSTER', 'patterns'):
                self.search_pattern = self.config.get('CLUSTER', 'patterns')
            if self.config.has_option('CLUSTER', 'nodes'):
                # self.nodes_tuple = tuple([ self.hostname[0:2] + element for element in self.config.get('CLUSTER', 'nodes').split(',')])
                self.nodes_tuple = tuple([ self.cluster_prefix + element for element in self.config.get('CLUSTER', 'nodes').split(',')])
