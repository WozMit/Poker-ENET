import numpy as np;
import Network;

def Evaluate(x):
	fitness = np.zeros(n);
	for i in range(n):
		fitness[i] = np.sum(np.abs(x[i]));
	x = x[np.argsort(fitness)[::-1]];
	print("Current fitness:", np.sum(np.abs(x[0])));
	return x;

def CrossPopulation(x, y):
	z = np.copy(x);
	for i in range(len(z)):
		if(np.random.random() >= 0.5):
			z[i] = y[i];
	return z;

# Choose the parameters for training the players
n = 100;
generations = 500;
mutation_prob = 0.1;
mutations_per_indiv = 50;
np.random.seed(0);

# Initialize first generation randomly
Population = np.array([Network.Network().GetWeights() for _ in range(n)]);

for _ in range(generations):
	# Evaluate the population and take them sorted
	Population = Evaluate(Population);

	# Construct next population

	# Reproduction
	k = 10;
	for i in range(11):
		for j in range(i, 12):
			Population[k] = CrossPopulation(Population[i], Population[j]);
			k += 1;
	while(k < n):
		Population[k] = Network.Network().GetWeights();
		k += 1;

	# Mutation
	for i in range(2, n):
		if(np.random.random() <= mutation_prob):
			for _ in range(mutations_per_indiv):
				idx = np.random.randint(len(Population[i]));
				Population[i][idx] = 2 * np.random.random() - 1;