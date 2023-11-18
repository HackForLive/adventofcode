import os
import pathlib

from collections import defaultdict, deque

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


class Graph:
    def __init__(self) -> None:
        self._adjestancy = defaultdict(list)
        self._counter = 0

    def add_edge(self, u: str, v: str):
        self._adjestancy[u].append(v)
        self._adjestancy[v].append(u)

    def traverse(self, start: str, end: str, visited, path, paths):
        # Mark the current node as visited and store in path
        if not start.isupper():
            visited[start] = True
        path.append(start)

        if start == end:
            paths.append(path)

        for u in self._adjestancy[start]:
            if u not in visited:
                self.traverse(start=u, end=end, visited=visited, path=path, paths=paths)

        path.pop()
        visited.pop(start, None)

    def traverse_stack(self, start: str, end: str):
        stack = deque()
        stack.append(start)
        visited = {}
        res = 0

        while stack:
            curr = stack.pop()
            for u in self._adjestancy[curr]:
                if u == end:
                    res += 1
                elif u not in visited:
                    stack.append(u)
            if not start.isupper():
                visited[start] = True
        return res

    def print_all_paths(self, start: str, end: str):
        visited = {}
        path = []
        paths = []
        self.traverse(start=start, end=end, visited=visited, path=path, paths=paths)
        print(len(paths))


def solve_1():
    g = Graph()
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            parts = line.strip().split('-')
            g.add_edge(parts[0], parts[1])
        print ("Following are all different paths from start to end.")
        # g.print_all_paths('start', 'end')
        g.traverse_stack('start', 'end')


if __name__ == '__main__':
    solve_1()
