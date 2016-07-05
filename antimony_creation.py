import numpy as np

def readfiles(filename):
    input_f = open(filename + '.txt','r')
    input_arr = input_f.read()
    input_f.close()
    
    input_arr = input_arr.split('\n')
    
    init_ind = []
    for i in range(len(input_arr)) :
        temp = input_arr[i].split(' ')
        init_ind.append([int(temp[0]) + 19, int(temp[1]) + 5])
    return init_ind

def neighbors(x, y):
    return np.array([(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)])

def create_grid(gsize_x, gsize_y, filename):
    
    grid = np.chararray([gsize_x, gsize_y], itemsize=99)
    nbor = np.chararray([gsize_x, gsize_y], itemsize=99)
    
    for i in range(gsize_x):
        for j in range(gsize_y):
            grid[i][j] = 'p' + str(i) + '_' + str(j)
            nbor[i][j] = 'n' + str(i) + '_' + str(j)
    
    ant_str = "model smallgridb()\n  species "
    
    for i in range(gsize_x):
        for j in range(gsize_y):
            ant_str += grid[i][j] + ', '
    
    for i in range(gsize_x):
        for j in range(gsize_y):
            ant_str += nbor[i][j] + ', '
            
    ant_str = ant_str[:-2] + "\n\n  E000: at (timer > 1), priority=2: "
    
    grid_nbor = np.chararray([gsize_x, gsize_y], itemsize=99)
    
    for i in range(gsize_x):
        for j in range(gsize_y):
            ind = zip(*np.where(grid == 'p' + str(i) + '_' + str(j)))
            neighb = np.concatenate([neighbors(*l) for l in ind])
            temp = ''
            for k in range(len(neighb)):
                if (neighb[k][0] < 0 or neighb[k][1] < 0):
                    pass
                elif (neighb[k][0] >= gsize_x or neighb[k][1] >= gsize_y):
                    pass
                else:
                    temp += 'p' + str(neighb[k][0]) + '_' + str(neighb[k][1]) + ' + '
            
            grid_nbor[i][j] = temp[:-3]
            
    for i in range(gsize_x):
        for j in range(gsize_y):
            if i == 0 and j == 0:
                ant_str += nbor[i][j] + ' = ' +  grid_nbor[i][j] + ',\n'
            else:
                ant_str += '  ' + nbor[i][j] + ' = ' +  grid_nbor[i][j] + ',\n'
            
    ant_str = ant_str[:-2] + ';\n\n'
    
    for i in range(gsize_x):
        for j in range(gsize_y):
            ant_str += '  E' + str(i) + '_' + str(j) + '1: at ((timer > 1) && (p' + str(i) + '_' + str(j) + ' == 0) && (n' + str(i) + '_' + str(j) + ' == 3)), priority=1: p' + str(i) + '_' + str(j) + ' = 1;\n'
            ant_str += '  E' + str(i) + '_' + str(j) + '2: at ((timer > 1) && (p' + str(i) + '_' + str(j) + ' == 1) && (n' + str(i) + '_' + str(j) + ' < 2 || n' + str(i) + '_' + str(j) + ' > 3)), priority=1: p'+ str(i) + '_' + str(j) + ' = 0;\n'
    
    ant_str += "\n  timer = 0;\n  timer' = 1;\n  at(timer > 1), priority=0: timer = 0;\n\n"

    init_ind = readfiles(filename)
    
    temp_str_p = ''
    for i in range(gsize_x):
        temp = ''
        for j in range(gsize_y):
            if [j, i] in init_ind:
                temp += 'p' + str(i) + '_' + str(j) + ' = 1; '
            else:
                temp += 'p' + str(i) + '_' + str(j) + ' = 0; '
        
        temp_str_p += '  ' + temp + '\n'

    ant_str = ant_str + temp_str_p
    ant_str += '\n'
    
    temp_str_n = ''
    for i in range(gsize_x):
        temp = ''
        for j in range(gsize_y):
            count = 0
            if [j, i] in init_ind:
                for m in range(len(grid_nbor[i][j].split(' + '))):
                    if grid_nbor[i][j].split(' + ')[m] + ' = 1' in temp_str_p:
                        count += 1
                temp += 'n' + str(i) + '_' + str(j) + ' = ' + str(count) + '; '
            else:
                temp += 'n' + str(i) + '_' + str(j) + ' = 0; '
        
        temp_str_n += '  ' + temp + '\n'
        
    ant_str = ant_str + temp_str_n
    ant_str += "end"
    
    f = open("ant_str.txt", "w")
    f.write(ant_str)
    f.close()
