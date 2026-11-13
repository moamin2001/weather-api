# Weather Summary

A short Python program that calls the OpenWeatherMap current-weather API, parses the JSON response into a small `Weather` class, and prints a formatted summary. The API key is read from a `.env` file.

## Setup

Get a free API key at [openweathermap.org](https://openweathermap.org/api). New keys can take a little while to activate.

### macOS / Linux

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then paste your key into .env
python main.py "Alexandria"
```

### Windows (PowerShell)

```powershell
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then paste your key into .env
python main.py "Alexandria"
```

## Usage

```bash
python main.py [city]
```

The city defaults to Cairo if none is given.

## Files

- `main.py`: the program
- `requirements.txt`: dependencies (`requests`, `python-dotenv`)
- `.env.example`: template for your `.env` file (set `OPENWEATHER_API_KEY`)
