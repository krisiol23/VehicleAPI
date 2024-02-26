# VehicleAPI
Simple cars makes and models database interacting with API. Create in FastAPI and sqlalchemy.

# Setup
```
pip install -r requirements.txt
```
# Endpoints:
#### POST /cars
Add a car make and model

#### POST /rate
Add a rate for a car from 1 to 5

#### GET /cars
list of all cars with their current average rate
```
[
    {
        "make": "Ford",
        "model": "Fiesta",
        "avgRate": 2.75
    },
    {
        "make": "Ford",
        "model": "Focus",
        "avgRate": 3.5
    }
]
```

#### GET /popular
list of top cars based on number of rates
```
[
    {
        "make": "Ford",
        "model": "Fiesta",
        "number_of_rates": 4
    },
    {
        "make": "Ford",
        "model": "Focus",
        "number_of_rates": 2
    }
]
```
