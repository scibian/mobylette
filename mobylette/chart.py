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
''' Implements Chart class '''

from matplotlib import use
use('Svg')
import matplotlib.pyplot as plt
plt.rcdefaults()
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator

class Chart(object):

    def __init__(self, x, y, options, x_label, title, chart_color = None):
        self.options = options
        self.x_label = x_label
        self.title = title
        self.x = x
        self.y = y
        if chart_color is None:
            self.chart_color = '#2792ea'
        else:
            self.chart_color = '#' + chart_color
        self.setup_chart()

    def setup_chart(self):
        ''' Creates several DataFrames '''
        #import pdb ; pdb.set_trace()
        if self.options['chart']['max_charts'] is not None:
            setup = self._distribute_charts(len(self.x), self.options['chart']['max_charts'])
        else:
            setup = self._distribute_rows(len(self.x), self.options['chart']['max_rows'])
        boxes = self._seq_to_list(setup)
        for count, interval in enumerate(boxes):
            self.do_simple(self.x[interval[0]:interval[1] + 1], self.y[interval[0]:interval[1] + 1], count)

    def _seq_to_list(self, seq):
        ''' Returns list of tupples representing the intervals
        of 3 sets `len(seq)`, each one having the corresponding
        number of elements.

        Example:

        Given    :   [3,3,2],
        returns  :   [(0, 2), (3, 5), (6, 7)]
        '''
        result = []
        for count, item in enumerate(seq):
            floor = 0 if count == 0 else result[count - 1][1] + 1
            ceiling = floor + item - 1
            result.append((floor, ceiling))
        return(result)

    def _distribute_charts(self, balls, box_num):
        ''' Distributes balls over boxes.

        Returns : list with the number of balls per box,
                  such that the difference of number of
                  balls in two different boxes cannot be
                  greater than 1. That is, the distribution
                  of balls over boxes is equillibrated.

        Example : balls = 31, box_dim = 7
                  31 / 7 = 4
                  31 % 7 = 3
                  4 boxes will have 4 balls and 3 will have 5 balls.
                  4*4 + 3*5 = 16 + 15 = 31
        '''
        base = balls / box_num
        if base == 0:
            base = 1
        extra_ball_boxes = balls % box_num
        result = [base] * box_num
        while extra_ball_boxes > 0:
            result[extra_ball_boxes - 1] += 1
            extra_ball_boxes -= 1
        return(result)

    def _distribute_rows(self, balls, box_dim):
        ''' Distributes balls over boxes.

        Returns : list with the number of balls for each box,
                  knowing that each box can have no more than
                  box_dim + 1 balls.

        Example : balls = 31, box_dim = 7
                  31 / 7 = 4
                  31 % 7 = 3
                  4 boxes will have 4 balls and 3 will have 5 balls.
                  4*4 + 3*5 = 16 + 15 = 31
        '''

        box_num = balls / box_dim
        if box_num == 0:
            box_num = 1
        extra_balls = balls % box_dim
        result = [box_dim] * box_num
        for i in range(extra_balls):
            result[i%len(range(box_num))] += 1
        return(result)
        
    def do_simple(self, x, y, count):
        ''' Creates horizontal bar chart with ordered
        labels and stores the image in a SVG file whose
        name is defined by the first and last labels of
        the elements being represented. Count will also
        enter in the composition of the file name.
        '''
        L = sorted(zip(x,y), reverse=True)
        x = [i[0] for i in L]
        y = [i[1] for i in L]

        fig, ax = plt.subplots()
        plt.xlabel(self.x_label)
        ax.set_title(self.title)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.tick_params(top=False, bottom=True, left=False, right=False, labelleft=True, labelbottom=True)
        ax.barh(range(len(x)), y, facecolor=self.chart_color, align='center', edgecolor='white')
        plt.yticks(range(len(x)), x)
        ax.margins(x=0, y=0.05)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.locator_params(axis='x', nbins=5)
        file_name = str(count) + '_' + x[-1] + '_' + x[0] + '.svg'
        plt.savefig(file_name.replace('/', ''), bbox_inches='tight')
