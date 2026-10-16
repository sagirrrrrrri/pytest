"""练习 3 参考答案：参数化完整测试"""
import pytest

from temperature import TemperatureConverter


@pytest.mark.parametrize("celsius, expected", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (25, 77),
], ids=["0°C", "100°C", "-40°C等值点", "人体体温37°C", "常温25°C"])
def test_c_to_f(celsius, expected):
    assert TemperatureConverter.c_to_f(celsius) == pytest.approx(expected)


@pytest.mark.parametrize("fahrenheit, expected", [
    (32, 0),
    (212, 100),
    (-40, -40),
    (98.6, 37),
], ids=["冰点32°F", "沸点212°F", "-40°F等值点", "体温98.6°F"])
def test_f_to_c(fahrenheit, expected):
    assert TemperatureConverter.f_to_c(fahrenheit) == pytest.approx(expected)


@pytest.mark.parametrize("celsius, expected", [
    (0, 273.15),
    (100, 373.15),
    (-273.15, 0),
], ids=["0°C=273.15K", "100°C=373.15K", "绝对零度边界"])
def test_c_to_k(celsius, expected):
    assert TemperatureConverter.c_to_k(celsius) == pytest.approx(expected)


@pytest.mark.parametrize("celsius", [-274, -300, -1000],
                         ids=["-274°C", "-300°C", "-1000°C"])
def test_c_to_k_below_absolute_zero(celsius):
    with pytest.raises(ValueError, match="绝对零度"):
        TemperatureConverter.c_to_k(celsius)


@pytest.mark.parametrize("kelvin, expected", [
    (273.15, 0),
    (0, -273.15),
    (373.15, 100),
], ids=["273.15K=0°C", "0K=绝对零度", "373.15K=100°C"])
def test_k_to_c(kelvin, expected):
    assert TemperatureConverter.k_to_c(kelvin) == pytest.approx(expected)


@pytest.mark.parametrize("kelvin", [-1, -273.15],
                         ids=["-1K", "-273.15K"])
def test_k_to_c_negative_kelvin(kelvin):
    with pytest.raises(ValueError, match="不能为负"):
        TemperatureConverter.k_to_c(kelvin)
