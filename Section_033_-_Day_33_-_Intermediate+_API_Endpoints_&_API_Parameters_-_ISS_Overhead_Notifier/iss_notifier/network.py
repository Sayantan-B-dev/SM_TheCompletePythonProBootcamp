import requests
from typing import Dict
from config import REQUEST_TIMEOUT

def safe_get(url: str, *, params=None, headers=None) -> Dict:
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()
