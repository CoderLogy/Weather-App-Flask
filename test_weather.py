import pytest
import Weather_App.weather as weather
def test_weather():
    response = weather.get_weather()
    assert response.status_code == 200