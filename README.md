# PrecisionCalc — Modern Responsive Calculation Application

PrecisionCalc demonstrates division with controlled display precision, reverse calculations, and exact recovery using Python's Decimal for reliable precision handling. The project is lightweight and easy to run locally.

## Requirements

- Python 3.8+
- pip

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
# Then open http://127.0.0.1:5000 in your browser
```

## Project Structure

calculation_app/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js

## Features

- Clean responsive dashboard UI
- Light and dark themes with persistence
- Font selector with persistence
- Calculator that shows exact result, display rounded value, reverse calculation, and precision difference
- Uses Python `Decimal` for exact calculations
- Calculation history stored in `localStorage` with delete and clear options
- Accessible UI and keyboard navigation

## API

POST `/api/calculate` — JSON body:

```json
{
  "number": 100,
  "divisor": 3,
  "precision": 1
}
```

Response includes `exact_result`, `display_result`, `reverse_result_from_display`, `precision_difference`, and `recovered_result`.

## Notes

This app is intentionally small and built with vanilla JavaScript and Flask to be easy to understand and extend.
