large= None
small= None    
while True:
    num=input("enter numbers")
    if num == "done":
        break
    try:
        num=int(num)
    except:
        print("Invalid input")
        continue

    
    if small is None:
            small=num
    elif small>num:
            small=num
    if large is None:
            large=num
    elif large<num:  
            large=num
print ('Maximum is',large)        
print ('Minimum is',small)   

         
 