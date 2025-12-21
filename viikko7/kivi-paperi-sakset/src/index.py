from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari


def main(tuomari=Tuomari(), tekoaly=Tekoaly(), tekoaly_parannettu=TekoalyParannettu(10)):
    komennot = {
    "a": KPSPelaajaVsPelaaja(tuomari),
    "b": KPSTekoaly(tuomari, tekoaly),
    "c": KPSTekoaly(tuomari, tekoaly_parannettu)
    }
    while True:

        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()

        print("Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s")
        if vastaus in komennot:
            peli = komennot[vastaus]
            peli.pelaa()
        else:
            break


if __name__ == "__main__":
    main()
