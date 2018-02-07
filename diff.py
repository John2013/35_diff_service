#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""
from operator import itemgetter

import difflib
import string


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
        except IndexError:
            pass

    letters_count = max(len(str1), len(str2))
    return equal_letters_count / letters_count


def text_diff(text_from, text_to):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    text_to = similize(text_from, text_to)
    out = []
    text_from, text_to = html2list(text_from), html2list(text_to)
    try:  # autojunk can cause malformed HTML, but also speeds up processing.
        matcher = difflib.SequenceMatcher(
            None,
            text_from,
            text_to,
            autojunk=False
        )
    except TypeError:
        matcher = difflib.SequenceMatcher(None, text_from, text_to)
    for action, from_1, to_1, from_2, to_2 in matcher.get_opcodes():
        if action == "replace":
            # @@ need to do something more complicated here
            # call textDiff but not for html, but for some html... ugh
            # gonna cop-out for now
            out.append(
                '<del class="diff modified">{del_}</del>'
                '<ins class="diff modified">{ins}</ins>'.format(
                    del_=''.join(text_from[from_1:to_1]),
                    ins=''.join(text_to[from_2:to_2])
                )
            )
        elif action == "delete":
            out.append(
                '<del class="diff">{}</del>'.format(
                    ''.join(text_from[from_1:to_1])
                )
            )
        elif action == "insert":
            out.append(
                '<ins class="diff">{}</ins>'.format(
                    ''.join(text_to[from_2:to_2])
                )
            )
        elif action == "equal":
            out.append(
                ''.join(
                    text_to[from_2:to_2]
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


def similize(text1, text2):
    moove_map = []
    similized_text2 = ''
    text1_str_list = text1.split('\n')
    text2_str_list = text2.split('\n')
    for index1, string1 in enumerate(text1_str_list):
        equality_map = []
        for index2, string2 in enumerate(text2_str_list):
            equality_map.append(
                (index1, index2, get_equality(string1, string2))
            )
        result_string_tuple = max(equality_map, key=itemgetter(2))
        # print(result_string_tuple)
        moove_map.append(result_string_tuple)
    for index_tuple in moove_map:
        similized_text2 += text2_str_list[index_tuple[1]]
        if index_tuple[0] + 1 < len(moove_map):
            similized_text2 += '\n'
    return similized_text2


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
    print(
        text_diff(
            text1,
            text2
        )
    )
