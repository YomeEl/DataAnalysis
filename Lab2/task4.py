from money import Money

DEBUG = 0


class Spending:
    def __init__(self, name: str, amount: Money):
        self.name: str = name
        self.amount: Money = amount

    def copy(self):
        return Spending(self.name, self.amount.copy())


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: Money):
        self.sender: str = sender
        self.receiver: str = receiver
        self.amount: Money = amount

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"


def calculate_transactions(spendings: list[Spending]) -> list[Transaction]:
    sum = Money(0)
    for item in spendings:
        sum += item.amount
    average = sum / len(spendings)

    balances = [x.copy() for x in spendings]
    balances.sort(key=lambda x: float(x.amount))
    transactions: list[Transaction] = []
    
    if DEBUG > 0:
        print("before: ", [str(x.amount) for x in balances])

    left_index = 0
    right_index = len(balances) - 1
    while left_index < right_index:
        left = balances[left_index]
        right = balances[right_index]
        left_needs: Money = average - left.amount
        if left_needs <= Money(0):
            left_index += 1
            continue
        right_can_provide: Money = right.amount - average
        if right_can_provide <= Money(0):
            right_index -= 1
            continue
        right_provides = (
            left_needs if right_can_provide >= left_needs else right_can_provide
        )
        balances[left_index].amount += right_provides
        balances[right_index].amount -= right_provides
        transactions.append(Transaction(left.name, right.name, right_provides))

    if DEBUG > 0:
        print("after: ", [str(x.amount) for x in balances])
    return transactions


def parse_line(line: str) -> Spending | str:
    if line == "":
        return "Введена пустая строка"

    split = line.strip().split(" ")
    try:
        spending = Spending(split[0], Money(float(split[1])))
    except:
        return "Неверный формат входных данных"

    return spending


def read_file(filename: str) -> list[Spending] | str:
    try:
        file = open(filename)
    except:
        return "Файл не существует"

    spendings: list[Spending] = []
    line_number = 1
    while True:
        line = file.readline()
        if line == "":
            break
        spending = parse_line(line)
        if spending is not str:
            spendings.append(spending)
        else:
            print(f"Строка {line_number}: {spending}")
        line_number += 1

    return spendings


def read_stdin() -> list[Spending]:
    spendings: list[Spending] = []
    while True:
        line = input('Введите затраты в формате "имя сумма" или "конец" для завершения')
        if line == "конец":
            break
        spending = parse_line(line)
        if spending is Spending:
            spendings.append(spending)
        else:
            print(f"Ошибка: {spending}")

    return spendings


def main() -> int:
    mode = ""
    while not mode in ["1", "2"]:
        mode = input(
            "Выберите режим работы:\n\t1 - ввод с клавиатуры\n\t2 - чтение из файла\nВведите номер режима: "
        )

    spendings: list[Spending] = []
    if mode == "1":
        spendings = read_stdin()
    else:
        filename = input("Введите имя файла или нажмите enter, чтобы использовать task4.txt: ")
        if filename == "":
            filename = "task4.txt"
        spendings = read_file(filename)
        if type(spendings) is type(""):
            print(f"Ошибка: {spendings}")
            return 1

    print("Необходимые переводы:")
    for item in [f"\t{x}" for x in calculate_transactions(spendings)]:
        print(item)
    return 0


if __name__ == "__main__":
    main()
