class Money:
    def __init__(
        self, number: float, int_symbol: str = "руб.", frac_symbol: str = "коп."
    ):
        self.__frac: int = int(number * 100)
        self.__int_symbol: str = int_symbol
        self.__frac_symbol: str = frac_symbol

    def __str__(self):
        return f"{self.__frac // 100} {self.__int_symbol} {self.__frac % 100} {self.__frac_symbol}"

    def __float__(self):
        return self.__frac / 100

    def __add__(self, other):
        result = Money(0, self.__int_symbol, self.__frac_symbol)
        result.__frac = self.__frac + other.__frac
        return result

    def __sub__(self, other):
        result = Money(0, self.__int_symbol, self.__frac_symbol)
        result.__frac = self.__frac - other.__frac
        return result

    def __floordiv__(self, num):
        result = Money(0, self.__int_symbol, self.__frac_symbol)
        result.__frac = self.__frac // num
        return result

    def __truediv__(self, num):
        result = Money(0, self.__int_symbol, self.__frac_symbol)
        result.__frac = int(self.__frac / num)
        return result

    def __lt__(self, other):
        return self.__frac < other.__frac

    def __le__(self, other):
        return self.__frac <= other.__frac

    def __gt__(self, other):
        return self.__frac > other.__frac

    def __ge__(self, other):
        return self.__frac >= other.__frac

    def __eq__(self, other):
        return self.__frac == other.__frac

    def copy(self):
        result = Money(0, self.__int_symbol, self.__frac_symbol)
        result.__frac = self.__frac
        return result
