import csv
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


total_char = ["int","void","float","char","string","bool","if","else","while","for","get","put","return","and","or",
              '+','-','*','/',"=","<",">","!=",">=","<=","==" , "," , ";" ,"(",")","{","}","&","|","!"]
num2char = {}
for i in range(len(total_char)):
    num2char[str(i + 1)] = total_char[i]

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

    path = "syntax_rule.txt"
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

    print(first)

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
    print(follow)

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
    with open('syntax_rule.txt', "r") as f:
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


def analyze(sentence):
    stack = []
    stack.append('$')
    stack.append('Z')
    # g.node(name='Z')

    while 1:
        x = stack[-1]
        if(x == '$' or x in VT.values()):
            if(x == sentence[0]):
                stack.pop(-1)
                sentence = sentence [1:]
            else:
                # 错误处理，弹出不匹配的终结符
                print('error!!当前终结符不匹配！')
                stack.pop(-1)
        elif(x == '@'):
            stack.pop(-1)
        else:
            row = find_key(x , VN)
            column = find_key2(sentence[0] , VT) - 16
            if(pred_table[row][column] != 0 and pred_table[row][column] != synch ):
                stack.pop(-1)
                temp = proce[pred_table[row][column] - 1]
                temp = temp[2:]
                temp = temp.split(' ')
                for i in range(len(temp)-1,-1,-1):
                    stack.append(temp[i])
                # g.edge(x,sentence[0])
                used_proce.append(proce1[pred_table[row][column] - 1])
                print(proce1[pred_table[row][column] - 1])
            elif(pred_table[row][column] == 0):
                print('error!!!栈顶非终结符和当前语句无匹配产生式！')
                sentence = sentence[1:]
            elif(pred_table[row][column] == synch):
                print('error!!!栈顶非终结符和当前语句无匹配产生式！')
                stack.pop(-1)
        if(x == '$' or len(sentence) == 0):
            used_proce.append(proce1[1])
            print(proce1[1])
            print('finish!')
            break


def read_lexical(path3):
    sentence = []
    with open(path3,"r") as f:
        lines =f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            sentence.append(line)
    f.close()
    sentence = trans_lexi(sentence)
    print(sentence)

    return sentence

def draw_pic():
    # list2 = []
    # for i in used_proce:
    #     if i not in list2:
    #         list2.append(i)
    # print(list2)
    with open('proce.txt', 'w') as f:
        for i in range(len(used_proce)):
            used_proce[i] = used_proce[i].replace('->',' ')
            f.write(used_proce[i])
            f.write('\n')
    f.close()

    # for i in range(len(list2)):
    #     x = list2[i]
    #     tail = x[0]
    #     x = x[3:]
    #     x = x.split(' ')
    #     for j in x:
    #         g.edge(tail,j)



def generate(dirs):
    f = open(dirs)
    lines = f.readlines()
    para = []
    for line in lines:
        l1 = line.strip('\n')
        l2 = l1.strip('\t')
        l = l2.split(' ')
        para.append(l)
    f.close()
    # 返回规约产生式的倒序
    return para

def draw_ast(dirs , output):
    proce2 = generate(dirs)
    context = ["digraph d {\n"]
    father = []
    nodenum = 1
    root = '\tnode{} [label="{}"]\n'.format(nodenum, proce2[0][0])
    father.append([nodenum,proce2[0][0]])
    nodenum += 1
    context.append(root)

    # 根节点与根节点的孩子相连
    for i in range(1, len(proce2[0])):

        father.append([nodenum,proce2[0][i]])
        s = '\tnode{} [label="{}"]\n'.format(nodenum, proce2[0][i])
        context.append(s)
        s = '\tnode{} -> node{}\n'.format(1, nodenum)
        context.append(s)
        nodenum = nodenum + 1

    for i in range(1, len(proce2)):
        curr_father_num = 0
        for j in range(len(proce2[i])):
            if j == 0:
                k = len(father) - 1
                while (father[k][1] != proce2[i][0]):
                    k = k - 1
                    if(k<0):
                        break
                curr_father_num = father[k][0]
                father.remove(father[k])
            else:
                s = '\tnode{} [label="{}"]\n'.format(nodenum, proce2[i][j])
                context.append(s)
                s = '\tnode{} -> node{}\n'.format(curr_father_num, nodenum)
                context.append(s)
                father.append([nodenum, proce2[i][j]])
                nodenum  += 1
    context.append('}')
    # for i in context:
    #     print(i)

    f = open(output, "w")
    for i in context:
        f.write(i)
    f.close()
    #生成图片
    os.system('dot -Tpng tree_node_leaf.txt -o tree.png')


if __name__ == "__main__":
    read_in()
    get_first()
    get_follow()

    pred_table = [[0 for i in range(len(VT))] for j in range(len(VN))]
    get_table()
    get_table_synch()
    print_table('predict_table.csv')
    sentence = ['get' ,'(' ,'id' , ')',';','if','(','id','==','num',')','{','id','=','num',';','}',';']
    # sentence = ['if','(','id','==','num',')','{','id','=','num',';','}',';','else','{','id','=','id','+','num',';','}',';']
    # sentence = ['if', '(', 'id', '==', 'num', ')', '{', 'id', '=', 'num', '}', ';']
    # sentence = ['int', 'id', '(', 'id',',' , 'id', ')', '{', 'int', 'id', ';', 'id', '=', 'id', '+', 'id', ';',
    #             'return', 'id', ';', '}', ';']
    # sentence = ['int', 'id', '(', 'id',',' ,'id', ')', '{', 'int', 'id', ';', 'id', '=', 'id', ';', 'return', 'id', ';',
    #             '}', ';']
    # sentence = ['id', '(', 'id', ',', 'id', ')']
    # sentence = read_lexical('lexical_result2.txt')
    # sentence = [ 'if', '(', 'id', '==', 'num', ')', '{', 'id', '=', 'id', ';', '}']
    # sentence = ['void','id','(',')','{','get','(','id', ')', ';','}']
    # sentence = ['id' , '=' , 'id' ,'id' ,'num' , ';']
    analyze(sentence)
    draw_pic()
    # g.view()
    draw_ast('proce.txt' , "tree_node_leaf.txt")


