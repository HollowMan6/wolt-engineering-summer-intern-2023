# Backend for Delivery Fee Calculator
This is an HTTP API which could be used for calculating the delivery fee. It is written in Python using the Flask framework. The API is documented using Swagger Editor in openapi.yaml. The API is deployed to Azure and can be accessed at https://delivery-fee-calculator.azurewebsites.net/

## Codebase Tree
```bash
.
├── app.py                 # main application
├── Dockerfile             # Dockerfile for building the production image
├── .github            
│   └── workflows          # GitHub Actions workflows
│       ├── pylint.yml     # workflow for running pylint
│       └── python-app.yml # workflow for running tests and coverage
├── .gitignore             # gitignore file
├── openapi.yaml           # openapi specification
├── .pylintrc              # configuration for pylint
├── README.md              # this file
├── requirements-dev.txt   # development requirements
├── requirements.txt       # production requirements
├── setup.cfg              # configuration for pytest and coverage
└── tests
    ├── conftest.py        # pytest configuration
    ├── __init__.py
    ├── test_api.py        # tests for the API
    └── test.rest          # test file for VSCode REST Client
└── .vscode                # VSCode configuration
    └── settings.json      # VSCode settings
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

### Run the application
```bash
flask run
```

### Run the tests and coverage
```bash
pytest
coverage run -m pytest
coverage report
coverage html
```

The latest coverage is 100%:
```log
tests/test_api.py ..........................................             [100%]

============================== 42 passed in 0.21s ==============================
Name     Stmts   Miss Branch BrPart  Cover
------------------------------------------
app.py      40      0     18      0   100%
------------------------------------------
TOTAL       40      0     18      0   100%
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
