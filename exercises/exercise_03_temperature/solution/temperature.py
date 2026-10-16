"""练习 3 参考答案：temperature 完整实现"""


class TemperatureConverter:
    @staticmethod
    def c_to_f(celsius: float) -> float:
        return celsius * 9 / 5 + 32

    @staticmethod
    def f_to_c(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5 / 9

    @staticmethod
    def c_to_k(celsius: float) -> float:
        kelvin = celsius + 273.15
        if kelvin < 0:
            raise ValueError("温度低于绝对零度")
        return kelvin

    @staticmethod
    def k_to_c(kelvin: float) -> float:
        if kelvin < 0:
            raise ValueError("开尔文温度不能为负")
        return kelvin - 273.15
