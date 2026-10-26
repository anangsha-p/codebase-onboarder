import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

MAX_LINES = 100      # functions longer than this get split
PIECE_LINES = 60     # size of each piece
BLOCK_LINES = 50     # for files with no functions

def make_chunk(lines, start, end, path, name, kind):
    """start/end are 1-based, inclusive."""
    return {
        "code": "\n".join(lines[start - 1:end]),
        "path": path,
        "start": start,
        "end": end,
        "language": "python",
        "name": name,
        "kind": kind,
    }

def split_long(lines, start, end, path, name, kind):
    """Split a long span into ~PIECE_LINES pieces, merging a tiny tail."""
    if end - start + 1 <= MAX_LINES:
        return [make_chunk(lines, start, end, path, name, kind)]
    ranges = []
    s = start
    while s <= end:
        e = min(s + PIECE_LINES - 1, end)
        ranges.append([s, e])
        s = e + 1
    # merge a tiny last piece into the previous one
    if len(ranges) > 1 and ranges[-1][1] - ranges[-1][0] + 1 < 15:
        ranges[-2][1] = ranges[-1][1]
        ranges.pop()
    return [
        make_chunk(lines, a, b, path, f"{name} (part {i})", kind)
        for i, (a, b) in enumerate(ranges, 1)
    ]

def unwrap(node):
    """A decorated function/class is wrapped; return the inner definition."""
    if node.type == "decorated_definition":
        return node.child_by_field_name("definition")
    return node

def collect(node, lines, path, class_stack, chunks, covered):
    for child in node.children:
        target = unwrap(child)
        if target is None:
            continue
        # use the outer node's range so decorators are included
        start = child.start_point[0] + 1
        end = child.end_point[0] + 1

        if target.type == "function_definition":
            name = target.child_by_field_name("name").text.decode()
            full = ".".join(class_stack + [name])
            kind = "method" if class_stack else "function"
            chunks.extend(split_long(lines, start, end, path, full, kind))
            covered.update(range(start, end + 1))
            # nested functions stay inside the parent chunk (no recursion)

        elif target.type == "class_definition":
            cname = target.child_by_field_name("name").text.decode()
            full = ".".join(class_stack + [cname])
            body = target.child_by_field_name("body")
            # class header = from class line to the line before the first member
            first_member = None
            for m in body.children:
                if unwrap(m) is not None and unwrap(m).type in ("function_definition", "class_definition"):
                    first_member = m.start_point[0] + 1
                    break
            header_end = (first_member - 1) if first_member else end
            if header_end >= start:
                chunks.extend(split_long(lines, start, header_end, path, f"{full} (class header)", "class"))
            covered.update(range(start, header_end + 1))
            collect(body, lines, path, class_stack + [cname], chunks, covered)

def chunk_python_file(path, display_path=None):
    display_path = display_path or path
    code = open(path, "rb").read()
    text = code.decode("utf-8", errors="replace")
    lines = text.split("\n")
    tree = parser.parse(code)

    chunks = []
    covered = set()
    collect(tree.root_node, lines, display_path, [], chunks, covered)

    # module header: everything not inside a function/class (imports, constants)
    leftover = [i for i in range(1, len(lines) + 1) if i not in covered and lines[i - 1].strip()]
    if not chunks:
        # no functions at all: split into fixed blocks
        s = 1
        while s <= len(lines):
            e = min(s + BLOCK_LINES - 1, len(lines))
            if "".join(lines[s - 1:e]).strip():
                chunks.append(make_chunk(lines, s, e, display_path, f"block {s}-{e}", "block"))
            s = e + 1
    elif leftover:
        first, last = leftover[0], leftover[-1]
        header_code = "\n".join(lines[i - 1] for i in leftover)
        chunks.insert(0, {
            "code": header_code[:4000],
            "path": display_path,
            "start": first,
            "end": last,
            "language": "python",
            "name": "module header",
            "kind": "module",
        })
    return chunks

if __name__ == "__main__":
    for c in chunk_python_file(sys.argv[1]):
        print(f"{c['kind']:9} {c['name']:45} lines {c['start']}-{c['end']}")