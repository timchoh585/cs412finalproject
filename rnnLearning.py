#rnn model
#input -> blocks weights (regarding the logreg model)
#1 fully connected hidden layer
#recurent depth is 7(up to discussion)


#12/1 NOTES
#the model haven't been debugged yet
#

import numpy as np
import theano as th
import theano.tensor as T

#return matrix^(nXm) with random weight
def init_weight(n, m):
    return np.random.randn(n, m) / np.sqrt(n + m)

class RNN:
    def __init__(self, X,H,O):
        self.X = X #input size
        self.H = H #hidden layer size
        self.O = O #output size

        #init weights
        Wx = init_weight(self.X,self.H) #input->hidden matrix
        bh = np.zeros(self.H)           #bias for hidden
        Wh = init_weight(self.H,self.H) #recurrent hidden matrix
        h0 = np.zeros(self.H)           #bias for recurrent
        Wo = init_weight(self.H,self.O) #hidden->output matrix
        bo = np.zeros(O)                #bias for output

        #share with theano environment
        self.Wx = th.shared(Wx)
        self.bh = th.shared(bh)
        self.Wh = th.shared(Wh)
        self.h0 = th.shared(h0)
        self.Wo = th.shared(Wo)
        self.bo = th.shared(bo)
        self.params = [self.Wx,self.bh,self.Wh,self.h0,self.Wo,self.bo]


    def fit(self, learning_rate=1e-6, momentum=1e-8, batch=200,activation=T.tanh, depth=7):
        self.f = activation

        #define set of input and corresponding output for supervise learning
        X = [[]]
        Y = [[]]
        
        #theano input-output vectors
        thX = T.fvector('X')
        thY = T.fvector('Y')
        thK = T.iscalar('depth')
        
        #reccurent call of evaluation, return next pair of input\reccurent hidden values
        def recurrence(x_t, h_t1):
            #update reccurent hidden values
            #h_t = f(Wx*x + Wh*h_t1 + b)
            h_t = self.f(x_t.dot(self.Wx) + h_t1.dot(self.Wh) + self.bh)
            #calculate current output, note in our model it is the next time step disctribution
            #y_t = f(Wo*h_t + b)
            y_t = self.f(h_t.dot(self.Wo) + self.bo)
            return h_t, y_t

        #define theano scan function for call
        [h,y], _ = th.scan(
            fn=recurrence,
            outputs_info=[self.h0,None],
            sequences=thX,
            n_steps = thK,
        )

        #define prediction, should be normalyze function
        #temporal approache -- softmax
        prediction = T.softmax(Y)

        #define learning model
        #for the cost is usuall log loss function
        cost = -T.mean(T.log(Y[T.arange(thY.shape[0]),thY]))
        #for grad use theano grad function
        grads = T.gtrad(cost, self.params)
        #calculate the change of params for momentum
        #init to all zero
        dparams = [theano.shared(p.get_value()*0) for p in self.params]

        #define the update using gradient decent algorithm with momentum
        #i.e. w <- w + momentum * dw - n * grad_w(E)
        #     dw<- momentum * dw - n * grad_w(E)
        updates = [
            (p, p + mu*dp - learning_rate*g) for p, dp, g in zip(self.params, dparams, grads)
        ] + [
            (dp, mu*dp - learning_rate*g) for dp, g in zip(dparams, grads)
        ]

        #define complete training model for theano
        self.predict_op = th.function(inputs=[thX,thK], outputs=prediction)
        self.train_op = th.function(
            inputs=[thX, thY],
            outputs=[cost, prediction, y],
            updates=updates
        )

        #
        # TODO: run training loop over the data from db
        #

    
    def save(self, filename):
        np.savez(filename, *[p.get_value() for p in self.params])
    

def create_forest(rnn, filename):
    learning_rates = [1e-6]
    momentums = [1e-8]
    batches = [200]
    depths = [7]
    activations = [T.nnet.softmax]

    for n in learning_rates:
        for m in momentums:
            for b in batches:
              for d in depths:
                  for f in activations:
                      #output the model
                      rnn.fit(n,m,b,f,d)
                      rnn.save(filename)

def rnn_train(filename, seed, inputsize, numneurals, outputsize):
    rnn = RNN(inputsize,numneurals,outputsize)
    np.random.rand(seed)
    create_forest(rnn, filename)

rnn_train("rnn_forest.data", seed=1, inputsize=4, numneurals=16, outputsize=4)
