"""练习 3：温度转换（实现我，然后写参数化测试）"""


class TemperatureConverter:
    @staticmethod
    def c_to_f(celsius: float) -> float:
        # TODO: F = C * 9/5 + 32
        raise NotImplementedError

    @staticmethod
    def f_to_c(fahrenheit: float) -> float:
        # TODO: C = (F - 32) * 5/9
        raise NotImplementedError

    @staticmethod
    def c_to_k(celsius: float) -> float:
        # TODO: K = C + 273.15
        # TODO: 结果低于 0 抛 ValueError("温度低于绝对零度")
        raise NotImplementedError

    @staticmethod
    def k_to_c(kelvin: float) -> float:
        # TODO: C = K - 273.15
        # TODO: K < 0 抛 ValueError("开尔文温度不能为负")
        raise NotImplementedError
