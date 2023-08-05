# -*- coding: utf-8 -*-
# 0.1  = 2020-07-31 = dict for using as: from n0utils.translate import translit_dict;dst_str = src_str.translate(translit_dict)

translit_dict = {
# https://en.wikipedia.org/wiki/Dotted_and_dotless_I
    ord('İ'): 'I',
    ord('ı'): 'i',
# Cyrillic languages:
# BG: https://ru.wikipedia.org/wiki/Болгарский_язык
#     https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA
# BY: https://ru.wikipedia.org/wiki/Белорусский_алфавит
#     https://ru.wikipedia.org/wiki/%D0%91%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82
# KZ: https://ru.wikipedia.org/wiki/Казахская_письменность
#     https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D0%B8%D1%81%D1%8C%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C
# MD: https://ru.wikipedia.org/wiki/Молдавский_алфавит
#     https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D0%BB%D0%B4%D0%B0%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82
# MK: https://ru.wikipedia.org/wiki/Македонский_язык
#     https://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D0%BA%D0%B5%D0%B4%D0%BE%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA
# MN: https://ru.wikipedia.org/wiki/Монгольский_алфавит
#     https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D0%BD%D0%B3%D0%BE%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82    
# RU: https://ru.wikipedia.org/wiki/Русский_язык
#     https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA
# SR: https://ru.wikipedia.org/wiki/Сербский_кириллический_алфавит
#     https://ru.wikipedia.org/wiki/%D0%A1%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82
# TG: https://ru.wikipedia.org/wiki/Таджикская_письменность
#     https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B4%D0%B6%D0%B8%D0%BA%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D0%B8%D1%81%D1%8C%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C
# UK: https://ru.wikipedia.org/wiki/Украинский_язык
#     https://ru.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA
    ord('А'):'A',   ord('а'):'a',
    ord('Б'):'B',   ord('б'):'b',
    ord('В'):'V',   ord('в'):'v',
    ord('Г'):'G',   ord('г'):'g',
    ord('Ғ'):'G',   ord('ғ'):'g',   # KZ
    ord('Ѓ'):'G',   ord('ѓ'):'g',   # MK
    ord('Ғ'):'G',   ord('ғ'):'g',   # TG
    ord('Ґ'):'G',   ord('ґ'):'g',   # UK
    ord('Д'):'D',   ord('д'):'d',
    ord('Ђ'):'D',   ord('ђ'):'d',   # SR
    ord('Е'):'E',   ord('е'):'e',
    ord('Ё'):'JO',  ord('ё'):'jo',  # BY+KZ+RU
    ord('Ә'):'E',   ord('ә'):'e',   # KZ sounds like russian Э
    ord('Є'):'E',   ord('є'):'e',   # UK
    ord('Ӂ'):'DZH', ord('ӂ'):'dzh', # MD
    ord('Ж'):'ZH',  ord('ж'):'zh',
    ord('З'):'Z',   ord('з'):'z',
    ord('Ѕ'):'S',   ord('ѕ'):'s',   # MK
    ord('И'):'I',   ord('и'):'i',
    ord('Й'):'Y',   ord('й'):'y',   # BG+BY+KZ+MD+MN+RU+TG+UK (-MK-SR)
    ord('Ӣ'):'Y',   ord('ӣ'):'y',   # TG
    ord('І'):'I',   ord('і'):'i',   # BY+KZ+UK
    ord('Ї'):'Y',   ord('ї'):'y',   # UK
    ord('Ј'):'Ј',   ord('ј'):'ј',   # MK+SR
    ord('К'):'K',   ord('к'):'k',
    ord('Ќ'):'K',   ord('ќ'):'k',   # MK
    ord('Қ'):'K',   ord('қ'):'k',   # KZ+TG
    ord('Л'):'L',   ord('л'):'l',
    ord('Љ'):'L',   ord('љ'):'l',   # MK+SR
    ord('М'):'M',   ord('м'):'m',
    ord('Н'):'N',   ord('н'):'n',
    ord('Ң'):'N',   ord('ң'):'n',   # KZ
    ord('Њ'):'N',   ord('њ'):'n',   # MK+SR
    ord('О'):'O',   ord('о'):'o',
    ord('Ө'):'O',   ord('ө'):'o',   # KZ+MN sounds like russian О and Э
    ord('П'):'P',   ord('п'):'p',
    ord('Р'):'R',   ord('р'):'r',
    ord('С'):'S',   ord('с'):'s',
    ord('Т'):'T',   ord('т'):'t',
    ord('Ћ'):'T',   ord('ћ'):'t',   # SR
    ord('У'):'U',   ord('у'):'u',
    ord('Ў'):'U',   ord('ў'):'u',   # BY
    ord('Ӯ'):'U',   ord('ӯ'):'u',   # TG
    ord('Ү'):'Y',   ord('ү'):'y',   # KZ+MN sounds like russian Ы
    ord('Ұ'):'O',   ord('ұ'):'o',   # KZ
    ord('Ф'):'F',   ord('ф'):'f',
    ord('Х'):'H',   ord('х'):'h',
    ord('Ҳ'):'H',   ord('ҳ'):'h',   # TG
    ord('Һ'):'H',   ord('һ'):'h',   # KZ
    ord('Ц'):'TS',  ord('ц'):'ts',
    ord('Ч'):'CH',  ord('ч'):'ch',
    ord('Ҷ'):'CH',  ord('ҷ'):'ch',  # TG
    ord('Џ'):'DZH', ord('џ'):'dzh', # MK+SR
    ord('Ш'):'SH',  ord('ш'):'sh',
    ord('Щ'):'SCH', ord('щ'):'sch', # BG+BY+KZ+MD+MN+RU+TG+UK (-MK-SR)
    ord('Ъ'):'',    ord('ъ'):'',    # BG+KZ+RU
    ord('’'):'',                    # BY
    ord('Ы'):'Y',   ord('ы'):'y',   # RU+BY+KZ+MD
    ord('Ь'):'',    ord('ь'):'',    # BG+BY+KZ+MD+MN+RU+TG+UK (-MK-SR)
    ord('Э'):'E',   ord('э'):'e',   # BY+KZ+MD+MN+RU+TG+UK (-MK-SR-BG)
    ord('Ю'):'JU',  ord('ю'):'ju',  # BG+BY+KZ+MD+MN+RU+TG+UK (-MK-SR)
    ord('Я'):'JA',  ord('я'):'ja',  # BG+BY+KZ+MD+MN+RU+TG+UK (-MK-SR)

# https://en.wikipedia.org/wiki/Diacritic
# 1.1) https://en.wikipedia.org/wiki/Acute_accent
    ord('̩'): '',                   # Acute_accent
    ord('́'): '',                   # Acute_accent
    ord('Á'): 'A',  ord('á'): 'a',  # Acute_accent
    ord('Ấ'): 'A',  ord('ấ'): 'a',  # Acute_accent
    ord('Ā'): 'A',  ord('ā'): 'a',  # Acute_accent
    ord('Ắ'): 'A',  ord('ắ'): 'a',  # Acute_accent
    ord('Ǻ'): 'A',  ord('ǻ'): 'a',  # Acute_accent
    ord('Ą'): 'A',  ord('ą'): 'a',  # Acute_accent
    ord('Ǽ'): 'A',  ord('ǽ'): 'a',  # Acute_accent
    ord('Ć'): 'C',  ord('ć'): 'c',  # Acute_accent
    ord('Ḉ'): 'C',  ord('ḉ'): 'c',  # Acute_accent
    ord('É'): 'E',  ord('é'): 'e',  # Acute_accent
    ord('Ế'): 'E',  ord('ế'): 'e',  # Acute_accent
    ord('Ḗ'): 'E',  ord('ḗ'): 'e',  # Acute_accent
    ord('Ė'): 'E',  ord('ė'): 'e',  # Acute_accent
    ord('Ę'): 'E',  ord('ę'): 'e',  # Acute_accent
    ord('É'): 'E',  ord('é'): 'e',  # Acute_accent
    ord('Ə'): 'E',  ord('ə'): 'e',  # Acute_accent
                    ord('ɚ'): 'e',  # Acute_accent
    ord('F'): 'F',  ord('f'): 'f',  # Acute_accent
    ord('Ǵ'): 'G',  ord('ǵ'): 'g',  # Acute_accent
    ord('Í'): 'I',  ord('í'): 'i',  # Acute_accent
    ord('Ī'): 'I',  ord('ī'): 'i',  # Acute_accent
    ord('Į'): 'I',  ord('į'): 'i',  # Acute_accent
    ord('Ḯ'): 'I',  ord('ḯ'): 'i',  # Acute_accent
                    ord('ȷ'): 'j',  # Acute_accent
    ord('Ḱ'): 'K',  ord('ḱ'): 'k',  # Acute_accent
    ord('Ĺ'): 'L',  ord('ĺ'): 'l',  # Acute_accent
    ord('Ḿ'): 'M',  ord('ḿ'): 'm',  # Acute_accent
    ord('Ń'): 'N',  ord('ń'): 'n',  # Acute_accent
    ord('Ó'): 'Ó',  ord('ó'): 'ó',  # Acute_accent
    ord('Ố'): 'Ố',  ord('ố'): 'ố',  # Acute_accent
    ord('Ớ'): 'Ớ',  ord('ớ'): 'ớ',  # Acute_accent
    ord('Ṍ'): 'O',  ord('ṍ'): 'o',  # Acute_accent
    ord('Ṓ'): 'O',  ord('ṓ'): 'o',  # Acute_accent
    ord('Ó'): 'O',  ord('ó'): 'o',  # Acute_accent
    ord('Ǫ'): 'O',  ord('ǫ'): 'o',  # Acute_accent
    ord('Ǿ'): 'O',  ord('ǿ'): 'o',  # Acute_accent
    ord('Ɔ'): 'O',  ord('ɔ'): 'o',  # Acute_accent
    ord('Ṕ'): 'P',  ord('ṕ'): 'p',  # Acute_accent
    ord('Ŕ'): 'R',  ord('ŕ'): 'r',  # Acute_accent
    ord('Ś'): 'S',  ord('ś'): 's',  # Acute_accent
    ord('Ṥ'): 'S',  ord('ṥ'): 's',  # Acute_accent
    ord('Ú'): 'U',  ord('ú'): 'u',  # Acute_accent
    ord('Ǘ'): 'U',  ord('ǘ'): 'u',  # Acute_accent
    ord('Ứ'): 'U',  ord('ứ'): 'u',  # Acute_accent
    ord('Ṹ'): 'U',  ord('ṹ'): 'u',  # Acute_accent
    ord('Ū'): 'U',  ord('ū'): 'u',  # Acute_accent
    ord('Ų'): 'U',  ord('ų'): 'u',  # Acute_accent
    ord('Ʌ'): 'U',  ord('ʌ'): 'u',  # Acute_accent
    ord('Ẃ'): 'W',  ord('ẃ'): 'w',  # Acute_accent
    ord('Ý'): 'Y',  ord('ý'): 'y',  # Acute_accent
    ord('Ȳ'): 'Y',  ord('ȳ'): 'y',  # Acute_accent
    ord('Ź'): 'Z',  ord('ź'): 'z',  # Acute_accent
    ord('Ά'): 'A',  ord('ά'): 'a',  # Acute_accent
    ord('Έ'): 'E',  ord('έ'): 'e',  # Acute_accent
    ord('Ή'): 'H',  ord('ή'): 'h',  # Acute_accent
    ord('Ί'): 'I',  ord('ί'): 'i',  # Acute_accent
    ord('ΐ'): 'i',                  # Acute_accent
    ord('Ό'): 'O',  ord('ό'): 'o',  # Acute_accent
    ord('Ύ'): 'Y',  ord('ύ'): 'y',  # Acute_accent
    ord('ΰ'): 'U',                  # Acute_accent
    ord('ϓ'): 'Y',                  # Acute_accent
    ord('Ώ'): 'O',  ord('ώ'): 'o',  # Acute_accent
    ord('Ѓ'): 'G',  ord('ѓ'): 'g',  # Acute_accent
    ord('Ќ'): 'K',  ord('ќ'): 'k',  # Acute_accent

# 1.2) https://en.wikipedia.org/wiki/Grave_accent
    ord('̀'): '',                    # Grave_accent
    ord('À'): 'A',  ord('à'): 'a',  # Grave_accent
    ord('Ầ'): 'A',  ord('ầ'): 'a',  # Grave_accent
    # ord('Ā'): 'A',  ord('ā'): 'a',  # Acute_accent => Grave_accent
    ord('Ằ'): 'A',  ord('ằ'): 'a',  # Grave_accent
    ord('Æ'): 'A',  ord('æ'): 'a',  # Grave_accent
    ord('È'): 'E',  ord('è'): 'e',  # Grave_accent
    ord('Ề'): 'E',  ord('ề'): 'e',  # Grave_accent
    ord('Ḕ'): 'E',  ord('ḕ'): 'e',  # Grave_accent
    ord('È'): 'E',  ord('è'): 'e',  # Grave_accent
    ord('Ì'): 'I',  ord('ì'): 'i',  # Grave_accent
    ord('Ǹ'): 'N',  ord('ǹ'): 'n',  # Grave_accent
    ord('Ò'): 'O',  ord('ò'): 'o',  # Grave_accent
    ord('Ờ'): 'O',  ord('ờ'): 'o',  # Grave_accent
    ord('Ồ'): 'O',  ord('ồ'): 'o',  # Grave_accent
    ord('Ṑ'): 'O',  ord('ṑ'): 'o',  # Grave_accent
    ord('Ù'): 'U',  ord('ù'): 'u',  # Grave_accent
    ord('Ǜ'): 'U',  ord('ǜ'): 'u',  # Grave_accent
    ord('Ừ'): 'U',  ord('ừ'): 'u',  # Grave_accent
    ord('Ẁ'): 'W',  ord('ẁ'): 'w',  # Grave_accent
    ord('Ỳ'): 'Y',  ord('ỳ'): 'y',  # Grave_accent
    ord('Ὰ'): 'A',  ord('ὰ'): 'a',  # Grave_accent
    ord('Ὲ'): 'E',  ord('ὲ'): 'e',  # Grave_accent
    ord('Ὴ'): 'H',  ord('ὴ'): 'h',  # Grave_accent
    ord('Ὶ'): 'I',  ord('ὶ'): 'i',  # Grave_accent
                    ord('ῒ'): 'i',  # Grave_accent
    ord('Ὸ'): 'O',  ord('ὸ'): 'o',  # Grave_accent
    ord('Ὺ'): 'Y',  ord('ὺ'): 'y',  # Grave_accent
                    ord('ῢ'): 'u',  # Grave_accent
    ord('Ὼ'): 'O',  ord('ὼ'): 'o',  # Grave_accent
    ord('Ѐ'): 'E',  ord('ѐ'): 'e',  # Grave_accent
    ord('Ѝ'): 'I',  ord('ѝ'): 'i',  # Grave_accent

# 1.3) https://en.wikipedia.org/wiki/circumflex
    ord('̂'): '',                   # Circumflex
    ord('̄'): '',                   # Circumflex
    ord('̌'): '',                   # Circumflex
    ord('̭'): '',                   # Circumflex
    ord('Â'): 'A',  ord('â'): 'a',  # Circumflex
    ord('Ấ'): 'A',  ord('ấ'): 'a',  # Circumflex
    ord('Ầ'): 'A',  ord('ầ'): 'a',  # Circumflex
    ord('Ẩ'): 'A',  ord('ẩ'): 'a',  # Circumflex
    ord('Ẫ'): 'A',  ord('ẫ'): 'a',  # Circumflex
    ord('Ậ'): 'A',  ord('ậ'): 'a',  # Circumflex
    ord('Ḇ'): 'B',  ord('ḇ'): 'b',  # Circumflex
    ord('Ĉ'): 'C',  ord('ĉ'): 'c',  # Circumflex
    ord('Ḓ'): 'D',  ord('ḓ'): 'd',  # Circumflex
    ord('Ḙ'): 'E',  ord('ḙ'): 'e',  # Circumflex
    ord('Ế'): 'E',  ord('ế'): 'e',  # Circumflex
    ord('Ề'): 'E',  ord('ề'): 'e',  # Circumflex
    ord('Ể'): 'E',  ord('ể'): 'e',  # Circumflex
    ord('Ē'): 'E',  ord('ē'): 'e',  # Circumflex
    ord('Ễ'): 'E',  ord('ễ'): 'e',  # Circumflex
    ord('Ệ'): 'E',  ord('ệ'): 'e',  # Circumflex
    ord('Ĝ'): 'G',  ord('ĝ'): 'g',  # Circumflex
    ord('Ĥ'): 'H',  ord('ĥ'): 'h',  # Circumflex
    ord('Î'): 'I',  ord('î'): 'i',  # Circumflex
    # ord('Ī'): 'I',  ord('ī'): 'i',  # Acute_accent => Circumflex
    ord('Ĵ'): 'J',  ord('ĵ'): 'j',  # Circumflex
    ord('Ḽ'): 'L',  ord('ḽ'): 'l',  # Circumflex
    ord('Ṋ'): 'N',  ord('ṋ'): 'n',  # Circumflex
    ord('Ô'): 'O',  ord('ô'): 'o',  # Circumflex
    ord('Ố'): 'O',  ord('ố'): 'o',  # Circumflex
    # ord('Ồ'): 'O',  ord('ồ'): 'o',  # Grave_accent => Circumflex
    ord('Ổ'): 'O',  ord('ổ'): 'o',  # Circumflex
    ord('Ō'): 'O',  ord('ō'): 'o',  # Circumflex
    ord('Ỗ'): 'O',  ord('ỗ'): 'o',  # Circumflex
    ord('Ộ'): 'O',  ord('ộ'): 'o',  # Circumflex
    ord('Ŝ'): 'S',  ord('ŝ'): 's',  # Circumflex
    ord('Ṱ'): 'T',  ord('ṱ'): 't',  # Circumflex
    ord('Û'): 'U',  ord('û'): 'u',  # Circumflex
    # ord('Ū'): 'U',  ord('ū'): 'u',  # Acute_accent => Circumflex
    ord('Ṷ'): 'U',  ord('ṷ'): 'u',  # Circumflex
    ord('Ŵ'): 'W',  ord('ŵ'): 'w',  # Circumflex
    ord('Ŷ'): 'Y',  ord('ŷ'): 'y',  # Circumflex
    ord('Ẑ'): 'Z',  ord('ẑ'): 'z',  # Circumflex

# 1.4) https://en.wikipedia.org/wiki/Caron = háček
    ord('Ǎ'): 'A',  ord('ǎ'): 'a',  # Caron
    ord('Č'): 'CH', ord('č'): 'ch',  # Caron https://ru.forvo.com/word/%C4%8D/
    ord('Ď'): 'D',  ord('ď'): 'd',  # Caron
    ord('Ě'): 'E',  ord('ě'): 'e',  # Caron
    ord('Ê'): 'E',  ord('ê'): 'e',  # Caron
    ord('Ǧ'): 'G',  ord('ǧ'): 'g',  # Caron
    ord('Ȟ'): 'H',  ord('ȟ'): 'h',  # Caron
    ord('Ǐ'): 'I',  ord('ǐ'): 'i',  # Caron
                    ord('ǰ'): 'j',  # Caron: J̌
    ord('Ǩ'): 'K',  ord('ǩ'): 'k',  # Caron
    ord('Ľ'): 'L',  ord('ľ'): 'l',  # Caron
    ord('Ň'): 'N',  ord('ň'): 'n',  # Caron
    ord('Ǒ'): 'O',  ord('ǒ'): 'o',  # Caron
    ord('Ř'): 'ZH', ord('ř'): 'zh', # Caron https://ru.forvo.com/word/%C5%99/
    ord('Š'): 'SH', ord('š'): 'sh', # Caron https://ru.forvo.com/word/%C5%A1/
    ord('Ṧ'): 'S',  ord('ṧ'): 's',  # Caron
    ord('Ť'): 'T',  ord('ť'): 't',  # Caron
    ord('Ǔ'): 'U',  ord('ǔ'): 'u',  # Caron
    ord('Ǚ'): 'U',  ord('ǚ'): 'u',  # Caron
    ord('Ž'): 'ZH', ord('ž'): 'zh', # Caron https://ru.forvo.com/word/%C5%BE/
    ord('Ǯ'): 'DZH',ord('ǯ'): 'dzh',# Caron https://polonistka.by/uchit-polskiy-yazik/polskaya-fonetika-osobennosti-polskogo-proiznosheniya

# 1.5) https://en.wikipedia.org/wiki/Double_acute_accent
    ord('̋'): '',                   # Double_acute_accent
    ord('Ő'): 'O',  ord('ő'): 'o',  # Double_acute_accent
    ord('Ű'): 'U',  ord('ű'): 'u',  # Double_acute_accent
    ord('Ӳ'): 'Y',  ord('ӳ'): 'y',  # Double_acute_accent

# 1.6) https://en.wikipedia.org/wiki/Double_grave_accent
    ord('̏'): '',                   # Double_grave_accent
    ord('Ȁ'): 'A',  ord('ȁ'): 'a',  # Double_grave_accent
    ord('Ȅ'): 'E',  ord('ȅ'): 'e',  # Double_grave_accent
    ord('Ȉ'): 'I',  ord('ȉ'): 'i',  # Double_grave_accent
    ord('Ȍ'): 'O',  ord('ȍ'): 'o',  # Double_grave_accent
    ord('Ȑ'): 'R',  ord('ȑ'): 'r',  # Double_grave_accent
    ord('Ȕ'): 'U',  ord('ȕ'): 'u',  # Double_grave_accent
    ord('Ѷ'): 'V',  ord('ѷ'): 'v',  # Double_grave_accent

# 1.7), 3.4) https://en.wikipedia.org/wiki/Tilde
    ord('Ẵ'): 'A',  ord('ẵ'): 'a',  # Tilde
    ord('Ẫ'): 'A',  ord('ẫ'): 'a',  # Tilde
    ord('Ã'): 'A',  ord('ã'): 'a',  # Tilde
    ord('ᵬ'): 'b',                  # Tilde
    ord('ᵭ'): 'd',                  # Tilde
    ord('Ễ'): 'E',  ord('ễ'): 'e',  # Tilde
    ord('Ḛ'): 'E',  ord('ḛ'): 'e',  # Tilde
    ord('Ẽ'): 'E',  ord('ẽ'): 'e',  # Tilde
    ord('ᵮ'): 'f',                  # Tilde
    ord('Ḭ'): 'I',  ord('ḭ'): 'i',  # Tilde
    ord('Ĩ'): 'I',  ord('ĩ'): 'i',  # Tilde
    ord('Ɫ'): 'L',  ord('ɫ'): 'l',  # Tilde
    ord('ꭞ'): 'l',  ord('ꬸ'): 'l',  # Tilde
    ord('◌'): 'o',  ord('ᷬ'): '',  # Tilde
    ord('ᵯ'): 'm',  ord('ᵰ'): 'n',  # Tilde
    ord('Ñ'): 'N',  ord('ñ'): 'n',  # Tilde
    ord('Ỗ'): 'O',  ord('ỗ'): 'o',  # Tilde
    ord('Ỡ'): 'O',  ord('ỡ'): 'o',  # Tilde
    ord('Ṍ'): 'O',  ord('ṍ'): 'o',  # Tilde
    ord('Ṏ'): 'O',  ord('ṏ'): 'o',  # Tilde
    ord('Ȭ'): 'O',  ord('ȭ'): 'o',  # Tilde
    ord('Õ'): 'O',  ord('õ'): 'o',  # Tilde
    ord('ᵱ'): 'P',  ord('ᵳ'): '',  # Tilde
    ord('ᵲ'): 'r',  ord('ꭨ'): '',  # Tilde
    ord('ᵴ'): 's',  ord('ᵵ'): 't',  # Tilde
    ord('Ữ'): 'U',  ord('ữ'): 'u',  # Tilde
    ord('Ṹ'): 'U',  ord('ṹ'): 'u',  # Tilde
    ord('Ṵ'): 'U',  ord('ṵ'): 'u',  # Tilde
    ord('Ũ'): 'U',  ord('ũ'): 'u',  # Tilde
    ord('Ṽ'): 'V',  ord('ṽ'): 'v',  # Tilde
    ord('Ỹ'): 'Y',  ord('ỹ'): 'y',  # Tilde
    ord('ᵶ'): 'z',                  # Tilde


# 2.1) 2.2) https://en.wikipedia.org/wiki/Dot_(diacritic)
    ord('̣'): '',                    # Dot_(diacritic)
    # ord('́'): '',                    # Acute_accent => Dot_(diacritic)
    ord('̃'): '',                    # Dot_(diacritic)
    # ord('̀'): '',                    # Grave_accent => Dot_(diacritic)
    ord('͘'): '',                    # Dot_(diacritic)
    ord('̈'): '',                    # Dot_(diacritic)
    ord('̄'): '',                    # Dot_(diacritic)
    ord('̇'): '',                    # Dot_(diacritic)
    ord('Ȧ'): 'A',  ord('ȧ'): 'a',   # Dot_(diacritic)
    ord('Ǡ'): 'A',  ord('ǡ'): 'a',   # Dot_(diacritic)
    ord('Ạ'): 'A',  ord('ạ'): 'a',   # Dot_(diacritic)
    ord('Ậ'): 'A',  ord('ậ'): 'a',   # Dot_(diacritic)
    ord('Ặ'): 'A',  ord('ặ'): 'a',   # Dot_(diacritic)
    ord('Ḃ'): 'B',  ord('ḃ'): 'b',   # Dot_(diacritic)
    ord('Ḅ'): 'B',  ord('ḅ'): 'b',   # Dot_(diacritic)
    ord('Ċ'): 'C',  ord('ċ'): 'c',   # Dot_(diacritic)
    ord('Ç'): 'C',  ord('ç'): 'c',   # Dot_(diacritic)
    ord('Ć'): 'C',  ord('ć'): 'c',   # Dot_(diacritic)
    # ord('Č'): 'CH',  ord('č'): 'ch',   # Caron => Dot_(diacritic)
    ord('Ꜿ'): 'C',  ord('ꜿ'): 'c',   # Dot_(diacritic)
    ord('Ḋ'): 'D',  ord('ḋ'): 'd',   # Dot_(diacritic)
    ord('Ḍ'): 'D',  ord('ḍ'): 'd',   # Dot_(diacritic)
    ord('Ė'): 'E',  ord('ė'): 'e',   # Dot_(diacritic)
    ord('Ẹ'): 'E',  ord('ẹ'): 'e',   # Dot_(diacritic)
    ord('Ệ'): 'E',  ord('ệ'): 'e',   # Dot_(diacritic)
    ord('Ḟ'): 'F',  ord('ḟ'): 'f',   # Dot_(diacritic)
    ord('Ġ'): 'G',  ord('ġ'): 'g',   # Dot_(diacritic)
    ord('Ḣ'): 'H',  ord('ḣ'): 'h',   # Dot_(diacritic)
    ord('Ḥ'): 'H',  ord('ḥ'): 'h',   # Dot_(diacritic)
                    # ord('į'): ' ',   # Acute_accent / Dot_(diacritic)
    ord('Ị'): 'I',  ord('ị'): 'i',   # Dot_(diacritic)
    ord('Ḳ'): 'K',  ord('ḳ'): 'k',   # Dot_(diacritic)
    ord('Ḷ'): 'L',  ord('ḷ'): 'l',   # Dot_(diacritic)
    ord('Ḹ'): 'L',  ord('ḹ'): 'l',   # Dot_(diacritic)
    ord('Ŀ'): 'L',  ord('ŀ'): 'l',   # Dot_(diacritic)
    ord('Ṁ'): 'M',  ord('ṁ'): 'm',   # Dot_(diacritic)
    ord('Ṃ'): 'M',  ord('ṃ'): 'm',   # Dot_(diacritic)
    ord('Ṅ'): 'N',  ord('ṅ'): 'n',   # Dot_(diacritic)
    ord('Ṇ'): 'N',  ord('ṇ'): 'n',   # Dot_(diacritic)
    ord('Ȯ'): 'O',  ord('ȯ'): 'o',   # Dot_(diacritic)
    ord('Ọ'): 'O',  ord('ọ'): 'o',   # Dot_(diacritic)
    ord('Ộ'): 'O',  ord('ộ'): 'o',   # Dot_(diacritic)
    ord('Ȱ'): 'O',  ord('ȱ'): 'o',   # Dot_(diacritic)
    ord('Ợ'): 'O',  ord('ợ'): 'o',   # Dot_(diacritic)
    ord('Ṗ'): 'P',  ord('ṗ'): 'p',   # Dot_(diacritic)
    ord('Ṙ'): 'R',  ord('ṙ'): 'r',   # Dot_(diacritic)
    ord('Ṛ'): 'R',  ord('ṛ'): 'r',   # Dot_(diacritic)
    ord('Ṝ'): 'R',  ord('ṝ'): 'r',   # Dot_(diacritic)
    ord('Ṡ'): 'S',  ord('ṡ'): 's',   # Dot_(diacritic)
                    ord('ẛ'): 's',   # Dot_(diacritic)
    ord('Ṣ'): 'S',  ord('ṣ'): 's',   # Dot_(diacritic)
    ord('Ṥ'): 'S',  ord('ṥ'): 's',   # Dot_(diacritic)
    ord('Ṧ'): 'S',  ord('ṧ'): 's',   # Dot_(diacritic)
    ord('Ṩ'): 'S',  ord('ṩ'): 's',   # Dot_(diacritic)
    ord('Ṫ'): 'T',  ord('ṫ'): 't',   # Dot_(diacritic)
    ord('Ṭ'): 'T',  ord('ṭ'): 't',   # Dot_(diacritic)
    ord('Ụ'): 'U',  ord('ụ'): 'u',   # Dot_(diacritic)
    ord('Ự'): 'U',  ord('ự'): 'u',   # Dot_(diacritic)
    ord('V'): 'V',  ord('v'): 'v',   # Dot_(diacritic)
    ord('Ṿ'): 'V',  ord('ṿ'): 'v',   # Dot_(diacritic)
    ord('Ẇ'): 'W',  ord('ẇ'): 'w',   # Dot_(diacritic)
    ord('Ẉ'): 'W',  ord('ẉ'): 'w',   # Dot_(diacritic)
    ord('Ẋ'): 'X',  ord('ẋ'): 'x',   # Dot_(diacritic)
    ord('Ẏ'): 'Y',  ord('ẏ'): 'y',   # Dot_(diacritic)
    ord('Ỵ'): 'Y',  ord('ỵ'): 'y',   # Dot_(diacritic)
    ord('Ż'): 'Z',  ord('ż'): 'z',   # Dot_(diacritic)
    ord('Ẓ'): 'Z',  ord('ẓ'): 'z',   # Dot_(diacritic)

# 2.3) https://en.wikipedia.org/wiki/Interpunct
    ord('·'): '',  ord('·'): '',  # Interpunct
    ord('ּ'): '',  ord('᛫'): '',  # Interpunct
    ord('•'): '',  ord('‧'): '',  # Interpunct
    ord('∘'): '',  ord('∙'): '',  # Interpunct
    ord('⋅'): '',  ord('⏺'): '',  # Interpunct
    ord('●'): '',  ord('◦'): '',  # Interpunct
    ord('⚫'): '',  ord('⦁'): '',  # Interpunct
    ord('⸰'): '',  ord('⸱'): '',  # Interpunct
    ord('⸳'): '',  ord('・'): '',  # Interpunct
    ord('ꞏ'): '',  ord('･'): '',  # Interpunct
    ord('𐄁'): '',                 # Interpunct

# 2.4) https://en.wikipedia.org/wi ki/Tittle

# 2.5) https://en.wikipedia.org/wi ki/Umlaut_(linguistics) https://en.wikipedia.org/wiki/Diaeresis_(diacritic)
    ord('̈'): '',                   # Diaeresis_(diacritic)
    ord('Ä'): 'A',  ord('ä'): 'a',  # Diaeresis_(diacritic)
    ord('Ǟ'): 'A',  ord('ǟ'): 'a',  # Diaeresis_(diacritic)
    # ord('Ą'): 'A',  ord('ą'): 'a',  # Acute_accent => Diaeresis_(diacritic)
    ord('Ë'): 'E',  ord('ë'): 'e',  # Diaeresis_(diacritic)
    ord('Ḧ'): 'H',  ord('ḧ'): 'h',  # Diaeresis_(diacritic)
    ord('Ï'): 'I',  ord('ï'): 'i',  # Diaeresis_(diacritic)
    ord('Ḯ'): 'I',  ord('ḯ'): 'i',  # Diaeresis_(diacritic)
    ord('Ö'): 'O',  ord('ö'): 'o',  # Diaeresis_(diacritic)
    ord('Ȫ'): 'O',  ord('ȫ'): 'o',  # Diaeresis_(diacritic)
    # ord('Ǫ'): 'O',  ord('ǫ'): 'o',  # Acute_accent => Diaeresis_(diacritic)
    ord('Ṏ'): 'O',  ord('ṏ'): 'o',  # Diaeresis_(diacritic)
    ord('T'): 'T',  ord('ẗ'): 't',  # Diaeresis_(diacritic)
    ord('Ü'): 'U',  ord('ü'): 'u',  # Diaeresis_(diacritic)
    ord('Ǖ'): 'U',  ord('ǖ'): 'u',  # Diaeresis_(diacritic)
    ord('Ǘ'): 'U',  ord('ǘ'): 'u',  # Diaeresis_(diacritic)
    ord('Ǚ'): 'U',  ord('ǚ'): 'u',  # Diaeresis_(diacritic)
    # ord('Ǜ'): 'U',  ord('ǜ'): 'u',  # Grave_accent => Diaeresis_(diacritic)
    ord('Ṳ'): 'U',  ord('ṳ'): 'u',  # Diaeresis_(diacritic)
    ord('Ṻ'): 'U',  ord('ṻ'): 'u',  # Diaeresis_(diacritic)
                    ord('ᴞ'): 'u',  # Diaeresis_(diacritic)
    ord('Ẅ'): 'W',  ord('ẅ'): 'w',  # Diaeresis_(diacritic)
    ord('Ẍ'): 'X',  ord('ẍ'): 'x',  # Diaeresis_(diacritic)
    ord('Ÿ'): 'Y',  ord('ÿ'): 'y',  # Diaeresis_(diacritic)
    ord('Ϊ'): 'I',  ord('ϊ'): 'i',  # Diaeresis_(diacritic)
                    # ord('ῒ'): 'i',  # Diaeresis_(diacritic)
                    ord('ΐ'): 'i',  # Diaeresis_(diacritic)
                    ord('ῗ'): 'i',  # Diaeresis_(diacritic)
    ord('Ϋ'): 'Y',  ord('ϋ'): 'y',  # Diaeresis_(diacritic)
                    # ord('ῢ'): 'u',  # Diaeresis_(diacritic)
                    ord('ΰ'): 'u',  # Diaeresis_(diacritic)
                    ord('ῧ'): 'u',  # Diaeresis_(diacritic)
    ord('ϔ'): 'Y',                  # Diaeresis_(diacritic)
    ord('Ӓ'): 'A',  ord('ӓ'): 'a',  # Diaeresis_(diacritic)
    #ord('Ё'): 'E',  ord('ё'): 'e',  # Cyrillic = Diaeresis_(diacritic)
    ord('Ӛ'): 'E',  ord('ӛ'): 'e',  # Diaeresis_(diacritic)
    ord('Ӝ'): 'DZH',ord('ӝ'): 'dzh',# Diaeresis_(diacritic)
    ord('Ӟ'): 'Z',  ord('ӟ'): 'z',  # Diaeresis_(diacritic)
    ord('Ӥ'): 'J',  ord('ӥ'): 'j',  # Diaeresis_(diacritic)
    ord('Ӧ'): 'O',  ord('ӧ'): 'o',  # Diaeresis_(diacritic)
    ord('Ӫ'): 'O',  ord('ӫ'): 'o',  # Diaeresis_(diacritic)
    ord('Ӱ'): 'Y',  ord('ӱ'): 'y',  # Diaeresis_(diacritic)
    ord('Ӵ'): 'CH', ord('ӵ'): 'ch', # Diaeresis_(diacritic)
    ord('Ӹ'): 'Y',  ord('ӹ'): 'y',  # Diaeresis_(diacritic)
    ord('Ӭ'): 'E',  ord('ӭ'): 'e',  # Diaeresis_(diacritic)

# 3.1) https://en.wikipedia.org/wiki/Breve
    ord('̆'): '',                   # Breve
    ord('Ă'): 'A',  ord('ă'): 'a',  # Breve
    ord('Ắ'): 'A',  ord('ắ'): 'a',  # Breve
    ord('Ằ'): 'A',  ord('ằ'): 'a',  # Breve
    ord('Ẳ'): 'A',  ord('ẳ'): 'a',  # Breve
    ord('Ẵ'): 'A',  ord('ẵ'): 'a',  # Breve
    ord('Ặ'): 'A',  ord('ặ'): 'a',  # Breve
    ord('Ĕ'): 'E',  ord('ĕ'): 'e',  # Breve
    ord('Ḝ'): 'E',  ord('ḝ'): 'e',  # Breve
    ord('Ğ'): 'G',  ord('ğ'): 'g',  # Breve
    ord('Ḫ'): 'H',  ord('ḫ'): 'h',  # Breve
    ord('Ĭ'): 'I',  ord('ĭ'): 'i',  # Breve
    ord('Ŏ'): 'O',  ord('ŏ'): 'o',  # Breve
    ord('Œ'): 'E',  ord('œ'): 'e',  # Breve
    ord('Ŭ'): 'U',  ord('ŭ'): 'u',  # Breve
    ord('Ᾰ'): 'A',  ord('ᾰ'): 'a',  # Breve
    ord('Ῐ'): 'I',  ord('ῐ'): 'i',  # Breve
    ord('Ῠ'): 'y',  ord('ῠ'): 'y',  # Breve
    ord('Ӑ'): 'A',  ord('ӑ'): 'a',  # Breve
    ord('Ӗ'): 'E',  ord('ӗ'): 'e',  # Breve

# 3.2) https://en.wikipedia.org/wiki/Inverted_breve
    ord('Ȃ'): 'A',  ord('ȃ'): 'ȃ',  # Inverted_breve
    ord('Ȇ'): 'E',  ord('ȇ'): 'ȇ',  # Inverted_breve
    ord('Ȋ'): 'I',  ord('ȋ'): 'ȋ',  # Inverted_breve
    ord('Ȏ'): 'O',  ord('ȏ'): 'ȏ',  # Inverted_breve
    ord('Ȓ'): 'R',  ord('ȓ'): 'ȓ',  # Inverted_breve
    ord('Ȗ'): 'U',  ord('ȗ'): 'ȗ',  # Inverted_breve

# 3.3) https://en.wikipedia.org/wiki/Sicilicus
# 1.7), 3.4) https://en.wikipedia.org/wiki/Tilde
# 3.5) https://en.wikipedia.org/wiki/Titlo
# 4.1) https://en.wikipedia.org/wiki/Syllabic_consonant

# 5.1) https://en.wikipedia.org/wiki/Macron_(diacritic)
	ord('Ǣ'): 'A',	ord('ǣ'): 'a',  # Macron_(diacritic)
	ord('Ḡ'): 'G',	ord('ḡ'): 'g',  # Macron_(diacritic)
	ord('Ǭ'): 'O',	ord('ǭ'): 'o',  # Macron_(diacritic)
	ord('Ᾱ'): 'A',	ord('ᾱ'): 'a',  # Macron_(diacritic)
	ord('Ῑ'): 'I',	ord('ῑ'): 'i',  # Macron_(diacritic)
	ord('Ῡ'): 'Y',	ord('ῡ'): 'y',  # Macron_(diacritic)

# 5.2) https://en.wikipedia.org/wiki/Macron_below
	ord('Ḏ'): 'D',	ord('ḏ'): 'd',  # Macron_below
                    ord('ẖ'): 'h',  # Macron_below
	ord('Ḵ'): 'K',	ord('ḵ'): 'k',  # Macron_below
	ord('Ḻ'): 'L',	ord('ḻ'): 'l',  # Macron_below
	ord('Ṉ'): 'N',	ord('ṉ'): 'n',  # Macron_below
	ord('Ṟ'): 'R',	ord('ṟ'): 'r',  # Macron_below
	ord('Ṯ'): 'T',	ord('ṯ'): 't',  # Macron_below
	ord('Ẕ'): 'Z',	ord('ẕ'): 'z',  # Macron_below
	ord('₫'): 'D',	                # Macron_below

# 6.1) 6.2) 6.3) https://en.wikipedia.org/wiki/Bar_(diacritic)
# 7.1) https://en.wikipedia.org/wiki/Ring_(diacritic)
    ord('̊'): '',                   # Ring_(diacritic)
    ord('̱'): '',                   # Ring_(diacritic)
    ord('̥'): '',                   # Ring_(diacritic)
	ord('Å'): 'A',	ord('å'): 'a',  # Ring_(diacritic)
	ord('Ḁ'): 'A',	ord('ḁ'): 'a',  # Ring_(diacritic)
	ord('Ů'): 'U',	ord('ů'): 'u',  # Ring_(diacritic)
	ord('W'): 'W',	ord('ẘ'): 'w',  # Ring_(diacritic)
	ord('Y'): 'Y',	ord('ẙ'): 'y',  # Ring_(diacritic)

# 8.1) https://en.wikipedia.org/wiki/Apostrophe
# 8.4) https://en.wikipedia.org/wiki/Hook_above
    ord('Ả'): 'A',  ord('ả'): 'a',  # Hook_above
    ord('Ẩ'): 'A',  ord('ẩ'): 'a',  # Hook_above
    ord('Ẳ'): 'A',  ord('ẳ'): 'a',  # Hook_above
    ord('Ẻ'): 'E',  ord('ẻ'): 'e',  # Hook_above
    ord('Ể'): 'E',  ord('ể'): 'e',  # Hook_above
    ord('Ỉ'): 'I',  ord('ỉ'): 'i',  # Hook_above
    ord('Ỏ'): 'O',  ord('ỏ'): 'o',  # Hook_above
    ord('Ổ'): 'O',  ord('ổ'): 'o',  # Hook_above
    ord('Ở'): 'O',  ord('ở'): 'o',  # Hook_above
    ord('Ủ'): 'U',  ord('ủ'): 'u',  # Hook_above
    ord('Ử'): 'U',  ord('ử'): 'u',  # Hook_above
    ord('Ỷ'): 'Y',  ord('ỷ'): 'y',  # Hook_above

# 8.5) https://en.wikipedia.org/wiki/Horn_(diacritic)
    ord('Ơ'): 'O',  ord('ơ'): 'o',  # Horn_(diacritic)
    ord('Ớ'): 'O',  ord('ớ'): 'o',  # Horn_(diacritic)
    # ord('Ờ'): 'O',  ord('ờ'): 'o',  # Grave_accent => Horn_(diacritic)
    ord('Ở'): 'O',  ord('ở'): 'o',  # Horn_(diacritic)
    ord('Ỡ'): 'O',  ord('ỡ'): 'o',  # Horn_(diacritic)
    ord('Ợ'): 'O',  ord('ợ'): 'o',  # Horn_(diacritic)
    ord('Ư'): 'U',  ord('ư'): 'u',  # Horn_(diacritic)
    ord('Ứ'): 'U',  ord('ứ'): 'u',  # Horn_(diacritic)
    # ord('Ừ'): 'U',  ord('ừ'): 'u',  # Grave_accent => Horn_(diacritic)
    ord('Ử'): 'U',  ord('ử'): 'u',  # Horn_(diacritic)
    ord('Ữ'): 'U',  ord('ữ'): 'u',  # Horn_(diacritic)
    ord('Ự'): 'U',  ord('ự'): 'u',  # Horn_(diacritic)

# 9.1) https://en.wikipedia.org/wiki/Comma#Diacritical_usage
# 9.2) https://en.wikipedia.org/wiki/Cedilla
    ord('̧'): '',                   # Cedilla
    ord('Ç'): 'C',  ord('ç'): 'c',  # Cedilla
    ord('Ḉ'): 'C',  ord('ḉ'): 'c',  # Cedilla
    ord('Ḑ'): 'D',  ord('ḑ'): 'd',  # Cedilla
    ord('Ȩ'): 'E',  ord('ȩ'): 'e',  # Cedilla
    ord('Ḝ'): 'E',  ord('ḝ'): 'e',  # Cedilla
    ord('Ɛ'): 'E',  ord('ɛ'): 'e',  # Cedilla
    ord('Ģ'): 'G',  ord('ģ'): 'g',  # Cedilla
    ord('Ḩ'): 'H',  ord('ḩ'): 'h',  # Cedilla
    ord('Ɨ'): 'I',  ord('ɨ'): 'i',  # Cedilla
    ord('Ķ'): 'K',  ord('ķ'): 'k',  # Cedilla
    ord('Ļ'): 'L',  ord('ļ'): 'l',  # Cedilla
    ord('Ņ'): 'N',  ord('ņ'): 'n',  # Cedilla
    # ord('Ɔ'): 'O',  ord('ɔ'): 'o',  # Acute_accent => Cedilla
    ord('Ŗ'): 'R',  ord('ŗ'): 'r',  # Cedilla
    ord('Ş'): 'S',  ord('ş'): 'sh', # Cedilla
                    ord('ſ'): 's',  # Cedilla
                    ord('ß'): 'ss', # Cedilla
    ord('Ţ'): 'T',  ord('ţ'): 't',  # Cedilla

# 9.3) https://en.wikipedia.org/wiki/Hook_(diacritic)
# NOT DONE:
# LatinᶏᶐƁɓᶀꞖꞗƇƈꟄꞔƊɗᶁƉɖᶑᶒꬴᶕɚᶓᶔɝƑƒᶂƓɠʛᶃꬶꞪɦʱꞕɧʮʯᶖꞲʝᶨʄƘƙᶄᶅᶪɭᶩꞎⱮɱᶬᶆꬺƝɲᶮɳᶯᶇꬻꬼᶗƤƥᶈꝒꝓꝔꝕʠɊɋⱤɽᶉⱹɻʵꭉꭊⱾȿᶊꟅʂᶳᶋᶘƬƭƮʈƫᶵᶙꭒꭟᶌⱱƲʋᶹⱲⱳᶍƳƴȤȥʐᶼⱿɀꟆᶎᶚƺGreekϒCyrillicӺӻҊҋӃӄԒԓӅӆӍӎӇӈԨԩӉӊӼӽ

# https://en.wikipedia.org/wiki/Ogonek
    ord('̨'): '',                   # Ogonek
	ord('Ł'): 'L',	ord('ł'): 'l',  # Ogonek
	ord('Ɫ'): 'L',	ord('ɫ'): 'l',  # Ogonek
	ord('᷎'): '',                   # Ogonek
	ord('᷎'): '',                   # Ogonek
	ord('᷎'): '',                   # Ogonek
	ord('᷎'): '',                   # Ogonek
	ord('Ø'): 'O',	ord('ø'): 'o',  # Ogonek
}

safechars_dict = {
}

if __name__ == '__main__':
    import sys
    import os
    print("Translit cyrillic/french/spanish/other latin like languages from UTF-8 into ASCII-7 encoding.")
    if len(sys.argv) < 2:
        print("Usage: %s <input file> [output file]" % os.path.split(sys.argv[0])[1])
        sys.exit(0)
    
    with open(sys.argv[1],"rb") as fIn:
        src_string = fIn.read().decode("utf-8")
        dst_string = src_string.translate(translit_dict)
        if len(sys.argv) > 2:
            with open(sys.argv[2],"wt") as fOut:
                fOut.write(dst_string)
        else:
            print(dst_string)
            
    print("Mission accomplished")
        
        
