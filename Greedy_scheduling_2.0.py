
import sys
# Create input
teacher= {}
class_sub = {}
period_sub = {}
period = 6
session = 10
[T, N, M] = [int(x) for x in sys.stdin.readline().split()]
for i in range(1, N+1):
        class_sub[i] ={int(x) for x in sys.stdin.readline().split()[:-1]}
for j in range(N+1, T+N+1):
        teacher[j-N] = {int(x) for x in sys.stdin.readline().split()[:-1]}
period_sub = [int(x) for x in sys.stdin.readline().split()]
period_sub.insert(0,0)

#Construct list of Sub-class
C_s_p = [] #list of class_subject_periods
Timetable = [[0 for sessons in range(session+1)] for room in range(N+1)]
# Timetable is the timetable for all class each is built by the start period of each sessons
for c in class_sub:
    for sub in class_sub[c]:
        p = period_sub[sub]
        C_s_p.append((sub,c,p)) #Containing subject-class-period in a list
        
C_s_p= sorted(C_s_p, key = lambda x: x[2],reverse = True)
teacher_list = [] # construct teacher PriorityQueue
for t in teacher:
    teacher_list.append((0,t,[0 for sessons in range(session+1)])) 
    # Containing number of periods that teacher teach, name, timetable for that teacher
    # Timetable for teacher is built by the start period of each sessons 
    
def select(name_teacher,classes_teacher):
    # Select the first sub-class that satisfies the condition and the start period of 
    # classes and teacher must be the same
    global C_s_p
    for y in C_s_p:

        if (y[0] in teacher[name_teacher]):
            for i in range(1,session+1):
                 if (Timetable[y[1]][i]+y[2]<=6) and (classes_teacher[i]+y[2]<=6) and Timetable[y[1]][i] == classes_teacher[i]:

                     Timetable[y[1]][i] = Timetable[y[1]][i]+y[2] #update start periods classes 
                     classes_teacher[i] = classes_teacher[i]+y[2]

                     return y,(Timetable[y[1]][i]-y[2]+1,i),classes_teacher # teacher, start period, teacher_period
    return None,None,None

def select2(name_teacher,classes_teacher):
    # Select the first sub-class that satisfies the condition and the start period of 
    # classes and teacher must be the same
    global C_s_p
    for y in C_s_p:

        if (y[0] in teacher[name_teacher]):
            for i in range(1,session+1):
                 if (Timetable[y[1]][i]+y[2]<=6) and (classes_teacher[i]+y[2]<=6) :
                    if Timetable[y[1]][i] >= classes_teacher[i]:
                        classes_teacher[i] = Timetable[y[1]][i]+y[2]
                        Timetable[y[1]][i] = Timetable[y[1]][i]+y[2]
                    else:
                        Timetable[y[1]][i] = classes_teacher[i]+y[2]
                        classes_teacher[i] = classes_teacher[i]+y[2]
                    return y,(Timetable[y[1]][i]-y[2]+1,i),classes_teacher  # teacher, start period, teacher_period
    return None,None,None  

def Greedy():
    global C_s_p
    Class_sub_sastify = [] # list of sastify class - sub - start classes - teacher
    # start classes for teacher in each session
    # start classes for room in each session
    
    while len(C_s_p)>0:
        temp = [] # remember the updated teacher
        check=[] #teacher that has already checked
        while not teacher_list == []:        
            t = teacher_list.pop()
            check.append(t)
            x,s,c_t = select(t[1],t[2])
            if x==None:
                temp.append(t)
                continue 
            Class_sub_sastify.append((x[1],x[0],s[0]+6*(s[1]-1),t[1]))
            C_s_p.remove(x)                
            temp.append((t[0]+x[2],t[1],c_t)) #update teacher_period
        if check==temp: # no more changes on teacher that can teach 
            for t in temp:
                teacher_list.append(t) # update the teacher queue for improvedGreedy
            return Class_sub_sastify
        for t in temp:
            teacher_list.append(t) # update the teacher queue for next iteration     
    return Class_sub_sastify

def improvedGreedy():
    global C_s_p
    Class_sub_sastify = [] # list of sastify class - sub - start classes - teacher
    # start classes for teacher in each session
    # start classes for room in each session    
    while len(C_s_p)>0:
         # Timetable classes that have already scheduled (in current iteration)
        temp = []
        check=[]
        while not teacher_list == []:        
            t = teacher_list.pop()
            check.append(t)        
            x,s,c_t = select2(t[1],t[2])
            if x==None:
                temp.append(t)
                continue 
            Class_sub_sastify.append((x[1],x[0],s[0]+6*(s[1]-1),t[1])) # append solution in list
            C_s_p.remove(x)
            temp.append((t[0]+x[2],t[1],c_t)) #update teacher_period
        if check==temp: # no more change can make on teacher
            return Class_sub_sastify
        for t in temp:
            teacher_list.append(t) #update teacher_list for next interation     
    return Class_sub_sastify

S1 = Greedy()
S2 = improvedGreedy()
Schedual=[]
Schedual=S1+S2
Schedual.sort()
print('----------------------------------------------------------------')
print(Schedual)
with open('data.txt','w') as f:
    
    f.write(str(len(Schedual))+'\n')
    for i in Schedual:
        for v in i:
            f.write(str(v)+" ")
        f.write('\n')
    f.close()
'''
37
1 3 1 1
1 4 7 2
1 9 13 4
1 10 5 4
2 1 5 1
2 5 7 1
2 10 1 4
3 8 2 3
3 9 7 4
4 3 13 1
4 4 2 2
4 6 7...

    '''
