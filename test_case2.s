add $a0, $t2, $t3
addu $a0, $t2, $t3
sb $s3, -56303($s2)
nor $v0, $a1, $a2
or $at, $s1, $t1
slt $t2, $s5, $s6
sltu $a2, $t5, $t6
sub $at, $a0, $t0
subu $v0, $a2, $a3
lw $t1, 57344($t0)
lw $t2, 55808($t0)
sw $t1, $t0, 57344
sw $t2, $t0, 55808
lw $t1, 57344($s0)
sw $t1, $s1, 55936
sll $t0, $s1, $2
srl $t0, $s0, $36
andi $t7, $t8, 256
ori $t7, $t8, 123
addi $t7, $t7, 52496
