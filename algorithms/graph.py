"""Graph algorithms for prerequisite validation."""


def build_prereq_graph(courses):
    """Return {course_code: [prerequisite codes]}."""
    return {c["course_code"]: list(c.get("prerequisites", [])) for c in courses}


def all_prerequisites(course_code, graph):
    """Return the transitive set of prerequisite course codes."""
    result = set()
    stack = list(graph.get(course_code, []))
    while stack:
        code = stack.pop()
        if code in result:
            continue
        result.add(code)
        stack.extend(graph.get(code, []))
    return result


def prerequisites_met(course_code, completed, graph):
    """True if every transitive prerequisite is in `completed`."""
    return all_prerequisites(course_code, graph).issubset(set(completed))


def has_cycle(graph):
    """DFS cycle detection (invalid curriculum guard)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}

    def visit(node):
        color[node] = GRAY
        for nxt in graph.get(node, []):
            c = color.get(nxt, WHITE)
            if c == GRAY:
                return True
            if c == WHITE and visit(nxt):
                return True
        color[node] = BLACK
        return False

    for node in list(graph):
        if color.get(node, WHITE) == WHITE and visit(node):
            return True
    return False


def topological_sort(graph):
    """Order course codes so prerequisites come before dependents."""
    visited, order = set(), []

    def visit(node):
        if node in visited:
            return
        visited.add(node)
        for nxt in graph.get(node, []):
            visit(nxt)
        order.append(node)

    for node in graph:
        visit(node)
    return order