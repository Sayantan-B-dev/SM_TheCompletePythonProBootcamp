import datetime as dt

def parse_dob(input_text: str) -> dt.datetime:
    try:
        return dt.datetime.strptime(
            input_text.strip(),
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        raise ValueError(
            "Invalid format. Use: YYYY-MM-DD HH:MM:SS"
        )
