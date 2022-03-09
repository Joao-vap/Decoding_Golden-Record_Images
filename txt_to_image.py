#relevant imports
import numpy as np
import matplotlib.pyplot as plt
from sympy import Matrix

# global variables
RANGE_FIRST_PEAK = 800 # range of the first peak
RANGE_SEARCH_VALLEY = 50 # range of the first valley
MATRIX_COLS = 1100 # size of the matrix
MATRIX_ROWS = 690*MATRIX_COLS # size of the matrix
SIZE_OF_SEARCH = 1000 # size of the search region
MARGIN = 100 # margin to wich we start to search for the first peak

# loop over both folders where we keep the txt files with the arrays
for folder in ('left', 'right'):
    i = 0
    flag = True
    while flag:
        matrix = np.array([]) # matrix to wich we append the values

        try : # try to read the txt file
            with open(f'text/{folder}/text_{i}.txt', 'r') as f:
                text = f.readlines()
        except : # if the file does not exist, we stop the loop
            flag = False
            continue

        for j in range(len(text)): 
            text[j] = int(text[j][:-1]) # remove the \n at the end of the line

        peak = np.argmax(text[0:RANGE_FIRST_PEAK]) # find the first peak
        valley = np.argmin(text[peak:peak+RANGE_SEARCH_VALLEY]) + peak # find the first valley

        image_left = True # define if there are still size to keep searching
        while image_left:
            # check if there is image left
            if valley + SIZE_OF_SEARCH > len(text):
                image_left = False
            else:
                #   check next SIZE_OF_SEARCH points for a peak and valley
                next_peak = np.argmax(text[peak+MARGIN:peak+SIZE_OF_SEARCH]) + peak + MARGIN
                next_valley = np.argmin(text[next_peak:next_peak+RANGE_SEARCH_VALLEY]) + next_peak
                # add section to matrix line with MATRIX_SIZE points
                matrix = np.append(matrix, text[valley:next_valley]+[0]*(MATRIX_COLS-(next_valley-valley)))
                # update peak
                peak = next_peak
                # update valley
                valley = next_valley
        
        #create margin in last lines to keep ratio
        matrix = np.append(matrix, [0]*(MATRIX_ROWS-matrix.shape[0]))
        matrix = matrix.reshape(-1,MATRIX_COLS) # reshape the matrix
        plt.imshow(matrix, cmap='Greys', interpolation='nearest', aspect=1.107) # plot the matrix
        plt.savefig(f'images/{folder}/image_{i}.png', aspect='auto') # save the image
        i += 1
        print(i) # print the number of the image so we can keep track of advances