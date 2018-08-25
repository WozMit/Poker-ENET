import numpy as np;
import Network;

#np.random.seed(0);
strategy = Network.Network();
t = np.random.random((32, 1));
t = t.reshape(32, 1);
w = strategy.GetWeights();
print(strategy.Predict(t));