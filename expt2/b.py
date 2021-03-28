
class literal:
    def __init__(self,lit,address):
        self.lit=lit
        self.address=address
        self.used=False

class symbol:
    def __init__(self,sym,address):
        self.sym=sym
        self.address=address

class instruction:
    def __init__(self,name,type,machinecode,weight):
        self.name=name
        self.weight=weight
        self.machineCode=machinecode
        self.type=type

class inputInstruction(instruction):
    register=""
    memory=""
    locationCounter=0
    optab = open("optab.txt", 'r')
    global instructionList
    def __init__(self,name,register,memory,locationCounter):
        self.name=name
        self.register=register
        self.memory=memory
        self.locationCounter=locationCounter

        #instruction parameters
        for _instruction in instructionList:
            if _instruction.name==self.name:
                self.type=_instruction.type
                self.weight=_instruction.weight
                self.machineCode=_instruction.machineCode


def loadTableOptab(instructionList):
    optabInstructionList=[]
    for _instruction in instructionList:
        myInstr=instruction(_instruction[0],_instruction[1],_instruction[2][0],_instruction[2][1])
        optabInstructionList.append(myInstr)
    return optabInstructionList

def parseInstructions(optab):       #optab in readbale form
    instructionList=[]
    for line in optab:
        instruction=line.split()
        if len(instruction)>2:
            instruction[2]=instruction[2].strip('(')
            instruction[2] = instruction[2].strip(')')
            instruction[2]=instruction[2].split(',')
        instructionList.append(instruction)
    return (instructionList)

def getIndexOfOpcode(ele):          #index of opcode from instruction
    global instructionList
    for _instruction in instructionList:
        for i in range(len(ele)):
            if ele[i]==_instruction.name:
                return i
    return -1

def getInstructionType(opcode):
    global instructionList
    for _instruction in instructionList:
        if _instruction.name==opcode:
            return _instruction.type
    return ""

def getRegister(ele,index):
    type=getInstructionType(ele[index])

    if type=="IS":
        return ele[1]
    return ""

def getMemory(ele,index):
    type=getInstructionType(ele[index])
    if type=="IS":
        return ele[2]
    elif type=="AD":
        if ele[index]=="LTORG":
            return ""
        return ele[index+1]



def loadTableInput(inputInstructionsTable):
    inputInstructionClass=[]
    for ele in inputInstructionsTable:
        name=""
        register=""
        memory=""
        index=getIndexOfOpcode(ele)
        name=ele[index]
        register=getRegister(ele,index)
        memory=getMemory(ele,index)

def getWeight(opcode):
    global instructionList

    if opcode=="END":
        return '1'
    for ele in instructionList:
        if ele.name==opcode:
            return ele.weight

def classUp(inputInstructionsTable):
    global locationCounter
    global literalTable
    global symbolTable

    increment=0
    inputInstructionClassList=[]
    currentLiterals=[]      #only literal values
    previnst=''

    for row in inputInstructionsTable:
        opcode=getIndexOfOpcode(row)
        opcode=row[opcode]
        type=getInstructionType(opcode)

        if type=='IS':
            increment+=1
            try:
                register=row[1]
            except:
                register=""

            try:
                memory=row[2]
            except:
                memory=""

            try:
                if memory[0][0]=='=':
                    currentLiterals.append(memory[0])
            except:
                pass

        elif type=='AD':
            if opcode=='LTORG' or opcode=='END':
                #push literals
                for lit in currentLiterals:
                    literalTable.append(literal(lit,locationCounter))
                    locationCounter+=1
                currentLiterals=[]
            register=""
            try:
                memory=row[1]
            except:
                memory=""

        elif type=='DL':
            if opcode=='DC':
                symbolTable.append(symbol(row[0],locationCounter))
                locationCounter+=1
            elif opcode=='DS':
                symbolTable.append(symbol(row[0], locationCounter))
                locationCounter+=int(row[2][0])
            register=row[0]
            memory=row[2]

        if opcode=='START':
            inputInstructionClassList.append(inputInstruction(opcode, register.strip(','), memory, locationCounter))
            locationCounter=int(memory)
        else:
            inputInstructionClassList.append(inputInstruction(opcode,register.strip(','),memory,locationCounter))
            locationCounter+=increment
        increment=0

    return inputInstructionClassList

def getRegisterindex(reg):
    global registerList
    #print("reglist=",reg)
    for i in range(len(registerList)):
        if reg==registerList[i]:
            return i+1
    return 0

def getMemoryType(instruction):
    memory=instruction.memory
    if len(memory)==0:
        return ''
    memory=memory[0]
    if('=' in memory):
        return 'L'
    elif instruction.type=='DL' or memory.isdigit():
        return 'C'
    elif len(memory)!=0:
        return 'S'

def fourthCol(instruction,memorytype):
    global literalTable
    global symbolTable
    if memorytype=='C':
        temp= instruction.memory#[0].strip('(')
        if type(temp) is not str:
            temp=temp[0].strip('(')
            temp=temp.strip(')')
        temp.strip(')')
        return temp
    if memorytype=='L':
        #print("memory= ", instruction.memory[0])
        index=0
        for lit in literalTable:
            print("lit.lit= {} inst.mem= {}".format(lit.lit,instruction.memory[0]))
            if lit.lit==instruction.memory[0] and lit.used==False:

                lit.used=True
                return index+1
            else:
                index+=1
        return -9
    if memorytype=='S':
        index=0
        for symbol in symbolTable:
            if symbol.sym==instruction.memory[0]:
                return index+1
            else:
                index+=1

def writeToFile(file):
    global inputInstructionsTable
    global instructionList
    global symbolTable
    global literalTable
    global registerList

    file.write("\n")
    file.write("intermediate code \n")
    for _instruction in inputInstructionsTable:
        insType=_instruction.type
        insMXCode=_instruction.machineCode
        insRegisterIndex=getRegisterindex(_instruction.register)
        memoryType = getMemoryType(_instruction)
        insFourth=fourthCol(_instruction, memoryType)

        file.write('('+insType+','+insMXCode+')')       #6
        if(insRegisterIndex>0):
            file.write('\t('+str(insRegisterIndex)+')\t')       #11
        else:
            file.write('         ')

        if len(memoryType)!=0:
            file.write('(' + memoryType + ',' + str(insFourth) + ')')   #5
        else:
            file.write("     ")

        file.write('\t\t'+str(_instruction.locationCounter))

        file.write('\n')

    file.write("\n\n\n")
    file.write("Symbol Table\n")
    index=1
    for symbol in symbolTable:
        file.write('{}\t{}\t{}'.format(index,symbol.sym,symbol.address))
        file.write('\n')
        index+=1

    file.write("\n\n\n")
    file.write("Literal Table\n")
    index=1
    for literal in literalTable:
        file.write('{}\t{}\t{}'.format(index,literal.lit,literal.address))
        file.write('\n')
        index+=1


locationCounter=0
literalTable=[]
symbolTable=[]

optab=open("optab.txt",'r')
ip=open("code1.txt",'r')

registerList=['AREG','BREG','CREG','DREG']

instructionList=loadTableOptab(parseInstructions(optab))     #array of classes of optab
inputInstructionsTable=parseInstructions(ip)         #array of instructions of input code
inputInstructionsTable=classUp(inputInstructionsTable)
#for ele in inputInstructionsTable:
 #   print(ele.type,ele.name,ele.register,ele.memory,ele.locationCounter)

for ele in inputInstructionsTable:
     print(ele.type,ele.name,ele.register,ele.memory,end="\t\t\t")
     #if(ele.type!="AD"):
     print(ele.locationCounter,ele.weight,end="")
     print()


print("literals: ")
for ele in literalTable:
    print(ele.lit,ele.address)


print("------------")
print("symbol table: ")
for ele in symbolTable:
    print(ele.sym,ele.address)

print("------")
codeop=open("codeop.txt",'w')
writeToFile(codeop)
