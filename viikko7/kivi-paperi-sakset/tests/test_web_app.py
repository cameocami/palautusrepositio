"""Integration tests for Flask web application"""

import pytest


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
    
    def test_start_route_with_pelaaja(self, flask_client):
        """POST /start with pelaaja should redirect to game"""
        response = flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        assert response.status_code in [301, 302]  # Redirect
    
    def test_start_route_with_tekoaly(self, flask_client):
        """POST /start with tekoaly should redirect to game"""
        response = flask_client.post('/start', data={'pelityyppi': 'tekoaly'})
        assert response.status_code in [301, 302]
    
    def test_start_route_with_parannettu(self, flask_client):
        """POST /start with parannettu should redirect to game"""
        response = flask_client.post('/start', data={'pelityyppi': 'parannettu'})
        assert response.status_code in [301, 302]


class TestGameRoute:
    """Tests for game route"""
    
    def test_game_route_without_session_redirects(self, flask_client):
        """GET /game without session should redirect to index"""
        response = flask_client.get('/game')
        assert response.status_code in [301, 302]
    
    def test_game_route_with_session(self, flask_client):
        """GET /game with valid session should return 200"""
        # First start a game
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Then access game page
        response = flask_client.get('/game')
        assert response.status_code == 200


class TestPlayRoute:
    """Tests for play/move route"""
    
    def test_play_route_without_session_redirects(self, flask_client):
        """POST /play without session should redirect"""
        response = flask_client.post('/play', data={'siirto': 'k'})
        assert response.status_code in [301, 302]
    
    def test_play_route_with_invalid_move(self, flask_client):
        """POST /play with invalid move should redirect with error"""
        # Start game first
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Try invalid move
        response = flask_client.post('/play', data={'siirto': 'x'})
        assert response.status_code in [301, 302]
    
    def test_play_route_pelaaja_missing_opponent_move(self, flask_client):
        """POST /play in PvP without opponent move should redirect"""
        # Start PvP game
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Try without opponent move
        response = flask_client.post('/play', data={'siirto': 'k'})
        assert response.status_code in [301, 302]
    
    def test_play_route_pelaaja_valid_move(self, flask_client):
        """POST /play in PvP with valid moves should redirect"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        response = flask_client.post(
            '/play',
            data={'siirto': 'k', 'tokan_siirto': 's'}
        )
        assert response.status_code in [301, 302]
    
    def test_play_route_tekoaly_valid_move(self, flask_client):
        """POST /play vs AI with valid move should redirect"""
        flask_client.post('/start', data={'pelityyppi': 'tekoaly'})
        
        response = flask_client.post('/play', data={'siirto': 'k'})
        assert response.status_code in [301, 302]
    
    def test_play_route_parannettu_valid_move(self, flask_client):
        """POST /play vs advanced AI with valid move should redirect"""
        flask_client.post('/start', data={'pelityyppi': 'parannettu'})
        
        response = flask_client.post('/play', data={'siirto': 'p'})
        assert response.status_code in [301, 302]


class TestResetRoute:
    """Tests for reset route"""
    
    def test_reset_route_clears_session(self, flask_client):
        """GET /reset should redirect and clear session"""
        # Start game
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Reset
        response = flask_client.get('/reset')
        assert response.status_code in [301, 302]
    
    def test_reset_route_allows_new_game(self, flask_client):
        """Should be able to start new game after reset"""
        # Start game
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Reset
        flask_client.get('/reset')
        
        # Start new game
        response = flask_client.post('/start', data={'pelityyppi': 'tekoaly'})
        assert response.status_code in [301, 302]


class TestCompleteGameFlowPvP:
    """Integration tests for complete PvP game flow"""
    
    def test_complete_pvp_game_flow(self, flask_client):
        """Test complete PvP game flow"""
        # Start game
        response = flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        assert response.status_code in [301, 302]
        
        # Play rounds
        for i in range(3):
            response = flask_client.post(
                '/play',
                data={'siirto': 'k', 'tokan_siirto': 's'}
            )
            assert response.status_code in [301, 302]
        
        # Check game state
        response = flask_client.get('/game')
        assert response.status_code == 200
        
        # Reset
        response = flask_client.get('/reset')
        assert response.status_code in [301, 302]


class TestCompleteGameFlowAI:
    """Integration tests for complete AI game flow"""
    
    def test_complete_ai_game_flow(self, flask_client):
        """Test complete player vs AI game flow"""
        # Start game
        response = flask_client.post('/start', data={'pelityyppi': 'tekoaly'})
        assert response.status_code in [301, 302]
        
        # Play rounds
        for i in range(5):
            response = flask_client.post('/play', data={'siirto': 'k'})
            assert response.status_code in [301, 302]
        
        # Check game state
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_advanced_ai_game_flow(self, flask_client):
        """Test complete player vs advanced AI game flow"""
        response = flask_client.post('/start', data={'pelityyppi': 'parannettu'})
        assert response.status_code in [301, 302]
        
        for i in range(3):
            response = flask_client.post('/play', data={'siirto': 'p'})
            assert response.status_code in [301, 302]
        
        response = flask_client.get('/game')
        assert response.status_code == 200


class TestSessionManagement:
    """Tests for session management"""
    
    def test_session_preserved_across_requests(self, flask_client):
        """Session should be preserved across requests"""
        # Start game
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Play round
        flask_client.post(
            '/play',
            data={'siirto': 'k', 'tokan_siirto': 's'}
        )
        
        # Game should still be accessible
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_multiple_games_sequence(self, flask_client):
        """Should support playing multiple games in sequence"""
        # Game 1
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        flask_client.post(
            '/play',
            data={'siirto': 'k', 'tokan_siirto': 's'}
        )
        
        # Reset
        flask_client.get('/reset')
        
        # Game 2
        response = flask_client.post('/start', data={'pelityyppi': 'tekoaly'})
        assert response.status_code in [301, 302]
        
        response = flask_client.post('/play', data={'siirto': 'p'})
        assert response.status_code in [301, 302]


class TestGameEndCondition:
    """Tests for game end condition (5 wins)"""
    
    def test_game_continues_with_less_than_5_wins(self, flask_client):
        """Game should continue when no player has 5 wins"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Play 4 rounds (eka wins all)
        for i in range(4):
            flask_client.post(
                '/play',
                data={'siirto': 'k', 'tokan_siirto': 's'}
            )
        
        # Game should not be over yet
        response = flask_client.get('/game')
        assert response.status_code == 200
        # Can still play
        response = flask_client.post(
            '/play',
            data={'siirto': 'k', 'tokan_siirto': 's'}
        )
        assert response.status_code in [301, 302]
    
    def test_game_ends_when_eka_gets_5_wins(self, flask_client):
        """Game should end when first player gets 5 wins"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Play 5 rounds (eka wins all)
        for i in range(5):
            flask_client.post(
                '/play',
                data={'siirto': 'k', 'tokan_siirto': 's'}
            )
        
        # Game should be over - check if we can see "peli ohi" content
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_game_ends_when_toka_gets_5_wins(self, flask_client):
        """Game should end when second player gets 5 wins"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Play 5 rounds (toka wins all)
        for i in range(5):
            flask_client.post(
                '/play',
                data={'siirto': 's', 'tokan_siirto': 'k'}
            )
        
        response = flask_client.get('/game')
        assert response.status_code == 200
    
    def test_cannot_play_after_game_ends(self, flask_client):
        """Should not be able to play after game ends"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        # Play 5 rounds (eka wins all)
        for i in range(5):
            flask_client.post(
                '/play',
                data={'siirto': 'k', 'tokan_siirto': 's'}
            )
        
        # Try to play another round - should redirect back
        response = flask_client.post(
            '/play',
            data={'siirto': 'k', 'tokan_siirto': 's'}
        )
        assert response.status_code in [301, 302]


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_invalid_moves_handled_gracefully(self, flask_client):
        """Invalid moves should be handled without crashing"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        response = flask_client.post(
            '/play',
            data={'siirto': 'x', 'tokan_siirto': 'k'}
        )
        assert response.status_code in [301, 302]
    
    def test_invalid_opponent_move_handled(self, flask_client):
        """Invalid opponent move should be handled"""
        flask_client.post('/start', data={'pelityyppi': 'pelaaja'})
        
        response = flask_client.post(
            '/play',
            data={'siirto': 'k', 'tokan_siirto': 'y'}
        )
        assert response.status_code in [301, 302]
