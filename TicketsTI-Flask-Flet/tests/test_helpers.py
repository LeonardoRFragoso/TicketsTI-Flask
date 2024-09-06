from app.utils.helpers import calculate_sla, is_valid_email
from datetime import datetime, timedelta

def test_calculate_sla():
    start_time = datetime(2023, 9, 6, 10, 0, 0)
    end_time = datetime(2023, 9, 6, 12, 0, 0)
    sla = calculate_sla(start_time, end_time)
    assert sla == timedelta(hours=2)

def test_is_valid_email():
    assert is_valid_email("test@example.com")
    assert not is_valid_email("invalid-email")
