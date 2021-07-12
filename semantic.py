import csv
import struct

from graphviz import Digraph
import os

VN = {}
VT = {}
proce = []
first = {}
follow = {}
proce1 = []
synch = 100
used_proce = []
g = Digraph('AST')

## 把return改成了struct
total_char = ["int","void","float","char","string","bool","if","else","while","for","get","put","struct","and","or",
              '+','-','*','/',"=","<",">","!=",">=","<=","==" , "," , ";" ,"(",")","{","}","&","|","!"]
num2char = {}
for i in range(len(total_char)):
    num2char[str(i + 1)] = total_char[i]

def read_lexical():
    sentence = []
    sem_sentence = []
    line = []
    with open('lexical_result.txt',"r") as f:
        lines =f.readlines()
        for i in lines:
            i = i.replace('\n', '')
            i = i.split(' ')
            sentence.append(i[0])
            sem_sentence.append(i[1])
            line.append(int(i[2]))
    f.close()
    sentence = trans_lexi(sentence)
    print(sentence)
    print(sem_sentence)
    print(line)

    return sentence , sem_sentence , line

def trans_lexi(numlist):
    for i in range(len(numlist)):
        if(numlist[i] == '38'):
            numlist[i] = 'num'
        elif(numlist[i] == '36'):
            numlist[i] = 'id'
        else:
            numlist[i] = num2char[numlist[i]]

    return numlist

def read_in():

    path = "../rule.txt"
    with open(path,"r") as f:
        line1 = f.readline()
        line1 =  line1.replace('\n','')
        temp = []
        temp = line1.split(' ')
        for i in range(len(temp)):
            VN[i] = temp[i]
        print(VN)

    with open(path,"r") as f:
        next(f)
        line1 = f.readline()
        line1 =  line1.replace('\n','')
        temp1 = line1.split(' ')
        for i in range(len(temp1)):
            VT[i+16] = temp1[i]
        print(VT)


    with open(path,"r") as f:
        next(f)
        next(f)
        lines = f.readlines()
        for i in range(len(lines)):
            proce1.append(lines[i].rstrip(('\n')))
            lines[i] = lines[i].replace('->','1')
            proce.append(lines[i].rstrip('\n'))

def get_first():
    # 初始化first集字典，key：string value：[]
    for i in range(16 , 16 + len(VT)):
        first[VT[i]] = [VT[i]]
    for i in range(len(VN)):
        first[VN[i]] = []
    for j in range(len(proce)):
        # 若可直接推出epsilon，直接添加
        if(proce[j][2] == '@'):
            first[proce[j][0]].append('@')
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')
        # 若可直接推出终结符，直接添加
        if(procetemp[0] in VT.values()):
            first[proce[j][0]].append(procetemp[0])
        if(procetemp[0] in VN.values()):
            while 1:
                if('@' in first[procetemp[0]]):
                    # first[proce[j][0]] += first[procetemp[0]]

                    # 添加所有不为空的元素，同时下移
                    templist = first[procetemp[0]]
                    for i in range(len(templist)):
                        if(templist[i] != '@'):
                            first[proce[j][0]].append(templist[i])
                    procetemp = procetemp[1:]
                    if (len(procetemp) == 0):
                        break
                else:
                    first[proce[j][0]] += first[procetemp[0]]
                    break

    # 再倒序执行一次
    for j in range(len(proce)-1 , -1 ,-1):
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')
        if(procetemp[0] in VN.values()):
            while 1:
                if ('@' in first[procetemp[0]]):
                    # first[proce[j][0]] += first[procetemp[0]]
                    templist = first[procetemp[0]]
                    for i in range(len(templist)):
                        if (templist[i] != '@'):
                            first[proce[j][0]].append(templist[i])
                    procetemp = procetemp[1:]
                    if (len(procetemp) == 0):
                        break
                else:
                    first[proce[j][0]] += first[procetemp[0]]
                    break


    # 去除重复元素
    for i in range(len(VN)):
        templist = first[VN[i]]
        first[VN[i]] = sorted(set(templist), key = templist.index)


def get_follow():
    for i in range(len(VN)):
        follow[VN[i]] = []
    follow['Z'].append('$')
    for j in range(len(proce)):
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')
        while 1:
            if(procetemp[0] in VT.values()):
                procetemp = procetemp[1:]
            if(len(procetemp) <= 1):
                break
            if(procetemp[0] in VN.values()):
                # follow[procetemp[0]] += first[procetemp[1]]
                templist = first[procetemp[1]]
                for i in range(len(templist)):
                    if (templist[i] != '@'):
                        follow[procetemp[0]].append(templist[i])
                procetemp = procetemp[1:]
    for j in range(len(proce)):
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')
        if(procetemp[-1] in VN.values()):
            follow[procetemp[-1]] += follow[proce[j][0]]
        if(len(procetemp)>=2):
            if((procetemp[-1] in VN.values()) & (procetemp[-2] in VN.values()) & ('@' in first[procetemp[-1]])):
                follow[procetemp[-2]] += follow[proce[j][0]]
    for j in range(len(proce)-1 , -1 ,-1):
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')
        if(procetemp[-1] in VN.values()):
            follow[procetemp[-1]] += follow[proce[j][0]]
        if(len(procetemp)>=2):
            if((procetemp[-1] in VN.values()) & (procetemp[-2] in VN.values()) & ('@' in first[procetemp[-1]])):
                follow[procetemp[-2]] += follow[proce[j][0]]
    # 去除重复元素
    for i in range(len(VN)):
        templist = follow[VN[i]]
        follow[VN[i]] = sorted(set(templist), key = templist.index)

def find_key(value,dic):
    for i in range(len(dic)):
        if(dic[i] == value):
             return i

def find_key2(value ,dic):
    for i in range(len(dic)):
        if(dic[i+16] == value):
            return i + 16


def get_table():
    for j in range(len(proce)):
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')

        row = find_key(proce[j][0] , VN)
        for k in range(len(VT)):
            if(procetemp[0] != '@'):
                if(VT[k+16] in first[procetemp[0]]):
                    pred_table[row][k] = j+1
    for j in range(len(proce)):
        procetemp = proce[j][2:]
        procetemp = procetemp.split(' ')

        row = find_key(proce[j][0], VN)
        if (procetemp[0] != '@'):
            if('@' in first[procetemp[0]]):
                for fol in follow[proce[j][0]]:
                    k = find_key2(fol , VT) - 16
                    pred_table[row][k] = j+1
        else:
            for fol in follow[proce[j][0]]:
                if(fol != '@' and fol != '$'):
                    k = find_key2(fol, VT) - 16
                    pred_table[row][k] = j + 1

def get_table_synch():
    for i in range(len(VN)):
        for fol in follow[VN[i]]:
            if(fol == '@' or fol =='$'):
                continue
            else:
                k = find_key2(fol,VT) - 16
                if(pred_table[i][k] == 0):
                    pred_table[i][k] = synch


def print_table(path2):

    temp_proce = []
    with open('../rule.txt', "r") as f:
        next(f)
        next(f)
        lines = f.readlines()
        for i in range(len(lines)):
            temp_proce.append(lines[i])
    f.close()

    with open(path2, 'w') as f:
        f_csv = csv.writer(f)
        temp2 = []
        for i in range(len(VT)):
            temp2.append(VT[i+16])
        f_csv.writerow(temp2)
        for i in range(len(VN)):
            temp = []
            for j in range(len(VT)):
                if(pred_table[i][j] == 0):
                    temp.append(' ')
                elif(pred_table[i][j] == synch):
                    temp.append('synch')
                else:
                    temp.append(temp_proce[pred_table[i][j] - 1])
            f_csv.writerow(temp)
    f.close()



# sentence = ['id' , '=','num' , '*' ,'num',';' , 'id' , '=' , 'id' , ';' ]
sentence = ['int','id','(','int', 'id', ')','{', 'id', '=', 'num', ';','}',';','int','id','(','int', 'id', ')','{', 'id', '=', 'num', ';','}']
# sem_sentence = ['x' , '=','1' ,'*' , '2',';' , 'y' , ' = ' , 'x' ,' ;']
sem_sentence = ['int','make','(','int', 'x', ')','{', 'x', '=', '1', ';','}',';','int','make','(','int', 'y', ')','{', 'y', '=', '2', ';','}']
# sentence = ['if','(','id','==','num',')','{','id','=','id',';','}']
# sem_sentence = ['if','(','x','==','1',')','{','x','=','y',';','}']
line = [1,1,1,1,1,2,3,3,3,3,4,4,5,5,5,5,5,6,7,7,7,7,8]


context = ["digraph d {\n"]
count = 1
# sentence , sem_sentence , line = read_lexical()
id_table = []
func_talbe = []

class id:
    def __init__(self,type , name , val):
        self.type = type
        self.val = val
        self.name = name

class func:
    def __init__(self,type , name , para_type):
        self.type = type
        self.name = name
        self.para = para_type

id1 = id('int' , 'x' , 1)
id2 = id('bool' , 'y' ,0)
id_table.append(id1)
id_table.append(id2)


def judge_null():
    if(len(sentence) == 0):
        return 1

def forward():
    global sentence
    sentence = sentence[1:]
    global sem_sentence
    sem_sentence = sem_sentence[1:]
    global line
    line = line[1:]

def add_sym(sym):
    sentence1 = []
    sentence1.append(sym)
    global sentence
    for i in sentence:
        sentence1.append(i)

    sentence = sentence1

    sem_sentence1 = []
    sem_sentence1.append(sym)
    global sem_sentence
    for i in sem_sentence:
        sem_sentence1.append(i)

    sem_sentence = sem_sentence1

def find_id(name):
    for i in id_table:
        if(i.name == name):
            return i

def find_func(name):
    for i in func_talbe:
        if(i.name == name):
            return i

def add_context(s):
    global context
    context.append(s)

def add_count():
    global count
    count = count + 1

def semantic_analyze():
    fxZ()
    print('error! 丢失运算符，默认补上+')
    print('finish')

s = '\tnode{} [label="{}"]\n'.format(1 , 'root')
add_context(s)
add_count()

def fxZ():
    if (judge_null()):
        s = '}'
        add_context(s)
        add_count()
        f = open('tree_node_leaf.txt', "w")
        for i in context:
            f.write(i)
        f.close()
        # 生成图片
        os.system('dot -Tpng tree_node_leaf.txt -o tree.png')
        return 0
    x = sentence[0]
    row = find_key('Z' , VN)
    column = find_key2(x, VT) - 16

    if( (pred_table[row][column] - 1) == 0):
        val = fxS()
        if(val!=0):
            # print(val)
            pass
        fxZ()
    elif((pred_table[row][column] - 1) == 1):
        pass
    else:
        return 0


def fxS():
    x = sentence[0]
    row = find_key('S', VN)
    column = find_key2(x, VT) - 16
    if (judge_null()):
        return 0

    if ((pred_table[row][column] - 1) == 2):
        type = fxA()
        s = '\tnode{} [label="{}"]\n'.format(count , type)
        add_context(s)
        add_count()
        s = '\tnode{} -> node{}\n'.format(1 ,count)
        add_context(s)
        id = fxL(type)
        if(id != 0):
            s = '\tnode{} [label="{}"]\n'.format(count , id.name)
            add_context(s)
            add_count()
            s = '\tnode{} -> node{}\n'.format(1 , count)
            add_context(s)

        if (judge_null()):
            return 0
        if(sentence[0] != ';' and id != 0):
            print('在{}行发生error! 声明语句结尾缺少分号'.format(line[0]))
            add_sym(';')
        forward()
        return id

    elif ((pred_table[row][column] - 1) == 3):
        temp_id = find_id(sem_sentence[0])
        forward()
        temp_id = fxB(temp_id)
        if(temp_id != None or 0):
            # print( temp_id.type , temp_id.name ,temp_id.val)
            pass
        if (sentence[0] != ';'):
            print('在{}行发生error! 语句结束缺少；'.format(line[0]))
            add_sym(')')
        forward()
        return 0
    elif ((pred_table[row][column] - 1) == 4):
        if (x != 'if'):
            add_sym('if')
        forward()
        if (sentence[0] != '('):
            print('在{}行发生error!if语句后应该紧跟着左括号'.format(line[0]))
            add_sym('(')
        forward()
        xeval = fxX()
        if (sentence[0] != ')'):
            print('在{}行发生error!if条件表达式缺少右括号'.format(line[0]-1))
            add_sym(')')
        forward()
        if(xeval):
            if (sentence[0] != '{'):
                print('在{}行发生error!if语句缺少左大括号'.format(line[0]-1))
                add_sym('{')
            forward()
            fxZ()

            if (sentence[0] != '}'):
                print('在{}行发生error!if语句缺少右括号'.format(line[0]-1))
                add_sym('}')
            forward()
            fxQ()
            return 0
        else:
            return 0
    elif ((pred_table[row][column] - 1) == 5):
        if (x != 'while'):
            add_sym('while')
        forward()
        if (sentence[0] != '('):
            print('在{}行发生error!if语句后应该紧跟着左括号'.format(line[0]))
            add_sym('(')
        forward()
        xeval = fxX()
        if (sentence[0] != ')'):
            print('在{}行发生error!if条件表达式缺少右括号'.format(line[0]-1))
            add_sym(')')
        forward()
        if(xeval):
            if (sentence[0] != '{'):
                print('在{}行发生error!if语句缺少左大括号'.format(line[0]-1))
                add_sym('{')
            forward()
            fxZ()

            if (sentence[0] != '}'):
                # print('在{}行发生error!if语句缺少右括号'.format(line[0]-1))
                add_sym('}')
            forward()
            return 0
        else:
            return 0

    elif ((pred_table[row][column] - 1) == 6):
        forward()
        x = sentence[0]
        if (x != '('):
            add_sym('(')
            print('在{}行发生error! get后应紧跟左括号'.format(line[0]))
        forward()
        eval = fxL(None)
        if (sentence[0] != ')'):
            add_sym(')')
            print('在{}行发生error! 缺少右括号'.format(line[0]-1))
        forward()
        if (sentence[0] != ';'):
            add_sym(';')
            print('在{}行发生error! 缺少分号'.format(line[0]-1))
        forward()
        return eval.val

    elif ((pred_table[row][column] - 1) == 7):
        forward()
        x = sentence[0]
        if (x != '('):
            add_sym('(')
            print('在{}行发生error! put后应紧跟左括号'.format(line[0]))
        forward()
        eval = fxL(None)
        if (sentence[0] != ')'):
            add_sym(')')
            print('在{}行发生error! 缺少右括号'.format(line[0]-1))
        forward()
        if (sentence[0] != ';'):
            add_sym(';')
            print('在{}行发生error! 缺少分号'.format(line[0]-1))
        forward()
        return eval.val




def fxA():
    x = sentence[0]
    row = find_key('A', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 38):
        forward()
        return 'char'
    elif ((pred_table[row][column] - 1) == 39):
        forward()
        return 'string'
    elif ((pred_table[row][column] - 1) == 40):
        forward()
        return 'int'
    elif ((pred_table[row][column] - 1) == 41):
        forward()
        return 'long'
    elif ((pred_table[row][column] - 1) == 42):
        forward()
        return 'float'
    elif ((pred_table[row][column] - 1) == 43):
        forward()
        return 'double'
    elif ((pred_table[row][column] - 1) == 44):
        forward()
        return 'bool'
    elif ((pred_table[row][column] - 1) == 45):
        forward()
        return 'void'
    elif ((pred_table[row][column] - 1) == 46):
        forward()
        return 'struct'
    else:
        print('在{}行发生error! 未知数据类型'.format(line[0]))
        forward()
        return 0


def fxB(id):
    x = sentence[0]
    row = find_key('B', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 8):
        if(sentence[0] != '('):
            print('在{}行发生error! 函数定义缺少左括号'.format(line[0]))
            add_sym('(')
        forward()
        fxS()
        if (sentence[0] != ')'):
            print('在{}行发生error! 函数定义缺少右括号'.format(line[0]-1))
            add_sym(')')
        forward()
        if (sentence[0] != '；'):
            print('在{}行发生error! 语句结束缺少分号'.format(line[0]-1))
            add_sym(';')
        forward()

        return 0

    elif ((pred_table[row][column] - 1) == 9):
        if(sentence[0] != '='):
            print('在{}行发生error! 缺少赋值符号'.format(line[0]-1))
            add_sym('=')
        forward()
        id1 = fxE()

        if(id.type != id1.type):
            print('在{}行发生error! 类型不同不能直接赋值！'.format(line[0]))
            return 0
        else:
            id.val = id1.val
            print(id.type , id.name ,id.val)
            return id


def fxH():
    if (judge_null()):
        return 0
    x = sentence[0]
    row = find_key('H', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 22):
        return 0
    elif ((pred_table[row][column] - 1) == 21):
        sym , temp_id = fxM()
        fxH()
        return [sym , temp_id]
    else:
        return 0

def fxL(type):
    x = sentence[0]
    row = find_key('L', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 10):
        id1 = id(type , sem_sentence[0] , val=0)
        if (find_id(sem_sentence[0])):
            print('在{}行发生error! 该变量{}重复定义'.format(line[0],sem_sentence[0]))
            forward()
            return 0
        id_table.append(id1)
        forward()
        temp = fxP(id1)
        if(temp == 1):
            return 0
        return id1
    elif ((pred_table[row][column] - 1) == 11):
        pass
    elif((pred_table[row][column] - 1) == 12):
        return 0


def fxP(id1):
    x = sentence[0]
    row = find_key('P', VN)
    column = find_key2(x, VT) - 16
    if (judge_null()):
        return None
    if ((pred_table[row][column] - 1) == 13):
        if(x != ','):
            add_sym(',')
            print('在{}行发生error! 缺少,'.format(line[0]))
        forward()
        if(sentence[0] != 'id'):
            print('在{}行发生error!后面应跟id符号'.format(line[0]))
            return -1
        id2 = id(id1.type, sem_sentence[0], val=0)
        if (find_id(sem_sentence[0])):
            print('在{}行发生error! 该变量{}重复定义'.format(line[0],sem_sentence[0]))
            forward()
            return 0
        id_table.append(id2)
        forward()
        fxP(id2)
        return 0

    elif((pred_table[row][column] - 1) == 14):
        if (find_func(id1.name)):
            print('在{}行发生error! 当前函数已存在不可重复定义'.format(line[0]))
            return 0
        if(sentence[0] != '('):
            print('在{}行发生error! 缺少左括号'.format(line[0]))
            add_sym('(')
        forward()
        temp_id = fxS()
        if (sentence[0] != ')'):
            print('在{}行发生error! 缺少右括号'.format(line[0]))
            add_sym(')')
        forward()
        if (sentence[0] != '{'):
            print('在{}行发生error! 缺少左括号'.format(line[0]-1))
            add_sym('{')
        forward()
        fxZ()
        if (sentence[0] != '}'):
            print('在{}行发生error! 缺少右括号'.format(line[0]-1))
            add_sym('}')
        forward()
        func1 = func(id1.type , id1.name , temp_id.type)
        func_talbe.append(func1)

        return 1

    elif ((pred_table[row][column] - 1) == 47):
        if (sentence[0] != '{'):
            print('在{}行发生error! 缺少左括号'.format(line[0]))
            add_sym('{')
        forward()
        fxZ()
        if (sentence[0] != '}'):
            print('在{}行发生error! 缺少右括号'.format(line[0]))
            add_sym('}')
        forward()

        return 0

    elif ((pred_table[row][column] - 1) == 15):
        return 0

def fxQ():
    if (judge_null()):
        return None
    x = sentence[0]
    row = find_key('Q', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 17):
        return 0
    elif ((pred_table[row][column] - 1) == 18):
        fxS()
def fxX():

    x = sentence[0]
    row = find_key('X', VN)
    column = find_key2(x, VT) - 16
    if (judge_null()):
        return None
    if ((pred_table[row][column] - 1) == 19):
        temp_id = fxE()
        op = fxR()
        temp_id2 = fxE()
        if(temp_id.type != temp_id2.type):
            print('在{}行发生error! 类型不同不能比较'.format(line[0]))
        if(op == '>'):
            if(temp_id.val > temp_id2.val):
                return 1
            else:
                return 0
        elif (op == '=='):
            if (temp_id.val == temp_id2.val):
                return 1
            else:
                return 0

def fxE():
    x = sentence[0]
    row = find_key('E', VN)
    column = find_key2(x, VT) - 16
    if (judge_null()):
        return 0
    if ((pred_table[row][column] - 1) == 20):
        temp_id = fxF()
        temp = fxH()
        if(temp != 0 ):
            sym, temp_id2 = temp[0] , temp[1]
            if(sym == '+'):
                if (temp_id.type != 'int' or temp_id2.type != 'int'):
                    print('在{}行发生error! 非int类型不能参与算术运算'.format(line[0]))
                else:
                    # g.node(name='+')
                    # g.node(name=str(temp_id.val))
                    # g.node(name=str(temp_id2.val))
                    # g.edge('+',str(temp_id.val))
                    # g.edge('+' ,str(temp_id2.val))
                    temp_id.val = temp_id2.val + temp_id.val

            elif (sym == '-'):
                if (temp_id.type != 'int' or temp_id2.type != 'int'):
                    print('在{}行发生error! 非int类型不能参与算术运算'.format(line[0]))
                else:
                    temp_id.val = temp_id2.val - temp_id.val
            elif (sym == '&'):
                if (temp_id.type != temp_id2.type):
                    print('在{}行发生error! 类型不同不能运算'.format(line[0]))
                else:
                    temp_id.val = temp_id2.val and temp_id.val
            elif (sym == '|'):
                if (temp_id.type != temp_id2.type):
                    print('在{}行发生error! 类型不同不能运算'.format(line[0]))
                else:
                    temp_id.val = temp_id2.val or temp_id.val
            elif (sym == '*'):
                if (temp_id.type != 'int' or temp_id2.type != 'int'):
                    print('在{}行发生error! 非int类型不能参与算术运算'.format(line[0]))
                else:
                    temp_id.val = temp_id2.val * temp_id.val
            elif (sym == '/'):
                if (temp_id.type != 'int' or temp_id2.type != 'int'):
                    print('在{}行发生error! 非int类型不能参与算术运算'.format(line[0]))
                else:
                    temp_id.val = temp_id2.val / temp_id.val

        return temp_id

def fxM():
    x = sentence[0]
    row = find_key('M', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 23):
        sym = '+'
        forward()
        temp_id = fxF()
        return sym , temp_id
    elif ((pred_table[row][column] - 1) == 24):
        sym = '-'
        forward()
        temp_id = fxF()
        return sym, temp_id

    elif ((pred_table[row][column] - 1) == 25):
        sym = '&'
        forward()
        temp_id = fxF()
        return sym, temp_id

    elif ((pred_table[row][column] - 1) == 26):
        sym = '|'
        forward()
        temp_id = fxF()
        return sym, temp_id

    elif ((pred_table[row][column] - 1) == 27):
        sym = '*'
        forward()
        temp_id = fxF()
        return sym, temp_id

    elif ((pred_table[row][column] - 1) == 28):
        sym = '/'
        forward()
        temp_id = fxF()
        return sym, temp_id
    else:
        print('在{}行发生error! 缺失运算符'.format(line[0]))
        temp_id = fxF()
        return '+' , temp_id


def fxF():
    x = sentence[0]
    row = find_key('F', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 29):
        temp_id = find_id(sem_sentence[0])
        forward()
        return temp_id
    elif ((pred_table[row][column] - 1) == 30):
        temp_id = id('int' , sem_sentence[0] , int(sem_sentence[0]))
        forward()
        return temp_id
    elif ((pred_table[row][column] - 1) == 31):
        if(sentence[0] != '('):
            print('在{}行发生error! 缺少左括号'.format(line[0]))
            add_sym('(')
        forward()
        temp_id = fxE()
        if(sentence[0] != ')'):
            add_sym(')')
            print('在{}行发生error! 缺少右括号'.format(line[0]))
        forward()
        return temp_id
    else:
        print('在{}行发生error! 缺少操作数'.format(line[0]))
        return 0

def fxR():
    x = sentence[0]
    row = find_key('R', VN)
    column = find_key2(x, VT) - 16
    if ((pred_table[row][column] - 1) == 32):
        forward()
        return '>'
    elif ((pred_table[row][column] - 1) == 33):
        forward()
        return '>='
    elif ((pred_table[row][column] - 1) == 34):
        forward()
        return '<'
    elif ((pred_table[row][column] - 1) == 35):
        forward()
        return '<='
    elif ((pred_table[row][column] - 1) == 36):
        forward()
        return '=='
    elif ((pred_table[row][column] - 1) == 37):
        forward()
        return '!='


if __name__ == "__main__":
    read_in()
    get_first()
    get_follow()

    pred_table = [[0 for i in range(len(VT))] for j in range(len(VN))]
    get_table()
    get_table_synch()
    # print_table('predict_table.csv')
    # sentence = ['get' ,'(' ,'id' , ')',';','if','(','id','==','num',')','{','id','=','num',';','}',';']
    # sem_sentence = ['get' , '(' , 'x' , ')',';','if','(','x','==','1',')','{','x','=','2',';','}',';']
    # sentence = ['if','(','id','==','num',')','{','id','=','num',';','}',';','else','{','id','=','id','+','num',';','}',';']

    print(proce1)
    # analyze(sentence)

    semantic_analyze()
    # read_lexical()


