import numpy as np
import Network
from game import *


def Evaluate(strategies, juegos = 10):
    Jugadores = []
    for i in range(len(strategies)):
        Jugadores.append(Jugador(500, strategies[i]))
    for h in range(juegos):
        random.shuffle(Jugadores)
        for i in range(0,len(Jugadores)//9, 9):
            #print(len(Jugadores[i*9:(i+1)*9]))
            Juego(Jugadores[i*9:(i+1)*9], 10, juegos).torneo()
            print("Tournament", i);
        print("Tournament round %d finished" %h);
        for x in Jugadores:
            x.fichas = 500

    fitness = [x.puesto for x in Jugadores]
    x = np.array([x.getStrategy() for x in Jugadores])
    return x[np.argsort(fitness)]