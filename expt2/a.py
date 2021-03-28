

ip=open("input.txt",'r')
noLine=0
noWords=0
noBlank=0
noCharacter=0
for line in ip:
    noLine+=1
    #
    wordsinLine=len(line.split(" "))
    noWords+=wordsinLine
    print("noWords= ",wordsinLine)

    blankinLine=wordsinLine-1
    noBlank+=blankinLine
    print("noBlank= ", blankinLine)

    characterinLine=0
    for ele in line:
        if ele!='\n' and ele!=' ':
            characterinLine+=1
    noCharacter+=characterinLine
    print("noCharaac= ", characterinLine)

    print()
    print()

print("lines= ",noLine)
print("words= ",noWords)
print("blank= ",noBlank)
print("characters= ",noCharacter)

op=open("output.txt",'w')

op.write("lines = "+str(noLine)+"\n")
op.write("words= "+str(noWords)+"\n")
op.write("characters= "+str(noCharacter)+"\n")
op.write("blank= "+str(noBlank)+"\n")
