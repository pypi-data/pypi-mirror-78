import inspect
import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")
import n0translate

def test__n0utils_translate_ru():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Съешь ещё этих мягких французских булок да выпей же чаю"
    result = src.translate(n0translate.translit_dict)
    expected = "Sesh eschjo etih mjagkih frantsuzskih bulok da vypey zhe chaju"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_az():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Zəfər, jaketini də, papağını da götür, bu axşam hava çox soyuq olacaq"
    result = src.translate(n0translate.translit_dict)
    expected = "Zefer, jaketini de, papagini da gotur, bu axsham hava cox soyuq olacaq"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_bg():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Ах, чудна българска земьо, полюшвай цъфтящи жита"
    result = src.translate(n0translate.translit_dict)
    expected = "Ah, chudna blgarska zemo, poljushvay tsftjaschi zhita"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_by():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "У рудога вераб’я ў сховішчы пад фатэлем ляжаць нейкія гаючыя зёлкі"
    result = src.translate(n0translate.translit_dict)
    expected = "U rudoga verabja u shovishchy pad fatelem ljazhats neykija gajuchyja zjolki"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_ga(): # Irish
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Chuaigh bé mhórshách le dlúthspád fíorfhinn trí hata mo dhea-phorcáin bhig"
    result = src.translate(n0translate.translit_dict)
    expected = "Chuaigh be mhorshach le dluthspad fiorfhinn tri hata mo dhea-phorcain bhig"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_es():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "El pingüino Wenceslao hizo kilómetros bajo exhaustiva lluvia y frío, añoraba a su querido cachorro - el búho"
    result = src.translate(n0translate.translit_dict)
    expected = "El pinguino Wenceslao hizo kilometros bajo exhaustiva lluvia y frio, anoraba a su querido cachorro - el buho"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_lv():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Četri psihi faķīri vēlu vakarā zāģēja guļbūvei durvis, fonā šņācot mežam"
    result = src.translate(n0translate.translit_dict)
    expected = "CHetri psihi fakiri velu vakara zageja gulbuvei durvis, fona shnacot mezham"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_de():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Falsches Üben von Xylophonmusik quält jeden größeren Zwerg"
    result = src.translate(n0translate.translit_dict)
    expected = "Falsches Uben von Xylophonmusik qualt jeden grosseren Zwerg"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_pl():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Stróż pchnął kość w quiz gędźb vel fax myjń"
    result = src.translate(n0translate.translit_dict)
    expected = "Stroz pchnal kosc w quiz gedzb vel fax myjn"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_pt():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "À noite, vovô Kowalsky vê o ímã cair no pé do pinguim queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz"
    result = src.translate(n0translate.translit_dict)
    expected = "A noite, vovo Kowalsky ve o ima cair no pe do pinguim queixoso e vovo poe acucar no cha de tamaras do jabuti feliz"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_uk():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Жебракують філософи при ґанку церкви в Гадячі, ще й шатро їхнє п’яне знаємо"
    result = src.translate(n0translate.translit_dict)
    expected = "ZHebrakujut filosofi pri ganku tserkvi v Gadjachi, sche y shatro yhne pjane znaemo"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_fr():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Dès Noël où un zéphyr haï me vêt de glaçons würmiens je dîne d’exquis rôtis de bœuf au kir à l’aÿ d’âge mûr & cætera"
    result = src.translate(n0translate.translit_dict)
    expected = "Sesh esche etih mjagkih frantsuzskih bulok da vypey zhe chaju"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    # assert result == expected

def test__n0utils_translate_cz():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Příliš žluťoučký kůň úpěl ďábelské ódy"
    result = src.translate(n0translate.translit_dict)
    expected = "Pzhilish zhlutouchky kun upel dabelske ody"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected

def test__n0utils_translate_eo():
    print ("*"*50 + "\n" + "*"*3 + " %s" % inspect.stack()[0][3] + "\n" + "*"*50)
    src = "Laŭ Ludoviko Zamenhof bongustas freŝa ĉeĥa manĝaĵo kun spicoj"
    result = src.translate(n0translate.translit_dict)
    expected = "Lau Ludoviko Zamenhof bongustas fresa ceha mangajo kun spicoj"

    print("src = '%s'" % src)
    print("result = '%s'" % result)
    print("expected = '%s'" % expected)
    assert result == expected


def main():
    test__n0utils_translate_ru()
    test__n0utils_translate_az()
    test__n0utils_translate_bg()
    test__n0utils_translate_by()
    test__n0utils_translate_ga()
    test__n0utils_translate_es()
    test__n0utils_translate_lv()
    test__n0utils_translate_de()
    test__n0utils_translate_pl()
    test__n0utils_translate_pt()
    test__n0utils_translate_uk()
    test__n0utils_translate_fr()
    test__n0utils_translate_cz()
    test__n0utils_translate_eo()

if __name__ == '__main__':
    main()
