#SNN
import hyperparameters as hp
import numpy as np

# return matrix^(nXm) with random weight
def init_weight(n, m):
    return np.random.randn(n, m) / np.sqrt(n + m)



class SNN:
    def __init__(self, size_x, size_y, size_h, activation=empty, inv_activation=empty):
        self.Wx = init_weight(size_x, size_h)
        self.Wh = init_weight(size_h, size_y)
        self.bo = np.zeros(size_y)
        self.f = activation
        self.f1 = inv_activation


    def fit(self,X,Y,lr=1e-6,limit=1000, mu=0.95):
        for i in range(limit):
            for x,y in zip(X,Y):
                y_pred,h = self.predict(x)
                err = (y - y_pred)

                dWh = np.matmul(np.array([h]).T, np.array([err]))
                dbo = err

                dWx = np.matmul(np.array([x]).T,[np.matmul(err, self.Wh.T)])

                self.Wh += lr * dWh
                self.bo += lr * dbo
                self.Wx += lr * dWx
            if i % 50 == 0:
                print("At " + str(i))

    def predict(self, X):
        h = self.f(np.matmul(X,self.Wx))
        return np.matmul(h, self.Wh) + self.bo, h

    def save(self, file):
        "save to file"

def forest(X,Y):
    for l in hp.learning_rates:
        for h in hp.num_neurals:
            for f,f1 in zip(hp.activations, hp.inv_activations):
                rnn = SNN(X.shape[0],Y.shape[0], h,f,f1)
                rnn.fit(X,Y,l,hp.limit)
                rnn.save("filename")