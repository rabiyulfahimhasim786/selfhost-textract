import re
from datetime import datetime

GSTIN_REGEX = r"[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}"


def normalize_date(s):
    for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%d %B %Y"]:
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except Exception:
            pass
    return None


def validate_gstin(s):
    return bool(re.search(GSTIN_REGEX, s.replace(' ', '').upper()))