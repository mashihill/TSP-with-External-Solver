#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from subprocess import call

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2): return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def maketable(points):
    table = [ [] for _ in range(len(points))]
    for item in range(len(points)):
        for item2 in range(len(points)):
            table[item].append(length(points[item], points[item2]))
    return table


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # Write par, tsp file
    f_par = open('LKH.par', 'w')
    f_par.write('PROBLEM_FILE = LKH.tsp\n')
    f_par.write('OUTPUT_TOUR_FILE = LKH.out\n')
    f_par.write('RUNS = 1\n')
    f_par.write('MOVE_TYPE = 2\n')
    f_par.write('MAX_CANDIDATES = 2 SYMMETRIC\n')
    f_par.write('INITIAL_PERIOD = 600\n')
    f_par.write('MAX_SWAPS = 30\n')
    f_par.write('MAX_TRIALS = 30\n')
    f_par.write('INITIAL_TOUR_ALGORITHM = GREEDY\n')
    f_par.write('MAX_BREADTH = 5\n')
    #f_par.write('PATCHING_C = 2\n')
    #f_par.write('PATCHING_A = 1\n')
    f_par.close()

    f_tsp = open('LKH.tsp', 'w')
    f_tsp.write('NAME : LKH\n')
    f_tsp.write('COMMENT : none\n')
    f_tsp.write('TYPE : TSP\n')
    f_tsp.write('DIMENSION : ' + str(len(points)) + '\n')
    f_tsp.write('EDGE_WEIGHT_TYPE : EUC_2D\n')
    f_tsp.write('NODE_COORD_SECTION\n')
    for i in range(len(points)):
        f_tsp.write(str(i+1) +' '+ str(points[i][0]) + ' '+str(points[i][1]) + '\n')
    f_tsp.write('EOF')
    f_tsp.close()

    solution = range(0, nodeCount)
    # LKHlib
    #call('./LKH-2.0.7/LKH ./LKH.par &> /dev/null', shell = True)
    call('./LKH-2.0.7/LKH ./LKH.par ', shell = True)


    outfile = open('./LKH.out', 'r')
    outdata = ''.join(outfile.readlines())
    outfile.close()

    outlines = outdata.split('\n')
    tmp = []
    for i in range(6, 6+len(points)):
        tmp.append(int(outlines[i]))
        
    # print 'tmp: ', tmp
    solution = [ i-1 for i in tmp]

    # build a trivial solution
    # visit the nodes in the order they appear in the file

    

     # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

