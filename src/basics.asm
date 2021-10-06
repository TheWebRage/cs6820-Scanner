section .data

    stringBuffer: db 0
    var0_num1: db 0
    var1_num2: db 0
    var2_num3: db 0

section .text

global _start

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

_printInt: 
    mov  ecx, [stringBuffer]    ; Number 1
    add  ecx, 0x30              ; Add 30 hex for ascii
    mov  [stringBuffer], ecx    ; Save number in buffer
    mov  ecx, stringBuffer      ; Store address of stringBuffer in ecx

    mov  eax, 1                 ; sys_write
    mov  ebx, 1                 ; to STDOUT
    mov  edx, 1                 ; length = one byte
    int  0x80                   ; Call the kernel

    ret
    
_start:

;		num num1;
;		num num2 = 3;
mov rax, 3
mov [var1_num2], rax

;		num num3 = num2;
mov rax, [var1_num2]
mov [var2_num3], rax

;		num3 = num3 + 10;
mov rax, [var2_num3]
mov rbx, 10
add rax, rbx
mov [var2_num3], rax

;		num2 = num3 + num2;
mov rax, [var2_num3]
mov rbx, [var1_num2]
add rax, rbx
mov [var1_num2], rax

;		num1 = 2 * 5;
mov rax, 2
mov rbx, 5
imul rax, rbx
mov [var0_num1], rax

;		num1 = num3 * num2;
mov rax, [var2_num3]
mov rbx, [var1_num2]
imul rax, rbx
mov [var0_num1], rax

;		num2 = 8 - 5; //subtracting is fun!
mov rax, 8
mov rbx, 5
sub rax, rbx
mov [var1_num2], rax

;		num2=8- 5;
mov rax, 8
mov rbx, 5
sub rax, rbx
mov [var1_num2], rax

;		num3 = 8 ^ 6;
mov rax, 8
mov rbx, 8
imul rax, rbx
imul rax, rbx
imul rax, rbx
imul rax, rbx
imul rax, rbx
imul rax, rbx
mov [var2_num3], rax

;		write "Basics.txt:";
mov  rcx, "Basi" 
mov  [stringBuffer + 0], rcx
mov  rcx, "cs.t" 
mov  [stringBuffer + 4], rcx
mov  rcx, "xt:" 
mov  [stringBuffer + 8], rcx
call _printString


mov  rcx, 0xA 
mov  [stringBuffer + 0], rcx
call _printString

;		write num1;
mov  rcx, [var0_num1] 
add rcx, 0x30
mov  [stringBuffer + 0], rcx
call _printString

mov  rcx, 0xA 
mov  [stringBuffer + 0], rcx
call _printString

;		write num2;
mov  rcx, [var1_num2] 
add rcx, 0x30
mov  [stringBuffer + 0], rcx
call _printString

mov  rcx, 0xA 
mov  [stringBuffer + 0], rcx
call _printString

;		write num3;	
mov  rcx, [var2_num3] 
add rcx, 0x30
mov  [stringBuffer + 0], rcx
call _printString

mov  rcx, 0xA 
mov  [stringBuffer + 0], rcx
call _printString


mov       rax, 60                 ; system call for exit
xor       rdi, rdi                ; exit code 0
syscall                           ; invoke operating system to exit

