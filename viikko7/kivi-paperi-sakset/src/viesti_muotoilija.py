"""
ViestiMuotoilija - Käsittelee viestien muotoilun ja lokalisoinnin
Erottaa esityslogiikan liiketoimintalogiikasta
"""


class ViestiMuotoilija:
    """Muotoilee pelin viestit näyttöä varten"""
    
    SIIRTOJEN_NIMET = {
        'k': 'Kivi',
        'p': 'Paperi',
        's': 'Sakset'
    }
    
    TULOS_VIESTIT = {
        'tasapeli': 'Tasapeli!',
        'ekan_voitto': 'Pelaaja 1 voitti!',
        'tokan_voitto': None  # Asetetaan dynaamisesti pelityypin mukaan
    }
    
    @staticmethod
    def muotoile_siirron_nimi(siirto):
        """Muuntaa siirron lyhenteen ihmisluettavaksi nimeksi"""
        return ViestiMuotoilija.SIIRTOJEN_NIMET.get(siirto, siirto)
    
    @staticmethod
    def muotoile_kierroksen_viesti(kierros, ekan_siirto, tokan_siirto, tulos, pelityyppi):
        """Muotoilee kierroksen tuloksen viestin
        
        Args:
            kierros: Kierroksen numero
            ekan_siirto: Ensimmäisen pelaajan siirto
            tokan_siirto: Toisen pelaajan siirto
            tulos: Kierroksen tulos ('tasapeli', 'ekan_voitto', 'tokan_voitto')
            pelityyppi: Pelin tyyppi ('pelaaja', 'tekoaly', 'parannettu')
        
        Returns:
            Muotoiltu viesti
        """
        # Määritä voittajaviesti pelin tyypin mukaan
        tulos_tekstit = {
            'tasapeli': 'Tasapeli!',
            'ekan_voitto': 'Pelaaja 1 voitti!',
            'tokan_voitto': 'Pelaaja 2 voitti!' if pelityyppi == 'pelaaja' else 'Tietokone voitti!'
        }
        
        eka_nimi = ViestiMuotoilija.muotoile_siirron_nimi(ekan_siirto)
        toka_nimi = ViestiMuotoilija.muotoile_siirron_nimi(tokan_siirto)
        
        viesti = f"Kierros {kierros}: "
        viesti += f"Pelaaja 1: {eka_nimi}"
        
        if pelityyppi == 'pelaaja':
            viesti += f", Pelaaja 2: {toka_nimi}"
        else:
            viesti += f", Tietokone: {toka_nimi}"
        
        viesti += f" - {tulos_tekstit[tulos]}"
        
        return viesti
    
    @staticmethod
    def muotoile_virheviesti(virhe_tyyppi):
        """Muotoilee virheviestin
        
        Args:
            virhe_tyyppi: Virheen tyyppi
        
        Returns:
            Muotoiltu virheviesti
        """
        virhe_viestit = {
            'invalid_move': 'Virheellinen siirto! Valitse k, p tai s.',
            'invalid_opponent_move': 'Virheellinen siirto toiselta pelaajalta! Valitse k, p tai s.',
            'no_game': 'Peliä ei ole alustettu. Aloita uusi peli.',
        }
        
        return virhe_viestit.get(virhe_tyyppi, 'Virhe tapahtui!')
