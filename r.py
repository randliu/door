import os
path='./27/'
f=os.listdir(path)

n=0
for i in f:
    
    oldname=path+f[n]
    
    newname=path+'a'+str(n+1)+'.JPG'
    
    os.rename(oldname,newname)
    print(oldname,'======>',newname)
    
    n+=1
 
