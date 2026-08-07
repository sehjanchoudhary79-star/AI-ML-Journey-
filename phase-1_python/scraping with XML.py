import urllib.request
import xml.etree.ElementTree as ET

total=0

lis=list()

url=input("Enter url ")
stuff= urllib.request. urlopen(url).read()

tree=ET.fromstring(stuff)

count=tree.findall('comments/comment')

for item in count:
     t=item.find('count').text 
     lis.append(int(t))
     
print(sum (lis))