def read(file):
    with open("../htmls/%s.html"%file,"r",encoding="utf8") as f:
        text = f.read()

    return text

import re

def getToken():
    reserve = read("reserve")
    token = "".join( re.findall("token.*?'(.*?)'",reserve) ) 
    print(token)

getToken()