import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def walk(node, found):
    if node.type in ("function_definition", "class_definition"):
        name = node.child_by_field_name("name").text.decode()
        found.append((node.type, name, node.start_point[0] + 1, node.end_point[0] + 1))
    for child in node.children:
        walk(child, found)

path = sys.argv[1]
code = open(path, "rb").read()
tree = parser.parse(code)

found = []
walk(tree.root_node, found)
for kind, name, start, end in found:
    print(f"{kind:20} {name:30} lines {start}-{end}")