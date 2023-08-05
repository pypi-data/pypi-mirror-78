def sqrt(a):
    a=int(a)
    if (a==1) or (a==0):
         print('Root :-',a)
    elif a<0:
         print('Its an complex no.')
    else:
         x=[]
         test=a
         i=1
         while i <= test : 
             if test%i==0:
                 x.append(i)
                 test=test/i
                 i=2
             else:
                 i+=1
         test=x[0]
         real=1
         count=0
         root=[]
         t=0
         for i in x:
             t+=1
             if i==test:
                 count+=1
                 if count==2:
                     real*=i
                     count=0
                 if t==(len(x)):
                     if count==1:
                         root.append(x[len(x)-1])


             else:
                  if t==(len(x)):
                     root.append(x[len(x)-1])
                  if count==1:
                     root.append(test)
                  count=1
                  test=i
         rt=1
         for j in root:
             rt*=j
         if rt==1:
             print('Root :- ',real)
         elif real==1:
             print('Root :- ','√',rt)
         else:
             print('Root :- ',real,'√',rt)
