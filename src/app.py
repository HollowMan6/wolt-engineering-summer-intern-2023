"""Module defining the flask app."""
from flask import Flask, jsonify, request
from dateutil.parser import isoparse
from datetime import datetime, timezone
from deps.calculator.calculator import Calculator


def create_app():
  """Application factory."""

  app = Flask(__name__)

  @app.route('/', methods=['POST'])
  def _():
    """The endpoint for calculating the delivery fee."""
    body = request.get_json()

    # Check if the request body is valid
    if not body:
      return jsonify({'error': 'Invalid request body'}), 400

    # Check if the required parameters are present and valid (integers > 0)
    for key in ['cart_value', 'delivery_distance', 'number_of_items']:
      if key not in body:
        return jsonify({'error': f'Missing parameter: {key}'}), 422
      if not isinstance(body[key], int) or body[key] <= 0:
        return jsonify({'error': f'Invalid parameter: {key}'}), 422

    time = datetime.now(timezone.utc)
    # Check if the time parameter is present
    if 'time' not in body:
      return jsonify({'error': 'Missing parameter: time'}), 422
    # Check if the time parameter string is correctly formatted in ISO 8601
    try:
      # Check if the time parameter is a string
      if not isinstance(body['time'], str):
        raise ValueError
      # Parse and convert the time to UTC
      body_time = isoparse(body['time']).replace(tzinfo=timezone.utc)
      # Check if the time is in the past instead of a future time
      if body_time > time:
        raise ValueError
      time = body_time
    except ValueError:
      return jsonify({'error': 'Invalid parameter: time'}), 422

    calculator = Calculator()
    return jsonify({
        'delivery_fee':
            calculator.calculate_delivery_fee(body['cart_value'],
                                              body['delivery_distance'],
                                              body['number_of_items'],
                                              time.hour)
    }), 200

  return app

if __name__ == '__main__':
  create_app().run()
