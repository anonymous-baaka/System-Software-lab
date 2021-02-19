org 100h

mov bl,05h      ;number
mov bh,00h
mov cl,bl  
mov ch,00h

mov ax,cx
dec cl

again:
mul cx
dec cx
jz end
jmp again


end:
ret
