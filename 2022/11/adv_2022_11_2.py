import os

class Monkey:
    def __init__(self, operation,  divisibleTestNumber: int, testSuccessMonkey: int, testFailureMonkey: int, items ):
        self.items = items
        self.operation = operation
        self.divisibleTestNumber = divisibleTestNumber
        self.testSuccessMonkey = testSuccessMonkey
        self.testFailureMonkey = testFailureMonkey
        self.inspectItemCount = 0

class Number:
    def __init__(self, number, modulos):
        self.modulos = modulos
        self.numbers = [number] * len(modulos)

def get_operation(line: str):
    new = line.split('=')[1].strip()
    if new.__contains__('*'):
        operands = list(map(lambda x: x.strip(), new.split('*')))
        if operands[0] == operands[1]:
            return lambda x,y: (x * x) % y
        else:
            return lambda x,y: (x * int(operands[1])) % y

    elif new.__contains__('+'):
        operands = new.split('+')
        if operands[0] == operands[1]:
            return lambda x,y: (x + x) % y
        else:
            return lambda x,y: (x + int(operands[1])) % y
    
    raise NotImplementedError("Not implemented operation!")

def print_result(monkeys, rounds: int):
    for round in range(0, rounds):
        for monkey in monkeys:
            for item in monkey.items:
                for i in range(0, len(item.numbers)):
                    item.numbers[i] = monkey.operation(item.numbers[i], item.modulos[i])
                if item.numbers[item.modulos.index(monkey.divisibleTestNumber)] == 0:
                    monkeys[monkey.testSuccessMonkey].items.append(item)
                else:
                    monkeys[monkey.testFailureMonkey].items.append(item)
                monkey.inspectItemCount += 1
            monkey.items = []
    activeMonkeys = sorted(monkeys, key=lambda x: x.inspectItemCount, reverse=True)
    print(list(map(lambda x: x.inspectItemCount, monkeys)))

    print(activeMonkeys[0].inspectItemCount * activeMonkeys[1].inspectItemCount)
    

if __name__ == "__main__" :

    rounds:int = 10000
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input11.txt'), 'r')
    lines = f.readlines()
    
    modulos = []
    monkeys = []

    for i in range(0, len(lines), 7):
        modulos.append(int(lines[i+3].split(' ')[-1].strip()))

    for i in range(0, len(lines), 7):
        items = list(map(lambda x: Number(int(x.strip()), modulos), lines[i+1].split(':')[1].split(',')))
        op = get_operation(lines[i+2])
        div = int(lines[i+3].split(' ')[-1].strip())
        success = int(lines[i+4].split(' ')[-1].strip())
        failure = int(lines[i+5].split(' ')[-1].strip())
        monkeys.append(Monkey(operation=op, divisibleTestNumber=div, testSuccessMonkey=success,
         testFailureMonkey=failure, items=items))
        
    print_result(monkeys=monkeys, rounds=rounds)
