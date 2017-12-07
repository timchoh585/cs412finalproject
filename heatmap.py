import numpy as np
import matplotlib.pyplot as plt

# show heat map
def create_heat(output, title="Chicago heat map"):
    #plt.figure(create_heat.counter)
    create_heat.counter += 1
    im = plt.matshow(output, cmap=plt.cm.cool, aspect='auto')
    plt.colorbar(im)
    plt.show()

create_heat.counter = 0

x = np.random.randn(10,10)
create_heat(x)
