from collections import defaultdict


def simple_cycles(G):
    """Yield every elementary cycle in G exactly once."""

    def unblock(thisnode, blocked, B):
        stack = {thisnode}
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()

    # Create a working copy of the graph
    G = {v: set(nbrs) for (v, nbrs) in G.items()}
    sccs = strongly_connected_components(G)

    while sccs:
        scc = sccs.pop()
        startnode = scc.pop()
        path = [startnode]
        blocked = set()
        B = defaultdict(set)
        blocked.add(startnode)
        stack = [(startnode, list(G[startnode]))]

        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs:
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield path[:]
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append((nextnode, list(G[nextnode])))
                    blocked.add(nextnode)
                    continue
            if not nbrs:
                if thisnode in path:
                    unblock(thisnode, blocked, B)
                else:
                    for nbr in G[thisnode]:
                        B[nbr].add(thisnode)
                stack.pop()
                path.pop()

        remove_node(G, startnode)
        H = subgraph(G, set(scc))
        sccs.extend(strongly_connected_components(H))


def strongly_connected_components(graph):
    """Identify strongly connected components using Tarjan's algorithm."""
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []

    def strong_connect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        for successor in graph[node]:
            if successor not in index:
                strong_connect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in stack:
                lowlink[node] = min(lowlink[node], index[successor])

        if lowlink[node] == index[node]:
            connected_component = []
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node:
                    break
            result.append(connected_component)

    for node in graph:
        if node not in index:
            strong_connect(node)

    return result


def remove_node(G, target):
    """Remove a node from the graph."""
    G.pop(target, None)
    for nbrs in G.values():
        nbrs.discard(target)


def subgraph(G, vertices):
    """Get the subgraph of G induced by vertices."""
    return {v: G[v] & vertices for v in vertices}


def cycle_printing_fn(graph):
    """Print all cycles in the graph."""
    if not graph:
        print("No cycles detected as the graph is empty.")
        return

    cycle_no = 0
    for cycle in simple_cycles(graph):
        string = " -> ".join(f"T{ele + 1}" for ele in cycle)
        print(f"Cycle #{cycle_no + 1} => {string}")
        cycle_no += 1
