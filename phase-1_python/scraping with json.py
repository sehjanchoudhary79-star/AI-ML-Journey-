import urllib.request
import json

total=0

url=input("Enter url ")
stuff= urllib.request. urlopen(url).read()
 
count=json.loads(stuff)

for coun in count['comments']:
    t=coun['count']
    total+=t

print(total)
