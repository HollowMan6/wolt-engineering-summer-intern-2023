# Backend for Delivery Fee Calculator

By [Songlin Jiang](https://github.com/HollowMan6)

This is an HTTP API which could be used for calculating the delivery fee. It is written in Python using the Flask framework. The API is documented using Swagger Editor in openapi.yaml. The build system for the project is bazel. The API is deployed to Azure and can be accessed at https://delivery-fee-calculator.azurewebsites.net/

## Codebase Tree (Some files are omitted)
```bash
.
├── app.py                 # main application
├── Dockerfile             # Dockerfile for building the production image
├── openapi.yaml           # openapi specification
├── .pylintrc              # configuration for pylint
├── README.md              # this file
├── requirements-dev.txt   # development requirements
├── requirements.txt       # production requirements
├── setup.cfg              # configuration for pytest and coverage
└── tests
    ├── conftest.py        # pytest configuration
    ├── test_api.py        # tests for the API
    └── test.rest          # test file for VSCode REST Client
```

## Specification
THe HTTP API (single endpoint) calculates the delivery fee based on the information in the request payload (JSON) and includes the calculated delivery fee in the response payload (JSON).

Rules for calculating a delivery fee
* If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
* A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
  * Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  * Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  * Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
* If the number of items is five or more, an additional 50 cent surcharge is added for each item above five. An extra "bulk" fee applies for more than 12 items of 1,20€
  * Example 1: If the number of items is 4, no extra surcharge
  * Example 2: If the number of items is 5, 50 cents surcharge is added
  * Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
  * Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
* The delivery fee can __never__ be more than 15€, including possible surcharges.
* The delivery is free (0€) when the cart value is equal or more than 100€. 
* During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€).

### Request
Example: 
```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}
```

#### Field details

| Field             | Type    | Description                                                           | Example value                            |
| :---------------- | :------ | :-------------------------------------------------------------------- | :--------------------------------------- |
| cart_value        | Integer | Value of the shopping cart __in cents__.                              | __790__ (790 cents = 7.90€)              |
| delivery_distance | Integer | The distance between the store and customer’s location __in meters__. | __2235__ (2235 meters = 2.235 km)        |
| number_of_items   | Integer | The __number of items__ in the customer's shopping cart.              | __4__ (customer has 4 items in the cart) |
| time              | String  | Order time in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).   | __2021-01-16T13:00:00Z__                 |

### Response
Example:
```json
{"delivery_fee": 710}
```

#### Field details

| Field        | Type    | Description                           | Example value               |
| :----------- | :------ | :------------------------------------ | :-------------------------- |
| delivery_fee | Integer | Calculated delivery fee __in cents__. | __710__ (710 cents = 7.10€) |

## Development
Run the following commands to setup the development environment:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

You can also [install the bazel](https://bazel.build/install) without the above steps for easily running and testing the application.

### Run the application
Run with flask directly:
```bash
FLASK_APP=src/app.py flask run
```

Or using bazel:
```bash
bazel run //src:app
```

### Run the tests and coverage
Directly:
```bash
pytest
coverage run -m pytest
coverage report
coverage html
```

Or using bazel to run the tests:
```bash
bazel test //...
```

The coverage is 100% (The missed one is the `create_app().run()` and it should be ignored):
```log
tests/test_api.py ..........................................             [100%]

============================== 42 passed in 0.21s ==============================
Name                            Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------------
deps/calculator/calculator.py      12      0      2      0   100%
src/app.py                         33      1     16      1    96%
tests/__init__.py                   0      0      0      0   100%
tests/conftest.py                  12      1      0      0    92%
tests/test_api.py                  30      0     10      0   100%
-----------------------------------------------------------------
TOTAL                              87      2     28      1    97%
```

## Deployment
We use gunicorn for running the application in production. We specify 10 workers for handling the requests.

Build the Docker image:
```bash
docker build -t delivery-fee-calculator .
```

Run the Docker image:
```bash
docker run -p 80:8000 delivery-fee-calculator
```

Now the API is available at http://localhost
