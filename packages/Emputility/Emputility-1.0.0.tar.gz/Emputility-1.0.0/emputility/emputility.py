import json
from collections import OrderedDict
lang = "ko" #언어 설정. 아무 것도 뜨게 하고 싶지 않다면 아무거나 쓰자.(물론 문자열이 아니면 오류난다.)
if lang == 'ko':
    print("[ SYSTEM ] Emputility 모듈이 성공적으로 로딩되었습니다!")
elif lang == 'en':
    print("[ SYSTEM ] Emputility module has succfully loaded!")
def makejson(list_name, list_gab, file_name):
    name = list_name
    gab = list_gab
    ff = len(name)
    data = OrderedDict()
    for i in range(0, ff):
        data[name[i]] = gab[i]
    with open(file_name, 'w', encoding="UTF8") as make_file:
        json.dump(data, make_file, ensure_ascii=False, indent="\t")
def lang(): #이 모듈에서 사용되는 언어를 리턴. 필요할 때 쓰자.
    return lang
def randomd(per, min_, max_):
    if per >= 10:
        return
    n = random.randrange(1, 11)
    if n == per:
        nn = random.randrange(min_, max_)
        return nn
    else:
        return 'failed'
            