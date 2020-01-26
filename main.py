from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def execute(filename):
    to_return =dict()
    with open(filename, 'r') as f:
        data = f.read()
        to_return[filename] = data
    return to_return

class instruction:
    def __init__(self,name,opr1='None',opr2='None',opr3='None'):
        self.name=name
        self.opr1=opr1
        self.opr2=opr2
        self.opr3=opr3
        self.started=False
        self.executed=False
        self.exeed=False
        self.written=False
    
class ins_condition:
    def __init__(self,number,op,execute_time,start_time=0):
        self.number=number
        self.op=op
        self.start_time=start_time
        self.execute_time=execute_time
        self.started=False
        self.executed=False
        self.exeed=False
        self.ex_Rb_number='None'
        self.written=False

class reservation_station:
    def __init__(self,Op,number,cur_Op='None',Qj='None',Qk='None',Vj='None',Vk='None',Busy=False,A='None'):
        self.Op=Op
        self.cur_Op=cur_Op
        self.number=number
        self.Qj=Qj
        self.Qk=Qk
        self.Vj=Vj
        self.Vk=Vk
        self.Busy=Busy
        self.A=A
        self.started_time='None'
        self.result='None'
    def finis(self):
        self.Busy=False
        self.cur_Op='None'
        self.Qj='None'
        self.Qk='None'
        self.Vj='None'
        self.Vk='None'
        self.A='None'
        self.started_time='None'
        self.result='None'
class register:
    def __init__(self,name,val=0):
        self.name=name
        self.val=val

def available_reservation_station(op):
    if op=='L.D':
        for i in range(1,3):
            if not Reservation_station_state[i].Busy:
                return i
    elif op=='ADD.D' or op=='SUB.D':
        for i in range(3,6):
            if not Reservation_station_state[i].Busy:
                return i
    elif op=='DIV.D' or op=='MUL.D':
        for i in range(6,8):
            if not Reservation_station_state[i].Busy:
                return i
    else:
        return -1


Delay_time={'L.D':2,'ADD.D':3,'SUB.D':3,'DIV.D':41,'MUL.D':11,}

ins='1	L.D 	F6,34(R2)\n2	L.D 	F2,45(R3)\n3	MUL.D	F0,F2,F4\n4	SUB.D	F8,F2,F6\n5	DIV.D	F0,F0,F6\n6	ADD.D	F6,F8,F2'
ins=ins.split('\n')

instruction_quantity=len(ins)

instructions=[]
print('The executed instruction sequence is:')
for x in ins:
    x=x.replace('\t','')
    x=x.replace('\n','')
    x=x.replace(' ','')
    print(x)
    i=0
    while not(x[i-1]=='.'and x[i]=='D'):
        i+=1
    i+=1

    op=str(x[1:i])
    j=i+1
    while x[j]!=',':
        j+=1
    op1=str(x[i:j])
    j+=1

    if x[j]<='9' and x[j]>='0':
        i=j
        j=i+1
        while x[j]!='(':
            j+=1

        op3=str(x[i:j])
        i=j+1
        j=i+1
        while x[j]!=')':
            j+=1
        op2=str(x[i:j])
        temp=op2
        op2=op3
        op3=temp
    else:

        i=j
        j=i+1
        while x[j]!=',':
            j+=1
        op2=str(x[i:j])
        j+=1
        i=j
        op3=str(x[i:len(x)])

    instructions.append(instruction(op,op1,op2,op3))

Regs={'F0':0,'F2':2,'F4':4,'F6':6,'F8':8,'F10':10,'R2':11,'R3':12,}

registers={'F0':'F0','F2':'F2','F4':'F4','F6':'F6','F8':'F8','F10':'F10','R2':'R2','R3':'R3',}

Qi={'F0':0,'F2':0,'F4':0,'F6':0,'F8':0,'F10':0,'R2':0,'R3':0,}


Instruction_state=[ins_condition(i,instructions[i].name,Delay_time[instructions[i].name]) for i in range(instruction_quantity)]

Reservation_station_state=['']
for i in range(1,3):
    Reservation_station_state.append(reservation_station('L.D',i))
for i in range(3,6):
    Reservation_station_state.append(reservation_station('ADD.D',i))
for i in range(6,8):
    Reservation_station_state.append(reservation_station('DIV.D',i))

basic_time=0
cur_started_instructions=0


def single_step():
    
    global basic_time
    global cur_started_instructions
    global Reservation_station_state
    global Instruction_state
    global instructions
    global Qi

    basic_time+=1

    if cur_started_instructions<len(Instruction_state):
        op=Instruction_state[cur_started_instructions].op
        res=available_reservation_station(op)
        if res>0:           
            cur_instuction=instructions[cur_started_instructions]

            Reservation_station_state[res].Busy=True
            Reservation_station_state[res].cur_Op=op
            Reservation_station_state[res].started_time=basic_time
            '''
            if op=='L.D':
            else:
            '''

            if(res>0 and res<3):
                seq=res
            elif (res>2 and res<6):
                seq=res-2
            elif (res>5):
                seq=res-5
          
            if Qi[cur_instuction.opr1]==0:
                Qi[cur_instuction.opr1]=cur_instuction.name+str(seq)

            if op=='L.D':
                Reservation_station_state[res].A=str(cur_instuction.opr2)+'+'+str(cur_instuction.opr3)
            else:    
                if Qi[cur_instuction.opr2]==0:
                    Reservation_station_state[res].Vj=registers[cur_instuction.opr2]
                    Reservation_station_state[res].Qj='None'                
                else:
                    Reservation_station_state[res].Vj='None'
                    Reservation_station_state[res].Qj=Qi[cur_instuction.opr2]

            if op!='L.D':
                if Qi[cur_instuction.opr3]==0:
                    Reservation_station_state[res].Vk=registers[cur_instuction.opr3]
                    Reservation_station_state[res].Qk='None'
                else:
                    Reservation_station_state[res].Vk='None'
                    Reservation_station_state[res].Qk=Qi[cur_instuction.opr3]
        Instruction_state[cur_started_instructions].start_time=basic_time
        Instruction_state[cur_started_instructions].started=basic_time
        Instruction_state[cur_started_instructions].ex_Rb_number=res
        cur_started_instructions+=1
        
    for i in range(1,8):
        if Reservation_station_state[i].Busy==True:
            for j in range(instruction_quantity):
                if Instruction_state[j].ex_Rb_number==i:
                    break

            if Reservation_station_state[i].Op=='L.D':
                if Reservation_station_state[i].started_time==basic_time-1:
                    Instruction_state[j].executed=basic_time
                if Reservation_station_state[i].started_time==basic_time-Delay_time[Reservation_station_state[i].cur_Op]:
                    Instruction_state[j].exeed=basic_time
                    Reservation_station_state[i].result='Mem'+'['+Reservation_station_state[i].A+']'
                elif Reservation_station_state[i].started_time==basic_time-1-Delay_time[Reservation_station_state[i].cur_Op]:
                    Instruction_state[j].written=basic_time
                    Reservation_station_state[i].Busy=False
                    Reservation_station_state[i].A='None'
                    for y in range(3,8):
                        if Reservation_station_state[y].Qj=='L.D'+str(i) and Reservation_station_state[y].Vj=='None':
                            Reservation_station_state[y].Vj=Reservation_station_state[i].result
                            Reservation_station_state[y].Qj='None' 
                        if Reservation_station_state[y].Qk=='L.D'+str(i) and Reservation_station_state[y].Vk=='None':
                            Reservation_station_state[y].Vk=Reservation_station_state[i].result
                            Reservation_station_state[y].Qk='None'
                    for x in Qi:
                        if Qi[x]=='L.D'+str(i):
                            Qi[x]=0
                    
            else:
                
                if(Reservation_station_state[i].Vj != 'None' and Reservation_station_state[i].Vk != 'None'):
                    if Instruction_state[j].executed==False:
                        Instruction_state[j].executed=basic_time
                    elif Instruction_state[j].executed==basic_time+1-Delay_time[Reservation_station_state[i].cur_Op]:
                        Instruction_state[j].exeed=basic_time
                        if Reservation_station_state[i].cur_Op=='ADD.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'+'+str(Reservation_station_state[i].Vk)
                        if Reservation_station_state[i].cur_Op=='SUB.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'-'+str(Reservation_station_state[i].Vk)
                        if Reservation_station_state[i].cur_Op=='MUL.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'*'+str(Reservation_station_state[i].Vk)
                        if Reservation_station_state[i].cur_Op=='DIV.D':
                            Reservation_station_state[i].result=str(Reservation_station_state[i].Vj)+'/'+str(Reservation_station_state[i].Vk)
                    elif Instruction_state[j].executed==basic_time-Delay_time[Reservation_station_state[i].cur_Op]:
                        Instruction_state[j].written=basic_time
                       
                        if Reservation_station_state[i].cur_Op=='ADD.D':
                            for x in Qi:
                                if Qi[x]=='ADD.D'+str(i-2):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='ADD.D'+str(i-2) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='ADD.D'+str(i-2) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis()
                        if Reservation_station_state[i].cur_Op=='SUB.D':
                            for x in Qi:
                                if Qi[x]=='SUB.D'+str(i-2):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='SUB.D'+str(i-2) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='SUB.D'+str(i-2) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis()
                        if Reservation_station_state[i].cur_Op=='MUL.D':
                            for x in Qi:
                                if Qi[x]=='MUL.D'+str(i-5):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='MUL.D'+str(i-5) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='MUL.D'+str(i-5) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis() 
                        if Reservation_station_state[i].cur_Op=='DIV.D':
                            for x in Qi:
                                if Qi[x]=='DIV.D'+str(i-5):
                                    Qi[x]=0
                            for j in range(1,8):
                                if Reservation_station_state[j].Qj=='DIV.D'+str(i-5) and Reservation_station_state[j].Vj=='None':
                                    Reservation_station_state[j].Vj=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qj=0
                                if Reservation_station_state[j].Qk=='DIV.D'+str(i-5) and Reservation_station_state[j].Vk=='None':
                                    Reservation_station_state[j].Vk=Reservation_station_state[i].result
                                    Reservation_station_state[j].Qk=0
                            Reservation_station_state[i].finis()

def printInfo():
    a = str(basic_time)
    df1 = pd.DataFrame(columns = ['Cycle Number']) 
    df1.loc[1] = [a]

    a = 'Instruction Status'
    df2 = pd.DataFrame(columns = [a]) 

    df3 = pd.DataFrame(columns = ['Instruction','type','execution delay','outflow','start executon','execution completed','write']) 
    for i in range(instruction_quantity):
        x=Instruction_state[i]
        print('Command'+str(x.number)+'\t'+str(x.op)+'\t\t'+str(x.execute_time)+'\t\t'+str(x.start_time)+'\t'+str(x.executed)+'\t\t'+str(x.exeed)+'\t\t'+str(x.written))
        df3.loc[i] = ["Command" + str(x.number) , str(x.op) , str(x.execute_time), str(x.start_time) , str(x.executed), str(x.exeed) , str(x.written)] # adding a row
      
    df4 = pd.DataFrame(columns = ['Load Buffer','Busy','Address']) 
    for i in range(1,3):
        x=Reservation_station_state[i]
        print('L.D'+str(i)+'\t'+str(x.Busy)+'\t'+str(x.A)+'\t')
        df4.loc[i] = ["L.D"+ str(i), str(x.Busy), str(x.A)]

    a = 'Reservation Stations'
    df5 = pd.DataFrame(columns = [a]) 

    df6 = pd.DataFrame(columns = ['Preserve Station Properties','Current Operation','Type','Number','Vj', 'Vk','Qj','Qk', 'Busy', 'A', 'start clock', 'result'])
    a = 0
    for i in range(3,len(Reservation_station_state)):
        x=Reservation_station_state[i]
        print('Reserved station'+str(i-2)+'\t'+str(x.Op)+'\t\t'+str(x.cur_Op)+'\t\t'+str(x.number)+'\t'+str(x.Vj)+'\t'+str(x.Vk)+'\t'+str(x.Qj)+'\t'+str(x.Qk)+'\t'+str(x.Busy)+'\t'+str(x.A)+'\t'+str(x.started_time)+'\t\t'+str(x.result))
        df6.loc[a] = ['Reserved station'+str(i-2),str(x.Op),str(x.cur_Op),str(x.number),str(x.Vj),str(x.Vk),str(x.Qj),str(x.Qk),str(x.Busy),str(x.A),str(x.started_time),str(x.result)]
        a=a+1

    a = 'Register Result status'
    df7 = pd.DataFrame(columns = [a]) 
    
    df8 = pd.DataFrame(columns = ['F0','F2','F4','F6','F8','F10'])
    df8.loc[0] = [str(Qi["F0"]), str(Qi["F2"]), str(Qi["F4"]), str(Qi["F6"]), str(Qi["F8"]), str(Qi["F10"])]
    return df1,df2,df3,df4,df5,df6,df7,df8
time = 0

@app.route('/')
def script_output():
    global time
    time = time + 1
    while(basic_time < time):
        single_step()
    df1,df2,df3,df4,df5,df6,df7,df8 = printInfo()
    return render_template('CA.html',tables=[df1.to_html(classes='df1'),df2.to_html(classes='df2'),df3.to_html(),df4.to_html(),df5.to_html(),df6.to_html(),df7.to_html(),df8.to_html()])

if __name__ == '__main__':
    app.run()

