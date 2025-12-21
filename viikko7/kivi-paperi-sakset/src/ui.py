from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari


class UI():
    def __init__(self):
        self._pelit = {
            "a": lambda: KPSPelaajaVsPelaaja(Tuomari()),
            "b": lambda: KPSTekoaly(Tuomari(), Tekoaly()),
            "c": lambda: KPSTekoaly(Tuomari(), TekoalyParannettu(10))
            }
    def nayta(self):
        while True:
            self._peli_valikko()
            vastaus = input()
            print("Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s")
            if vastaus in self._pelit:
                peli = self._pelit[vastaus]()
                peli.pelaa()
            else:
                break

    def _peli_valikko(self):
        print("Valitse pelataanko"
                "\n (a) Ihmistä vastaan"
                "\n (b) Tekoälyä vastaan"
                "\n (c) Parannettua tekoälyä vastaan"
                "\nMuilla valinnoilla lopetetaan"
                )