import re


def calculator(expression):
    try:
        if not re.fullmatch(r"[0-9+\-*/().% ]+", expression):
            return "Invalid expression."

        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)

    except Exception:
        return "Unable to calculate the expression."


def unit_converter(value, from_unit, to_unit):

    conversions = {
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x * 1.60934,
        ("kg", "pounds"): lambda x: x * 2.20462,
        ("pounds", "kg"): lambda x: x * 0.453592,
        ("m", "feet"): lambda x: x * 3.28084,
        ("feet", "m"): lambda x: x * 0.3048
    }

    key = (from_unit.lower(), to_unit.lower())

    if key not in conversions:
        return "Conversion not supported."

    result = conversions[key](value)

    return f"{result:.2f} {to_unit}"