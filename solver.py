#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import Goulib.optim

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

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

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = range(0, nodeCount)

    def findminedge(lst, point):
        excludept = [lst[lst.index(point)-1], point, lst[(lst.index(point)+1)%nodeCount]]
        searchlist = [i for i in lst if i not in excludept]
        return min(searchlist, key = lambda p: length(points[p], points[point]))

    def r2opt(solution):
        for i in range(nodeCount):
            for j in range(i):
                tmp = solution
                oldlen = length(points[solution[j-1]],points[solution[j]])+length(points[solution[i]], points[solution[(i+1)%nodeCount]])
                newlen = length(points[solution[j-1]],points[solution[i]])+length(points[solution[j]], points[solution[(i+1)%nodeCount]])
                if newlen < oldlen:
                    solution[j:i+1] = [ele for ele in reversed(tmp[j:i+1])]

    def twoopt(lst, startpt):
        lst[:] = lst[lst.index(startpt):] + lst[0:lst.index(startpt)]
        startpt = lst[0]
        nextpoint = findminedge(lst, lst[1])
        if (length(points[lst[0]], points[lst[1]]) <= 
            length(points[lst[lst.index(nextpoint)]], points[lst[1]])):
            return False
        beforenearest_idx = (lst.index(nextpoint) - 1) % nodeCount
        revstarpt_idx = (lst.index(startpt) + 1) %nodeCount
        lst[revstarpt_idx:(beforenearest_idx+1)] = reversed(lst[revstarpt_idx:(beforenearest_idx+1)])
        return True

    def kopt(lst, startpt):
        obj = length(points[solution[-1]], points[solution[0]])
        for index in range(0, nodeCount-1):
            obj += length(points[solution[index]], points[solution[index+1]])
        tmpvalue = obj
        while twoopt(lst, startpt):
            obj = length(points[solution[-1]], points[solution[0]])
            for index in range(0, nodeCount-1):
                obj += length(points[solution[index]], points[solution[index+1]])
            if obj >= tmpvalue:
                break
            tmpvalue = obj
    

    #print points[0], points[1]
    #print length(points[0], points[1])
    #iters, score, best = Goulib.optim.tsp(points, length, max_iterations=100000)
    _, score1, best1 = Goulib.optim.tsp(points, length, max_iterations=3000, start_temp=10, alpha=0.9)
    _, score2, best2 = Goulib.optim.tsp(points, length, max_iterations=3000)
    #print iters, score, best
    if score1 > score2:
        solution = best1
    else:
        solution = best2

    #for i in range(500):
    #    r2opt(solution)
            
    #for i in range(nodeCount):
    #    r2opt(solution)
    #    tmp = [k for k in solution]
    #    kopt(tmp, i)
    #    obj = length(points[tmp[-1]], points[tmp[0]])
    #    for index in range(0, nodeCount-1):
    #        obj += length(points[tmp[index]], points[tmp[index+1]])
    #    firstvalue = obj
    #    if obj < firstvalue:
    #        solution = tmp
    #        firstvalue = obj

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

