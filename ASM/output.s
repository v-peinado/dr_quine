;colleen
global main
extern printf

section .text

main:
push rbx
lea rdi, [rel format]
lea rsi, [rel format]
mov rdx, 10
mov rcx, 34
xor rax, rax
call printf
pop rsi
ret ;ret

format:
db ";colleen%2$cglobal main%2$cextern printf%2$c%2$csection .text%2$c%2$cmain:%2$cpush rbx%2$clea rdi, [rel format]%2$clea rsi, [rel format]%2$cmov rdx, 10%2$cmov rcx, 34%2$cxor rax, rax%2$ccall printf%2$cpop rsi%2$cret ;ret%2$c%2$cformat:%2$cdb %3$c%1$s%3$c, 0", 0