# coding=UTF-8
import copy
import re
import time
import csv
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


def getWinner(k, min_sup) :
    begin = level.index(k)
    end = len(items)
    string = ""
    List = []
    for i in range(begin, end) :
        if Supp[i] >= min_sup :
            string += str(items[i]) + "-(support=" + str(Supp[i]) + ")\n"
            List.append(items[i])
    return string #List

def getLoser(k, min_sup) :
    begin = level.index(k)
    end = len(items)
    List = []
    for i in range(begin, end) :
        if Supp[i] < min_sup :
            List.append(items[i])
    return List


starttime = time.time() 
min_sup = 0.01
initial = Apriori(min_sup, 'c:/Users/amychang0122/Desktop/Lectures/Data Mining/Project 1/IBM.data')
#initial.process()   # initial.data = 資料集
n=1
data_num = 100000
C = []#initial.scan()
Supp = []
items = []
level = []
total_len = len(initial.data)
maximum = 0
for each_src in initial.data:
    sup = 0
    for e in each_src:
        count = 0
        if e in C :
            continue
        for db in initial.data:
            if e in db :
                count = count + 1
        sup = count/total_len
        items.append(e)
        Supp.append(sup)
        level.append(n)
        if sup >= min_sup:
            C.append(e)
            if(sup>maximum) :
                maximum = sup
#        print("SUP=", sup)

L = C
L.sort()

'''# output testing data
topic = ['Transation']
for i in range(1, data_num) :
    topic.append(i)
 # 輸出成csv檔
with open('Output_Testing_Data.csv', 'w', newline='') as csvfile:  # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    writer.writerow(topic)
    for each in initial.data:
        topic.clear()
        now = 0
        for i in range(data_num) :
#            print("(", int(each[now]), ",", i, ")")
            if now >= len(each) :
                topic.append('0')
            elif int(each[now]) == i :
                topic.append('1')
                now += 1
            else :
                topic.append('0')
            
        writer.writerow(topic)
'''

while len(L)!=0 :
    print("\n{", n, "- itemset} :", len(L))
    print("------------------------------\n", getWinner(n, min_sup), "\n")


    
    n = n + 1

    DB = []
    for i in range(len(L)-1) :
        for j in range(i+1, len(L)) :
            temp = []
            if len(L[i]) != len(L[j]) :
#                print("Size is different!")
                continue
            if L[i][len(L[i])-1] == L[j][len(L[j])-1] :
#                print("Tail is the same", L[i][len(L[i])-1], L[j][len(L[j])-1])
                continue
            if L[i][0:len(L[i])-1] == L[j][0:len(L[j])-1] :
#                print("GotCHA!")
                temp.extend(L[i])
                temp.extend(L[j][len(L[j])-1])
                DB.append(temp)

    C = []
    lv = 1
    while lv < n :
        loser = getLoser(lv, min_sup)
        for item in DB :    ## DB = 還未掃描過的候選人
            for each in loser :
                flag = False
                if e not in each :
                    flag = True
                if flag == False :
                    if item in DB :
                        DB.remove(item)
        lv = lv + 1
    C = DB
    L = []
    for i in C :
        count = 0
        for src in initial.data :
            flag = True
            for e in i :
                if e not in src :
                    flag = False
            if flag == True :
                count = count + 1
        sup = count/total_len
        items.append(i)
        Supp.append(sup)
        level.append(n)
        if sup >= min_sup : 
            L.append(i)  

endtime =  time.time() 
print("It takes %d milliseconds to find the above patterns" %((endtime-starttime) * 1000))

