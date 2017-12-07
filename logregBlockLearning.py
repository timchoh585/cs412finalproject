# logistic regression model for each block
# (return vector of density businesses type)
# or argmax of densities
# up to discuss

import hyperparameters as hp
import numpy as np
import SNN

def predict(model, X):
    power = np.matmul(X, model)
    power = power - np.amax(power, axis=1)[:, None]
    exp = np.exp(power)
    prediction = exp / np.sum(exp, axis=1)[:, None]
    return prediction


def fit(X, Y, limit, n, eps, pred=predict):
    print("Number of iterations: " + str(limit))
    sizeX = len(X[0])
    sizeY = len(Y[0])
    w = np.zeros((sizeX, sizeY))
    grad = np.zeros((sizeX, sizeY))

    count = 0
    absgrad = eps + 1
    while absgrad > eps:
        prediction = pred(w, X)

        for j in range(len(w)):
            grad[j] = np.sum([(np.matmul(x[j],y) - np.matmul(x[j],s)) for x, y, s in zip(X, Y, prediction)], axis=0)
        w = w + n * grad
        count += 1

        if count > limit:
            break

        # if count % 100 == 0:
        #print("At iteration: " + str(count))

        absgrad = np.sum(np.square(grad))
    return w


def run_log_reg(X):
    model = np.fromfile(hp.logreg_db, dtype=float32)
    return predict(model, X)


def train_forest(forest, X, Y, last):
    data = []
    for x in X:
        row = []
        for snn in forest:
            y, _ = snn.predict(x)
            row.append(y)
        data.append(row)
    model = fit(data,Y,hp.limit, hp.learning_rates[0],1e-4)

    question = []
    for snn in forest:
        y, _ = snn.predict(last)
        question.append(y)

    y = predict(model, question)

    return model, y
