import numpy as np;

class Network(object):
	def __init__(self, sizes=[32, 20, 5], p_weights = None, p_biases = None):
		self.sizes = sizes;
		if(p_weights == None):
			self.biases = [ 2*np.random.random((y, 1))-1 for y in sizes[1:] ];
			self.weights = [ 2*np.random.random((y, x))-1 for x, y in zip(sizes[:-1], sizes[1:]) ];
		else:
			biases, weights = p_biases, p_weights;

	def Predict(self, a):
		for b, w in zip(self.biases, self.weights):
			a = 1 / (1 + np.exp(-np.dot(w, a) - b));
			print(a);
		return np.argmax(a);

	def GetWeights(self):
		we = np.array([]);
		bi = np.array([]);
		for b, w in zip(self.biases, self.weights):
			we = np.concatenate((we, w.flatten()));
			bi = np.concatenate((bi, b.flatten()));
		return np.concatenate((we, bi));

	def SetWeights(self, weights):
		i = 0;
		for k in range(len(self.sizes) - 1):
			si, sip = self.sizes[k], self.sizes[k + 1];
			self.weights[k] = weights[i: i + si*sip].reshape((sip, si));
			i += si * sip;
		for k in range(len(self.sizes) - 1):
			self.biases[k] = weights[i: i + self.sizes[k+1]].reshape((self.sizes[k+1], 1));
			i += self.sizes[k+1];