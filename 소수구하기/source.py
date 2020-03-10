#1929
line = input().split(" ")
minmax = [int(x) for x in line]
myrange = [x for x in range(0,minmax[1]+1)]
for var in myrange:
    if var <= 1 : 
        continue
    else :
        if var >= minmax[0] :
            print(var)
        loop = 2
        while var*loop<=minmax[1] :
            myrange[var*loop] = -1
            loop+=1
        
            
