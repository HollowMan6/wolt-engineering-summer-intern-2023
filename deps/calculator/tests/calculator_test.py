"""Module defining the test cases for the calculator."""
import unittest
from deps.calculator.calculator import Calculator

# Some default values for testing
DEFAULT_CART_VALUE = 790
DEFAULT_DELIVERY_DISTANCE = 2235
DEFAULT_NUMBER_OF_ITEMS = 4
DEFAULT_HOUR = 13

# The test cases are defined as a list of tuples. Each tuple contains
# the input parameters for the calculator and the expected output.
TEST_CASES = [
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      DEFAULT_HOUR), 710),
    # The delivery is free (0€) when the cart value is equal or more than 100€
    ((9999, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR),
     500),
    ((10000, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR),
     0),
    ((10001, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR),
     0),
    # If the delivery distance is 1499 meters, the delivery fee
    # for distance is: 2€ base fee + 1€ for the additional 500 m => 3€
    ((DEFAULT_CART_VALUE, 1499, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR), 510),
    # If the delivery distance is 1500 meters, the delivery fee
    # for distance is: 2€ base fee + 1€ for the additional 500 m => 3€
    ((DEFAULT_CART_VALUE, 1500, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR), 510),
    # If the delivery distance is 1501 meters, the delivery fee
    # for distance is: 2€ base fee + 1€ for the first 500 m + 1€
    # for the second 500 m => 4€
    ((DEFAULT_CART_VALUE, 1501, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR), 610),
    # If the cart value is less than 10€, a small order surcharge
    # is added to the delivery price. The surcharge is the difference
    # between the cart value and 10€.
    ((999, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR),
     501),
    ((1000, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR),
     500),
    ((1001, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS, DEFAULT_HOUR),
     500),
    # If the number of items is 4, no extra surcharge
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 4, DEFAULT_HOUR), 710),
    # If the number of items is 5, 50 cents surcharge is added
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 5, DEFAULT_HOUR), 760),
    # If the number of items is 6, 1€ surcharge (2 x 50 cents) is added
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 6, DEFAULT_HOUR), 810),
    # If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 10, DEFAULT_HOUR), 1010),
    # If the number of items is 12, 4€ surcharge (8 x 50 cents) is added
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 12, DEFAULT_HOUR), 1110),
    # If the number of items is 13, 5,70€
    # surcharge is added ((9 * 50 cents) + 1,20€)
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 13, DEFAULT_HOUR), 1280),
    # During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee
    # including possible surcharges) will be multiplied by 1.2x. However,
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      14), 710),
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      15), 852),
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      15), 852),
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      18), 852),
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      19), 710),
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, DEFAULT_NUMBER_OF_ITEMS,
      19), 710),
    # The fee cannot be more than the max (15€).
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 15, 16), 1500),
    ((DEFAULT_CART_VALUE, DEFAULT_DELIVERY_DISTANCE, 15, 20), 1380)
]


class TestCalculator(unittest.TestCase):

  def test_delivery_fee_calculator(self):
    calculator = Calculator()
    for test_case in TEST_CASES:
      self.assertEqual(calculator.calculate_delivery_fee(*test_case[0]),
                       test_case[1])


if __name__ == '__main__':
  unittest.main()
