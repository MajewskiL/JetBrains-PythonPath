#  https://hyperskill.org/projects/162

marks = {"plain": "", "bold": "", "italic": "", "inline-code": "", "link": "",
         "header": "", "unordered-list": "", "ordered-list": "", "new-line": ""}
txt = ""

while True:
    form = input("- Choose a formatter: ")
    if form == "!help":
        print(f"Available formatters: {' '.join(x for x in marks)}")
        print("Special commands: !help !done")
    elif form in (x for x in marks):
        if form == "header":
            while True:
                level = int(input("- Level: "))
                if level >= 1 and level <=6:
                    break
                print("The level should be within the range of 1 to 6")
            text = input("- Text: ")
            txt += "#" * level + " " + text + "\n"
        elif form == "link":
            label = input("- Label: ")
            url = input("- URL: ")
            txt += "[" + label + "](" + url + ")"
            pass
        elif form == "plain":
            text = input("- Text: ")
            txt += text
        elif form == "bold":
            text = input("- Text: ")
            txt += f"**{text}**"
        elif form == "italic":
            text = input("- Text: ")
            txt += f"*{text}*"
        elif form == "inline-code":
            text = input("- Text: ")
            txt += f"`{text}`"
        elif form == "new-line":
            txt += "\n"
        elif form in ("unordered-list", "ordered-list"):
            while True:
                nr = int(input("- Number of rows: "))
                if nr <= 0:
                    print("The number of rows should be greater than zero")
                else:
                    for x in range(1, nr + 1):
                        line = input(f"- Row #{x}: ")
                        txt += f"{x}. {line}\n" if form == "ordered-list" else f"* {line}\n"
                    break
        print(txt)
    elif form == "!done":
        with open("output.md", "w") as f:
            f.write(txt)
        exit()
    else:
        print("Unknown formatting type or command")
