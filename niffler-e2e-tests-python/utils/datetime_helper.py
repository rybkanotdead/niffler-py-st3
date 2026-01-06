from datetime import datetime, timedelta


def get_past_date_iso(days_ago: int = 7) -> str:
    """Возвращает дату в прошлом в ISO формате."""
    past_date = datetime.now() - timedelta(days=days_ago)
    return past_date.isoformat() + "Z"