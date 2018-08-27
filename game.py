import random
from Player import *

A = []

class Juego:
    def __init__(self, Jugadores, minima, juegos):
        self.Jugadores = Jugadores
        self.minima = minima
        self.big = minima
        self.inicializar()
        self.juegos = juegos
        self.a = np.array([[100, 100, 82, 80, 75, 74, 72, 71, 73, 76, 76, 76, 76],
            [100, 100, 90, 79, 78, 73, 71, 70, 69, 68, 67, 67, 66],
            [74, 72, 89, 87, 85, 80, 76, 74, 73, 72, 71, 71, 70],
            [72, 70, 78, 86, 92, 87, 77, 77, 75, 74, 74, 73, 72],
            [69, 69, 73, 82, 84, 91, 86, 78, 76, 75, 74, 73, 73],
            [64, 64, 71, 75, 80, 90, 89, 83, 79, 75, 74, 73, 72],
            [63, 62, 66, 72, 76, 80, 78, 87, 82, 77, 73, 72, 71],
            [62, 61, 65, 68, 71, 75, 78, 75, 85, 80, 76, 71, 70],
            [61, 60, 64, 66, 67, 70, 73, 76, 72, 83, 79, 74, 70],
            [60, 59, 63, 65, 65, 66, 68, 71, 74, 70, 82, 77, 73],
            [60, 58, 62, 64, 65, 64, 64, 66, 69, 72, 68, 76, 72],
            [59, 57, 61, 64, 64, 64, 63, 62, 65, 68, 67, 67, 71],
            [59, 57, 61, 63, 63, 63, 62, 61, 61, 63, 63, 62, 67]])/100

    def inicializar(self):
        self.minima = self.big
        self.pozo = []
        self.pozo_reparticion = []
        self.Cartas = []
        self.Maso = [x for x in range(52)]
        random.shuffle(self.Maso)
        self.maso_pos = 0
        self.dealer = random.randint(0, len(self.Jugadores) - 1)

    def preflop(self, jugadores,jug_torneo):
        #print("Preflop")
        com = 0
        i = 1

        while com < 2 :
            x = (self.dealer + i) % len(self.Jugadores)
            if jugadores.count(x) == 0:
                i += 1
                continue
            if com == 0: self.Jugadores[x].apuesta += self.minima / 2 if self.minima/2<= self.Jugadores[x].fichas else self.Jugadores[x].fichas
            else: self.Jugadores[x].apuesta += self.minima if self.minima <= self.Jugadores[x].fichas else self.Jugadores[x].fichas
            com += 1
            i += 1


        for j in range(len(self.Jugadores)):
            x = (self.dealer + j) % len(self.Jugadores)
            if jugadores.count(x) == 0: continue
            self.Jugadores[x].Cartas.append(self.Maso[self.maso_pos])
            self.Jugadores[x].Cartas.append(self.Maso[self.maso_pos+1])
            self.maso_pos += 2

        self.ronda_apuestas(jugadores, (self.dealer + i)%len(self.Jugadores), self.minima,jug_torneo)

    def flop(self, jugadores,jug_torneo):
        #print("Flop")
        self.Cartas.append(self.Maso[self.maso_pos])
        self.Cartas.append(self.Maso[self.maso_pos + 1])
        self.Cartas.append(self.Maso[self.maso_pos + 2])
        self.maso_pos += 3
        self.ronda_apuestas(jugadores, (self.dealer + 1)%len(self.Jugadores), 0,jug_torneo)

    def turn(self, jugadores,jug_torneo):
        #print("Turn")
        self.Cartas.append(self.Maso[self.maso_pos])
        self.maso_pos += 1
        self.ronda_apuestas(jugadores, (self.dealer+ 1) % len(self.Jugadores), 0,jug_torneo)

    def river(self, jugadores,jug_torneo):
        #print("River")
        self.Cartas.append(self.Maso[self.maso_pos])
        self.maso_pos += 1
        self.ronda_apuestas(jugadores, (self.dealer + 1) % len(self.Jugadores), 0,jug_torneo)

    def terminar_partida(self, ganador):
        self.Jugadores[ganador].fichas += sum(self.pozo)
        self.pozo = []
        self.pozo_reparticion = []

    def ronda_apuestas(self, jugadores, inicio, minima, jug_torneo):
        i = inicio
        apuesta = minima
        aumento = self.minima
        ult = i
        flag = False
        while True:
            if (i == ult and flag) or len(jugadores)==1: break
            flag = True
            if jugadores.count(i) == 0 or self.Jugadores[i].fichas-self.Jugadores[i].apuesta == 0:
                i = (i + 1) % len(self.Jugadores)
                continue
            pot = [0]
            for x in range(len(self.pozo)):
                if i in self.pozo_reparticion[x]: pot[0] += self.pozo[x]
            pot[0] /=2000
            ap = [(apuesta - self.Jugadores[i].apuesta)/2000]
            size = [(len(jugadores)-1)/8]
            fuerza = [1/(1+math.e**(-10*(self.Jugadores[i].mejor_mano(self.Cartas)/9-0.3)))] if len(self.Cartas) != 0 else [self.a[self.Jugadores[i].Cartas[0]%13,self.Jugadores[i].Cartas[1]%13]]
            ##print("la fuerza es",fuerza)
            manos_dealer = [((jug_torneo.index(i)-jug_torneo.index(self.dealer)+len(jug_torneo))%len(jug_torneo))/8]
            chips = [x.fichas/2000 for x in self.Jugadores]
            rage = [x.rage()/50 for x in self.Jugadores]
            recent_rage = [x.recent_rage()/50 for x in self.Jugadores]

            v = pot+ap+size+fuerza+manos_dealer+rage[i:]+rage[:i]+recent_rage[i:]+recent_rage[:i]+chips[i:]+chips[:i]
            ##print(v)
            #print(len(chips));

            #print("Jugada del jugador " + str(i) + ": ", end="")
            jugada = self.Jugadores[i].jugar(v)
            #print(jugada)
            #jugada = int(input("Jugada del jugador " + str(i) + ":"))
            if jugada == 0 and apuesta != 0: #fold
                jugadores.remove(i)
                self.Jugadores[i].agresividad.append(0)
            elif jugada == 1 or (jugada == 0 and apuesta == 0) or \
                    (jugada == 2 and self.Jugadores[i].fichas<apuesta) or \
                    ((jugada == 3 or jugada == 4) and aumento+apuesta>=self.Jugadores[i].fichas): #call
                self.Jugadores[i].apuesta = apuesta if apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas
                self.Jugadores[i].agresividad.append(1)
            elif jugada == 2: #small raise
                ult = i
                #print(apuesta)
                self.Jugadores[i].agresividad.append((apuesta+(aumento if aumento+apuesta<=self.Jugadores[i].fichas else self.Jugadores[i].fichas-apuesta))/apuesta if apuesta != 0 else 0)
                apuesta += aumento if aumento+apuesta<=self.Jugadores[i].fichas else self.Jugadores[i].fichas-apuesta
                self.Jugadores[i].apuesta = apuesta if apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas

            elif jugada == 3:
                ult = i
                aumento = 3*aumento if aumento*3 <= self.Jugadores[i].fichas-apuesta else self.Jugadores[i].fichas - apuesta
                self.Jugadores[i].agresividad.append((apuesta+(aumento if aumento + apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas - apuesta))/apuesta if apuesta != 0 else 0)
                apuesta += aumento if aumento + apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas - apuesta
                self.Jugadores[i].apuesta = apuesta if apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas
            elif jugada == 4:
                ult = i
                aumento = 10000 * aumento if aumento * 10000 <= self.Jugadores[i].fichas - apuesta else self.Jugadores[i].fichas - apuesta
                self.Jugadores[i].agresividad.append((apuesta + (aumento if aumento + apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas - apuesta))/apuesta if apuesta != 0 else 0)
                apuesta += aumento if aumento + apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas - apuesta
                self.Jugadores[i].apuesta = apuesta if apuesta <= self.Jugadores[i].fichas else self.Jugadores[i].fichas
            #salto si no puede realizar una jugada
            #print("Apuesta:", apuesta)
            #print("Aumento:", aumento)
            #print("-------------------------")
            #for x in jugadores:
                #print(x, self.Jugadores[x])
            #print("-------------------------")

            i = (i + 1) % len(self.Jugadores)
        #print("Termino ronda de apuestas")
        Apuestas = []
        for i in range(len(self.Jugadores)):
            Apuestas.append(self.Jugadores[i].apuesta)
        #print(Apuestas)
        while max(Apuestas) != 0:
            mini = 1000000000000000000
            for i in jugadores:
                if Apuestas[i] != 0: mini = min(mini, Apuestas[i])
            monto = 0
            reparto = set()
            for i in range(len(Apuestas)):
                if Apuestas[i] != 0:
                    reparto.add(i)
                    minimo = mini if mini<=Apuestas[i] else Apuestas[i]
                    monto += minimo
                    self.Jugadores[i].apuesta -= minimo
                    self.Jugadores[i].fichas -= minimo
                    Apuestas[i] -= minimo
            if len(self.pozo_reparticion) == 0:
                self.pozo.append(monto)
                self.pozo_reparticion.append(reparto)
            elif self.pozo_reparticion[len(self.pozo_reparticion)-1] == reparto:
                self.pozo[len(self.pozo)-1] += monto
            else:
                self.pozo.append(monto)
                self.pozo_reparticion.append(reparto)
        #print("El pozo es: ")
        #print(self.pozo)
        #print(self.pozo_reparticion)

    def orden_jugadores(self, jugadores):
        puntajes = []
        for i in jugadores:
            puntajes.append([self.Jugadores[i].mejor_mano(self.Cartas),i])
        puntajes.sort(reverse=True)
        return(puntajes)

    def partida(self, jugadores,jug_torneo):
        self.Cartas = []
        self.maso_pos = 0
        for x in jugadores:
            self.Jugadores[x].Cartas = []
            self.Jugadores[x].agresividad = []
        self.dealer = (self.dealer+1)%len(self.Jugadores)
        while jugadores.count(self.dealer) == 0: self.dealer = (self.dealer+1)%len(self.Jugadores)
        #print("El dealer es el jugador", self.dealer)

        self.preflop(jugadores,jug_torneo)

        for x in jugadores: self.Jugadores[x].apuesta = 0
        if len(jugadores) == 1:
            self.terminar_partida(jugadores[0])
            return

        self.flop(jugadores,jug_torneo)

        for x in jugadores: self.Jugadores[x].apuesta = 0
        if len(jugadores) == 1:
            self.terminar_partida(jugadores[0])
            return

        self.turn(jugadores,jug_torneo)

        for x in jugadores: self.Jugadores[x].apuesta = 0
        if len(jugadores) == 1:
            self.terminar_partida(jugadores[0])
            return

        self.river(jugadores,jug_torneo)

        for x in jugadores: self.Jugadores[x].apuesta = 0
        if len(jugadores) == 1:
            self.terminar_partida(jugadores[0])
            return

        #print(self.Cartas)

        J = self.orden_jugadores(jugadores)
        #print(J)
        i = 0
        for g in range(len(self.pozo_reparticion)):
            if J[i][1] in self.pozo_reparticion[g]: self.Jugadores[J[i][1]].fichas += self.pozo[g]
            else:
                while i < len(J)-1 and not(J[i][1] in self.pozo_reparticion[g]): i+=1
                self.Jugadores[J[i][1]].fichas += self.pozo[g]
        #for i in jugadores:
            #print(i,self.Jugadores[i].fichas)
        self.pozo_reparticion = []
        self.pozo = []
        #print()

    def torneo(self):
        self.inicializar()
        Jug_torneo = [x for x in range(len(self.Jugadores))]
        cont = 1
        while len(Jug_torneo) >= 2:
            if cont % 10 == 0: self.minima += self.big
            #print("                 big:", self.minima)
            #print("Partida numero: ", cont)
            Jug_partida = Jug_torneo.copy()
            self.partida(Jug_partida, Jug_torneo)
            elimi = []
            for i in range(len(Jug_torneo)):
                if self.Jugadores[Jug_torneo[i]].fichas == 0: elimi.append(Jug_torneo[i])
            elimi.reverse()
            for i in elimi:
                self.Jugadores[i].puesto += len(Jug_torneo)/self.juegos
                Jug_torneo.remove(i)
            #print(Jug_torneo)
            cont += 1
            if len(Jug_torneo) == 1: self.Jugadores[Jug_torneo[0]].puesto += 1/self.juegos

        #for i in self.Jugadores:
            #print(i.fichas)



'''
j1 = Jugador(500,[])
#j1.Cartas = [4,5]
#j1.mejor_mano([7,20,6,27,3])

j2 = Jugador(500,[])
j3 = Jugador(500,[])
j4 = Jugador(500,[])
j5 = Jugador(500,[])
j6 = Jugador(500,[])
j7 = Jugador(500,[])
j8 = Jugador(500,[])
j9 = Jugador(500,[])


p1 = Juego([j1, j2, j3, j4, j5, j6, j7, j8, j9], 10, 100)
#p1.torneo()

for _ in range(100):
    p1.torneo()
    for x in p1.Jugadores:
        x.fichas = 500
#print("paso")
for x in p1.Jugadores:
    #print(x.puesto)
#print(j1.puesto)
'''