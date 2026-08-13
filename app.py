from decimal import Decimal, localcontext, ROUND_HALF_UP
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')


def decimal_str(d: Decimal) -> str:
    # Normalize and remove trailing zeros while keeping at least one decimal if needed
    try:
        s = format(d.normalize(), 'f')
    except Exception:
        s = str(d)
    return s


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    try:
        original = Decimal(str(data.get('number', '')))
        divisor = Decimal(str(data.get('divisor', '')))
    except Exception:
        return jsonify({'error': 'Invalid number or divisor'}), 400

    if divisor == 0:
        return jsonify({'error': 'Divisor cannot be zero'}), 400

    # Requested display precision (number of decimal places)
    try:
        precision = int(data.get('precision', 1))
    except Exception:
        precision = 1
    if precision < 0:
        precision = 0

    # Use high precision context to generate a long exact result string
    with localcontext() as ctx:
        ctx.prec = 60
        exact = original / divisor

    # Build exact_result string with many digits (trim trailing zeros where appropriate)
    exact_result = decimal_str(exact)

    # Prepare quantize format for display rounding
    if precision > 0:
        q_str = '1.' + ('0' * precision)
    else:
        q_str = '1'
    q = Decimal(q_str)

    # Displayed (rounded) value
    display = exact.quantize(q, rounding=ROUND_HALF_UP)

    # Reverse calculation using displayed value
    reverse_from_display = (display * divisor).normalize()

    # Precision difference (original - reverse_from_display)
    precision_diff = (original - reverse_from_display).normalize()

    # Exact recovery using the high-precision exact value
    with localcontext() as ctx:
        ctx.prec = 60
        recovered = (exact * divisor).normalize()

    response = {
        'original': decimal_str(original),
        'divisor': decimal_str(divisor),
        'exact_result': exact_result,
        'display_result': decimal_str(display),
        'reverse_result_from_display': decimal_str(reverse_from_display),
        'precision_difference': decimal_str(precision_diff),
        'recovered_result': decimal_str(recovered),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
