#here is the list of all hyperparameters of the model

import theano.tensor as T

seed = 1                        #seed to repeat the result
depth = 7                       #depth of rnn
block_size = 2                  #meaning 2x2 km^2


db = "Business_Licenses.csv"    #full database
test_db = "test_sample.csv"     #partition of database for testing
db_fixed = "fixed_data.csv"     #fixed database
edge_data = "edgeData.csv"      #short summary of database
rnn_db = "rnn_forest.data"      #saved trained rnns
logreg_db = "logreg.data"       #saved trained logreg tensor

##
#RNN pace hyperparameters
##


def empty(X):
    return X

def inv_empty(X):
    return np.ones((X.shape[0],X.shape[1]))


def sigmoid(X):
    return np.exp(X) / (1 + np.exp(X))


def inv_sigmoid(X):
    return X * (1 - X)


def softmax(X):
    v = X - np.amax(X, axis=1)[:, None]
    exp = np.exp(v)
    return exp / np.sum(exp, axis=1)[:, None]


learning_rates = [1e-6, 1e-4,1e-2,1e0,1e2]          #set of learing rates
activations = [empty, sigmoid, softmax]             #set of activation functions for hidden layer
inv_activations = [inv_empty, sigmoid, softmax]
num_neurals = [1024, 2048, 4096]
limit = 5000
###
# logreg hyperparameters
###
