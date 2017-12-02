#here is the list of all hyperparameters of the model

import theano.tensor as T

seed = 1                        #seed to repeat the result
depth = 7                       #depth of rnn
block_size = 2                  #meaning 2x2 km^2


db = "Business_Licenses.csv"    #full database
db_fixed = "fixed_data.csv"     #fixed database
test_db = "test_sample.csv"     #partition of database for testing
rnn_db = "rnn_forest.data"      #saved trained rnns
logreg_db = "logreg.data"       #saved trained logreg tensor

##
#RNN pace hyperparameters
##
learning_rates = [1e-6]         #set of learing rates
momentums = [0.98]              #set of momentums
batches = [200]                 #set of batch sizes
depths = [depth]                #set of depthes 
activations = [T.nnet.softmax]  #set of activation functions for hidden layer
