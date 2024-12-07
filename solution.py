import json
import schedule
with open('Milestone1.json','r') as file:
    data= json.load(file)


total_time=[]
schedule_plan={}
quantity=data["wafers"][0]["quantity"]
wafers=data["wafers"][0]["processing_times"]
n=len(total_time)
arrival_time=[0]*n

for x in wafers.values():
    total_time.append(x)
j=0
completion_time=0
while j <n:
    for x,y in arrival_time,total_time:
        i=0
        arrival_time[i]=x+y
        i+=1
    completion_time=arrival_time[n-1]
    arrival_time=[completion_time]*n
    j+=1
    
print(completion_time)

    
    
    
