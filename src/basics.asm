extern printf

section .data
stringFormat: .asciz "%s\n"
intFormat: .asciz "%d\n"
num1: dd 0
num2: dd 0
num3: dd 0

section .text
mov eax, 3
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

push %rbx
lea  stringFormat(%rip), %rdi
mov  $1, ["Basics.txt:"]
xor %eax, %eax
call printf
pop %rbx

push %rbx
lea  intFormat(%rip), %rdi
mov  $1, [num1]
xor %eax, %eax
call printf
pop %rbx

push %rbx
lea  intFormat(%rip), %rdi
mov  $1, [num2]
xor %eax, %eax
call printf
pop %rbx

push %rbx
lea  intFormat(%rip), %rdi
mov  $1, [num3]
xor %eax, %eax
call printf
pop %rbx

