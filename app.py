from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder="static", template_folder="templates")

MAX_INPUT_LENGTH = 100
MAX_ABS_VALUE = Decimal("1e100")
MAX_PRECISION = 10


def decimal_str(value: Decimal) -> str:
    """Return a non-exponential decimal string without unnecessary trailing zeros."""
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def parse_decimal(value, field_name: str) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{field_name} must be a finite number.")
    text = str(value).strip()
    if not text or len(text) > MAX_INPUT_LENGTH:
        raise ValueError(f"{field_name} must contain 1–{MAX_INPUT_LENGTH} characters.")
    try:
        number = Decimal(text)
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} must be a valid number.") from None
    if not number.is_finite():
        raise ValueError(f"{field_name} must be a finite number.")
    if abs(number) > MAX_ABS_VALUE:
        raise ValueError("Numbers must have an absolute value no greater than 1e100.")
    return number


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    try:
        original = parse_decimal(data.get("number"), "number")
        divisor = parse_decimal(data.get("divisor"), "divisor")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if divisor == 0:
        return jsonify({"error": "Divisor cannot be zero."}), 400

    raw_precision = data.get("precision", 1)
    if isinstance(raw_precision, bool):
        return jsonify({"error": "precision must be an integer from 0 to 10."}), 400
    try:
        precision = int(raw_precision)
        if str(raw_precision).strip() not in (str(precision), f"+{precision}"):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "precision must be an integer from 0 to 10."}), 400
    if not 0 <= precision <= MAX_PRECISION:
        return jsonify({"error": "precision must be between 0 and 10."}), 400

    try:
        with localcontext() as ctx:
            ctx.prec = 120
            exact = original / divisor
            quantum = Decimal("1") if precision == 0 else Decimal("1." + ("0" * precision))
            display = exact.quantize(quantum, rounding=ROUND_HALF_UP)
            reverse_from_display = display * divisor
            precision_diff = original - reverse_from_display
            recovered = exact * divisor
    except (InvalidOperation, ArithmeticError, ValueError):
        return jsonify({"error": "These values are outside the supported calculation range."}), 400

    response = {
        "original": decimal_str(original),
        "divisor": decimal_str(divisor),
        "exact_result": decimal_str(exact),
        "display_result": decimal_str(display),
        "reverse_result_from_display": decimal_str(reverse_from_display),
        "precision_difference": decimal_str(precision_diff),
        "recovered_result": decimal_str(recovered),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return jsonify(response)


if __name__ == "__main__":
    debug_enabled = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(debug=debug_enabled, port=5000)
