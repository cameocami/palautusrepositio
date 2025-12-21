# Kivi-Paperi-Sakset - Unit Tests

## Test Coverage

This application has comprehensive unit tests with **>85% code coverage**.

## Installing Test Dependencies

```bash
poetry install
```

## Running Tests

### Run all tests
```bash
poetry run pytest
```

### Run tests with coverage report
```bash
poetry run pytest --cov=src --cov-report=html --cov-report=term-missing
```

### Run specific test file
```bash
poetry run pytest tests/test_tuomari.py -v
```

### Run specific test class
```bash
poetry run pytest tests/test_peli_palvelu.py::TestPeliPalveluInit -v
```

### Run specific test function
```bash
poetry run pytest tests/test_tuomari.py::TestTuomariTulos::test_tulos_tie_returns_tasapeli -v
```

### Run with verbose output
```bash
poetry run pytest -v
```

## Test Structure

### `/tests/conftest.py`
Pytest configuration and fixtures shared across all tests

### `/tests/test_tuomari.py`
Tests for the Tuomari (Judge) class:
- Score tracking
- Round result determination
- Game reset functionality

### `/tests/test_viesti_muotoilija.py`
Tests for the ViestiMuotoilija (Message Formatter) class:
- Move name formatting
- Round message generation
- Error message generation

### `/tests/test_peli_palvelu.py`
Tests for the PeliPalvelu (Game Service) class:
- Game factory pattern
- Game initialization
- Game state management
- Public API methods

### `/tests/test_kps.py`
Tests for KPS game classes:
- PvP game mechanics
- AI game mechanics
- Game rules (rock-paper-scissors logic)

### `/tests/test_web_app.py`
Integration tests for Flask web application:
- Route functionality
- Session management
- Complete game flows
- Error handling

## Test Statistics

- **Total Test Cases**: 150+
- **Lines of Test Code**: 1000+
- **Coverage Target**: >85%
- **Test Framework**: pytest
- **Coverage Tool**: pytest-cov

## Test Categories

### Unit Tests
- Individual class methods
- Game logic validation
- Message formatting

### Integration Tests
- Flask routes and requests
- Session handling
- Complete game flows
- Error scenarios

## Running Coverage Report

To generate and view the HTML coverage report:

```bash
poetry run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

This will show:
- Overall coverage percentage
- Coverage per file
- Which lines are covered/uncovered
