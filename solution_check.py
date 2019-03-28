#Author:Zhao fei
import os
import re


def dataRead(file):
    with open(file) as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    data = [re.split(r' +', x) for x in data]
    return data

def dataStore(ins,file):
    data=dataRead(file)

    ins.number_job = int(data[5][4])
    ins.number_renewable_resources =int(data[8][3])
    ins.number_unrenewable_resources = int(data[9][3])
    ins.resource_capacity=[int(i) for i in data[77]]
    # print(ins.resource_capacity)

    #successor
    for job in range(18,18+ins.number_job):
        ins.job_num_successors.append(int(data[job][2]))
        ins.job_successors.append([int(i) for i in data[job][3:]])
    #predecessors
    for _ in range(ins.number_job):
        ins.job_predecessors.append([])
    for job in range(ins.number_job):
        for successor in ins.job_successors[job]:
            ins.job_predecessors[successor-1].append(job+1)
    #duration and resources  fsdf
    Row = 37
    for job in range(2,ins.number_job):
        resource={}
        duration={}
        for model in range(3):
            if model==0:
                duration[model+1]=int(data[Row+model][2])
                ins.job_model_duration[job]=duration

                resource[model+1]=[int(res) for res in data[Row+model][3:]]
                ins.job_model_resource[job]=resource
            else:
                duration[model + 1] = int(data[Row + model][1])
                ins.job_model_duration[job] = duration

                resource[model + 1] = [int(res) for res in data[Row + model][2:]]
                ins.job_model_resource[job] = resource
        Row+=3

class Instance():
    def __init__(self):
        self.successors=[]
        self.job_num_successors=[]
        self.job_predecessors = []
        self.job_successors=[]
        self.job_model_resource={1:{1:[0,0,0,0]},14:{1:[0,0,0,0]}}
        self.job_model_duration={1:{1:0},14:{1:0}}
        self.resource_capacity=[]

        self.number_job =None
        self.number_renewable_resources = None
        self.number_unrenewable_resources = None
        self.resource_capacity = None
        self.upper_bound=228

    def loadData(self,file):
        dataStore(self,file)

    def solutionCost(self, solution_set, solution_model):

        scheduled_list = [1]
        start_time = [0 for _ in range(self.number_job)]
        finish_time = [0 for _ in range(self.number_job)]
        use_renewable_resource_1 = [0 for i in range(self.upper_bound)]
        use_renewable_resource_2 = [0 for i in range(self.upper_bound)]
        solution_set.remove(1)
        # print("solution_set_cost2", solution_set)
        for job in solution_set:
            if set(self.job_predecessors[job - 1]).issubset(scheduled_list):
                start_time[job - 1] = max(finish_time[pre_job - 1] for pre_job in self.job_predecessors[job - 1])
                finish_time[job - 1] = start_time[job - 1] + self.job_model_duration[job][solution_model[job - 1]]
                while True:
                    count = 0
                    for i in range(self.job_model_duration[job][solution_model[job - 1]]):
                        if self.job_model_resource[job][solution_model[job - 1]][0] + use_renewable_resource_1[
                            start_time[job - 1] + i] < self.resource_capacity[0] and \
                                self.job_model_resource[job][solution_model[job - 1]][1] + use_renewable_resource_2[start_time[job - 1] + i] < self.resource_capacity[1]:
                            count += 1
                    if count == self.job_model_duration[job][solution_model[job - 1]]:
                        for duration in range(start_time[job - 1], start_time[job - 1] + self.job_model_duration[job][solution_model[job - 1]]):
                            use_renewable_resource_1[duration] += self.job_model_resource[job][solution_model[job - 1]][0]
                            use_renewable_resource_2[duration] += self.job_model_resource[job][solution_model[job - 1]][1]
                        scheduled_list.append(job)
                        break
                    else:
                        start_time[job - 1] += 1
                        finish_time[job - 1] += 1
            else:
                print("Solution Order Error !")
                print(self.job_predecessors[job - 1], scheduled_list)
        use_renewable_resource_1 = use_renewable_resource_1[:finish_time[self.number_job - 1]]
        use_renewable_resource_2 = use_renewable_resource_2[:finish_time[self.number_job - 1]]

        unrenewable_resource1 = 0
        unrenewable_resource2 = 0
        for job in solution_set:
            unrenewable_resource1 += self.job_model_resource[job][solution_model[job - 1]][2]
            unrenewable_resource2 += self.job_model_resource[job][solution_model[job - 1]][3]
        # penalty1=max(0,unrenewable_resource1-self.resource_capacity[2])
        # penalty2=max(0,unrenewable_resource2 -self.resource_capacity[3])
        # finish_time[-1]+=12*(penalty1+penalty2)
        print("unrenewable_resource1:",unrenewable_resource1)
        print("unrenewable_resource2:",unrenewable_resource2)
        solution_set.insert(0, 1)
        return start_time, finish_time, use_renewable_resource_1, use_renewable_resource_2

file="./data/j12.mm/j1226_1.mm"
ins=Instance()
ins.loadData(file)
best_model =[1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1]
best_solution = [1, 3, 4, 2, 5, 6, 8, 7, 12, 10, 9, 13, 11, 14]
res=ins.solutionCost(best_solution,best_model)
print(res)
