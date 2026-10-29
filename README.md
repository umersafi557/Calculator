# PrecisionCalc

A responsive web calculator built with **Python, Flask, and vanilla JavaScript** that explores how rounding affects calculations. It compares a high-precision result with a rounded display value and shows what happens when that displayed value is used in a reverse calculation.

> This project is intended as a learning/demo application, not as a financial or scientific system requiring certified numerical accuracy.

## Features

- Responsive calculator interface
- Division using Python's `Decimal` type
- Configurable display precision and half-up rounding
- Comparison of the calculated result and rounded display value
- Reverse calculation and precision-difference output
- Calculation history saved in browser `localStorage`
- Light/dark theme and font preferences
- Keyboard navigation and input validation

## Tech stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Numerical handling:** Python `decimal.Decimal`

## Getting started

### Requirements

- Python 3.8 or newer
- pip

### 1. Clone the repository

```bash
git clone https://github.com/umersafi557/Calculator.git
cd Calculator
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## API example

The app exposes a `POST /api/calculate` endpoint.

**Request:**

```json
{
  "number": 100,
  "divisor": 3,
  "precision": 2
}
```

**Response fields:**

- `original` — input number
- `divisor` — divisor used
- `exact_result` — division result calculated with a high-precision decimal context
- `display_result` — result rounded to the requested number of decimal places
- `reverse_result_from_display` — rounded result multiplied by the divisor
- `precision_difference` — difference between the original input and reverse calculation
- `recovered_result` — result recovered using the unrounded calculation
- `timestamp` — response timestamp

Example request with curl:

```bash
curl -X POST http://127.0.0.1:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"number":100,"divisor":3,"precision":2}'
```

## Project structure

```text
.
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Learning goals

This project is a practical exercise in building a small Flask application, designing a JSON API, validating input, handling decimal rounding, and connecting a browser interface to a Python backend.

## Ideas for future improvements

- Add automated tests for the API and rounding edge cases
- Add a screenshot or short demo GIF
- Add continuous integration with GitHub Actions
- Improve error messages and document supported input limits

## License

No license is currently specified. Contact the repository owner before reusing this project.
