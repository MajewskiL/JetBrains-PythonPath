# https://hyperskill.org/projects/79?track_id=2

import sys
import os
import requests
import bs4
from colorama import Fore
 
def get_name(www):
    try:
        www = www.lstrip("https://")
    except ValueError:
        pass
    return www[:www.index(".")]
 
www = ""
history = []
 
while True:
    www = input()
 
    if www == "exit":
        break
    elif www == "back":
        try:
            www = history.pop()
            www = history.pop()
        except IndexError:
            continue
 
    arg = sys.argv[1]
 
    if www.count(".") != 0:
        if not www.startswith("http://") and not www.startswith("https://"):
            www = "https://" + www
        history.append(www)
        wwwp = get_name(www)
        try:
            r = requests.get(www)
        except:
            print("InvalidURL")
            continue
        if r.status_code == 200:
            try:
                os.mkdir(arg)
            except FileExistsError:
                pass
            soup = bs4.BeautifulSoup(r.text, features="html.parser")
            with open(arg + "\\" + wwwp, "w", encoding="utf-8") as f:
                for tag in soup.find_all():
                    if tag.name == "a":
                        print(Fore.BLUE + tag.text)
                        f.write(tag.text + "\n")
                    elif tag.name in ["p", "ul", "ol", "li"]:
                        print(tag.text)
                        f.write(tag.text + "\n")
        elif r == 404:
            print("Nie ma takiej strony")
    else:
        try:
            f = open(arg + "\\" + www, "r", encoding="utf-8")
            print(f.read())
            f.close()
        except FileNotFoundError:
            pass
