from math import sqrt

def matrxidisp(matrix, start, end,
               test=None):  # fun wyswietlanko z kolorkami + podświetlanie danej krotki w celach testowych
    if test is None:
        test = [None, None]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "5":
                print('\033[91m' + str(matrix[i][j]) + '\033[0m' + '  ', end='')  # "sciany" czerwone
            elif matrix[i][j] == 3 and (start[0] != i or start[1] != j) and (end[0] != i or end[1] != j) and (
                    test[0] != i or test[1] != j):
                print('\033[94m' + str(matrix[i][j]) + '\033[0m' + '  ', end='')  # trasa niebieska
            elif matrix[i][j] == 1:
                print('\033[92m' + str(matrix[i][j]) + '\033[0m' + '  ', end='')  # start zielony
            elif i == end[0] and j == end[1]:
                print('\033[95m' + str(matrix[i][j]) + '\033[0m' + '  ', end='')  # cel rozowy
            elif matrix[i][j] == 2:
                print('\033[96m' + str(matrix[i][j]) + '\033[0m' + '  ',
                      end='')  # podświetla na morski komorke o podanych wspolzednych - w celach testowych
            else:
                print(str(matrix[i][j]) + '  ', end='')
        print()
def generujmapa(nazwa_pliku): #czyta mapę z pliku i wrzuca jej do dwuwymiarowej tablicy

    plik = open(nazwa_pliku)

    mapa = [[0 for x in range(20)] for y in range(20)]

    for y in range(20):
        for x in range(20):
            mapa[y][x] = plik.read(1)
            plik.read(1)

    plik.close()
    return mapa

def koniec(mapa, x, y): #ustala punkt koncowy wygenerowanej mapy
    koniecx = x
    koniecy = y
    mapa[koniecx][koniecy] = 0


def wyswietlliste(lista):
    for x in range(len(lista)):
        print(x, ".", "x:",lista[x].x , " y:" , lista[x].y , " h:" , lista[x].heurystyka , " k:" , lista[x].koszt)

def wyswietlostatnilista(lista):
    print(len(lista), ".", "x:", lista[-1].x, " y:", lista[-1].y, " h:", lista[-1].heurystyka , lista[-1].koszt)

class Punkt:

    def __init__(self, x=None, y=None , poprzedni=None):
            self.x = x
            self.y = y
            self.poprzedni = poprzedni

            if self.poprzedni is None:
                self.koszt = 0
                self.koniecx = 19
                self.koniecy = 19
            else:
                self.koszt = self.poprzedni.koszt + 1
                self.koniecx = self.poprzedni.koniecx
                self.koniecy = self.poprzedni.koniecy

            self.heurystyka = sqrt(pow(self.x - self.koniecx, 2) + pow(self.y - self.koniecy, 2))
            self.calk = self.koszt + self.heurystyka

    def zmienkoniec(self,x ,y): #ustala punkt końcowy
            self.koniecy = y
            self.koniecx = x
            self.heurystyka = sqrt(pow(self.x - self.koniecx, 2) + pow(self.y - self.koniecy, 2))
            self.calk = self.koszt + self.heurystyka

def sprawdzpunkt(mapa , x , y): #do funkcji dodaj rozwazane
    if (0<= x <= (len(mapa[0])-1)) and (0<= y <= (len(mapa)-1)) and (mapa[y][x] != '5'):
        return True

def najmniejszaheurystykaindex(lista):
    najmniejszy = lista[0]
    index = 0
    for x in range(len(lista)):

            if najmniejszy.calk > lista[x].calk:
                    najmniejszy = lista[x]
                    index = x

    return index

def czyniejestwliscie(punkt , lista): #do funkcji dodaj rozwazane
    for x in range(len(lista)):
        if lista[x].x == punkt.x and lista[x].y == punkt.y:
            return False
    return True


def dodajrozwazane(punkt , rozwazane , trasa, mapa):
    if sprawdzpunkt(mapa, punkt.x+1, punkt.y) is True:
        nowy = Punkt(punkt.x+1, punkt.y, punkt)
        if czyniejestwliscie(nowy, rozwazane) is True:
            if czyniejestwliscie(nowy, trasa) is True:
                rozwazane.append(nowy)

    if sprawdzpunkt(mapa, punkt.x-1, punkt.y) is True:
        nowy = Punkt(punkt.x-1, punkt.y, punkt)
        if czyniejestwliscie(nowy, rozwazane) is True:
            if czyniejestwliscie(nowy, trasa) is True:
                rozwazane.append(nowy)

    if sprawdzpunkt(mapa, punkt.x, punkt.y+1) is True:
        nowy = Punkt(punkt.x, punkt.y+1, punkt)
        if czyniejestwliscie(nowy, rozwazane) is True:
            if czyniejestwliscie(nowy, trasa) is True:
                rozwazane.append(nowy)

    if sprawdzpunkt(mapa, punkt.x, punkt.y-1) is True:
        nowy = Punkt(punkt.x, punkt.y-1, punkt)
        if czyniejestwliscie(nowy, rozwazane) is True:
            if czyniejestwliscie(nowy, trasa) is True:
                rozwazane.append(nowy)

def zmianapotomka(punkt , lista):
    for x in range(len(lista)):
        if lista[x].x == punkt.x and lista[x].y == punkt.y and lista[x].calk > punkt.calk:
            lista[x].calk = punkt.calk
            lista[x].poprzedni = punkt.poprzedni

def dodajdotrasy(rozwazane , trasa):
    indeks = najmniejszaheurystykaindex(rozwazane)
    nowy = rozwazane[indeks]
    if czyniejestwliscie(nowy, trasa) is True:
        trasa.append(nowy)
        rozwazane.pop(najmniejszaheurystykaindex(rozwazane))
    else:
        zmianapotomka(nowy, trasa)

def czykoniec(trasa):
    for x in range(len(trasa)):
        if trasa[x].heurystyka == 0:
            return True

    return False

def trasakoniecpunkt(trasa):
    for x in range(len(trasa)):
        if trasa[x].heurystyka == 0:

            return trasa[x]

def zapisztrase(punkt , mapa):
    mapa[punkt.y][punkt.x] = 3
    while punkt.poprzedni is not None:
        punkt = punkt.poprzedni
        mapa[punkt.y][punkt.x] = 3

def zobaczsprawdzone(trasa , rozwazane , mapa):
    for x in range(len(trasa)):
        mapa[trasa[x].y][trasa[x].x] = 1
    for x in range(len(rozwazane)):
        mapa[rozwazane[x].y][rozwazane[x].x] = 2

def szukajtrasy(mapa , trasa , rozwazane):
    temp = 0
    dodajrozwazane(trasa[0], rozwazane, trasa, mapa)
    while temp < 1:


        dodajdotrasy(rozwazane, trasa)
        dodajrozwazane(trasa[-1], rozwazane, trasa, mapa)


        #print("trasa")
        #wyswietlliste(trasa)
        #print("rozwazane")
        #wyswietlliste(rozwazane)

        if czykoniec(trasa) is True:

            zobaczsprawdzone(trasa,rozwazane,mapa)
            zapisztrase(trasakoniecpunkt(trasa), mapa)
            matrxidisp(mapa,mapa[0] , mapa)

            temp = 1

        elif len(rozwazane) == 0:
            print("brak elementow do rozwazania")
            zobaczsprawdzone(trasa, rozwazane, mapa)
            matrxidisp(mapa,mapa[0] , mapa)
            temp = 1











