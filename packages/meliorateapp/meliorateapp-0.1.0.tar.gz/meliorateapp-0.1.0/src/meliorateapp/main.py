import sys
import clang.cindex
from jinja2 import Template
from pathlib import Path

main_template = """\
#include <stdio.h>

int MELIORATE_NUM_TEST_FUNCTIONS = {{num_functions}};
bool meliorate_stop_on_error = false;

{% for func in functions %}
extern void {{ func[0] }}();{% endfor %}

void (*meliorate_test_functions[])() = {
{% for func in functions %}    &{{ func[0] }}{{ "," if not loop.last }}
{% endfor %}};

const char* meliorate_test_names[] = {
{% for func in functions %}    "{{ func[0] }}"{{ "," if not loop.last }}
{% endfor %}};
"""


def find_test_functions(tu):
    top_level_items = tu.cursor.get_children()

    functions = []

    for node in top_level_items:
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            if not node.spelling.startswith("test"):
                # print(f"Not a test function: {node.spelling}")
                continue

            if node.storage_class == clang.cindex.StorageClass.STATIC:
                print(f'Function starts with "test" but is static: {node.spelling} line: {node.location.line}')
                continue

            print(f"Found test function {node.spelling} line: {node.location.line}")
            functions.append((node.spelling, node.location.line))

    return functions


def script_entry():
    functions = []
    target_path = Path(sys.argv[1])

    assert target_path.exists(), f"The path {str(target_path.resolve())} does not exist."
    print(f"{str(target_path.resolve())}")

    file_paths = list(target_path.glob("*.cpp"))

    # Check files exist before we begin processing.
    for fp in file_paths:
        assert fp.exists(), f"File {str(fp)} does not exist."

    for fp in file_paths:
        if fp.name == "meliorate_gen.cpp":
            continue

        index = clang.cindex.Index.create()
        tu = index.parse(str(fp))
        functions += find_test_functions(tu)

    data = {
        "functions": functions,
        "num_functions": len(functions)
    }

    t = Template(main_template)
    render = t.render(data)
    print(render)

    out_path = Path(target_path) / "meliorate_gen.cpp"
    assert out_path.parent.exists(), f"The parent directory for {str(out_path)} does not exist."
    out_path.write_text(render)


if __name__ == '__main__':
    script_entry()
