import csv
from datetime import date

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

with open("pkn.txt", "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    linesNumber = sum(1 for line in open("pkn.txt"))

    ilosc=0
    while ilosc<linesNumber-1000:
        next(csv_reader)
        ilosc = ilosc + 1

    datyCen = []
    cenyZamkniecia = []
    for i, line in enumerate(csv_reader):
        line[2] = '-'.join([line[2][:4], line[2][4:6], line[2][6:]])
        line[2] = date.fromisoformat(line[2])
        cena = float(line[7])
        datyCen.append(line[2])
        cenyZamkniecia.append(cena)

EMA26 = []
EMA12 = []
MACD = []
SIGNAL = []

for i, cena in enumerate(cenyZamkniecia):
    if i>=25:
        licznik26 = 0
        mianownik26 = 0
        podstawa26 = 1 - (2/27)
        for j in range(0, 26):
            licznik26 = licznik26 + float(cenyZamkniecia[i-j])*(podstawa26**j)
            mianownik26 = mianownik26 + (podstawa26**j)
        EMA26.append(licznik26/mianownik26)
        licznik12 = 0
        mianownik12 = 0
        podstawa12 = 1 - (2 / 13)
        for j in range(0, 12):
            licznik12 = licznik12 + float(cenyZamkniecia[i-j])*(podstawa12**j)
            mianownik12 = mianownik12 + (podstawa12**j)
        EMA12.append(licznik12/mianownik12)
        MACD.append(EMA12[i-25]-EMA26[i-25])

for i, wskaznik in enumerate(MACD):
    if i>=8:
        licznik9 = 0
        mianownik9 = 0
        podstawa9 = 1 - (2/10)
        for j in range(0, 9):
            licznik9 = licznik9 + float(MACD[i - j]) * (podstawa9 ** j)
            mianownik9 = mianownik9 + (podstawa9 ** j)
        SIGNAL.append(licznik9/mianownik9)

for i in range(len(MACD)-len(SIGNAL)):
    MACD.pop(i)

for i in range(len(datyCen)-len(SIGNAL)):
    datyCen.pop(i)

for i in range(len(cenyZamkniecia)-len(SIGNAL)):
    cenyZamkniecia.pop(i)
'''
def kupno(datyCen, cenyZamkniecia, MACD, SIGNAL):
    daty_kupna = []
    ceny_kupna = []
    MACD_kupna = []
    for i, cena in enumerate(datyCen):
        if i > 0:
            if MACD[i-1] < SIGNAL[i-1] and MACD[i] > SIGNAL[i]:
                daty_kupna.append(datyCen[i])
                ceny_kupna.append(cenyZamkniecia[i])
                MACD_kupna.append(MACD[i])
    return daty_kupna, ceny_kupna, MACD_kupna

def sprzedaz(datyCen, cenyZamkniecia, MACD, SIGNAL):
    daty_sprzedazy = []
    ceny_sprzedazy = []
    MACD_sprzedazy = []
    for i, cena in enumerate(datyCen):
        if i > 0:
            if MACD[i-1] > SIGNAL[i-1] and MACD[i] < SIGNAL[i]:
                daty_sprzedazy.append(datyCen[i])
                ceny_sprzedazy.append(cenyZamkniecia[i])
                MACD_sprzedazy.append(MACD[i])
    return daty_sprzedazy, ceny_sprzedazy, MACD_sprzedazy
'''

def kupnaSprzedaze(kwota, datyCen, cenyZamkniecia, MACD, SIGNAL):
    daty_kupna = []
    ceny_kupna = []
    MACD_kupna = []
    daty_sprzedazy = []
    ceny_sprzedazy = []
    MACD_sprzedazy = []
    iloscAkcji = 0
    for i, cena in enumerate(datyCen):
        if i == len(datyCen)-1:
            kwota = kwota + iloscAkcji*float(cenyZamkniecia[i])
        elif i > 0:
            if kwota > 0 and MACD[i-1] < SIGNAL[i-1] and MACD[i] > SIGNAL[i]:
                daty_kupna.append(datyCen[i])
                ceny_kupna.append(cenyZamkniecia[i])
                MACD_kupna.append(MACD[i])
                iloscAkcji=kwota/float(cenyZamkniecia[i])
                kwota=0
            elif iloscAkcji > 0 and MACD[i-1] > SIGNAL[i-1] and MACD[i] < SIGNAL[i]:
                daty_sprzedazy.append(datyCen[i])
                ceny_sprzedazy.append(cenyZamkniecia[i])
                MACD_sprzedazy.append(MACD[i])
                kwota=iloscAkcji*float(cenyZamkniecia[i])
                iloscAkcji=0

    return daty_kupna, ceny_kupna, MACD_kupna, daty_sprzedazy, ceny_sprzedazy, MACD_sprzedazy

def kupnaSprzedazeUsprawnione(kwota, datyCen, cenyZamkniecia, MACD, SIGNAL):
    daty_kupna = []
    ceny_kupna = []
    MACD_kupna = []
    daty_sprzedazy = []
    ceny_sprzedazy = []
    MACD_sprzedazy = []
    iloscAkcji = 0
    for i, cena in enumerate(datyCen):
        if i == len(datyCen) - 1:
            kwota = kwota + iloscAkcji * float(cenyZamkniecia[i])
        elif i > 0:
            if kwota > 0 and MACD[i - 1] < SIGNAL[i - 1] and MACD[i] > SIGNAL[i] and SIGNAL[i] >= SIGNAL[i - 1] and MACD[i] < 0:
                daty_kupna.append(datyCen[i])
                ceny_kupna.append(cenyZamkniecia[i])
                MACD_kupna.append(MACD[i])
                iloscAkcji = kwota / float(cenyZamkniecia[i])
                kwota = 0
            elif iloscAkcji > 0 and MACD[i - 1] > SIGNAL[i - 1] and MACD[i] < SIGNAL[i] and SIGNAL[i] <= SIGNAL[i - 1] and MACD[i] > 0:
                daty_sprzedazy.append(datyCen[i])
                ceny_sprzedazy.append(cenyZamkniecia[i])
                MACD_sprzedazy.append(MACD[i])
                kwota = iloscAkcji * float(cenyZamkniecia[i])
                iloscAkcji = 0

    return daty_kupna, ceny_kupna, MACD_kupna, daty_sprzedazy, ceny_sprzedazy, MACD_sprzedazy

datyK, cenyK, MACDK, datyS, cenyS, MACDS = kupnaSprzedaze(1000, datyCen, cenyZamkniecia, MACD, SIGNAL)
datyKU, cenyKU, MACDKU, datySU, cenySU, MACDSU = kupnaSprzedazeUsprawnione(1000, datyCen, cenyZamkniecia, MACD, SIGNAL)

print(cenyZamkniecia)

print(len(datyK))
print(len(datyS))
print(len(datyKU))
print(len(datySU))

print(datyK)
print(cenyK)

figure, axis = plt.subplots(2, 1)

axis[0].plot(datyCen, MACD)
axis[0].plot(datyCen, SIGNAL)
axis[0].scatter(datyK, MACDK, marker="^", color="green")
axis[0].scatter(datyS, MACDS, marker="v", color="red")
axis[0].set_title("Wykresy MACD i SIGNAL")
axis[0].set_xlabel("Dzien na gieldzie")
axis[0].set_ylabel("Wartosci wskaznikow")
axis[0].legend(["MACD", "SIGNAL", "Momenty kupna", "Momenty sprzedazy"])

plt.tight_layout()

axis[1].plot(datyCen, cenyZamkniecia)
axis[1].scatter(datyK, cenyK, marker="^", color="green")
axis[1].scatter(datyS, cenyS, marker="v", color="red")
axis[1].set_title("Wykres cen zamkniecia")
axis[1].set_xlabel("Dzien na gieldzie")
axis[1].set_ylabel("Cena zamkniecia")
axis[1].legend(["Ceny wyjsciowe"])

# plt.show()
# plt.figure()
figure, axis = plt.subplots(2, 1)

axis[0].plot(datyCen, MACD)
axis[0].plot(datyCen, SIGNAL)
axis[0].plot(datyCen, np.zeros(len(datyCen)), color="black", linewidth=0.5)
axis[0].scatter(datyKU, MACDKU, marker="^", color="blue")
axis[0].scatter(datySU, MACDSU, marker="v", color="gold")
axis[0].set_title("Wykresy MACD i SIGNAL usprawnionego")
axis[0].set_xlabel("Dzien na gieldzie")
axis[0].set_ylabel("Wartosci wskaznikow")
axis[0].legend(["MACD", "SIGNAL", "Wartosc zero", "Momenty kupna", "Momenty sprzedazy"])

plt.tight_layout()

axis[1].plot(datyCen, cenyZamkniecia)
axis[1].scatter(datyKU, cenyKU, marker='^', color="blue")
axis[1].scatter(datySU, cenySU, marker="v", color="gold")
axis[1].set_title("Wykres cen zamkniecia")
axis[1].set_xlabel("Dzien na gieldzie")
axis[1].set_ylabel("Cena zamkniecia")
axis[1].legend(["Ceny wyjsciowe"])

plt.show()

def inwestycja(kwota, datyCen, cenyZamkniecia, MACD, SIGNAL):
    iloscAkcji = 0
    for i, cena in enumerate(datyCen):
        if i == len(datyCen)-1:
            kwota = kwota + iloscAkcji*float(cenyZamkniecia[i])
        elif i > 0:
            if kwota > 0 and MACD[i-1] < SIGNAL[i-1] and MACD[i] > SIGNAL[i]:
                iloscAkcji=kwota/float(cenyZamkniecia[i])
                kwota=0
            elif iloscAkcji > 0 and MACD[i-1] > SIGNAL[i-1] and MACD[i] < SIGNAL[i]:
                kwota=iloscAkcji*float(cenyZamkniecia[i])
                iloscAkcji=0

    return kwota

def inwestycja_usprawnione(kwota, datyCen, cenyZamkniecia, MACD, SIGNAL):
    iloscAkcji = 0
    for i, cena in enumerate(datyCen):
        if i == len(datyCen)-1:
            kwota = kwota + iloscAkcji*float(cenyZamkniecia[i])
        elif i > 0:
            if kwota > 0 and MACD[i-1] < SIGNAL[i-1] and MACD[i] > SIGNAL[i] and SIGNAL[i] >= SIGNAL[i-1] and MACD[i] < 0:
                iloscAkcji=kwota/float(cenyZamkniecia[i])
                kwota=0
            elif iloscAkcji > 0 and MACD[i-1] > SIGNAL[i-1] and MACD[i] < SIGNAL[i] and SIGNAL[i] <= SIGNAL[i-1] and MACD[i] > 0:
                kwota=iloscAkcji*float(cenyZamkniecia[i])
                iloscAkcji=0

    return kwota

kwota = 1000
zwrotInwestycji = inwestycja(kwota, datyCen, cenyZamkniecia, MACD, SIGNAL)
zwrotInwestycjiUspr = inwestycja_usprawnione(kwota, datyCen, cenyZamkniecia, MACD, SIGNAL)
print("Zwrot z inwestycji to", zwrotInwestycji)
print("Stopa zwrotu z inwestycji to", 100*(zwrotInwestycji-kwota)/kwota, "%")
print("Zwrot z inwestycji usprawnionej to", zwrotInwestycjiUspr)
print("Stopa zwrotu z inwestycji usprawnionej to", 100*(zwrotInwestycjiUspr-kwota)/kwota, "%")