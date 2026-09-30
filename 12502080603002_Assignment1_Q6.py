import heapq


class InvalidInputError(Exception):
    """Raised when the input data is invalid."""
    pass


def validate_module_name(name):
    """Validate a module name."""
    if not name or len(name) > 50:
        raise InvalidInputError("Invalid module name")

    if not all(ch.isalnum() or ch == "_" for ch in name):
        raise InvalidInputError(f"Invalid module name: {name}")


def build_dependency_graph(n, e):
    """Read modules and import relationships and build the graph."""

    if n < 1 or n > 200000:
        raise InvalidInputError("Number of modules must be between 1 and 200000")

    if e < 0 or e > 500000:
        raise InvalidInputError("Invalid number of edges")

    modules = set()

    # Read all module names.
    for _ in range(n):
        name = input().strip()
        validate_module_name(name)

        if name in modules:
            raise InvalidInputError(f"Duplicate module: {name}")

        modules.add(name)

    # graph[dependency] contains modules that depend on it.
    graph = {module: set() for module in modules}
    indegree = {module: 0 for module in modules}

    for _ in range(e):
        parts = input().split()

        if len(parts) != 2:
            raise InvalidInputError("Invalid import relationship")

        module_a, module_b = parts
        validate_module_name(module_a)
        validate_module_name(module_b)

        if module_a not in modules or module_b not in modules:
            raise InvalidInputError("Import refers to an unknown module")

        # module_a imports module_b, so module_b must load first.
        # Set automatically ignores duplicate edges.
        if module_a not in graph[module_b]:
            graph[module_b].add(module_a)
            indegree[module_a] += 1

    return modules, graph, indegree


def find_loading_order(modules, graph, indegree):
    """
    Perform lexicographically smallest topological sorting.
    Returns the order and the remaining nodes if a cycle exists.
    """

    # Min-heap ensures lexicographically smallest module is selected.
    heap = []

    for module in modules:
        if indegree[module] == 0:
            heapq.heappush(heap, module)

    order = []

    while heap:
        current = heapq.heappop(heap)
        order.append(current)

        # Removing current may make dependent modules available.
        for dependent in graph[current]:
            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                heapq.heappush(heap, dependent)

    remaining = {
        module for module in modules
        if indegree[module] > 0
    }

    return order, remaining


def find_cycle(graph, remaining):
    """Find one directed cycle using iterative DFS."""

    color = {module: 0 for module in remaining}
    parent = {}

    for start in sorted(remaining):
        if color[start] != 0:
            continue

        color[start] = 1
        parent[start] = None

        # (node, next-neighbor-index)
        stack = [(start, 0)]

        while stack:
            current, index = stack[-1]
            neighbours = list(graph[current])

            if index >= len(neighbours):
                color[current] = 2
                stack.pop()
                continue

            next_node = neighbours[index]
            stack[-1] = (current, index + 1)

            if next_node not in remaining:
                continue

            if color[next_node] == 0:
                # Tree edge in DFS.
                parent[next_node] = current
                color[next_node] = 1
                stack.append((next_node, 0))

            elif color[next_node] == 1:
                # Back edge means a cycle has been found.
                cycle = [next_node]
                node = current

                while node != next_node:
                    cycle.append(node)
                    node = parent[node]

                cycle.append(next_node)
                cycle.reverse()

                return cycle

    return []


def main():
    try:
        first_line = input().split()

        if len(first_line) != 2:
            raise InvalidInputError("First line must contain n and e")

        n, e = map(int, first_line)

        modules, graph, indegree = build_dependency_graph(n, e)

        order, remaining = find_loading_order(
            modules, graph, indegree
        )

        if not remaining:
            print(" ".join(order))
        else:
            cycle = find_cycle(graph, remaining)

            print("CYCLE")

            if cycle:
                print(" ".join(cycle))

    except ValueError:
        print("INVALID INPUT")
    except InvalidInputError as error:
        print("INVALID INPUT:", error)


if __name__ == "__main__":
    main()