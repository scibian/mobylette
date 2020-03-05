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

import re

log_patt1 = re.compile(r"""lmod:[ ]
                       source=ModUsageTrack,[ ]
                       time=(?P<timestamp>[0-9]+.[0-9]*),[ ]
                       host=(?P<host>[\S]+),[ ]
                       user=(?P<user>[\S]+),[ ]
                       action=(?P<action>load),[ ]
                       module=(?P<module>[\S]+),[ ]
                       path=(?P<path>[\S]+)
                       """, re.VERBOSE)

log_patt2 = re.compile(r"""source=ModUsageTrack,[ ]
                       time=(?P<timestamp>[0-9]+.[0-9]*),[ ]
                       host=(?P<host>[\S]+),[ ]
                       user=(?P<user>[\S]+),[ ]
                       action=(?P<action>load),[ ]
                       module=(?P<module>[\S]+),[ ]
                       path=(?P<path>[\S]+),[ ]
                       cat=(?P<cat>[\S]+),[ ]
                       version=(?P<version>[\S]+),[ ]
                       shell=(?P<shell>[\S]+),[ ]
                       job_id=(?P<job_id>[0-9]+),[ ]
                       job_acc=(?P<job_acc>[\S]+),[ ]
                       job_part=(?P<job_part>[\S]+)
                       """, re.VERBOSE)

def _open_file(file):
    ''' Returns correct open command.
       Checks if file is compressed and returns the
       correct open command to handle the file.
    '''
    from binascii import hexlify
    def is_gz_file(filepath):
        with open(filepath, 'rb') as test_f:
            return hexlify(test_f.read(2)) == b'1f8b'

    if is_gz_file(file):
        from gzip import open as open_gzip
        result = open_gzip(file)
    else:
        result = open(file)
    return(result)

def read_users(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct users.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if log_patt1.search(line) is not None:

                if module is not None:
                    if log_patt1.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(log_patt1.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(log_patt1.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (log_patt1.search(line).groupdict()['module'], log_patt1.search(line).groupdict()['user']) ] = True
    return {file : dic.keys()}

def read_users_cat(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct users. Results
    are grouped by category
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if log_patt2.search(line) is not None:

                if module is not None:
                    if log_patt2.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (log_patt2.search(line).groupdict()['cat'],
                     (log_patt2.search(line).groupdict()['module'], log_patt2.search(line).groupdict()['user'])) ] = True
    return {file : dic.keys()}

def read_users_path(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct users. Results
    are grouped by path.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if log_patt2.search(line) is not None:

                if module is not None:
                    if log_patt2.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) > end_date:
                        continue

                path = log_patt2.search(line).groupdict()['path']
                dic[ (path[:path.find('/',1)],
                     (log_patt2.search(line).groupdict()['module'], log_patt2.search(line).groupdict()['user'])) ] = True
    return {file : dic.keys()}

def read_jobs(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct jobs.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if log_patt2.search(line) is not None:

                if module is not None:
                    if log_patt2.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (log_patt2.search(line).groupdict()['module'], log_patt2.search(line).groupdict()['job_id']) ] = True
    return {file : dic.keys()}

def read_jobs_cat(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct jobs. Results
    are grouped by category.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if log_patt2.search(line) is not None:

                if module is not None:
                    if log_patt2.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) > end_date:
                        continue

                dic[ (log_patt2.search(line).groupdict()['cat'],
                     (log_patt2.search(line).groupdict()['module'], log_patt2.search(line).groupdict()['job_id'])) ] = True
    return {file : dic.keys()}

def read_jobs_path(params):
    ''' Reads log file.
    This function will count the number of modules
    that have been loaded by distinct jobs. Results
    are grouped by path.
    '''
    dic = {}
    file, start_date, end_date, module = params
    with _open_file(file) as fp:
        for line in fp:
            if log_patt2.search(line) is not None:

                if module is not None:
                    if log_patt2.search(line).groupdict()['module'] not in module:
                        continue
                if start_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) < start_date:
                        continue
                if end_date is not None:
                    if float(log_patt2.search(line).groupdict()['timestamp']) > end_date:
                        continue

                path = log_patt2.search(line).groupdict()['path']
                dic[ (path[:path.find('/',1)],
                     (log_patt2.search(line).groupdict()['module'], log_patt2.search(line).groupdict()['job_id'])) ] = True
    return {file : dic.keys()}

