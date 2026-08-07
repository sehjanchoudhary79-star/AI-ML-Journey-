f=list()
file=input("Enter the file name: ")
list=open(file,'r')
list=list.read()
list=list.split()
for word in list:
    if word not in f:
        f.append(word)
f.sort()
print(f)
