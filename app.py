"""Module defining the flask app."""
from flask import Flask, jsonify, request
from dateutil.parser import isoparse
from datetime import datetime, timezone
import math


def calculate_delivery_fee(cart_value: int, delivery_distance: int,
                           number_of_items: int, hour: int) -> int:
  """Calculates the delivery fee according to the parameters.

    Args:
      cart_value: Value of the shopping cart in cents.
        e.g. 790 (790 cents = 7.90€)
      delivery_distance: The distance between the store and customer's
        location in meters. e.g. 2235 (2235 meters = 2.235 km)
      number_of_items: The number of items in the customer's shopping cart.
        e.g. 4 (customer has 4 items in the cart)
      hour: Order hour in UTC. e.g. 16 (4 PM UTC)

    Returns:
      The calculated delivery fee.
  """
  # The delivery is free (0€) when the cart value is equal or more than 100€.
  if cart_value >= 10000:
    return 0

  # A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery
  # distance is longer than that, 1€ is added for every additional 500
  # meters that the courier needs to travel before reaching the destination.
  # Even if the distance would be shorter than 500 meters, the minimum fee
  # is always 1€.
  delivery_fee = 200 + \
      math.ceil((delivery_distance - 1000) / 500) * \
      100 if delivery_distance > 1000 else 200

  # If the cart value is less than 10€, a small order surcharge
  # is added to the delivery price. The surcharge is the difference
  # between the cart value and 10€. For example if the cart value is
  # 8.90€, the surcharge will be 1.10€.
  delivery_fee += 1000 - cart_value if cart_value < 1000 else 0

  # If the number of items is five or more, an additional 50 cent surcharge is
  # added for each item above five. An extra "bulk" fee applies for more than
  # 12 items of 1,20€
  delivery_fee += (number_of_items - 4) * 50 if number_of_items > 4 else 0
  delivery_fee += 120 if number_of_items > 12 else 0

  # During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee
  # including possible surcharges) will be multiplied by 1.2x. However,
  # the fee still cannot be more than the max (15€).
  delivery_fee *= 1.2 if 15 <= hour <= 18 else 1

  # The delivery fee can never be more than 15€, including possible surcharges.
  delivery_fee = 1500 if delivery_fee > 1500 else delivery_fee
  return int(delivery_fee)


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

    return jsonify({
        'delivery_fee':
            calculate_delivery_fee(body['cart_value'],
                                   body['delivery_distance'],
                                   body['number_of_items'], time.hour)
    }), 200

  return app
