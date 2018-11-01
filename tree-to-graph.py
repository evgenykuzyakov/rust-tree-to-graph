#!/usr/local/bin/python3

# Use this command to generate a graph for package `srml-contract` crate
# cargo +nightly tree -p srml-contract --prefix-depth | ../tree-to-graph/tree-to-graph.py | dot -Tpng > /tmp/dep.png;  open /tmp/dep.png

import sys
import os

def main():

    node_ids = {}
    nodes = []
    edges = []
    internal = set()

    def get_node_id(s):
        if s in node_ids:
            return node_ids[s]
        node_ids[s] = len(nodes)
        nodes.append(s)
        return len(nodes) - 1

    stack = []
    with sys.stdin as f:
        for line in f:
            parts = line.split(' ')
            depth, name, version = int(parts[0]), parts[1], parts[2]
            name += " " + version.strip()
            node_id = get_node_id(name)
            while depth < len(stack):
                stack.pop()
            add_edges = len(parts) >= 4 and parts[3].startswith("(file")
            if add_edges:
                internal.add(node_id)
            if depth > 0 and stack[-1][1]:
                edges.append((stack[-1][0], node_id))
            stack.append((node_id, add_edges))

    print("digraph dependencies {")
    print("    rankdir=LR")
    visited_nodes = set(x[0] for x in edges).union([x[1] for x in edges])
    for node_id in visited_nodes:
        print("    N%d[label=\"%s\",color=%s];" % (node_id, nodes[node_id], "red" if node_id in internal else "green"))
    for from_id, to_id in edges:
        print("    N%d -> N%d[label=\"\"];" % (from_id, to_id))
    print("}")


if __name__ == "__main__":
    sys.exit(main())