import requests
from bs4 import BeautifulSoup

def get_values(date):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    result = requests.get("https://finance.yahoo.com/quote/AEGFX/history?p=AEGFX", headers = headers)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    
    ptr = soup.findAll('tr')
    td = []
    data = [date, "-1"]
    for tr in ptr:
        if date in tr.text:
            td = tr.findAll('td')
            break
    print(td[4].text)
    if len(td) == 7:
        if isFloat(td[4].text):
            return [date, float(td[4].text)]
        else:
            print("ERROR 2: date exists, no valid value")
    else:
        print("Error 1: No entry for entered date")
    return [date, "-1"]

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

print(get_values("Jan 28, 2022"))
