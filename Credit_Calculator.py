import math
import sys

# funkcje
def annuity_payment(P, i, n):
    return ((P * ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1))))

def credit_principal(A, i, n):
    return (A / ((i * pow(1 + i, n)) / (pow(1 + i, n) -1 )))

def years(A, P, i):
    return math.log((A / (A - i * P)), i + 1)

def month(P, n, i, m):
    return ((P / n) + i * (P - P * (m - 1) / n))

# zmienne
args = sys.argv
arg = { "type" : "",
        "payment" : "",
        "principal" : "",
        "periods" : "",
        "interest" : "" }
bug = False
principal, payment, periods, interest = 0, 0 ,0, 0

# przepisanie parametrów do słownika
for name in arg.keys():
    for data in args:
        if name in data: arg[name] = data[data.index("=")+1:]

type = arg["type"]
if arg["principal"] != "": principal = int(arg["principal"])
if arg["payment"] != "": payment = int(arg["payment"])
if arg["periods"] != "": periods = int(arg["periods"])
if arg["interest"] != "": interest = float(arg["interest"])/1200

# sprawdzanie kompletności parametrów
if type not in ("diff","annuity"): bug = True
if type == "diff" and arg["payment"] != "" : bug = True
if arg["principal"] == "":
    if arg["interest"] == "" or arg["payment"] == "" or arg["periods"] == "":
        bug = True
if arg["periods"] == "":
    if arg["interest"] == "" or arg["payment"] == "" or arg["principal"] == "":
        bug == True
if arg["interest"] == "": bug = True
if principal<0 or payment<0 or periods<0 or interest<0: bug = True

# obliczenia jeśli nie ma błędów w parametrach
if bug == True:
    print("Incorrect parameters")
else:

    if type == "annuity":
        if principal == 0:
            principal = credit_principal(payment,interest,periods)
            credit = annuity_payment(principal,interest,periods)
            print(f"Overpayment = {math.ceil((credit * periods) - principal)}")
            print(f"Your credit principal = {math.trunc(principal)}!")
        elif payment == 0:
            credit = annuity_payment(principal,interest,periods)
            principal = credit_principal(credit,interest,periods)
            print(f"Overpayment = {math.trunc((math.ceil(credit) * periods) - principal)}")
            print(f"Your annuity payment = {math.ceil(credit)}!")
        elif periods == 0:
            periods = years(payment,principal,interest)
            print(f"You need {math.ceil(periods / 12)} years to repay this credit!")
            print(f"Overpayment = {(payment * math.ceil(periods)) - principal}")
    else:
        credit = 0
        for m in range (1,periods+1):
            single_month=math.ceil(month(principal ,periods, interest,m))
            credit += single_month
            print(f"Month {m}: paid out {single_month}")
        print(f"Overpayment = {credit - principal}")
