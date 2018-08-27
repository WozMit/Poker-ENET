import math, itertools, time, Network
import numpy as np
class Jugador:
    def __init__(self, fichas, s):
        self.Cartas = []
        self.fichas = fichas
        self.apuesta = 0
        self.puesto = 0
        self.agresividad = []
        self.strategy = Network.Network()
        self.strategy.SetWeights(s)

    def __str__(self):
        return str(self.fichas) + " " + str(self.apuesta)

    def setStrategy(self, s):
        self.strategy.SetWeights(s)

    def getStrategy(self):
        return self.strategy.GetWeights()

    def rage(self):
        return sum(self.agresividad)/len(self.agresividad) if len(self.agresividad) != 0 else 0;

    def recent_rage(self):
        return sum(self.agresividad[-5:])/len(self.agresividad[-5:]) if len(self.agresividad[-5:]) != 0 else 0;

    def jugar(self, v):
        t = np.array(v)
        t = t.reshape(32, 1)
        return self.strategy.Predict(t)

    def mejor_mano(self, extras):
        cartas_real = ['1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S', '13S',
                       '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', '11D', '12D', '13D',
                       '1T', '2T', '3T', '4T', '5T', '6T', '7T', '8T', '9T', '10T', '11T', '12T', '13T',
                       '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C', '13C']
        mejor = -1
        cartas = self.Cartas + extras #list(set(self.Cartas).union(set(extras)))
        best = 0
        mano = []
        for m in itertools.combinations(cartas, 5):
            ma = self.reconocer_mano(m)
            if best < ma:
                best = ma
                mano = m
        '''
        for i in mano:
            print(cartas_real[i], "", end = '')
        print()
        '''
        return best
    def reconocer_mano(self, mano):
        '''
        0 carta alta
        1 par
        2 dos pares
        3 trio
        4 escalera
        5 Color
        6 full
        7 Poker
        8 Escalera color
        '''
        res = 0
        cont = [0 for _ in range(14)]
        for i in mano:
            cont[i%13]+=1
        cont[13] = cont[0]
        cont[0] = 0
        if 4 in cont:
            res += 7
        elif 3 in cont and 2 in cont:
            res += 6
        elif 3 in cont:
            res += 3
        elif len(self.find(cont,2)) == 2:
            res += 2
        elif len(self.find(cont, 2)) == 1:
            res = 1
        else:
            c = 0
            for i in range(len(cont)):
                if c == 4: break
                if cont[i] == cont[i-1] == 1: c+=1
                else: c = 0
            if c != 4 and cont[13] == 1:
                cont[0] = 1
                cont[13] = 0
                c = 0
                for i in range(len(cont)):
                    if c == 4: break
                    if cont[i] == cont[i - 1] == 1:
                        c += 1
                    else:
                        c = 0
                if c != 4:
                    cont[0] = 0
                    cont[13] = 1

            if c == 4:
                if self.in_r(mano,0,12) or self.in_r(mano,13,25) or self.in_r(mano,26,38) or self.in_r(mano,39,51):
                    res += 8
                else:
                    res += 4
            else:
                if self.in_r(mano,0,12) or self.in_r(mano,13,25) or self.in_r(mano,26,38) or self.in_r(mano,39,51):
                    res += 5
        d = 100
        for i in sorted(self.find(cont, 4), reverse=True):
            res = round(res + (i / d), int(math.log10(d)))
            d *= 100
        for i in sorted(self.find(cont, 3), reverse=True):
            res = round(res + (i / d), int(math.log10(d)))
            d *= 100
        for i in sorted(self.find(cont, 2), reverse=True):
            res = round(res + (i / d), int(math.log10(d)))
            d *= 100
        for i in sorted(self.find(cont, 1), reverse=True):
            res = round(res + (i / d), int(math.log10(d)))
            d *= 100

        return res
    def find(self, A, ob):
        res = []
        for i in range(len(A)):
            if A[i] == ob: res.append(i)
        return res
    def in_r(self, A, mini, maxi):
        for i in A:
            if not(mini<=i<=maxi): return False
        return True

