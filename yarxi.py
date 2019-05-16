
import romkan
import re
import operator


re_header = re.compile("""^(\d{2})  # stroke number
                          (\d{2})  # order  1-9 jouyou, 10 +
                          (\d{5})  # unicode
                          (\d+)(/\d+)? # Bushu
                          (.*)$  # Russian nickname
                          """,
                       re.VERBOSE)
re_onyomi_split = re.compile(';|,')


def get_kanji_nickname(header):

    m = re_header.match(header)
    if m is not None:
        #print(m.groups())
        _, order, code, _,  _, nickname = m.groups()
        kanji = chr(int(code))
        return kanji, nickname, int(order)
    else:
        raise RuntimeError(header + ' does not match the pattern')


def onromaji_to_katakana(reading):
    return reading
    return romkan.to_katakana(reading).replace(':', 'ウ')


def get_onyomi(onyomi_str):
    if ',' in  onyomi_str:
        a = 1
    readings = re_onyomi_split.split(onyomi_str)
    l = (reading.strip('*') for reading in readings)
    l = (onromaji_to_katakana(reading) for reading in l)
    return list(l)


kanji_table = []
with open('jr_kan.txt', mode='r', encoding='cp1251') as kanji_file:
    lines = kanji_file.readlines()
    creation_data = lines[0]
    line_number = int(lines[1])
    count = 1
    for line in lines[2:]:
        components = line.split('`')
        header = components[0]
        try:
            kanji, nickname, order = get_kanji_nickname(header)
        except Exception as e:
            print(header, line)
        onyomi = get_onyomi(components[1])
        #print(code)

        if order < 15:
            kanji_table.append((kanji, nickname, onyomi, order))
        count += 1
        if count > 30000 or count+1 >= line_number:
            break

kanji_table= sorted(kanji_table, key=operator.itemgetter(3))
for kanji in kanji_table:
    print(*kanji)
