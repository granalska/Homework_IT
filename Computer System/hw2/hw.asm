.model small
.stack 100h

.data
    a dw 5
    b dw 10
    c dw 3
    result dw ?

.code
main proc

    mov ax, @data
    mov ds, ax

    # AX = b
    mov ax, b

    # AX = b - c
    sub ax, c

    # AX = b - c + a
    add ax, a

    mov result, ax

    #вивід на екран
    mov ax, result
    call print_number

    mov ah, 4ch
    int 21h

main endp

print_number proc
    push ax
    push bx
    push cx
    push dx

    mov cx, 0
    mov bx, 10

convert:
    xor dx, dx
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne convert

print_loop:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop print_loop

    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_number endp

end main