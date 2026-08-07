import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup

url = input('Enter - ')
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

comment1 = soup('span')
totalsum = 0

for comment in comment1:
    totalsum += int(comment.text)
print(totalsum)    