#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""
import difflib
import string
from operator import itemgetter


def get_equality(str1: str, str2: str)->float:

    if len(str1) != len(str2):
        small_str = min(str1, str2)
        big_str = max(str1, str2)
    else:
        small_str = str1
        big_str = str2

    equal_letters_count = 0
    for number, letter in enumerate(small_str):
        try:
            if letter == big_str[number]:
                equal_letters_count += 1
            else:
                break
        except IndexError:
            pass

    letters_count = max(len(str1), len(str2))
    return equal_letters_count / letters_count


def get_max_equality_string_number(string1, text2_str_list, min_index=0):
    equality_map = []
    for index2, string2 in enumerate(text2_str_list):
        equality_map.append(
            (index2, get_equality(string1, string2))
        )
    most_similar_index, equality = max(equality_map, key=itemgetter(1))
    if equality == 0:
        return None
    else:
        return most_similar_index


def similize(text1, text2):
    text1_str_list = text1.split('\n')
    text2_str_list = text2.split('\n')
    index1_shift = 0
    for index in range(max(len(text1_str_list), len(text2_str_list))):
        try:
            str1 = text1_str_list[index + index1_shift]
            str2 = text2_str_list[index]
        except IndexError:
            continue
        if str1 == str2:
            continue
        else:
            most_similar_string_index = get_max_equality_string_number(
                str1,
                text2_str_list,
                index
            )
            if most_similar_string_index is None:
                index1_shift += 1
                continue
            elif index > most_similar_string_index:
                text2_str_list[index + index1_shift], text2_str_list[
                    most_similar_string_index
                ] = text2_str_list[most_similar_string_index], text2_str_list[
                    index + index1_shift
                ]
    return "\n".join(text2_str_list)


def text_diff(text1, text2, config=None):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    text2 = similize(text1, text2)

    config_default = {
        "deleted_element": "del",
        "inserted_element": "ins",
        "modified_class": "diff modified",
        "deleted_class": "diff deleted",
        "inserted_class": "diff inserted",
    }

    if config is None:
        config = {}

    for key, default_value in config_default.items():
        if key not in config:
            config[key] = default_value

    out = []
    text1, text2 = html2list(text1), html2list(text2)
    try:
        matcher = difflib.SequenceMatcher(
            None,
            text1,
            text2,
            autojunk=False
        )
    except TypeError:
        matcher = difflib.SequenceMatcher(None, text1, text2)
    for action, from_1, to_1, from_2, to_2 in matcher.get_opcodes():
        if action == "replace":
            # @@ need to do something more complicated here
            # call textDiff but not for html, but for some html... ugh
            # gonna cop-out for now
            out.append(
                '<{del_el} class="{mod_class}">{del_str}</{del_el}>'
                '<{ins_el} class="{mod_class}">{ins_str}</{ins_el}>'.format(
                    del_el=config["deleted_element"],
                    ins_el=config["inserted_element"],
                    mod_class=config["modified_class"],
                    del_str=''.join(text1[from_1:to_1]),
                    ins_str=''.join(text2[from_2:to_2])
                )
            )
        elif action == "delete":
            out.append(
                '<{del_el} class="{del_class}">{del_str}</{del_el}>'.format(
                    del_str=''.join(text1[from_1:to_1]),
                    del_el=config["deleted_element"],
                    del_class=config["deleted_class"]
                )
            )
        elif action == "insert":
            out.append(
                '<{ins_el} class="{ins_class}">{ins_str}</{ins_el}>'.format(
                    ins_str=''.join(text2[from_2:to_2]),
                    ins_el=config["inserted_element"],
                    ins_class=config["inserted_class"]
                )
            )
        elif action == "equal":
            out.append(
                ''.join(
                    text2[from_2:to_2]
                )
            )
        else:
            raise "Um, something's broken. I didn't expect a {}.'".format(
                action
            )
    return ''.join(out)


def html2list(text, b=0):
    mode = 'char'
    cur = ''
    out = []
    for char in text:
        if mode == 'tag':
            if char == '>':
                if b:
                    cur += ']'
                else:
                    cur += char
                out.append(cur)
                cur = ''
                mode = 'char'
            else:
                cur += char
        elif mode == 'char':
            if char == '<':
                out.append(cur)
                if b:
                    cur = '['
                else:
                    cur = char
                mode = 'tag'
            elif char in string.whitespace:
                out.append(cur + char)
                cur = ''
            else:
                cur += char
    out.append(cur)
    return list(filter(lambda x: x is not '', out))


def get_text_from_strings_sequense(string_list, strings_sequense):
    result_text = ""
    for list_number, string_number in enumerate(strings_sequense):
        result_text += string_list[string_number]
        if list_number + 1 < len(strings_sequense):
            result_text += "\n"
    return result_text


if __name__ == '__main__':
    import sys

    first_arg, last_arg = 1, 2
    try:
        a, b = sys.argv[first_arg:last_arg + 1]
    except ValueError:
        print("htmldiff: highlight the differences between two html files")
        print("usage: {} a b".format(sys.argv[0]))
        sys.exit(1)
    text1 = open(a, encoding='utf-8').read()
    text2 = open(b, encoding='utf-8').read()
    print(text1, text2, sep='\n')
    print("new text 2:")
    print(text2)
    print(
        text_diff(
            text1,
            text2
        )
    )
