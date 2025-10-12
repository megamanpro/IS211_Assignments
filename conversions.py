# conversions.py
def convertCelsiusToKelvin(c):
    return float(c) + 273.15

def convertCelsiusToFahrenheit(c):
    return float(c) * 9.0 / 5.0 + 32.0

def convertFahrenheitToCelsius(f):
    return (float(f) - 32.0) * 5.0 / 9.0

def convertFahrenheitToKelvin(f):
    return convertFahrenheitToCelsius(f) + 273.15

def convertKelvinToCelsius(k):
    return float(k) - 273.15

def convertKelvinToFahrenheit(k):
    return convertKelvinToCelsius(k) * 9.0 / 5.0 + 32.0
