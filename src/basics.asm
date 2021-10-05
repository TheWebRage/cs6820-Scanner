extern printf

section .data
stringBuffer: dd ""
var0_num1: dd 0
var1_num2: dd 0
var2_num3: dd 0
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
                        
                    _start:

mov eax, 3
mov eax, [var1_num2]
mov ebx, 10
add eax, ebx
mov [var2_num3], eax

mov ebx, [var1_num2]
add eax, ebx
mov [var1_num2], eax

mov ebx, 5
imul eax, ebx
mov [var0_num1], eax

mov ebx, [var1_num2]
imul eax, ebx
mov [var0_num1], eax

mov ebx, 5
sub eax, ebx
mov [var1_num2], eax

mov ebx, 5
sub eax, ebx
mov [var1_num2], eax

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
mov [var2_num3], eax

mov [var0_num1], 31

mov  ecx, 0xA 
               mov  [stringBuffer + 0], ecx
               call _printString

mov  ecx, [var0_num1] 
               mov  [stringBuffer + 0], ecx
               call _printString

mov  ecx, 0xA 
               mov  [stringBuffer + 0], ecx
               call _printString

mov  ecx, [var1_num2] 
               mov  [stringBuffer + 0], ecx
               call _printString

mov  ecx, 0xA 
               mov  [stringBuffer + 0], ecx
               call _printString

mov  ecx, [var2_num3] 
               mov  [stringBuffer + 0], ecx
               call _printString

mov  ecx, 0xA 
               mov  [stringBuffer + 0], ecx
               call _printString


mov       rax, 60                 ; system call for exit
          xor       rdi, rdi                ; exit code 0
          syscall                           ; invoke operating system to exit

