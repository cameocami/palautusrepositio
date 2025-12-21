#!/bin/bash
# Quick test runner script for kivi-paperi-sakset

set -e

echo "🧪 Kivi-Paperi-Sakset Test Suite"
echo "=================================="
echo ""

# Install dependencies if needed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry not found. Please install Poetry first."
    exit 1
fi

echo "📦 Installing dependencies..."
poetry install > /dev/null 2>&1 || poetry install

echo "✅ Dependencies installed"
echo ""

# Run tests
echo "🏃 Running tests..."
echo ""

case "${1:-all}" in
    "all")
        poetry run pytest tests/ -v
        ;;
    "quick")
        poetry run pytest tests/ -q
        ;;
    "coverage")
        poetry run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
        echo ""
        echo "📊 HTML coverage report generated in htmlcov/index.html"
        ;;
    "unit")
        poetry run pytest tests/test_tuomari.py tests/test_viesti_muotoilija.py tests/test_peli_palvelu.py tests/test_kps.py -v
        ;;
    "integration")
        poetry run pytest tests/test_web_app.py -v
        ;;
    "judge")
        poetry run pytest tests/test_tuomari.py -v
        ;;
    "formatter")
        poetry run pytest tests/test_viesti_muotoilija.py -v
        ;;
    "service")
        poetry run pytest tests/test_peli_palvelu.py -v
        ;;
    "game")
        poetry run pytest tests/test_kps.py -v
        ;;
    "web")
        poetry run pytest tests/test_web_app.py -v
        ;;
    *)
        echo "Usage: $0 {all|quick|coverage|unit|integration|judge|formatter|service|game|web}"
        echo ""
        echo "Options:"
        echo "  all          - Run all tests with verbose output"
        echo "  quick        - Run all tests with minimal output"
        echo "  coverage     - Run tests and generate coverage report"
        echo "  unit         - Run unit tests only"
        echo "  integration  - Run integration tests only"
        echo "  judge        - Run Tuomari tests"
        echo "  formatter    - Run ViestiMuotoilija tests"
        echo "  service      - Run PeliPalvelu tests"
        echo "  game         - Run KPS game tests"
        echo "  web          - Run Flask web app tests"
        exit 1
        ;;
esac

echo ""
echo "✅ Tests complete!"
