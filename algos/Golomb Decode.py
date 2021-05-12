import math

def decode(x):
    num=0;
    for i in range(len(x)):
        num+=(int(x[len(x)-1-i])*(math.pow(2,i)));
    return num;

x=str(input('Enter code: '))
x=list(x)
b=int(input('Enter value of b: '))
i=math.floor(math.log(b,2))
d=math.pow(2,i+1)-b

rnum = 0
p2=0;
l=1;
while(p2<len(x)):
    t=0;
    flag=0;
    r=[];
    k=i;
    q=0;
    for p in range(p2,len(x)):
        if(x[p]=='0' and flag==0):
            t+=1;
            continue;
        if(x[p]=='1' and flag==0):
            q=t;
            flag=1;
            continue;
        r.append(x[p]);
        k-=1;
        if(k==0):
            rnum=decode(r);
            if(rnum<d):
                p2=p+1;
                break;
        if(k==-1):
            rnum=decode(r);
            rnum=rnum-d;
            p2=p+1;
            break;
    ans=q*b+rnum;
    print(int(ans));
    break
    l=0;
