# converters.py

def miles_to_km(miles: float) -> float:
    return miles * 1.60934

def km_to_miles(km: float) -> float:
    return km / 1.60934

def kg_to_pound(kg: float) -> float:
    return kg * 2.20462

def pound_to_kg(pound: float) -> float:
    return pound / 2.20462

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9
