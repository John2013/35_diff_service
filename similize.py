from operator import itemgetter


# def get_equality(str1: str, str2: str)->float:
#
#     if len(str1) != len(str2):
#         small_str = min(str1, str2)
#         big_str = max(str1, str2)
#     else:
#         small_str = str1
#         big_str = str2
#
#     equal_letters_count = 0
#     for number, letter in enumerate(small_str):
#         try:
#             if letter == big_str[number]:
#                 equal_letters_count += 1
#             else:
#                 break
#         except IndexError:
#             pass
#
#     letters_count = max(len(str1), len(str2))
#     return equal_letters_count / letters_count
#
#
# def get_equalitiest_str_number(string1, text2_str_list):
#     equality_map = []
#     for index2, string2 in enumerate(text2_str_list):
#         equality_map.append(
#             (index2, get_equality(string1, string2))
#         )
#     most_similar_index, equality = max(equality_map, key=itemgetter(1))
#     if equality == 0:
#         return None
#     else:
#         return most_similar_index
#
#
# def compare_strings(list1, list2, index, index1_shift):
#     continue_bool = False
#     index1 = index + index1_shift
#     try:
#         str1 = list1[index1]
#         str2 = list2[index]
#     except IndexError:
#         continue_bool = True
#         return list1, list2, index, index1_shift, continue_bool
#     if str1 == str2:
#         continue_bool = True
#         return list1, list2, index, index1_shift, continue_bool
#     else:
#         index2 = get_equalitiest_str_number(str1, list2)
#         if index2 is None:
#             index1_shift += 1
#             continue_bool = True
#             return list1, list2, index, index1_shift, continue_bool
#         elif index > index2:
#             list2[index1], list2[index2] = list2[index2], list2[index1]
#     return list1, list2, index, index1_shift, continue_bool
#
#
# def similize(text1, text2):
#     list1, list2, index1_shift = text1.split("\n"), text2.split("\n"), 0
#     for index in range(max(len(list1), len(list2))):
#         list1, list2, index, index1_shift, continue_bool = compare_strings(
#             list1,
#             list2,
#             index,
#             index1_shift
#         )
#         if continue_bool:
#             continue
#     return "\n".join(list2)


def similize(text1, text2):
    # text1_rows = text1.split('\n')
    # text2_rows = text2.split('\n')
    # somolized_text2_rows = []
    # row_index_shift = 0
    #
    # for text1_row_index, text1_row in enumerate(text1_rows):
    #     for text2_row_index, text2_row in enumerate(text2_rows):
    #         if text1_row_index + row_index_shift == text2_row_index \
    #                 and text1_row != text2_row:
    #             pass
    #             text2_rows[text2_row_index + row_index_shift] = text1_row
    return text2


if __name__ == '__main__':
    text1 = '111\n222\n333\n444\n555'
    text2 = '111\n333\n222\n555\n441'

    print(similize(text1, text2))
