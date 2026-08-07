c=0
file=input("Enter the file name: ")
file=open(file)
emails=file.read()
emails=emails.splitlines()
for email in emails:
    
    if email.startswith("From:"):
        t=email.replace("From:","") 
        
        c=c+1
        print(t.lstrip())
print ('There were', c, 'lines in the file with From as the first word')       
 
      

    
    

    
  