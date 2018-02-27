#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""
import difflib
import string
from similize import similize


def get_config(config):
    default_config = {
        "deleted_element": "del",
        "inserted_element": "ins",
        "modified_class": "diff modified",
        "deleted_class": "diff deleted",
        "inserted_class": "diff inserted",
    }
    if config is None:
        config = {}

    for key, default_value in default_config.items():
        if key not in config:
            config[key] = default_value

    return config


def update_opcodes(
    out,
    text1,
    text2,
    action,
    from_1,
    to_1,
    from_2,
    to_2,
    config
):
    if action == "replace":
        out.append(
            "<{del_el} class=\"{mod_class}\">{del_str}</{del_el}>"
            "<{ins_el} class=\"{mod_class}\">{ins_str}</{ins_el}>".format(
                del_el=config["deleted_element"],
                ins_el=config["inserted_element"],
                mod_class=config["modified_class"],
                del_str="".join(text1[from_1:to_1]),
                ins_str="".join(text2[from_2:to_2])
            )
        )
    elif action == "delete":
        out.append(
            "<{del_el} class=\"{del_class}\">{del_str}</{del_el}>".format(
                del_str="".join(text1[from_1:to_1]),
                del_el=config["deleted_element"],
                del_class=config["deleted_class"]
            )
        )
    elif action == "insert":
        out.append(
            "<{ins_el} class=\"{ins_class}\">{ins_str}</{ins_el}>".format(
                ins_str="".join(text2[from_2:to_2]),
                ins_el=config["inserted_element"],
                ins_class=config["inserted_class"]
            )
        )
    elif action == "equal":
        out.append(
            "".join(
                text2[from_2:to_2]
            )
        )
    return out


def text_diff(text1, text2, config=None):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    # text2 = similize(text1, text2)

    config = get_config(config)

    out = []
    text1, text2 = html2list(text1), html2list(text2)
    try:
        matcher = difflib.SequenceMatcher(None, text1, text2, autojunk=False)
    except TypeError:
        matcher = difflib.SequenceMatcher(None, text1, text2)
    for action, from_1, to_1, from_2, to_2 in matcher.get_opcodes():
        out = update_opcodes(
            out,
            text1,
            text2,
            action,
            from_1,
            to_1,
            from_2,
            to_2,
            config
        )
    return "".join(out)


def html2list_tag(char, cur, out, mode, b):
    if char == ">":
        if b:
            cur += "]"
        else:
            cur += char
        out.append(cur)
        cur = ""
        mode = "char"
    else:
        cur += char
    return char, cur, out, mode


def html2list_char(char, cur, out, mode, b):
    if char == "<":
        out.append(cur)
        if b:
            cur = "["
        else:
            cur = char
        mode = "tag"
    elif char in string.whitespace:
        out.append(cur + char)
        cur = ""
    else:
        cur += char
    return char, cur, out, mode


def html2list(text, b=0):
    mode = "char"
    cur = ""
    out = []
    for char in text:
        if mode == "tag":
            char, cur, out, mode = html2list_tag(char, cur, out, mode, b)

        elif mode == "char":
            char, cur, out, mode = html2list_char(char, cur, out, mode, b)
    out.append(cur)
    return list(filter(lambda x: x is not "", out))


if __name__ == "__main__":
    import sys

    first_arg, last_arg = 1, 2
    try:
        a, b = sys.argv[first_arg:last_arg + 1]
    except ValueError:
        print("htmldiff: highlight the differences between two html files")
        print("usage: {} a b".format(sys.argv[0]))
        sys.exit(1)
    text1 = open(a, encoding="utf-8").read()
    text2 = open(b, encoding="utf-8").read()
    print(text1, text2, sep="\n")
    print("new text 2:")
    print(text2)
    print(
        text_diff(
            text1,
            text2
        )
    )
