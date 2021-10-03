global _start

sys_exit        equ     1
sys_write       equ     4
stdout          equ     1

section .text

_printString: 
; calculate the length of string
    mov     rdi, stringBuffer   ; stringBuffer to destination index
    xor     rcx, rcx            ; zero rcx
    not     rcx                 ; set rcx = -1
    xor     al,al               ; zero the al register (initialize to NUL)
    cld                         ; clear the direction flag
    repnz   scasb               ; get the string length (dec rcx through NUL)
    not     rcx                 ; rev all bits of negative results in absolute value
    dec     rcx                 ; -1 to skip the null-terminator, rcx contains length
    mov     rdx, rcx            ; put length in rdx

; write string to stdout
    mov     rsi, stringBuffer   ; stringBuffer to source index
    mov     rax, 1              ; set write to command
    mov     rdi,rax             ; set destination index to rax (stdout)
    syscall                     ; call kernel

    ret



_start: mov eax, 3
mov eax, [num2]
mov ebx, 10
add eax, ebx
mov [num3], eax

mov ebx, [num2]
add eax, ebx
mov [num2], eax

mov ebx, 5
imul eax, ebx
mov [num1], eax

mov ebx, [num2]
imul eax, ebx
mov [num1], eax

mov ebx, 5
sub eax, ebx
mov [num2], eax

mov ebx, 5
sub eax, ebx
mov [num2], eax

mov eax, 8
mov eax, 8
mov ebx, 6
imul eax, ebx
mov eax, 8
mov ebx, 6
imul eax, ebx
mov eax, 8
mov ebx, 6
imul eax, ebx
mov eax, 8
mov ebx, 6
imul eax, ebx
mov eax, 8
mov ebx, 6
imul eax, ebx
mov eax, 8
mov ebx, 6
imul eax, ebx
mov [num3], eax

    mov  ecx, "Hell" 
    mov  [stringBuffer], ecx
    mov  ecx, "o wo" 
    mov  [stringBuffer + 4], ecx
    mov  ecx, "rld!" 
    mov  [stringBuffer + 8], ecx
    mov  ecx, "" 
    mov  [stringBuffer+ 12], ecx
    call _printString

    mov  ecx, 0xA 
    mov  [stringBuffer], ecx
    call _printString

    mov  ecx, 1
    add  ecx, 0x30
    mov  [stringBuffer], ecx
    call _printString

    mov  ecx, 0xA 
    mov  [stringBuffer], ecx
    call _printString


mov eax, sys_exit
mov ebx, 0
int 0x80

section .data
newLine: dd 0xA
stringBuffer: dd ""
num1: dd 0
num2: dd 0
num3: dd 0


