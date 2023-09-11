from jamo import (
    h2j,
    is_hangul_char,
    is_jamo,
    is_jamo_modern,
    j2hcj
)


def get_choseong(string):
    choseong_list = []

    for item in string:
        if not is_hangul_char(item):
            continue

        hcj = j2hcj(h2j(item))
        if not is_jamo(hcj[0]) or not is_jamo_modern(hcj[0]):
            continue
        choseong_list.append(hcj[0])

    return ''.join(choseong_list)
