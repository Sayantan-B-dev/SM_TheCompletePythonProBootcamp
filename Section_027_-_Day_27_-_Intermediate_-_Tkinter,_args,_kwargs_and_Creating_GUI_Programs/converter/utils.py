# utils.py

def safe_float(value: str) -> float:
    value = value.strip()
    if not value:
        raise ValueError("Empty input")
    return float(value)
