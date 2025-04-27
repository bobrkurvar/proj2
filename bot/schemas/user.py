from pydantic import BaseModel

class User(BaseModel):
    game_is_active: bool = False

def valid_braces(string):
    cnt = 0
    sub = ''
    mp = {')': '(', ']': '[', '}': '{'}
    for bracket in string:
        if bracket in ('(', '[' ,'{'):
            cnt += 1
            sub += bracket
        elif bracket in (')', ']', '}'):
            if mp[bracket] in sub:
                cnt -= 1
    print(cnt)
    return not cnt

valid_braces("[(])")

def to_weird_case(words: str):
    res = None
    words_list = words.lower().split()
    print(words_list)
    res_list = []
    for word in words_list:
        for i in range(0, len(word), 2):
            print(word[i])
            word = word.replace(word[i], word[i].upper(), 1)
        res_list.append(word)
    print(res_list)
    res = " ".join(res_list)
    return res

print(to_weird_case("LOokS' should equal 'LoOkS"))


class Dinglemouse:

    def __init__(self):
        self.name = None
        self.sex = None
        self.age = None
        self.atr = []

    def setAge(self, age):
        self.age = age
        self.atr.append("age")
        return self

    def setSex(self, sex):
        self.sex = sex
        self.atr.append("sex")
        return self

    def setName(self, name):
        self.name = name
        self.atr.append("name")
        return self

    def hello(self):
        res = "Hello."
        patern = {"name": " My name is {n}.", "age": " I am {a}.", "sex": " I am {s}."}
        for key in self.atr:
            res += str(patern[key])

        return res.format(n=self.name, a=self.age, s="male" if self.sex == 'M' else "female")

per1 = Dinglemouse()
per1.setAge(25).setName("Betty").setSex("F").setAge(32)

def scramble1(s1, s2):
    tmp = s1
    cnt = 0
    for i in s2:
        if i not in tmp:
            return False
        cnt += 1
        tmp = tmp.replace(i, "", 1)
    if cnt == len(s2): return True



def scramble2(s1, s2):
    compos_s1 = {}
    compos_s2 = {}
    for i in s1:
        compos_s1[i] = compos_s1.setdefault(i, 0) + 1

    for i in s2:
        compos_s2[i] = compos_s2.setdefault(i, 0) + 1



def gcm(x,y):
    return x if y == 0 else gcm(y, x%y)

print(gcm(31000,1500))

def custom_filter(lst: list) -> bool:
    numbers = [int(i) for i in lst if isinstance(i, int) and int(i) % 7 == 0]
    print(numbers)
    return True if sum(numbers) <= 83 else False

print(custom_filter([7, 14, 28, 32, 32, 56]))