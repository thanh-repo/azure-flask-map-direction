# Deploy a Python (Flask) web app to Azure App Service.<br/>Find nearest US address and route.

## Requirements:
> We need to make a script that calculates which zip code from the given two is closer to a client's zip code. And then, we need to make an API microservice on Azure using this script. We will be sending three zip codes, and we need to receive one as a response.
</br>

> To build an accurate app, we will need to use a full address.

## Project Description:
This project is backend API flask-based which receive 3 US addresses (A, B, C), route and find the shortest direction of B to A or B to C.

## Data input:
```json
{
    "clinic1": {
        "street": "10333 El Camino Real",
        "city": "Atascadero",
        "county": "",
        "state": "California",
        "postalcode": "93422",
        "country": "United States"
    },
    "clinic2": {
        "street": "655 Palm Avenue",
        "city": "Palm",
        "county": "San Diego",
        "state": "California",
        "postalcode": "92154",
        "country": "United States"
    },
    "client": {
        "street": "23150 Crenshaw Blvd",
        "city": "Torrance",
        "county": "Los Angeles",
        "state": "California",
        "postalcode": "93422",
        "country": "United States"
    }
}
```

## Response Data:
```json
{
    "direction": "https://www.google.com/maps/dir/?api=1&origin=33.815394895155954,-118.327932&destination=32.5839179,-117.0915437",
    "nearest": "clinic2",
    "service": "Ok"
}
```

## Error Description:
Error sample
```json
{
    "direction": "",
    "nearest": "",
    "service": "EL000 clinic1"
}
```
### response["service"] available
+ EP: Error Parameter
+ EL: Error Location
+ ED: Error Direction
+ EP000: Parameter not found, (parameter)
+ EL000: Location not found, (location)
+ ED000: Direction to clinic 1, 2 not found
+ ED001: Direction to clinic 1 not found
+ ED002: Direction to clinic 2 not found

## Bonus function:
1. Google map route url.
2. Logging.

