#relevant imports
import numpy as np
import pydub as pd
import matplotlib.pyplot as plt

# global variables
AUDIO_PATH = "audios/Voyager-Golden-Record_encoded_image_data.mp3"
INIT = 1300000 # point of init on mp3 file that we want to read
END = 41150000 # point of end on mp3 file that we want to read
GROUP_SIZE = 400 # GROUP_SIZE of region to wich we calculate the density

if (END - INIT) % GROUP_SIZE != 0:
    END = INIT + (GROUP_SIZE * ((END - INIT) // GROUP_SIZE)) # redefine to have integer multiple

GROUP = 60 # number of pre-groups to wich we recalculate the density

#configurations
# amplitude_threshold -> threshold to wich we consider a peak (> threshold is peak)
# density_threshold -> threshold to wich we consider a dense area (number of peaks per points)
config1 = {'AMPLITUDE_THRESHOLD' : 1000, 'DENSITY_THRESHOLD' : 0.30} #configuration 1
config2 = {'AMPLITUDE_THRESHOLD' : 2000, 'DENSITY_THRESHOLD' : 0.30} #configuration 2

#threshold for redefine the density
redef_threshold = 1

#densities
density1 = [] #density of configuration 1
density2 = [] #density of configuration 2
true_density = [] #density of re-calculated groups

#read the mp3 file
def read_mp3(filename):
    #read the mp3 file
    song = pd.AudioSegment.from_mp3(filename)
    #separate the channels
    left, right = song.split_to_mono()[0], song.split_to_mono()[1]
    #convert the channels to numpy arrays
    left_array = np.array(left.get_array_of_samples())
    right_array = np.array(right.get_array_of_samples())
    #return the arrays
    return left_array, right_array


#read the mp3 file
left_array, right_array = read_mp3(AUDIO_PATH)
#loop over the arrays
loop = 0
for array in (left_array, right_array):
    # define folder to save results
    folder = ('left', 'right')[loop]

    for i in range(INIT, END, GROUP_SIZE):
        # count the number of peaks in a given region
        counter = [0,0]
        for j in array[i:i+GROUP_SIZE]:
            if j > config1['AMPLITUDE_THRESHOLD'] : counter[0] += 1
            if j > config2['AMPLITUDE_THRESHOLD'] : counter[1] += 1
        region_density = [counter[0]/GROUP_SIZE, counter[1]/GROUP_SIZE]

        if region_density[0] > config1['DENSITY_THRESHOLD']: # if the region is dense in configuration 1
            density1.append(1)
        else:
            density1.append(0)

        if region_density[1] > config2['DENSITY_THRESHOLD']: # if the region is dense in configuration 2
            density2.append(1)
        else:
            density2.append(0)

        index = (i-INIT)//GROUP_SIZE # index of the region

        if density1[index] & density2[index]: # if the region is dense in both configurations
            true_density.append(1)
        else:
            true_density.append(0)
        
    new_label = [] # new label for the regions

    # define regions with high density
    for i in range(INIT, END, GROUP_SIZE*GROUP): # loop over the regions to redefine density
        counter = 0
        for j in true_density[(i-INIT)//GROUP_SIZE:(i-INIT)//(GROUP_SIZE)+(GROUP)]:
            if j: counter += 1 # count the number of regions with high density
        if counter > redef_threshold: # if there are more than threshold regions with high density
            new_label.append(1)
        else:
            new_label.append(0)
    # divide original array into groups based on new_label
    # we need to start in a non sequence of zeros (->000...)
    # (->100...) works
    start = []
    end = []
    for i in range(1, len(new_label)-1): # loop over the regions
        if new_label[i] == 0: # if the region is not dense
            if new_label[i+1] == 0: # if the next region is not dense
                if new_label[i-1] == 1: # if the previous region is dense
                    start.append(INIT+(i)*GROUP_SIZE*GROUP)
            else:
                if new_label[i-1] == 0: # if the previous region is not dense
                    end.append(INIT+(i)*GROUP_SIZE*GROUP)
        
    # #plot array with array[start[i]:end[i]] colored diferently
    # plt.figure(figsize=(20,10))
    # plt.plot(array[INIT:END], color='black')
    # for i in range(len(start)):
    #     try:
    #         plt.plot(array[start[i]:end[i]], color='red')
    #     except:
    #         pass
    # plt.show()

    for item in range(len(end)): 
        with open(f"text/{folder}/text_{item}.txt", "w") as f: # save the text file
            print('start: ', start[item])
            print('end: ', end[item])
            print('length: ', end[item]-start[item])
            print()
            np.savetxt(f, array[start[item]:end[item]], fmt="%d")
    
    loop =+ 1
