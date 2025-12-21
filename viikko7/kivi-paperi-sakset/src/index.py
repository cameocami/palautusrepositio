from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari


def main():
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()
        print(
                "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
            )
        if vastaus.endswith("a"):
            kaksinpeli = KPSPelaajaVsPelaaja(Tuomari())
            kaksinpeli.pelaa()
        elif vastaus.endswith("b"):
            yksinpeli = KPSTekoaly(Tuomari(), Tekoaly())
            yksinpeli.pelaa()
        elif vastaus.endswith("c"):
            haastava_yksinpeli = KPSTekoaly(Tuomari(), TekoalyParannettu(10))
            haastava_yksinpeli.pelaa()
        else:
            break


if __name__ == "__main__":
    main()
