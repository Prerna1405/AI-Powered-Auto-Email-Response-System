from datetime import datetime
from random import randint


def generate_ticket_number() -> str:
    date_part = datetime.utcnow().strftime("%Y%m%d")
    serial = randint(1000, 9999)
    return f"TKT-{date_part}-{serial}"
