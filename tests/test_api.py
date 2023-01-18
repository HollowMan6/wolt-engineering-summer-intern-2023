"""Module defining the test cases for the api."""
import pytest
import json
import datetime

# Generates the response error JSON string
INVALID_PARAM = {}
MISSING_PARAM = {}
for key in ['cart_value', 'delivery_distance', 'number_of_items', 'time']:
  MISSING_PARAM[key] = json.dumps({'error': f'Missing parameter: {key}'})
  INVALID_PARAM[key] = json.dumps({'error': f'Invalid parameter: {key}'})

# Some default values for testing
DEFAULT_CART_VALUE = 790
DEFAULT_DELIVERY_DISTANCE = 2235
DEFAULT_NUMBER_OF_ITEMS = 4
DEFAULT_TIME = '2021-10-12T13:00:00Z'


def get_delivery_fee(delivery_fee: int) -> str:
  """Generates the response JSON string for delivery_fee.

    Args:
      delivery_fee: The calculated delivery fee.

    Returns:
      The JSON string for delivery_fee.
  """
  return json.dumps({'delivery_fee': delivery_fee})


def get_input_dict(cart_value: int, delivery_distance: int,
                   number_of_items: int, time: str) -> dict:
  """Generates the input dict for server request.

    Args:
      cart_value: Value of the shopping cart in cents.
        e.g. 790 (790 cents = 7.90€)
      delivery_distance: The distance between the store and customer's
        location in meters. e.g. 2235 (2235 meters = 2.235 km)
      number_of_items: The number of items in the customer's shopping cart.
        e.g. 4 (customer has 4 items in the cart)
      time: Order time in ISO format. e.g. 2021-01-16T13:00:00Z

    Returns:
      The input dict for making server request.
  """
  input_dict = {}
  if cart_value:
    input_dict['cart_value'] = cart_value
  if delivery_distance:
    input_dict['delivery_distance'] = delivery_distance
  if number_of_items:
    input_dict['number_of_items'] = number_of_items
  if time:
    input_dict['time'] = time
  return input_dict


@pytest.mark.parametrize(
    ('data', 'result'),
    (
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(710)),
        # The delivery is free (0€) when the cart value is equal
        # or more than 100€.
        (get_input_dict(9999, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(500)),
        (get_input_dict(10000, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(0)),
        (get_input_dict(10001, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(0)),
        # If the delivery distance is 1499 meters, the delivery fee
        # for distance is: 2€ base fee + 1€ for the additional 500 m => 3€
        (get_input_dict(DEFAULT_CART_VALUE, 1499, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(510)),
        # If the delivery distance is 1500 meters, the delivery fee
        # for distance is: 2€ base fee + 1€ for the additional 500 m => 3€
        (get_input_dict(DEFAULT_CART_VALUE, 1500, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(510)),
        # If the delivery distance is 1501 meters, the delivery fee
        # for distance is: 2€ base fee + 1€ for the first 500 m + 1€
        # for the second 500 m => 4€
        (get_input_dict(DEFAULT_CART_VALUE, 1501, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(610)),
        # If the cart value is less than 10€, a small order surcharge
        # is added to the delivery price. The surcharge is the difference
        # between the cart value and 10€.
        (get_input_dict(999, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(501)),
        (get_input_dict(1000, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(500)),
        (get_input_dict(1001, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), get_delivery_fee(500)),
        # If the number of items is 4, no extra surcharge
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 4,
                        DEFAULT_TIME), get_delivery_fee(710)),
        # If the number of items is 5, 50 cents surcharge is added
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 5,
                        DEFAULT_TIME), get_delivery_fee(760)),
        # If the number of items is 6, 1€ surcharge (2 x 50 cents) is added
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 6,
                        DEFAULT_TIME), get_delivery_fee(810)),
        # If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 10,
                        DEFAULT_TIME), get_delivery_fee(1010)),
        # If the number of items is 12, 4€ surcharge (8 x 50 cents) is added
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 12,
                        DEFAULT_TIME), get_delivery_fee(1110)),
        # If the number of items is 13, 5,70€
        # surcharge is added ((9 * 50 cents) + 1,20€)
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 13,
                        DEFAULT_TIME), get_delivery_fee(1280)),
        # During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee
        # including possible surcharges) will be multiplied by 1.2x. However,
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T14:59:23Z'), get_delivery_fee(710)),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T15:00:00Z'), get_delivery_fee(852)),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T15:01:01Z'), get_delivery_fee(852)),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T18:59:45Z'), get_delivery_fee(852)),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T19:00:00Z'), get_delivery_fee(710)),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T19:01:01Z'), get_delivery_fee(710)),
        # The fee cannot be more than the max (15€).
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 15,
                        '2021-10-12T16:21:45Z'), get_delivery_fee(1500)),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 15,
                        '2021-10-12T20:59:45Z'), get_delivery_fee(1380)),
        # Missing parameter
        (get_input_dict('', DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), MISSING_PARAM['cart_value']),
        (get_input_dict(DEFAULT_CART_VALUE, '', DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), MISSING_PARAM['delivery_distance']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, '',
                        DEFAULT_TIME), MISSING_PARAM['number_of_items']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS, ''), MISSING_PARAM['time']),
        # Invalid parameter
        (get_input_dict(7.3, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), INVALID_PARAM['cart_value']),
        (get_input_dict('7.3', DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), INVALID_PARAM['cart_value']),
        (get_input_dict(-6, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), INVALID_PARAM['cart_value']),
        (get_input_dict(DEFAULT_CART_VALUE, 7.3, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), INVALID_PARAM['delivery_distance']),
        (get_input_dict(DEFAULT_CART_VALUE, '7.3', DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), INVALID_PARAM['delivery_distance']),
        (get_input_dict(DEFAULT_CART_VALUE, -6, DEFAULT_NUMBER_OF_ITEMS,
                        DEFAULT_TIME), INVALID_PARAM['delivery_distance']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 7.3,
                        DEFAULT_TIME), INVALID_PARAM['number_of_items']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, '7.3',
                        DEFAULT_TIME), INVALID_PARAM['number_of_items']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, -6,
                        DEFAULT_TIME), INVALID_PARAM['number_of_items']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        '2021-10-12T19:01:68Z'), INVALID_PARAM['time']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS, 'abc'), INVALID_PARAM['time']),
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS, 23456), INVALID_PARAM['time']),
        # Time is in the future
        (get_input_dict(DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE,
                        DEFAULT_NUMBER_OF_ITEMS,
                        (datetime.datetime.now() +
                         datetime.timedelta(seconds=5)).isoformat()),
         INVALID_PARAM['time']),
        # Invalid request data
        ('', json.dumps({'error': 'Invalid request body'})),
    ))
def test_api_endpoint(client, data: dict, result: str):
  """Test the API endpoint.

    Args:
      data: The input data for testing.
      result: The expected result.
  """
  print(data)
  response = client.post('/', json=data)
  assert result == json.dumps(json.loads(response.data))
