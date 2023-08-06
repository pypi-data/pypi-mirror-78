# Simple communication library for ConnectedCars.io

This simple communication layer is originally created to accommodate a Home Assistant integration. Purpose is to pull current state of a vehicle connected to ConnectedCars.io (for instance with MinVolkswagen).

## Installation

```pip install connectedcarscomm```

## Namespace

Connected Cars needs a namespace to work. In my case (using MinVolkswagen) this was `semler:minvolkswagen`.

## Supplied queries

The package comes with three predefined queries:

- `QUERY_CURRENT_STATE`
- `QUERY_USER`
- `QUERY_VEHICLE_VIN`
