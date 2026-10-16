"""练习 3 的测试骨架：先实现 temperature.py，再用 parametrize 补全测试"""
import pytest

from temperature import TemperatureConverter


# ---------- 摄氏 → 华氏 ----------
@pytest.mark.parametrize("celsius, expected", [
    # TODO: 至少 5 组：0°C→32°F, 100°C→212°F, -40°C→-40°F, 37°C→98.6°F, 25°C→77°F
], ids=[])
def test_c_to_f(celsius, expected):
    assert TemperatureConverter.c_to_f(celsius) == pytest.approx(expected)


# ---------- 华氏 → 摄氏 ----------
@pytest.mark.parametrize("fahrenheit, expected", [
    # TODO: 至少 4 组：32→0, 212→100, -40→-40, 98.6→37
], ids=[])
def test_f_to_c(fahrenheit, expected):
    assert TemperatureConverter.f_to_c(fahrenheit) == pytest.approx(expected)


# ---------- 摄氏 → 开尔文 ----------
@pytest.mark.parametrize("celsius, expected", [
    # TODO: 0→273.15, 100→373.15, -273.15→0
], ids=[])
def test_c_to_k(celsius, expected):
    assert TemperatureConverter.c_to_k(celsius) == pytest.approx(expected)


# ---------- 非法：低于绝对零度 ----------
@pytest.mark.parametrize("celsius", [
    # TODO: -274, -300, -1000
], ids=[])
def test_c_to_k_below_absolute_zero(celsius):
    with pytest.raises(ValueError, match="绝对零度"):
        TemperatureConverter.c_to_k(celsius)


# ---------- 开尔文 → 摄氏 + 非法 ----------
@pytest.mark.parametrize("kelvin, expected", [
    # TODO: 273.15→0, 0→-273.15, 373.15→100
], ids=[])
def test_k_to_c(kelvin, expected):
    assert TemperatureConverter.k_to_c(kelvin) == pytest.approx(expected)


@pytest.mark.parametrize("kelvin", [
    # TODO: -1, -273.15
], ids=[])
def test_k_to_c_negative_kelvin(kelvin):
    with pytest.raises(ValueError, match="不能为负"):
        TemperatureConverter.k_to_c(kelvin)
