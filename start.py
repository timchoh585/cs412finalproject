#this is the main file that grate\instructor will run to repeat experience


#12/2 SAMPLE CODE

#there are 2 methods that can be run
#train -- train the model and saves at destination(see def below)
#show_result -- use data from destination to show learning results


import matplotlib.pyplot as plt
import rnnLearning
import sortInfo
import training
import logregBlockLearning

#list of all hyperparameters
seed = 1            #seed used to create rnn rf
depth = 7           #recurence depth
block_size = 2      #size of block in km, squares have been used
frame_sep = ";;;"   #token to parse different time frame of db

#source with db
#source = open("Business_Licenses.csv","rb")
source = open("test_sample.csv","rb")
#destination to store the data
destination = open("model_results.data","w")

##
#end of hyperparameters
##

def train:
    "perform traning"
    #1, formate the data by adding extra parameters i.e. (x,y) quazilocations
    #see sortInfo
    
    #2, sort data by time frame

    #3, convert data to block using logReg or what ever model is defined

    #4, train rnn rf based on blocks with time frames and save results



def show_result:
    "parse bac from destination and draw heat maps using .. plt
    #there are 2 possible heat maps
    #1. by chicago businesses density
    #2. by superior business type density (relative or absolute)
    #question for discussion
    
