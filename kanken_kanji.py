
import csv


def normalize_level(level):
    if level in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}:
        return level
    elif level == '1.5':
        return '1_5'
    elif level == '2.5':
        return '2_5'
    else:
        raise RuntimeError('Incorrect level: ' + level)


class KankenKanji:
    def __init__(self):
        self.kanji_dict = {}
        with open('Kanken levels.csv',  newline='', encoding='utf8') as csvfile:
            kanjireader = csv.reader(csvfile, dialect='unix')
            next(kanjireader) # headers
            for row in kanjireader:
                kanji, level = row[1], row[5]
                if len(kanji):
                    try:
                        self.kanji_dict[kanji] = normalize_level(level)
                    except Exception as e:
                        print('Kanji', kanji)
                        raise e

    def get_level(self, kanji):
        return self.kanji_dict.get(kanji, '')

