# -*- coding: utf-8 -*-

# Script to simulate Antimony model following Conway's Game of Life
# Copyright (c) 2017 Kiri Choi

import os, sys
import tellurium as te
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

workingDir = os.getcwd()

f = open('ant_str.txt','r')
ant_str = f.read()
f.close()

r = te.loada(ant_str)

results = r.simulate(0, 30, 31)

ind_1 = np.shape(results)[1]/2
#ind_2 = np.sqrt((np.shape(results)[1] - 2)/2)
ind_2 = 38
grid = []
for i in range(len(results[:,1:-ind_1])):
     grid.append(results[:,1:-ind_1][i].reshape(-1, int(ind_2)))

sb.set_style("white")


plt.figure()
cmap = matplotlib.colors.ListedColormap(['black','white'])

for i in range(np.shape(results)[0]):
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    plt.grid(linewidth=1)
    
    ax.set_xticks(np.linspace(0.5,38.5,39)) #gosper
    ax.set_yticks(np.linspace(0.5,38.5,39)) #gosper
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    im = ax.imshow(grid[i],interpolation='none')
    fig.tight_layout()
    #plt.savefig(os.path.join(workingDir, 'fig_' + str(i) + '.png'), bbox_inches='tight')
    plt.show()

r.reset()

