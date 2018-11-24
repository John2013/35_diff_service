def swap(list, index1, index2):
    list[index1], list[index2] = list[index2], list[index1]
    return list


def similize(text1, text2):
    text1_lines = text1.splitlines(True)
    text2_lines = text2.splitlines(True)

    for text1_line_number, text1_line in enumerate(text1_lines):
        if text1_line == text2_lines[text1_line_number]:
            continue

        for text2_line_number, text2_line in enumerate(text2_lines):
            if text1_line_number == text2_line_number:
                continue

            if text1_line == text2_line:
                text1_lines = \
                    swap(text1_lines, text1_line_number, text2_line_number)

    return text1_lines


if __name__ == '__main__':
    text1 = '111\n222\n333\n444\n555'
    text2 = '111\n333\n222\n555\n441'

    print(similize(text1, text2))
