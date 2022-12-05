import os
import stackcontainer

def addLine(stackContainer: stackcontainer.StackContainer, line: str):
    count: int = 0
    for i in range(1, len(line), 4):
        if line[i] != ' ':
            stackContainer.add_item_to_stack(count, line[i])
        count += 1

def moveItems(stackContainer: stackcontainer.StackContainer, line: str):
    parts = line.split(' ')
    stackContainer.move_items(int(parts[3]), int(parts[5]), int(parts[1]))

if __name__ == "__main__" :
    file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input5.txt'), 'r')
    
    stackContainer: stackcontainer.StackContainer = None
    count: int = 0

    while True:
        count += 1
        line = file.readline()
        if line.strip() == '':
            break
        if line.__contains__(" 1"):
            continue
    
        if count == 1:
            stackContainer = stackcontainer.StackContainer(int(len(line)/4))
        
        addLine(stackContainer, line)
    
    stackContainer.reverse_stacks()
    while True:
        line = file.readline().strip()
        if not line:
            break
        moveItems(stackContainer, line)

    for stack in stackContainer.stacks:
        print(stack.pop(),end ="")
        
    file.close()