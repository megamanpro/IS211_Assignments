class ConversionNotPossible(Exception):
    pass

def _normalize_unit(u):
    return u.strip().lower()


_TEMP_UNITS = {"celsius", "c", "fahrenheit", "f", "kelvin", "k"}
_DISTANCE_UNITS = {"miles", "mile", "mi", "yards", "yard", "yd", "meters", "meter", "m"}

def _to_celsius(value, from_unit):
    u = _normalize_unit(from_unit)
    if u in ("celsius", "c"):
        return float(value)
    if u in ("fahrenheit", "f"):
        return (float(value) - 32.0) * 5.0 / 9.0
    if u in ("kelvin", "k"):
        return float(value) - 273.15
    raise ConversionNotPossible(f"Unknown temperature unit: {from_unit}")

def _from_celsius(value_c, to_unit):
    u = _normalize_unit(to_unit)
    if u in ("celsius", "c"):
        return float(value_c)
    if u in ("fahrenheit", "f"):
        return float(value_c) * 9.0 / 5.0 + 32.0
    if u in ("kelvin", "k"):
        return float(value_c) + 273.15
    raise ConversionNotPossible(f"Unknown temperature unit: {to_unit}")

_DISTANCE_TO_METERS = {
    "m": 1.0, "meter": 1.0, "meters": 1.0,
    "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
    "mi": 1609.344, "mile": 1609.344, "miles": 1609.344
}

def _is_temperature_unit(u):
    return _normalize_unit(u) in _TEMP_UNITS

def _is_distance_unit(u):
    return _normalize_unit(u) in _DISTANCE_UNITS

def convert(fromUnit, toUnit, value):
    fu = _normalize_unit(fromUnit)
    tu = _normalize_unit(toUnit)

    if fu == tu:
        return float(value)


    if _is_temperature_unit(fu) and _is_temperature_unit(tu):
        c = _to_celsius(value, fu)
        return float(_from_celsius(c, tu))


    if _is_distance_unit(fu) and _is_distance_unit(tu):
        # convert fromUnit -> meters -> toUnit
        if fu not in _DISTANCE_TO_METERS or tu not in _DISTANCE_TO_METERS:
            raise ConversionNotPossible(f"Unknown distance unit: {fromUnit} or {toUnit}")
        meters = float(value) * _DISTANCE_TO_METERS[fu]
        return float(meters / _DISTANCE_TO_METERS[tu])

    raise ConversionNotPossible(f"Conversion from {fromUnit} to {toUnit} is not possible")
