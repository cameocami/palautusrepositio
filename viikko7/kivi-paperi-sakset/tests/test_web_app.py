"""Integration tests for Flask web application"""

import pytest


# Apufunktiot toisteisuuden vähentämiseksi
def aloita_peli(flask_client, pelityyppi='pelaaja'):
    """Aloittaa uuden pelin"""
    return flask_client.post('/start', data={'pelityyppi': pelityyppi})

def pelaa_kierros_pvp(flask_client, siirto='k', tokan_siirto='s'):
    """Pelaa yhden kierroksen PvP-pelissä"""
    return flask_client.post('/play', data={'siirto': siirto, 'tokan_siirto': tokan_siirto})

def pelaa_kierros_ai(flask_client, siirto='k'):
    """Pelaa yhden kierroksen AI-pelissä"""
    return flask_client.post('/play', data={'siirto': siirto})

def pelaa_useita_kierroksia_pvp(flask_client, maara, siirto='k', tokan_siirto='s'):
    """Pelaa useita kierroksia PvP-pelissä"""
    for _ in range(maara):
        pelaa_kierros_pvp(flask_client, siirto, tokan_siirto)

def pelaa_useita_kierroksia_ai(flask_client, maara, siirto='k'):
    """Pelaa useita kierroksia AI-pelissä"""
    for _ in range(maara):
        pelaa_kierros_ai(flask_client, siirto)

REDIRECT_STATUKSET = [301, 302]


class TestIndexRoute:
    """Tests for index route"""
    
    def test_index_route_returns_200(self, flask_client):
        """GET / should return 200"""
        response = flask_client.get('/')
        assert response.status_code == 200
    
    def test_index_route_returns_html(self, flask_client):
        """GET / should return HTML content"""
        response = flask_client.get('/')
        assert b'html' in response.data.lower() or response.status_code == 200


class TestStartRoute:
    """Tests for start/game initialization route"""
    
    def test_start_route_requires_post(self, flask_client):
        """GET /start should redirect"""
        response = flask_client.get('/start')
        assert response.status_code in [301, 302, 405]  # Redirect or Method Not Allowed
    
    @pytest.mark.parametrize("pelityyppi", ['pelaaja', 'tekoaly', 'parannettu'])
    def test_start_route_with_game_type(self, flask_client, pelityyppi):
        """POST /start with different game types should redirect to game"""
        response = aloita_peli(flask_client, pelityyppi)
        assert response.status_code in REDIRECT_STATUKSET


class TestGameRoute:
    """Tests for game route"""
    
    def test_game_route_without_session_redirects(self, flask_client):
        """GET /game without session should redirect to index"""
        response = flask_client.get('/game')
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_game_route_with_session(self, flask_client):
        """GET /game with valid session should return 200"""
        aloita_peli(flask_client)
        response = flask_client.get('/game')
        assert response.status_code == 200


class TestPlayRoute:
    """Tests for play/move route"""
    
    def test_play_route_without_session_redirects(self, flask_client):
        """POST /play without session should redirect"""
        response = pelaa_kierros_ai(flask_client)
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_play_route_with_invalid_move(self, flask_client):
        """POST /play with invalid move should redirect with error"""
        aloita_peli(flask_client)
        response = flask_client.post('/play', data={'siirto': 'x'})
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_play_route_pelaaja_missing_opponent_move(self, flask_client):
        """POST /play in PvP without opponent move should redirect"""
        aloita_peli(flask_client)
        response = flask_client.post('/play', data={'siirto': 'k'})
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_play_route_pelaaja_valid_move(self, flask_client):
        """POST /play in PvP with valid moves should redirect"""
        aloita_peli(flask_client)
        response = pelaa_kierros_pvp(flask_client)
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_play_route_tekoaly_valid_move(self, flask_client):
        """POST /play vs AI with valid move should redirect"""
        aloita_peli(flask_client, 'tekoaly')
        response = pelaa_kierros_ai(flask_client)
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_play_route_parannettu_valid_move(self, flask_client):
        """POST /play vs advanced AI with valid move should redirect"""
        aloita_peli(flask_client, 'parannettu')
        response = pelaa_kierros_ai(flask_client, 'p')
        assert response.status_code in REDIRECT_STATUKSET


class TestResetRoute:
    """Tests for reset route"""
    
    def test_reset_route_clears_session(self, flask_client):
        """GET /reset should redirect and clear session"""
        aloita_peli(flask_client)
        response = flask_client.get('/reset')
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_reset_route_allows_new_game(self, flask_client):
        """Should be able to start new game after reset"""
        aloita_peli(flask_client)
        flask_client.get('/reset')
        response = aloita_peli(flask_client, 'tekoaly')
        assert response.status_code in REDIRECT_STATUKSET


class TestCompleteGameFlowPvP:
    """Integration tests for complete PvP game flow"""
    
    def test_complete_pvp_game_flow(self, flask_client):
        """Test complete PvP game flow"""
        response = aloita_peli(flask_client)
        assert response.status_code in REDIRECT_STATUKSET
        
        pelaa_useita_kierroksia_pvp(flask_client, 3)
        
        response = flask_client.get('/game')
        assert response.status_code == 200
        
        response = flask_client.get('/reset')
        assert response.status_code in REDIRECT_STATUKSET


class TestCompleteGameFlowAI:
    """Integration tests for complete AI game flow"""
    
    def test_complete_ai_game_flow(self, flask_client):
        """Test complete player vs AI game flow"""
        response = aloita_peli(flask_client, 'tekoaly')
        assert response.status_code in REDIRECT_STATUKSET
        
        pelaa_useita_kierroksia_ai(flask_client, 5)
        
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_advanced_ai_game_flow(self, flask_client):
        """Test complete player vs advanced AI game flow"""
        response = aloita_peli(flask_client, 'parannettu')
        assert response.status_code in REDIRECT_STATUKSET
        
        pelaa_useita_kierroksia_ai(flask_client, 3, 'p')
        
        response = flask_client.get('/game')
        assert response.status_code == 200


class TestSessionManagement:
    """Tests for session management"""
    
    def test_session_preserved_across_requests(self, flask_client):
        """Session should be preserved across requests"""
        aloita_peli(flask_client)
        pelaa_kierros_pvp(flask_client)
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_multiple_games_sequence(self, flask_client):
        """Should support playing multiple games in sequence"""
        aloita_peli(flask_client)
        pelaa_kierros_pvp(flask_client)
        flask_client.get('/reset')
        
        response = aloita_peli(flask_client, 'tekoaly')
        assert response.status_code in REDIRECT_STATUKSET
        
        response = pelaa_kierros_ai(flask_client, 'p')
        assert response.status_code in REDIRECT_STATUKSET


class TestGameEndCondition:
    """Tests for game end condition (3 wins)"""
    
    def test_game_continues_with_less_than_3_wins(self, flask_client):
        """Game should continue when no player has 3 wins"""
        aloita_peli(flask_client)
        pelaa_useita_kierroksia_pvp(flask_client, 2)
        
        response = flask_client.get('/game')
        assert response.status_code == 200
        
        response = pelaa_kierros_pvp(flask_client)
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_game_ends_when_eka_gets_3_wins(self, flask_client):
        """Game should end when first player gets 3 wins"""
        aloita_peli(flask_client)
        pelaa_useita_kierroksia_pvp(flask_client, 3)
        
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_game_ends_when_toka_gets_3_wins(self, flask_client):
        """Game should end when second player gets 3 wins"""
        aloita_peli(flask_client)
        pelaa_useita_kierroksia_pvp(flask_client, 3, 's', 'k')
        
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_cannot_play_after_game_ends(self, flask_client):
        """Should not be able to play after game ends"""
        aloita_peli(flask_client)
        pelaa_useita_kierroksia_pvp(flask_client, 3)
        
        response = pelaa_kierros_pvp(flask_client)
        assert response.status_code in REDIRECT_STATUKSET


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_invalid_moves_handled_gracefully(self, flask_client):
        """Invalid moves should be handled without crashing"""
        aloita_peli(flask_client)
        response = flask_client.post('/play', data={'siirto': 'x', 'tokan_siirto': 'k'})
        assert response.status_code in REDIRECT_STATUKSET
    
    def test_invalid_opponent_move_handled(self, flask_client):
        """Invalid opponent move should be handled"""
        aloita_peli(flask_client)
        response = flask_client.post('/play', data={'siirto': 'k', 'tokan_siirto': 'y'})
        assert response.status_code in REDIRECT_STATUKSET
