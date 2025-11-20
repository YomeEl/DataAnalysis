from datetime import date as Date
from money import Money

DATE_SEPARATOR = "-"


class Order:
    def __init__(self, date: Date, name: str, price: Money):
        self.date: Date = date
        self.name: str = name
        self.price: Money = price


class ParsingError:
    def __init__(self, what: str):
        self.what = what


class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Counter:
    def __init__(self):
        self.items: list[Pair] = []

    def append(self, key, value=1):
        index = self.__find(key)
        if index == -1:
            self.items.append(Pair(key, value))
        else:
            self.items[index].value += 1

    def get_sorted(self):
        self.items.sort(key=lambda x: x.value)
        return self.items

    def __find(self, key):
        index = len(self.items) - 1
        while index >= 0 and self.items[index].key != key:
            index -= 1
        return index


class OrderAnalyzer:
    def __init__(self):
        self.name_counter: Counter = Counter()
        self.date_counter: Counter = Counter()

        self.most_expensive: Order | None = None

        self.count = 0
        self.sum = Money(0)

    def add_order(self, order: Order):
        self.name_counter.append(order.name)
        self.date_counter.append(order.date, order.price)

        if not self.most_expensive or self.most_expensive.price < order.price:
            self.most_expensive = order

        self.count += 1
        self.sum += order.price

    def print_result(self):
        print("1. Pizzas sorted by order count")
        for pair in self.name_counter.get_sorted():
            print(f"\t{pair.key} ordered {pair.value}")

        print("2. Dates with earnings")
        for pair in self.date_counter.get_sorted():
            print(f"\t{pair.key}: earned {pair.value}")

        print("3. Most expensive order")
        print(
            f"\t{self.most_expensive.name} sold for {self.most_expensive.price} at {self.most_expensive.date}"
        )

        print("4. Average order cost")
        print(f"\t{self.sum / self.count}")


def parse_date(line: str) -> Date | ParsingError:
    split = line.split(DATE_SEPARATOR)
    err = ParsingError("Date was in incorrect format")

    try:
        day, month, year = split
        return Date(int(year), int(month), int(day))
    except:
        return err


def parse_money(line: str) -> Money | ParsingError:
    try:
        return Money(float(line))
    except:
        return ParsingError("Price was in incorrect format")


def parse_line(line: str) -> Order | ParsingError:
    split = line.split(" ")
    if len(split) != 3:
        return ParsingError("Line was in incorrect format")

    date = parse_date(split[0])
    if date is ParsingError:
        return date

    name = split[1]
    if len(name) == 0:
        return ParsingError("Name can't be empty")

    price = parse_money(split[2])
    if price is ParsingError:
        return price

    return Order(date, name, price)


def read_file(filename: str) -> list[Order] | str:
    try:
        file = open(filename)
    except:
        return "Файл не существует"

    orders: list[Order] = []
    line_number = 1
    while True:
        line = file.readline()
        if line == "":
            break
        order = parse_line(line)
        if order is not str:
            orders.append(order)
        else:
            print(f"Строка {line_number}: {order.what}")
        line_number += 1

    return orders


def read_stdin() -> list[Order]:
    orders: list[Order] = []
    while True:
        line = input(
            'Введите заказы в формате "дд-мм-гггг название сумма" или "конец" для завершения'
        )
        if line == "конец":
            break
        order = parse_line(line)
        if order is Order:
            orders.append(order)
        else:
            print(f"Ошибка: {order.what}")

    return orders


def main() -> int:
    mode = ""
    while not mode in ["1", "2"]:
        mode = input(
            "Выберите режим работы:\n\t1 - ввод с клавиатуры\n\t2 - чтение из файла\nВведите номер режима: "
        )

    orders: list[Order] = []
    if mode == "1":
        orders = read_stdin()
    else:
        filename = input("Введите имя файла или нажмите enter, чтобы использовать task5.txt: ")
        if filename == "":
            filename = "task5.txt"
        orders = read_file(filename)
        if type(orders) is type(""):
            print(f"Ошибка: {orders}")
            return 1

    analyzer = OrderAnalyzer()
    for order in orders:
        analyzer.add_order(order)

    analyzer.print_result()

    return 0


if __name__ == "__main__":
    main()
