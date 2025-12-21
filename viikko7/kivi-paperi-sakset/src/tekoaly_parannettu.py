# "Muistava tekoäly"
class TekoalyParannettu:
    def __init__(self, muistin_koko):
        self._muisti = [None] * muistin_koko
        self._vapaa_muisti_indeksi = 0
        self._voittotaulukko = { "k": "p", "p": "s", "s": "k" } # kivi -> paperi, paperi -> sakset, sakset -> kivi

    def aseta_siirto(self, siirto):
        # jos muisti täyttyy, unohdetaan viimeinen alkio
        if self._vapaa_muisti_indeksi == len(self._muisti):
            for i in range(1, len(self._muisti)):
                self._muisti[i - 1] = self._muisti[i]

            self._vapaa_muisti_indeksi = self._vapaa_muisti_indeksi - 1

        self._muisti[self._vapaa_muisti_indeksi] = siirto
        self._vapaa_muisti_indeksi = self._vapaa_muisti_indeksi + 1

    def anna_siirto(self):
        if self._vapaa_muisti_indeksi < 2:
            return "k"

        viimeisin_siirto = self._muisti[self._vapaa_muisti_indeksi - 1]

        yleisin = self._laske_yleisin_seuraava_siirto(viimeisin_siirto)

        # Tehdään siirron valinta esimerkiksi seuraavasti;
        # - jos kiviä eniten, annetaan aina paperi
        # - jos papereita eniten, annetaan aina sakset
        # muulloin annetaan aina kivi

        return self._voittotaulukko[yleisin]

        # Tehokkaampiakin tapoja löytyy, mutta niistä lisää
        # Johdatus Tekoälyyn kurssilla!

    def _laske_yleisin_seuraava_siirto(self, siirto):
        maarat = {"k": 0, "p": 0, "s": 0}

        for i in range(0, self._vapaa_muisti_indeksi - 1):
            if siirto == self._muisti[i]:
                seuraava = self._muisti[i + 1]
                maarat[seuraava] += 1

        yleisin = max(maarat, key=maarat.get)

        return yleisin
