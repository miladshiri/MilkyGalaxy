from urllib.request import urlopen
from bs4 import BeautifulSoup


# Extract some information from a web page provided by a url 
def webpage_info(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.title.get_text()
    content = soup.get_text()
    word_count = len(content.split(' '))
    return title, word_count, content
