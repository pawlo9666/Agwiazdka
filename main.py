import funkcje
import time
start_time = time.time()

mapa=funkcje.generujmapa("grid.txt")
funkcje.koniec(mapa, 19, 19)
poczatek = funkcje.Punkt(0, 0)
poczatek.zmienkoniec(19,19)
trasa = [poczatek]
rozwazane = []

funkcje.szukajtrasy(mapa , trasa , rozwazane)

print()
print("--- %s ms ---" % ((time.time() - start_time)*1000))
