#SNN
import hyperparameters as hp
import numpy as np

# return matrix^(nXm) with random weight
def init_weight(n, m):
    return np.random.randn(n, m) / np.sqrt(n + m)



class SNN:
    def __init__(self, size_x, size_y, size_h, activation=hp.empty, inv_activation=hp.empty):
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

                self.Wh -= lr * np.multiply(dWh,self.Wh)
                self.bo -= lr * np.multiply(dbo,self.bo)
                self.Wx -= lr * np.multiply(dWx,self.Wx)
            #if i % 50 == 0:
               # print("At " + str(i))

    def predict(self, X):
        h = self.f(np.matmul(X,self.Wx))
        return np.matmul(h, self.Wh) + self.bo, h

    def save(self, file, i):
        data = np.array([self.Wx, self.Wh, self.bo, [i]]).T
        #np.savetxt(file,data, delimiter =',')

    def mean(self,X,Y):
        error = 0
        count = 0
        for (x,y) in zip(X,Y):
            p, _ = self.predict(x)
            error += np.sum(y) - np.sum(p)
            count += 1

        return error/count


def forest(X,Y, last):
    forest = []
    for l in hp.learning_rates:
        for h in hp.num_neurals:
            for f,f1,i in zip(hp.activations, hp.inv_activations,range(len(hp.activations))):
                rnn = SNN(len(X[0]),len(Y[0]), h,f,f1)
                rnn.fit(X,Y,l,hp.limit)
                filename = "SNN_lr=" + str(l) + "_h=" + str(h) + "_f=" + str(i) + ".data"
                print(filename)
                rnn.save(filename,i)
                mean = rnn.mean(X,Y)
                print(mean)
                # print(filename + " with mean error = " + str(rnn.mean))
                forest.append(rnn)
    return forest
