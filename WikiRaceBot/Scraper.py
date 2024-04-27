import requests
from bs4 import BeautifulSoup

def get_links(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    result = requests.get(url, headers = headers)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    final = []

    links = soup.find_all('a', href = True)
    for l in links:
        link = l['href']
        if not(link[0:5] == "/wiki"):
            continue
        else:
            final.append(link)
    return final

def calc_path(start, end):
    routes = []
    queue = [[start]]
    found = False

    while not found:
        path = queue.pop(0)
        #print(path)
        if path[-1] == end:
            found = True
            routes.append(path)

        else:
            links = get_links(path[-1])
            for link in links:
                queue.append(path + ["https://en.wikipedia.org"+link])
    return routes
   
def main():
    path = calc_path("https://en.wikipedia.org/wiki/Nico_Ditch", "https://en.wikipedia.org/wiki/Leonardo_Bruni")
    print(path)
    
main()
