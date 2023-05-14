def movImm(regval,reg,temp):
    regval[reg]=format(int(temp),"016b")

def movReg(regval,reg1,reg2):
    regval[reg1]=regval[reg2]

def load(regval,reg,var,address):
    regval[reg]=var[address]

def store(regval,reg,var,address):
    var[address]=regval[reg]

def xor(regval,reg1,reg2,reg3):
    regval[reg1]=format(int(regval[reg2][9:],2) ^ int(regval[reg3][9:],2),"016b")

def Or(regval,reg1,reg2,reg3):
    regval[reg1]=format(int(regval[reg2][9:],2) | int(regval[reg3][9:],2),"016b")

def And(regval,reg1,reg2,reg3):
    regval[reg1]=format(int(regval[reg2][9:],2) & int(regval[reg3][9:],2),"016b")

def invert(regval,reg1,reg2):
    Not=""
    for i in range(9,16):
        if regval[reg2][i]=="0":
            Not+="1"
        elif regval[reg2][i]=="1":
            Not+="0"
    regval[reg1]=format(int(Not,2),"016b")

def rshift(regval,reg1,num):
    regval[reg1]=format(int(regval[reg1][9:],2)>>int(num),"016b")

def lshift(regval,reg1,num):
    regval[reg1]=format(int(regval[reg1][9:],2)<<int(num),"016b")

def multiply(regval,reg1,reg2,reg3):
    prod=bin(int(regval[reg2][9:],2)*int(regval[reg3][9:],2))[2:]
    if len(prod)>7:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(int(prod,2),"016b")

def divide(regval,reg1,reg2):
    if regval[reg2]=="0000000000000000":
        regval["FLAGS"]="0000000000001000"
        regval["R0"]="0000000000000000"
        regval["R1"]="0000000000000000"
    else:
        regval["R0"]=format(int(regval[reg1][9:],2)//int(regval[reg2][9:],2),"016b")
        regval["R1"]=format(int(regval[reg1][9:],2)%int(regval[reg2][9:],2),"016b")
        regval["FLAGS"]="0000000000000000"

def add(regval, reg1, reg2, reg3):
    sum=bin(int(regval[reg2][9:],2)+int(regval[reg3][9:],2))[2:]
    if len(sum)>7:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(int(sum,2),"016b")

def sub(regval, reg1, reg2, reg3, dic):
    dif=bin(int(regval[reg2][9:],2)-int(regval[reg3][9:],2))[2:]
    if len(dif)>7:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(int(dif,2),"016b")

def cmp(regval,reg1,reg2):
    if (regval[reg1]<regval[reg2]):
        regval["FLAGS"]="0000000000000100"
    elif (regval[reg1]>regval[reg2]):
        regval["FLAGS"]="0000000000000010"
    else:
        regval["FLAGS"]="0000000000000001"

def jlt(regval,pc,address,labels):
    if regval["FLAGS"][-3]=="1":
        pc=int(labels[address],2)
        return pc
    return pc+1

def jgt(regval,pc,address,labels):
    if regval["FLAGS"][-2]=="1":
        pc=int(labels[address],2)
        return pc
    return pc+1

def je(regval,pc,address,labels):
    if regval["FLAGS"][-1]=="1":
        pc=int(labels[address],2)
        return pc
    return pc+1

def jmp(pc,address,labels):
    pc=int(labels[address],2)
    return pc

op={"add":"00000","sub":"00001","movi":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
regval={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
var={}
mem={}
labels={}
f=open("test.txt","r")
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
        cin=j.split()[0].index(":")
        labels[j.split()[0][:cin]]=i
temp=[]
f=open("test.txt","r")
for line in f.readlines():
    if line.strip()!="" and line.strip().split()[0]!="var":
        temp.append(line.strip())
f.close()
ans=[]
# print(addresses)
# print(var)
# print(labels)
# print(mem)
# print(temp)
for lines in temp:
    line=lines.split()
    t=""
    if "add" in line[0]:
        t+=op["add"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
    elif "sub" in line[0]:
        t+=op["sub"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
    elif ("mov" in line[0]) and ("$"==line[2][0]):
        t+=op["movi"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
    elif ("mov" in line[0]) and ("$"!=line[2][0]):
        t+=op["mov"]+"00000"+reg[line[1]]+reg[line[2]]
    elif "ld" in line[0]:
        t+=op["ld"]+"0"+reg[line[1]]+var[line[2]]
    elif "st" in line[0]:
        t+=op["st"]+"0"+reg[line[1]]+mem[line[2]]
    elif "mul" in line[0]:
        t+=op["mul"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
    elif "div" in line[0]:
        t+=op["div"]+"00000"+reg[line[1]]+reg[line[2]]
    elif "rs" in line[0]:
        t+=op["rs"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
    elif "ls" in line[0]:
        t+=op["ls"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
    elif "xor" in line[0]:
        t+=op["xor"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
    elif ("xor" not in line[0]) and ("or" in line[0]):
        t+=op["or"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
    elif "and" in line[0]:
        t+=op["and"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
    elif "not" in line[0]:
        t+=op["not"]+"00000"+reg[line[1]]+reg[line[2]]
    elif "cmp" in line[0]:
        t+=op["cmp"]+"00000"+reg[line[1]]+reg[line[2]]
    elif "jmp" in line[0]:
        t+=op["jmp"]+"0000"+labels[line[1]]
    elif "jlt" in line[0]:
        t+=op["jlt"]+"0000"+labels[line[1]]
    elif "jgt" in line[0]:
        t+=op["jgt"]+"0000"+labels[line[1]]
    elif "je" in line[0]:
        t+=op["je"]+"0000"+labels[line[1]]
    elif "hlt" in line[0]:
        t+=op["hlt"]+"00000000000"
    ans.append(t)
pc=0
flag=True
while True:
    if flag:
        regval["FLAGS"]="0000000000000000"
    flag=True
    # print(pc)
    # print(regval)
    bin_pc=format(pc,"07b")
    if "hlt" in addresses[bin_pc]:
        break
    if ("mov" in temp[pc].split()[0]) and (temp[pc].split()[2][0]=="$"):
        movImm(regval,temp[pc].split()[1],temp[pc].split()[2][1:])
    elif ("mov" in temp[pc].split()[0]) and (temp[pc].split()[2][0]!="$"):
        movReg(regval,temp[pc].split()[1],temp[pc].split()[2])
    elif "add" in temp[pc].split()[0]:
        add(regval,temp[pc].split()[1],temp[pc].split()[2],temp[pc].split()[2])
        flag=False
    elif "sub" in temp[pc].split()[0]:
        sub(regval,temp[pc].split()[1],temp[pc].split()[2],temp[pc].split()[2])
        flag=False
    elif "ld" in temp[pc].split()[0]:
        load(regval,temp[pc].split()[1],var,temp[pc].split()[2])
    elif "mul" in temp[pc].split()[0]:
        multiply(regval,temp[pc].split()[1],temp[pc].split()[2],temp[pc].split()[2])
        flag=False
    elif "div" in temp[pc].split()[0]:
        divide(regval,temp[pc].split()[1],temp[pc].split()[2])
        flag=False
    elif "st" in temp[pc].split()[0]:
        store(regval,temp[pc].split()[1],var,temp[pc].split()[2])
    elif "cmp" in temp[pc].split()[0]:
        cmp(regval,temp[pc].split()[1],temp[pc].split()[2])
        flag=False
    elif "jlt" in temp[pc].split()[0]:
        pc=jlt(regval,pc,temp[pc].split()[1],labels)
        continue
    elif "jgt" in temp[pc].split()[0]:
        pc=jgt(regval,pc,temp[pc].split()[1],labels)
        continue
    elif "je" in temp[pc].split()[0]:
        pc=je(regval,pc,temp[pc].split()[1],labels)
        continue
    elif "jmp" in temp[pc].split()[0]:
        pc=jmp(pc,temp[pc].split()[1],labels)
        continue
    pc+=1
for i in ans:
    print(i)
# print(addresses)
# print(var)
# print(labels)
# print(mem)

    
