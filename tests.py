# tests.py
import conversions
from conversions_refactored import convert, ConversionNotPossible

def almost_equal(a, b, tol=1e-2):
    return abs(a - b) <= tol

def test_celsius_conversions():
    cases = [
        (300.00, 573.15, 572.00),  # (C, expected K, expected F)
        (0.0, 273.15, 32.0),
        (-40.0, 233.15, -40.0),
        (100.0, 373.15, 212.0),
        (37.0, 310.15, 98.6)
    ]

    print("Testing convertCelsiusToKelvin:")
    for c, expected_k, _ in cases:
        got = conversions.convertCelsiusToKelvin(c)
        print(f" C={c} -> K={got} (expected {expected_k})")
        assert almost_equal(got, expected_k)

    print("Testing convertCelsiusToFahrenheit:")
    for c, _, expected_f in cases:
        got = conversions.convertCelsiusToFahrenheit(c)
        print(f" C={c} -> F={got} (expected {expected_f})")
        assert almost_equal(got, expected_f)

def test_fahrenheit_conversions():
    cases = [
        (572.0, 300.0, 573.15),  # (F, expected C, expected K)
        (32.0, 0.0, 273.15),
        (-40.0, -40.0, 233.15),
        (212.0, 100.0, 373.15),
        (98.6, 37.0, 310.15)
    ]

    print("Testing convertFahrenheitToCelsius:")
    for f, expected_c, _ in cases:
        got = conversions.convertFahrenheitToCelsius(f)
        print(f" F={f} -> C={got} (expected {expected_c})")
        assert almost_equal(got, expected_c)

    print("Testing convertFahrenheitToKelvin:")
    for f, _, expected_k in cases:
        got = conversions.convertFahrenheitToKelvin(f)
        print(f" F={f} -> K={got} (expected {expected_k})")
        assert almost_equal(got, expected_k)

def test_kelvin_conversions():
    cases = [
        (573.15, 300.0, 572.0),  # (K, expected C, expected F)
        (273.15, 0.0, 32.0),
        (233.15, -40.0, -40.0),
        (373.15, 100.0, 212.0),
        (310.15, 37.0, 98.6)
    ]

    print("Testing convertKelvinToCelsius:")
    for k, expected_c, _ in cases:
        got = conversions.convertKelvinToCelsius(k)
        print(f" K={k} -> C={got} (expected {expected_c})")
        assert almost_equal(got, expected_c)

    print("Testing convertKelvinToFahrenheit:")
    for k, _, expected_f in cases:
        got = conversions.convertKelvinToFahrenheit(k)
        print(f" K={k} -> F={got} (expected {expected_f})")
        assert almost_equal(got, expected_f)

def test_refactored_temperatures():
    print("Testing refactored temperature conversions via convert():")
    temp_triplets = [
        ("Celsius", "Kelvin", 100.0, 373.15),
        ("C", "F", 0.0, 32.0),
        ("Fahrenheit", "Celsius", -40.0, -40.0),
        ("K", "Fahrenheit", 310.15, 98.6),
        ("c", "k", 37.0, 310.15)
    ]
    for frm, to, val, expected in temp_triplets:
        got = convert(frm, to, val)
        print(f" {val} {frm} -> {got} {to} (expected {expected})")
        assert almost_equal(got, expected)

def test_refactored_distances():
    print("Testing refactored distance conversions via convert():")
    distance_cases = [
        ("miles", "meters", 1.0, 1609.344),
        ("mi", "yd", 1.0, 1760.0),
        ("yards", "meters", 10.0, 9.144),
        ("meters", "yards", 3.0, 3.2808398950131233),
        ("meter", "mile", 1609.344, 1.0)
    ]
    for frm, to, val, expected in distance_cases:
        got = convert(frm, to, val)
        print(f" {val} {frm} -> {got} {to} (expected {expected})")
        assert almost_equal(got, expected, tol=1e-6)

def test_refactored_identity_and_incompatible():
    print("Testing identity conversions:")
    units = ["Celsius", "Fahrenheit", "Kelvin", "meters", "yards", "miles"]
    for u in units:
        val = 123.456
        got = convert(u, u, val)
        print(f" {val} {u} -> {got} {u} (expected same)")
        assert almost_equal(got, val)

    print("Testing incompatible conversions raise ConversionNotPossible:")
    bad_pairs = [
        ("Celsius", "meters"),
        ("miles", "kelvin"),
        ("yards", "fahrenheit")
    ]
    for frm, to in bad_pairs:
        try:
            _ = convert(frm, to, 1.0)
            print(f" ERROR: {frm} -> {to} did not raise")
            assert False, f"Conversion from {frm} to {to} should have raised"
        except ConversionNotPossible:
            print(f" Correctly raised for {frm} -> {to}")

if __name__ == "__main__":
    test_celsius_conversions()
    test_fahrenheit_conversions()
    test_kelvin_conversions()
    test_refactored_temperatures()
    test_refactored_distances()
    test_refactored_identity_and_incompatible()
    print("All tests passed.")
