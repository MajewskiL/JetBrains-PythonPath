def param(ciag):
    txt = {
            "/help": "The program calculates the sum and diff of numbers",
            "/?": "Unknown command",
            "/uv": "Unknown variable",
            "/ii": "Invalid identifier",
            "/ia": "Invalid assignment",
            "/ie": "Invalid expression",
            "": "Unknown command"
           }
    try:
        return txt[ciag]
    except KeyError:
        return txt["/?"]


def list_ciag(ciag):  # list without import re
    tmp = ""
    out = []
    for x in ciag:
        if x == " ":
            if tmp != "":
                out.append(tmp)
            tmp = ""
            continue
        elif x.isalpha():
            if tmp == "" or tmp.isalpha():
                tmp += x
            else:
                out.append(tmp)
                tmp = x
        elif x.isdigit():
            if tmp == "" or tmp.isdigit():
                tmp += x
            else:
                out.append(tmp)
                tmp = x
        else:
            if len(tmp) != 0:
                out.append(tmp)
            out.append(x)
            tmp = ""
    if tmp:
        out.append(tmp)
    return out


def clear_all(ciag):
    ciag = "".join(ciag)
    bed_rep = ("**", "//")
    if any([True for x in bed_rep if x in ciag]):
        return False
    rep = {" ": "",
           "++": "+",
           "--": "+",
           "+-": "-",
           "-+": "-"}
    while any([True for x in rep.keys() if x in ciag]):
        for x in rep.keys():
            ciag = ciag.replace(x,rep[x])
    return list_ciag(ciag)


def valid_ciag(ciag):
    signs = "*/+-()="
    stan = 0
    ''' () Validation '''
    count = 0
    for x in range(len(ciag)):
        if ciag[x] == "(":
            count += 1
        elif ciag[x] == ")":
            count -= 1
        if count < 0:
            return "/ie"
        if x == len(ciag) - 1:
            if count != 0:
                return "/ie"
    ''' "=" Validation'''
    if ciag.count("=") != 0:
        if ciag.index("=") != 1:
            return "/ii"
        elif ciag.count("=") > 1:
            return "/ia"
        elif ciag[0].isalpha():
            if ciag[2:] != []:
                ciag2 = valid_ciag(ciag[2:])
                if "/" not in ciag2:
                    zmn[ciag[0]] = "".join(ciag2)
                    return False
                else:
                    return "/ia"
            else:
                return "/ia"
        else:
            return "/ii"
    ''' syntax validation '''
    if not ciag[0].isdigit() and not ciag[0].isalpha() and ciag[0] not in signs[2:]:
        return "/?"
    if not ciag[len(ciag)-1].isdigit() and not ciag[len(ciag)-1].isalpha() and ciag[len(ciag)-1] != ")":
        return "/?"
    for x in range(len(ciag)):
        if not ciag[x].isdigit() and not ciag[x].isalpha() and ciag[x] not in signs:
            return "/?"
        elif ciag[x].isdigit():
            stan += 1
        elif ciag[x].isalpha():
            try:
                ciag[x] = zmn[ciag[x]]
            except KeyError:
                return "/uv"
            stan += 1
        elif ciag[x] in signs:
            stan *= 0
        if stan > 1:
            return "/?"
    return ciag


def to_onp(dane):
    stos, wynik = [], []
    waga = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 2}
    for x in dane:
        if x.isdigit():
            wynik.append(x)
        elif x == "(":
            stos.append(x)
        elif x == ")":
            p = stos[::-1].index("(")
            wynik += stos[:len(stos)-p-1:-1]
            stos = stos[:len(stos)-p-1]
        elif x in waga.keys():
            if len(stos) == 0:
                stos.append(x)
            else:
                z = len(stos)-1
                while z > -1 and stos[z] != "(" and waga[stos[z]] >= waga[x] :
                    wynik.append(stos[z])
                    stos = stos[:-1]
                    z -= 1
                stos.append(x)
    wynik += stos[::-1]
    return(wynik)

def from_onp(ciag):
    ciag = ciag[::-1]
    stos = []
    while ciag:
        a = ciag.pop()
        if a.isdigit():
            stos.append(a)
        else:
            x = int(stos.pop())
            y = int(stos.pop())
            if a == "+":
                stos.append(x+y)
            elif a == "-":
                stos.append(y-x)
            elif a == "*":
                stos.append(x*y)
            elif a == "/":
                stos.append(y/x)

    return int(stos[0])



zmn = dict()

while True:
    dane = input()
    if dane == "":
        continue
    elif dane[0] == "/":
        if dane != "/exit":
            print(param(dane))
        else:
            break
    else:
        dane = list_ciag(dane)
        dane = clear_all(dane)
        if dane == False:
            print(param("/ie"))
            continue
        dane = valid_ciag(dane)
        if dane == False:
            continue
        elif dane[0] == "/":
            print(param(dane))
        else:
            try:
                print(from_onp(to_onp(dane)))
            except SyntaxError:
                print(param("/?"))

print("Bye!")
