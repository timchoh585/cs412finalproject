# this is the main file that grate\instructor will run to repeat experience


# 12/2 SAMPLE CODE

# there are 2 methods that can be run
# train -- train the model and saves at destination(see def below)
# show_result -- use data from destination to show learning results


import sortInfo as si
import logregBlockLearning as lg
import hyperparameters as hp
import heatmap as hm
import SNN

# source with db
# source = open("Business_Licenses.csv","rb")
source = open(hyperparameters.db, "rb")
# destination to store the data
destination = open("model_results.data", "w")


##
# end of hyperparameters
##

def train():
    "perform traning"
    # 1, formate the data by adding extra parameters i.e. (x,y) quazilocations
    # see sortInfo
    si.fix_data(hp.db)
    # 2, sort data by time frame

    # 3, convert data to block using logReg or what ever model is defined
    data = []
    X = []
    Y = []
    last = []
    # 4, train rnn rf based on blocks with time frames and save results
    forest = SNN.forest(X, Y, last)
    # 5, train logreg to weight each RNN properly
    model, y = lg.train_forest(forest, X, Y, last)
    # 6, show result
    hm.create_heat(y)

# def show_result():
# "parse bac from destination and draw heat maps using .. plt
# there are 2 possible heat maps
# 1. by chicago businesses density
# 2. by superior business type density (relative or absolute)
# question for discussion
