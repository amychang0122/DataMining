import re
import copy
import sys
import numpy as np
import itertools

class Apriori:
    def __init__(self,min_supp=0.5,datafile='Book_data'):
        inputfile = open(datafile,"r")
        trans = '1'
        self.data=[]
        self.size=0
        self.min_supp = min_supp
        arr = []
        for line in inputfile.readlines():
            linearray = re.findall(r'[\d]+',line)	#把每個數字節錄出來
            if(trans != linearray[1]):
                self.data.append(arr)
                arr = []
                trans = linearray[1]
            arr.append(linearray[2])
        self.data.append(arr)
        for each in self.data:
            print(each, sep='---', end='\n')
        print('\n')
        
        self.size=len(self.data)

    def sort(self, min_sup) :   #包含sort好了
        arr = np.zeros(1000000, int)
        List = []
        temp = []
        maximum = 0
        for i in self.data :
            for j in i :
                arr[int(j)] += 1
                if maximum < arr[int(j)] :
                    maximum = arr[int(j)]

#        for each_set in range(len(self.data)) :
#            for e in range(len(self.data[each_set])) :
#                for tar in range(e+1, len(self.data[each_set])) :
#                    break
        for src in self.data :
            src.sort()
            for i in range(min_sup,maximum+1) :
                for e in src :
                    if arr[int(e)] == i :
                        temp.append(e)
            temp.reverse()
            List.append(temp)
            temp = []

        for each in List :
            print(each)
        self.data = List
        print(self.data)
        return arr
####  sort-完畢



class Tree(object):
    def __init__(self) :
        self.parent = None
        self.sibling = None
        self.next = None
        self.child = None
        self.data = None
        self.num = 0

    def set_parent(self, pa) :
        self.parent = pa

    def set_sibling(self, sib) :
        self.sibling = sib

    def set_next(self, nxt) :
        self.next = next

    def set_child(self, chd) :
        self.child = chd

    def set_data(self, d) :
        self.data = d

    def set_num(self, n) :
        self.num = n

    
#You can use it like this:



min_sup = 3 # unsigned int
array = np.zeros(1000000, int)
initial = Apriori(min_sup, 'c:/Users/amychang0122/Desktop/Lectures/Data Mining/Project 1/data.data')
array = initial.sort(min_sup)
#initial.process()   # initial.data = 資料集


root = Tree()
root.parent = "NULL"
root.data = "root"
root.sibling = "NULL"
root.next = "NULL"
root.child = Tree() ##########
root.num = -1

root_list = []
total_len = len(initial.data)
maximum = 0
root_tail = None
temp = Tree()

for each_src in initial.data :
    if each_src[0] not in root_list :   # new itemset 
        root_list.append(each_src[0])
        if root_tail == None :  #最初最初的資料進來囉
            temp = Tree()
            temp.parent = root
            root.child = temp
            temp.data = each_src[0]
            temp.num = 1
            root_tail = temp
            string = str(temp.data) + "(" + str(temp.num) + ") __ "
        else :  #沒出現過的資料進來了
            temp = Tree()
            temp.data = each_src[0]
            temp.num = 1
            temp.parent = root
            root_tail.sibling = temp
            root_tail = temp
            string += str(temp.data) + "(" + str(temp.num) + ") __ "
        for i in range(1, len(each_src)) :
            temp.child = Tree()
            temp.child.parent = temp
            temp = temp.child
            temp.data = each_src[i]
            temp.num = 1
            string += str(temp.data) + "(" + str(temp.num) + ") __ "
    else :
        current = root.child
        while current.data != each_src[0] : # 從 root 裡面找itemset的開頭
            current = current.sibling
        current.num += 1
        string = str(current.data) + "(" + str(current.num) + ") __ "
        for i in range(1, len(each_src)) :
            if current.child:
                if current.child.data == each_src[i] :
                    current = current.child
                    current.num += 1
                    string += str(current.data) + "(" + str(current.num) + ") __ "
                    flag = False
                    continue
            #flag = True
                else :
                    #找手足
                    sib = current.child
                    if sib.sibling :
                        while sib.sibling != None : # can be suspended
                            sib = sib.sibling
                        if sib.data == each_src:
                            sib.num += 1
                            sib.parent = current
                            current = sib
                            string += str(current.data) + "(" + str(current.num) + ") ++ "
                            flag = False
                            break
                    else :
                        temp = Tree()
                        temp.data = each_src[i]
                        temp.num = 1
                        temp.parent = current
                        sib.sibling = temp
                        current = temp
                        string += str(current.data) + "(" + str(current.num) + ") +- "
            else : 
                temp = Tree()
                temp.data = each_src[i]
                temp.num = 1
                temp.parent = current
                current.child = temp
                #sib = current.child
                #while sib.sibling != None :
                #    sib = sib.sibling
                #sib.sibling = temp
                current = temp ###ADDD
                #current.sibling = temp
                string += str(temp.data) + "(" + str(temp.num) + ") __ "
    print("Produce: ", string)
    string = ""
# FP-Tree 建置完畢

# 找相同item的連結，從最尾端開始找
current = root.child
while current.child :
    current = current.child
    
done = True
while current != root_tail :    #最後一行不用掃
    if done == True :
        done = False
        if current.parent == root or current.sibling != None:
            temp = current.sibling
        else :
            temp = current.parent
            while temp.sibling == None :    #沒兄弟才找父母
#                print(current.data, "=vs=", temp.data)
                temp = temp.parent
                if temp == root :
                    current = root_tail
                    break
#            print(current.data, "-vs-", temp.data)
            temp = temp.sibling
#        print(current.data, "_vs_", temp.data)
        while temp.child != None :
            temp = temp.child   #鄰居的最小小孩
#            print("4.", temp.data)
#        print("parent=", temp.parent.data)
#        print(current.data, "-vs-", temp.data)

    # Calculation
    if current.data == temp.data :
#        print("Accept!", current.data, "-vs-", temp.data)
        done = True
        current.next = temp
    #    temp = root
    else :
        if temp.sibling != None:
            temp = temp.sibling
            while temp.child != None :
                temp = temp.child
        else :
            temp = temp.parent
    if temp == root :
        done = True

    if done :
        if current.sibling :
            current = current.sibling
            if current == root_tail :
                break
            while current.child != None :
                current = current.child
        else :
            current = current.parent
        done = True
# 找完所有人的.next

# 找condition pattern
current = root.child
while current.child != None :
    current = current.child

scan = current 
output = str(current.data) + "\t" 
output_data = []
string = []
flag = False
while scan != root :

    ################
    current = scan
    string = []
    temp_str = []
    while current != None :
        flag = current.parent
        temp_str.clear()
        while flag != root :
            temp_str.append(flag.data)
            flag = flag.parent
        if len(temp_str) != 0 :
            string.append(current.num)
            string.append(copy.copy(temp_str))
        if current.next == None :
            break 
        current = current.next
    # 數完某一element

    count = 0
    output_data.clear()
    array = np.zeros(1000000, int)
    for i in range(int(len(string)/2)) : ## 掃描的主角， 小心超過index
        for j in range(len(string[i*2+1])) :    ## 掃描的主角， element 的位置 string[i][j]
            count = string[i*2]
            if string[i*2+1][j] in output_data :
                continue
            for k in range(i+1, int(len(string)/2)) :  ## 比對的對象 string[k]
                if string[i*2+1][j] in string[k*2+1] :
                    count += string[k*2]
            if count >= min_sup :
                output_data.append(string[i*2+1][j])
                output +=  str(string[i*2+1][j]) + ":" + str(count) + ", "
                array[int(string[i*2+1][j])] = count
    
    # current.data 的 frequent patterns (1. find combination)
    if len(output_data) != 0 :
        output_data.reverse()
        pattern = []
        if current.next == None:
            fp = "item=" + str(current.data) + "\t"
    #        print("item=",output_data)
            for i in range(1, len(output_data)+1) :
                iter = itertools.combinations(output_data,i)
                pattern.append(list(iter))

        # current.data 的 frequent patterns (2.add current.data)
        fp = str(current.data) + "\n"
        for itemset in pattern :
            for item in itemset :
                linearray = re.findall(r'[\d]+',str(item))	#把每個數字節錄出來
                minimum = array[int(linearray[0])]
                for each in linearray :
                    if minimum > array[int(each)] :
                        minimum = array[int(each)]
                linearray.append(copy.copy(current.data))
                fp += str(linearray) + ":" + str(minimum) + "\t"
                #print(linearray, ":", minimum)
        print("\nFrequent Patterns:", fp )



    if current.next :
        current = current.next
    else :
        if scan.sibling :
            scan = scan.sibling
            if scan == root_tail :
                break
            while scan.child != None :
                scan = scan.child
        else :
            scan = scan.parent
        if len(output_data) != 0 :
            current = scan
            string.clear()
            print("------------------------ \nConditional FP-tree = ", output)
            output = str(current.data) + "\t" 
    
