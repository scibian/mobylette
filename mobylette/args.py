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
''' Implements ParseArgs class'''

import argparse                                     # ArgumentParser, RawTextHelpFormatter, SUPPRESS
from datetime import datetime as dt                 # fromtimestamp, now, strptime

class ParseArgs(object):
    ''' Reads arguments from command line

    The full path of a module is:

        mod path                 mod name
            |                       |
      /some_path/some_category/some_module/some_version
                     |                          |
                mod category               mod version

     mod version - this is the file, version of the module
     mod name - the directory where the `mod name` file exists. It is the name of the module
     mod category - is the directory where `mod name` directory exists (it could also be named library)
     mod path - is a path (more than one directory)
    '''

    parser = argparse.ArgumentParser(
                        formatter_class=argparse.RawTextHelpFormatter,
                        description="Parses system logs for Lmod `module load` entries and writes a csv report\n" +
                                    "with the result found as well as a beautiful SVG graph to tell the story!")

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # *                                                             *
    # * COUNT                                                       *
    # *                                                             *
    # *                                                             *
    # *                                                             *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    parser.add_argument('--version', action='version', version='mobylette 2.5')

    # What to count: users or modules
    parser.add_argument('-uniq', action='store', choices=['users', 'jobs'], dest='uniq', default=['jobs'],
                        help="" +
                             "Whether unique users or jobs are to be considered\n" +
                             "The default is to count modules found in distinct\n" +
                             "jobs. The -users option will create a list having\n" +
                             "the usernames of the users who loaded the module.")

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # *                                                             *
    # * GROUP BY                                                    *
    # *                                                             *
    # *                                                             *
    # *                                                             *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # How counts will be gruoped by
    parser.add_argument('-group', action='store', choices=['cat', 'path'], dest='group',
                        help="" +
                             "Data may be grouped by the modules category or by\n" +
                             "the first directory of it's path. No option given\n" +
                             "no grouping is done.") 

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # *                                                             *
    # * FILTER                                                      *
    # *                                                             *
    # *                                                             *
    # *                                                             *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # Start date
    parser.add_argument('-start', action='store', metavar="<yyyymmdd>", dest="start_date",
                        help="" +
                             "Modules have been loaded before this date will be\n" +
                             "be ignored. If no argument is passed then all the\n" +
                             "modules will be read.")

    # End date
    parser.add_argument('-end', action='store', metavar="<yyyymmdd>", dest="end_date",
                        help="" +
                             "If a module was loaded after this date it will be\n" +
                             "ignored. The default behaviour is to read modules\n" +
                             "of all dates.")

    # Module list
    parser.add_argument('-module', action='store', nargs='+', metavar="<module>", dest="module",
                        help="" +
                             "Modules can go here. mobylette can receive a list\n" +
                             "of modules and will exclude all other modules not\n" +
                             "in this list. The default behaviour will consider\n" +
                             "all modules. White space separated list. Both the\n" +
                             "name and version of the module should be present.\n")


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # *                                                             *
    # * Hidden options                                              *
    # *                                                             *
    # *                                                             *
    # *                                                             *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # Verbose
    parser.add_argument('-verbose', action='store_true', dest="verbose",
                        help=argparse.SUPPRESS)

    # Number of cpus to use while parsing the files
    parser.add_argument('-cpus', action='store', dest="cpus", type=int,
                        help=argparse.SUPPRESS)

    # Color fo the bars in the chart
    parser.add_argument('-chart-color', action='store', dest="chart_color",
                        help=argparse.SUPPRESS)

    # This is actually a trick to force namespace to create a parameter called 'pattern'
    # Later this parameter will be replaced
    parser.add_argument('-pattern', action='store', dest="pattern",
                        help=argparse.SUPPRESS)

    # The following two parameters control how to distribute the data over the charts
    # so that the chart does not become over crowded (and impossible to read).
    chart_size = parser.add_mutually_exclusive_group()
    chart_size.add_argument('-max-charts', action='store', dest="max_charts", type=int,
                        help=argparse.SUPPRESS)
    chart_size.add_argument('-max-rows', action='store', dest="max_rows", default=13, type=int,
                        help=argparse.SUPPRESS)

    args = parser.parse_args()

    def __init__(self):
        if 'figsize' not in self.args:
            self.args.figsize = None
        if 'dpi' not in self.args:
            self.args.dpi = None
        if 'cpus' not in self.args:
            self.args.cpus = None

        if self.args.start_date is not None:
            self.args.start_date = self.str2timestamp(self.args.start_date)
        if self.args.end_date is not None:
            self.args.end_date = self.str2timestamp(self.args.end_date)

        if 'pattern' not in self.args:
            self.args.pattern = None

        if 'max_rows' not in self.args:
            self.args.max_rows = None
        if 'max_charts' not in self.args:
            self.args.max_charts = None
            
    def str2date(self, date):
        '''
           input: yyyymmdd             output: datetime object
                  yyyymmddhhmmss
                  yyyymmddThhmmss
        '''
        if len(date) == 8:
            result = dt.strptime(date + '000000','%Y%m%d%H%M%S')
        elif len(date) == 14:
            result = dt.strptime(date, '%Y%m%d%H%M%S')
        elif len(date) == 15:
            result = dt.strptime(date, '%Y%m%dT%H%M%S')
        return(result)

    def str2timestamp(self, str_date):
        '''
        args:
          string: yyyymmdd             
                  yyyymmddhhmmss
                  yyyymmddThhmmss
        return:
          integer
        '''
        from time import mktime
        return(int(mktime(self.str2date(str_date).timetuple())))

    def date2timestamp(self, dt_obj):
        '''
        args:
          datetime.datetime

        return:
          integer
        '''
        from time import mktime
        return(int(mktime(dt_obj.timetuple())))
