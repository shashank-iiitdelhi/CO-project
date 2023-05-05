def hlt(arr,dic):
    arr.append(dic["hlt"]+"00000000000")

op={"add":"00000","sub":"00001","mov":"00010","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
regval={"FLAGS":"0000000000000000"}
var={}
mem={}
labels={}
f=open("test1.txt","r")
lines=[]
addresses={}
for line in f.readlines():
    if line.strip()!="":
        lines.append(line.strip())
f.close()
i=0
for line in lines:
    index=bin(i)[2:]
    while (len(index)!=7):
        index="0"+index
    if line.split()[0]!="var":
        addresses[index]=line
        i+=1
for line in lines:
    index=bin(i)[2:]
    while (len(index)!=7):
        index="0"+index
    if line.split()[0]!="var":
        break
    addresses[index]=line
    i+=1
for i,j in addresses.items():
    if j.split()[0]=="var":
        mem[j.split()[1]]=i
    if ":" in j:
        labels[j.split()[0][:-1]]=i
# print(addresses)
# print(mem)
# print(labels)
temp=[]
f=open("test1.txt","r")
for line in f.readlines():
    if line.strip()!="" and line.strip().split()[0]!="var":
        temp.append(line.strip())
f.close()
ans=[]
# print(temp)
pc="0000000"
while addresses[pc]!="hlt":
    ins=int(pc,2)
    t=""
    if temp[ins].split()[0]=="mov":
        t+=op["mov"]+"0"
        t+=reg[temp[ins].split()[1]]
        regval[temp[ins].split()[1]]=int(temp[ins].split()[2][1:])
        im=bin(int(temp[ins].split()[2][1:]))[2:]
        while len(im)!=7:
            im="0"+im
        t+=im
    elif temp[ins].split()[0]=="mul":
        regval[temp[ins].split()[1]]=regval[temp[ins].split()[2]]*regval[temp[ins].split()[3]]
        t+=op["mul"]+"00"
        t+=reg[temp[ins].split()[1]]+reg[temp[ins].split()[2]]+reg[temp[ins].split()[3]]
    elif temp[ins].split()[0]=="st":
        var[temp[ins].split()[2]]=regval[temp[ins].split()[1]]
        t+=op["st"]+"0"
        t+=reg[temp[ins].split()[1]]
        t+=mem[temp[ins].split()[2]]
    ans.append(t)
    pc=bin(ins+1)[2:]
    while (len(pc)!=7):
        pc="0"+pc
hlt(ans,op)
for i in ans:
    print(i)
