from datetime import datetime, timedelta


def generate_date_choices(days_ahead: int) -> list[str]:
    now = datetime.now()
    return [(now + timedelta(days=offset)).strftime("%d.%m") for offset in range(days_ahead)]


def generate_time_slots(start_hour: int, end_hour: int) -> list[str]:
    return [f"{hour}:00" for hour in range(start_hour, end_hour)]
