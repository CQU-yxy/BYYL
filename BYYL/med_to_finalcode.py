


def read_med_code(inpath):

    medcode = {}
    with open(inpath , 'r') as f:
        lines = f.readlines()
        for i in lines:
            i = i.replace('\n' , '')
            i = i.split('   ')
            medcode[i[0]] = i[1]

    f.close()
    return medcode

medcode = read_med_code('med_code.txt')
print(medcode)
final_code = {}
count = 0
reg_count = 0
id_reg = {}
num2num = {}

def add_code(s,count):
    global final_code
    final_code[count] = s

def add_count():
    global count
    count += 1


def judge_num(s):
    for i in range(0,10):
        if(str(i) in s and 't' not in s and 'n' not in s):
            return 1

    return 0

def add_reg(id ,reg):
    global id_reg
    id_reg[id] = reg

def add_reg_count():
    global reg_count
    reg_count += 1

def add_num(i , c):
    global num2num
    if i not in num2num:
        num2num[i] = []
        num2num[i].append(c)
    else:
        num2num[i].append(c)

def trans_code(medcode):


    target = []
    for i in medcode:

        if(i in target):
            s = 'loop{}: '.format(i)
            add_code(s, count)
            add_num(i, count)
            add_count()


        curr_code = medcode[i]
        # if语句
        if('if' in curr_code):
            curr_code = curr_code.split(' ')
            left = curr_code[1]
            op = curr_code[2]
            right = curr_code[3]
            target.append(curr_code[5])
            next = curr_code[5]

            reg = id_reg[left]
            if(judge_num(right)):
                s = 'addi $t{}, $zero, {}'.format(reg_count, right)
                add_code(s, count)
                add_reg_count()
                add_num(i, count)
                add_count()

                if(op == '=='):
                    s = 'beq {}, {}, {}'.format(reg, '$t{}'.format(reg_count-1) ,'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '<'):
                    s = 'blt {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '<='):
                    s = 'ble {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '>'):
                    s = 'bgt {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '>='):
                    s = 'bge {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '!='):
                    s = 'bnme {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
        elif ('while' in curr_code):
            curr_code = curr_code.split(' ')
            left = curr_code[1]
            op = curr_code[2]
            right = curr_code[3]
            target.append(curr_code[5])
            next = curr_code[5]

            reg = id_reg[left]
            if (judge_num(right)):
                s = 'addi $t{}, $zero, {}'.format(reg_count, right)
                add_code(s, count)
                add_reg_count()
                add_num(i, count)
                add_count()

                if (op == '=='):
                    s = 'beq {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '<'):
                    s = 'blt {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '<='):
                    s = 'ble {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '>'):
                    s = 'bgt {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '>='):
                    s = 'bge {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()
                elif (op == '!='):
                    s = 'bnme {}, {}, {}'.format(reg, '$t{}'.format(reg_count - 1), 'loop{}'.format(next))
                    add_code(s, count)
                    add_num(i, count)
                    add_count()

        # 赋值语句
        elif('=' in curr_code):
            # 运算 x op y 形式
            if('+' in curr_code or '-' in curr_code or '*' in curr_code
            or '/' in curr_code or '&' in curr_code or '|' in curr_code):
                curr_code = curr_code.split(' ')
                left = curr_code[0]
                operand1 = curr_code[2]
                op = curr_code[3]
                operand2 = curr_code[4]
                if(op == '+'):
                    if(left in id_reg):
                        reg = id_reg[left]
                        if(judge_num(operand1)):
                            pass
                        else:
                            reg1 = id_reg[operand1]
                            if(judge_num(operand2)):
                                pass
                            else:
                                reg2 = id_reg[operand2]
                                s = 'add {}, {}, {}'.format(reg, reg1 ,reg2)
                                add_code(s, count)
                                add_num(i,count)
                                add_count()
                    else:

                        if (judge_num(operand1)):
                            # left不存在，id1为num，id2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'add $t{}, $t{}, $t{}'.format(reg_count, reg_count-1, reg_count-2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                            # id不存在，id1为num ， id2为id
                            else:
                                reg1 = id_reg[operand2]
                                s = 'addi $t{}, {}, {}'.format(reg_count, reg1, operand1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                        else:
                            reg1 = id_reg[operand1]

                            # left不存在，op1为id，op2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, {}, {}'.format(reg_count, reg1, operand2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                            # left不存在，op1，op2均为id
                            else:
                                reg2 = id_reg[operand2]
                                s = 'add $t{}, {}, {}'.format(reg_count, reg1, reg2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                elif (op == '-'):
                    if (left in id_reg):
                        reg = id_reg[left]
                        if (judge_num(operand1)):
                            pass
                        else:
                            reg1 = id_reg[operand1]
                            if (judge_num(operand2)):
                                pass
                            else:
                                reg2 = id_reg[operand2]
                                s = 'sub {}, {}, {}'.format(reg, reg1, reg2)
                                add_code(s, count)
                                add_num(i, count)
                                add_count()
                    else:

                        if (judge_num(operand1)):
                            # left不存在，id1为num，id2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'sub $t{}, $t{}, $t{}'.format(reg_count, reg_count - 1, reg_count - 2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                            # id不存在，id1为num ， id2为id
                            else:
                                reg1 = id_reg[operand2]
                                s = 'addi $t{}, {}, {}'.format(reg_count, reg1, operand1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                        else:
                            reg1 = id_reg[operand1]

                            # left不存在，op1为id，op2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, {}, {}'.format(reg_count, reg1, operand2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                            # left不存在，op1，op2均为id
                            else:
                                reg2 = id_reg[operand2]
                                s = 'sub $t{}, {}, {}'.format(reg_count, reg1, reg2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                elif (op == '*'):
                    if (left in id_reg):
                        reg = id_reg[left]
                        if (judge_num(operand1)):
                            pass
                        else:
                            reg1 = id_reg[operand1]
                            if (judge_num(operand2)):
                                pass
                            else:
                                reg2 = id_reg[operand2]
                                s = 'mul {}, {}, {}'.format(reg, reg1, reg2)
                                add_code(s, count)
                                add_num(i, count)
                                add_count()
                    else:

                        if (judge_num(operand1)):
                            # left不存在，id1为num，id2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'mul $t{}, $t{}, $t{}'.format(reg_count, reg_count - 1, reg_count - 2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                            # id不存在，id1为num ， id2为id
                            else:
                                reg1 = id_reg[operand2]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_reg(operand1, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'mul $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                        else:
                            reg1 = id_reg[operand1]

                            # left不存在，op1为id，op2为num
                            if (judge_num(operand2)):
                                reg1 = id_reg[operand1]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_reg(operand2, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'mul $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                            # left不存在，op1，op2均为id
                            else:
                                reg2 = id_reg[operand2]
                                s = 'mul $t{}, {}, {}'.format(reg_count, reg1, reg2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                elif (op == '/'):
                    if (left in id_reg):
                        reg = id_reg[left]
                        if (judge_num(operand1)):
                            pass
                        else:
                            reg1 = id_reg[operand1]
                            if (judge_num(operand2)):
                                pass
                            else:
                                reg2 = id_reg[operand2]
                                s = 'div {}, {}, {}'.format(reg, reg1, reg2)
                                add_code(s, count)
                                add_num(i, count)
                                add_count()
                    else:

                        if (judge_num(operand1)):
                            # left不存在，id1为num，id2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'div $t{}, $t{}, $t{}'.format(reg_count, reg_count - 1, reg_count - 2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                            # id不存在，id1为num ， id2为id
                            else:
                                reg1 = id_reg[operand2]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_reg(operand1, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'div $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                        else:
                            reg1 = id_reg[operand1]

                            # left不存在，op1为id，op2为num
                            if (judge_num(operand2)):
                                reg1 = id_reg[operand1]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_reg(operand2, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'div $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                            # left不存在，op1，op2均为id
                            else:
                                reg2 = id_reg[operand2]
                                s = 'div $t{}, {}, {}'.format(reg_count, reg1, reg2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                elif (op == '&'):
                    if (left in id_reg):
                        reg = id_reg[left]
                        if (judge_num(operand1)):
                            pass
                        else:
                            reg1 = id_reg[operand1]
                            if (judge_num(operand2)):
                                pass
                            else:
                                reg2 = id_reg[operand2]
                                s = 'and {}, {}, {}'.format(reg, reg1, reg2)
                                add_code(s, count)
                                add_num(i, count)
                                add_count()
                    else:

                        if (judge_num(operand1)):
                            # left不存在，id1为num，id2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'and $t{}, $t{}, $t{}'.format(reg_count, reg_count - 1, reg_count - 2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                            # id不存在，id1为num ， id2为id
                            else:
                                reg1 = id_reg[operand2]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_reg(operand1, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'and $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                        else:
                            reg1 = id_reg[operand1]

                            # left不存在，op1为id，op2为num
                            if (judge_num(operand2)):
                                reg1 = id_reg[operand1]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_reg(operand2, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'and $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                            # left不存在，op1，op2均为id
                            else:
                                reg2 = id_reg[operand2]
                                s = 'and $t{}, {}, {}'.format(reg_count, reg1, reg2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                elif (op == '|'):
                    if (left in id_reg):
                        reg = id_reg[left]
                        if (judge_num(operand1)):
                            pass
                        else:
                            reg1 = id_reg[operand1]
                            if (judge_num(operand2)):
                                pass
                            else:
                                reg2 = id_reg[operand2]
                                s = 'or {}, {}, {}'.format(reg, reg1, reg2)
                                add_code(s, count)
                                add_num(i, count)
                                add_count()
                    else:

                        if (judge_num(operand1)):
                            # left不存在，id1为num，id2为num
                            if (judge_num(operand2)):
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'or $t{}, $t{}, $t{}'.format(reg_count, reg_count - 1, reg_count - 2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                            # id不存在，id1为num ， id2为id
                            else:
                                reg1 = id_reg[operand2]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand1)
                                add_reg(operand1, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'or $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                        else:
                            reg1 = id_reg[operand1]

                            # left不存在，op1为id，op2为num
                            if (judge_num(operand2)):
                                reg1 = id_reg[operand1]
                                s = 'addi $t{}, $zero, {}'.format(reg_count, operand2)
                                add_reg(operand2, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()
                                s = 'mul $t{}, $t{}, {}'.format(reg_count, reg_count - 1, reg1)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

                            # left不存在，op1，op2均为id
                            else:
                                reg2 = id_reg[operand2]
                                s = 'or $t{}, {}, {}'.format(reg_count, reg1, reg2)
                                add_reg(left, '$t{}'.format(reg_count))
                                add_code(s, count)
                                add_reg_count()
                                add_num(i, count)
                                add_count()

            # 单赋值形式
            else:
                curr_code = curr_code.split(' ')
                left = curr_code[0]
                right = curr_code[2]
                if(judge_num(right)):
                    if(left in id_reg):
                        reg = id_reg[left]
                        s = 'add {}, $zero, {}'.format(reg, right)
                        add_code(s, count)
                        add_num(i,count)
                        add_count()
                    else:
                        s = 'addi $t{}, $zero, {}'.format(reg_count , right)
                        add_reg(left, '$t{}'.format(reg_count))
                        add_code(s, count)
                        add_reg_count()
                        add_num(i, count)
                        add_count()
                else:
                    reg = id_reg[right]
                    if(left in id_reg):
                        reg1 = id_reg[left]
                        s = 'add {}, $zero, {}'.format(reg1, reg)
                        add_code(s, count)
                        add_num(i, count)
                        add_count()
                    else:
                        s = 'add $t{}, $zero, {}'.format(reg_count, reg)
                        add_reg(left, '$t{}'.format(reg_count))
                        add_code(s, count)
                        add_reg_count()
                        add_num(i, count)
                        add_count()


        elif('goto' in curr_code):
            curr_code =curr_code.split(' ')
            next = curr_code[1]
            target.append(next)

            s = 'j loop{}'.format(next)
            add_code(s, count)
            add_num(i, count)
            add_count()


trans_code(medcode)
print(id_reg)
print(final_code)

def code_to_txt(outpath):
    with open(outpath, 'w') as f:
        for i in final_code:
            f.write(str(i))
            f.write('   ')
            f.write(final_code[i])
            f.write('\n')
    f.close()

def delete_num(inpath , outpath):

    mips_code = []
    with open(inpath , 'r') as f1:
        lines = f1.readlines()
        for i in lines:
            i = i.split('   ')
            mips_code.append(i[1])
    f1.close()

    with open(outpath , 'w') as f2:
        for i in mips_code:
            f2.write(i)
    f2.close()


code_to_txt('target_code.txt')
delete_num('target_code.txt','target_code_without_num.txt')