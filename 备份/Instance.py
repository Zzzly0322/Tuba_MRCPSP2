
import data_read
import random
import matplotlib.pyplot as plt
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
        data_read.dataStore(self,file)

    def initialSolution(self):
        """
        initial the path
        :return: a adapative path
        """
        complete_set=[1]
        for w in range(self.number_job-1):
            ready_set = []
            for job in range(2,self.number_job+1):
                if job not in complete_set:
                    if set(self.job_predecessors[job-1]).issubset(complete_set):
                        ready_set.append(job)
            if len(ready_set)!=0:
                act_job=random.choice(ready_set)
                complete_set.append(act_job)
        initial_set=complete_set
        model_set=[]
        [model_set.append(random.choice([1,2,3])) for i in range(self.number_job)]
        model_set[0]=1
        model_set[self.number_job-1]=1
        # unrenewable_resource1=0
        # unrenewable_resource2=0
        # print(initial_set)
        # for job in initial_set:
        #     unrenewable_resource1+=self.job_model_resource[job][model_set[job-1]][2]
        #     unrenewable_resource2+=self.job_model_resource[job][model_set[job-1]][3]
        # print("unrenew:",unrenewable_resource1,"\n","unrenew:",unrenewable_resource2)
        # if unrenewable_resource1<self.resource_capacity[2] and unrenewable_resource2 <self.resource_capacity[3]:
        #
        # print(unrenewable_resource1,"\n",unrenewable_resource2)

        return initial_set, model_set

    def solutionCost(self,solution_set,solution_model):

        scheduled_list = [1]
        start_time = [0 for _ in range(self.number_job)]
        finish_time = [0 for _ in range(self.number_job)]
        use_renewable_resource_1=[0 for i in range(self.upper_bound)]
        use_renewable_resource_2= [0 for i in range(self.upper_bound)]
        solution_set.remove(1)
        # print("solution_set_cost2", solution_set)
        for job in solution_set:
            if set(self.job_predecessors[job - 1]).issubset(scheduled_list):
                start_time[job-1]=max(finish_time[pre_job-1] for pre_job in self.job_predecessors[job-1])
                finish_time[job-1]=start_time[job-1]+self.job_model_duration[job][solution_model[job-1]]
                while True:
                    count=0
                    for i in range(self.job_model_duration[job][solution_model[job-1]]):
                        # print( self.job_model_resource[job][solution_model[job-1]][0]+use_renewable_resource_1[start_time[job-1]+i])
                        # print( self.job_model_resource[job][solution_model[job-1]][1]+use_renewable_resource_2[start_time[job-1]+i])
                        if self.job_model_resource[job][solution_model[job-1]][0]+use_renewable_resource_1[start_time[job-1]+i]<self.resource_capacity[0] and \
                                self.job_model_resource[job][solution_model[job-1]][1]+use_renewable_resource_2[start_time[job-1]+i]< self.resource_capacity[1]:
                                count+=1
                    if count==self.job_model_duration[job][solution_model[job-1]]:
                        for duration in range(start_time[job-1],start_time[job-1]+self.job_model_duration[job][solution_model[job-1]]):
                            use_renewable_resource_1[duration]+=self.job_model_resource[job][solution_model[job-1]][0]
                            use_renewable_resource_2[duration]+=self.job_model_resource[job][solution_model[job-1]][1]
                        scheduled_list.append(job)
                        break
                    else:
                        start_time[job-1]+=1
                        finish_time[job-1]+=1
            else:
                print("Solution Order Error !")
                print(self.job_predecessors[job - 1],scheduled_list)
        use_renewable_resource_1=use_renewable_resource_1[:finish_time[self.number_job-1]]
        use_renewable_resource_2=use_renewable_resource_2[:finish_time[self.number_job-1]]

        unrenewable_resource1=0
        unrenewable_resource2=0
        for job in solution_set:
             unrenewable_resource1+=self.job_model_resource[job][solution_model[job-1]][2]
             unrenewable_resource2+=self.job_model_resource[job][solution_model[job-1]][3]
        # penalty1=max(0,unrenewable_resource1-self.resource_capacity[2])
        # penalty2=max(0,unrenewable_resource2 -self.resource_capacity[3])
        # finish_time[-1]+=12*(penalty1+penalty2)
        solution_set.insert(0,1)
        return  start_time,finish_time,use_renewable_resource_1,use_renewable_resource_2


    def fitness(self,solution_set,solution_model):
        start_time, finish_time, use_renewable_resource_1, use_renewable_resource_2=self.solutionCost(solution_set,solution_model)
        fit=1/finish_time[-1]
        return fit


    def tabu(self,iter_times,move_times, tabu_length,candidate_length):

        def candidateGenerate(solution_gene,model):

            limit_solution_set=[]
            limit_model_set = []
            solution_candidate=[]
            model_candidate=[]
            fit_candidate=[]
            move_candidate=[]
            print("-----------------初始解",solution)
            for i in range(candidate_length):
                # print("solution_gene", solution)
                solution_new,model_new,move_new=solutionMove(solution_gene,model,limit_solution_set,limit_model_set)

                # print('solution_new',solution_new)
                fitness=self.fitness(solution_new,model_new)
                solution_candidate.append(solution_new)
                model_candidate.append(model_new)
                fit_candidate.append(fitness)
                move_candidate.append(move_new)
            return  solution_candidate,model_candidate,fit_candidate,move_candidate


        def solutionMove(solution,model,limit_solution_set,limit_model_set):
            while True:
                # print("solution",solution)
                move_job1=random.choice(solution[1:14])
                ava_move_job=[]
                move_job=()
                solution_set_copy=solution
                # if move_job not in limit_solution_set:
                if True:
                    #before
                    # print("move_job1:",move_job1)
                    # print("solution_set_copy",solution_set_copy)
                    # print([i for i in self.job_predecessors[move_job1-1]])
                    premove_maxindex=max([solution_set_copy.index(i) for i in self.job_predecessors[move_job1-1]])
                    # print("premove_maxindex",premove_maxindex)
                    if len( solution_set_copy[premove_maxindex+1:solution_set_copy.index(move_job1)])!=0:
                        for job in solution_set_copy[premove_maxindex+1:solution_set_copy.index(move_job1)]:
                                insidepre=[]
                                for job_inside1 in solution_set_copy[solution_set_copy.index(job) + 1:solution_set_copy.index(move_job1)]:
                                    # print("before",job)
                                    # print("succer_before",self.job_successors[job-1])
                                    insidepre+=self.job_predecessors[job_inside1-1]
                                if job not in insidepre:
                                    ava_move_job.append(job)

                    #back
                    scheduled_list=solution_set_copy[:solution_set_copy.index(move_job1)]
                    for job in solution_set_copy[solution_set_copy.index(move_job1)+1:]:
                        if set(self.job_predecessors[job-1]).issubset(scheduled_list) :
                            if len(solution_set_copy[solution_set_copy.index(move_job1)+1:solution_set_copy.index(job)]) !=0:
                                insideaft = []
                                for job_inside2 in solution_set_copy[solution_set_copy.index(move_job1) + 1:solution_set_copy.index(job)]:
                                    insideaft+=self.job_predecessors[job_inside2-1]
                                if move_job1 not in insideaft:
                                    ava_move_job.append(job)


                    if len(ava_move_job)!=0:
                        move_job2=random.choice(ava_move_job)
                        move_job=(move_job1,move_job2)
                        solution_set_copy[solution_set_copy.index(move_job[0])] = move_job[1]
                        solution_set_copy[solution_set_copy.index(move_job[1])] = move_job[0]
                        limit_solution_set.append(move_job)
                        break


            while True:
                move_model=random.sample(model,2)
                move_model.sort()
                model_copy=model[:]
                if True:
                    model_copy[model_copy.index(move_model[0])] = move_model[1]
                    model_copy[model_copy.index(move_model[1])] = move_model[0]
                    limit_model_set.append(move_model)
                    break
            model_candidate=model_copy
            solution_candidate=solution_set_copy
            move=[move_job,move_model]
            return solution_candidate, model_candidate,move

        def chooseBest(solution_list,model_list,fit_list,move_list):
            max_index=fit_list.index(max(fit_list))
            solution_best=solution_list[max_index]
            model_best=model_list[max_index]
            move_best=move_list[max_index]
            fit_best=max(fit_list)
            return solution_best,model_best,move_best,fit_best



        finall_solution=[]
        finall_cost=[]
        finall_model=[]
        best_generation = []
        for i in range(iter_times):    # increasing the initial solution muti
            solution, model = self.initialSolution()
            tabu_fitness=[]
            tabu_move=[]
            for i in range(move_times):     # based one solution change
                # print("before solution",solution)
                solution_candidate, model_candidate, fit_candidate, move_candidate = candidateGenerate(solution, model)

                while True:
                    solution_best, model_bset, move_best, fit_best = chooseBest(solution_candidate, model_candidate,fit_candidate, move_candidate)
                    # print("solution_best", solution_best)
                    # print("cost_best", 1 / fit_best)
                    if move_best in tabu_move:

                        index=tabu_move.index(move_best)
                        if fit_best>max(tabu_fitness):
                            finall_solution.append(solution_best)
                            finall_cost.append(1/fit_best)
                            finall_model.append(model_bset)
                            tabu_fitness.append(fit_best)
                            tabu_move.append(move_best)
                            if len(tabu_fitness) > tabu_length:
                                del tabu_fitness[0]
                            if len(tabu_move) > tabu_length:
                                del tabu_move[0]
                            break

                        else:

                            solution_candidate.remove(solution_best)
                            model_candidate.remove(model_bset)
                            fit_candidate.remove(fit_best)
                            move_candidate.remove(move_best)
                            if len(solution_candidate)==0:
                                break
                    else:
                        finall_solution.append(solution_best)
                        finall_cost.append(1 / fit_best)
                        finall_model.append(model_bset)
                        tabu_fitness.append(fit_best)
                        tabu_move.append(move_best)
                        if len(tabu_fitness) > tabu_length:
                            del tabu_fitness[0]
                        if len(tabu_move) > tabu_length:
                            del tabu_move[0]
                        break
                print("完成了一次初始值")
                best_generation.append(min(finall_cost))
        index=finall_cost.index(min(finall_cost))
        finall_best_solution=finall_solution[index]
        finall_best_model=finall_model[index]
        print("best model", "\n", finall_best_model)
        print("best solution", "\n", finall_best_solution)
        print("best time","\n",min(finall_cost))
        print(finall_cost)


        plt.plot(best_generation)
        plt.ylabel("Min_cost")
        plt.xlabel("Generation")

        plt.savefig("Tabu.png", dpi=600)
        plt.show()
file="./data/j12.mm/j1226_1.mm"
ins=Instance()
ins.loadData(file)
ins.tabu(iter_times=500,move_times=100, tabu_length=10,candidate_length=30)
# print(ins.job_model_resource)
# print(ins.resource_capacity)
# solution_set,model_set=ins.initialSolution()
# print(model_set)
# # print(solution_set)
# start_time,finish_time,use_renewable_resource_1,use_renewable_resource_2=ins.solutionCost(solution_set,model_set)
# print("after_optimal start and finish time:","\n",start_time,"\n",finish_time,"\n",use_renewable_resource_1,"\n",use_renewable_resource_2)
