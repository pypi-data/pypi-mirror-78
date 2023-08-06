API_DEFAULT_TIMEOUT = 30
API_REQUEST_RETIES = 2

HEADER_NAMESPACE = "x-organization-namespace"
TYPE_APP_JSON = "application/json"

URL_AUTH = "https://auth-api.connectedcars.io/auth/login/email/password"
URL_REQ = "https://api.connectedcars.io/graphql"

QUERY_CURRENT_STATE = """
query User {
    viewer {
        id
        firstname
        lastname
        email
        vehicles {
        vehicle {
            id
            vin
            class
            brand
            make
            model
            name
            licensePlate
            fuelType
            fuelLevel {
                liter
            }
            fuelPercentage {
                percent
            }
            odometer {
                odometer
            }
            position {
                latitude
                longitude
            }
            latestBatteryVoltage {
                voltage
            }
            health {
                ok
                recommendation
            }
        }
    }
}"""
QUERY_USER = """
query User {
    viewer {
        id
        firstname
        lastname
        email
    }
}"""
QUERY_VEHICLE_VIN = """
query User {
    viewer {
        vehicles {
            vehicle {
                id
                vin
            }
        }
    }
}"""