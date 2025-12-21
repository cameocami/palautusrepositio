from flask import Flask, render_template, request, session, redirect, url_for
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from peli_palvelu import PeliPalvelu, PeliTehdas
from viesti_muotoilija import ViestiMuotoilija

app = Flask(__name__)
app.secret_key = 'kivi-paperi-sakset-secret-key-2025'

# Globaali peli-instanssi (yksinkertainen ratkaisu yhdelle käyttäjälle)
_peli_palvelu = PeliPalvelu(PeliTehdas())

def hae_peli_palvelu():
    """Palauttaa globaalin peli-palvelun"""
    return _peli_palvelu

def kasittele_pelaaja_siirto(ekan_siirto, peli_palvelu):
    """Käsittelee pelaaja vs pelaaja -siirron"""
    tokan_siirto = request.form.get('tokan_siirto')
    if tokan_siirto not in ['k', 'p', 's']:
        session['viesti'] = ViestiMuotoilija.muotoile_virheviesti('invalid_opponent_move')
        return None
    return peli_palvelu.pelaa_kierros(ekan_siirto, tokan_siirto)

def kasittele_tekoaly_siirto(ekan_siirto, peli_palvelu):
    """Käsittelee pelaaja vs tekoäly -siirron"""
    peli_palvelu.tallenna_siirto_tekoalylle(ekan_siirto)
    return peli_palvelu.pelaa_kierros(ekan_siirto)

@app.route('/')
def index():
    """Etusivu - valitse pelityyppi"""
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    """Aloita peli"""
    peli_palvelu = hae_peli_palvelu()
    pelityyppi = request.form.get('pelityyppi')
    session['pelityyppi'] = pelityyppi
    peli_palvelu.alusta_peli(pelityyppi)
    return redirect(url_for('game'))

@app.route('/game')
def game():
    """Pelisivu"""
    if 'pelityyppi' not in session:
        return redirect(url_for('index'))
    
    peli_palvelu = hae_peli_palvelu()
    if not peli_palvelu.onko_alustettu():
        session.clear()
        return redirect(url_for('index'))
    
    pelityyppi = session['pelityyppi']
    viesti = session.pop('viesti', None)
    peli_paattynyt = peli_palvelu.onko_peli_paattynyt()
    voittaja = peli_palvelu.hae_voittaja() if peli_paattynyt else None
    
    return render_template('game.html', 
                         pelityyppi=pelityyppi,
                         tuomari=peli_palvelu.hae_pisteet(),
                         kierros=peli_palvelu.hae_kierrosten_maara(),
                         viesti=viesti,
                         peli_paattynyt=peli_paattynyt,
                         voittaja=voittaja)

@app.route('/play', methods=['POST'])
def play():
    """Pelaa kierros"""
    peli_palvelu = hae_peli_palvelu()
    
    if 'pelityyppi' not in session or not peli_palvelu.onko_alustettu():
        return redirect(url_for('index'))
    
    # Tarkista onko peli jo päättynyt
    if peli_palvelu.onko_peli_paattynyt():
        return redirect(url_for('game'))
    
    pelityyppi = session['pelityyppi']
    ekan_siirto = request.form.get('siirto')
    
    # Validoi ensimmäisen pelaajan siirto
    if ekan_siirto not in ['k', 'p', 's']:
        session['viesti'] = ViestiMuotoilija.muotoile_virheviesti('invalid_move')
        return redirect(url_for('game'))
    
    # Käsittelyt pelityypin mukaan
    kasittelyt = {
        'pelaaja': lambda: kasittele_pelaaja_siirto(ekan_siirto, peli_palvelu),
        'tekoaly': lambda: kasittele_tekoaly_siirto(ekan_siirto, peli_palvelu),
        'parannettu': lambda: kasittele_tekoaly_siirto(ekan_siirto, peli_palvelu)
    }
    
    kasittely_tulos = kasittelyt.get(pelityyppi, lambda: None)()
    if kasittely_tulos is None:
        session.modified = True
        return redirect(url_for('game'))
    
    tulos, tokan_siirto = kasittely_tulos
    
    # Muotoile viesti
    viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
        peli_palvelu.hae_kierrosten_maara(),
        ekan_siirto,
        tokan_siirto,
        tulos,
        pelityyppi
    )
    
    session['viesti'] = viesti
    session.modified = True
    
    return redirect(url_for('game'))

@app.route('/reset')
def reset():
    """Nollaa peli"""
    peli_palvelu = hae_peli_palvelu()
    peli_palvelu.nollaa()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
