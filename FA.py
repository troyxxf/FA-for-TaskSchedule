import random
import numpy as np
import copy
import matplotlib.pyplot as plt
from init import server,task,loadServer,loadTask

def showTaskDoneTime(allTask):
    for i in range (len(allTask)):
        print(allTask[i].DoneTime)

class FireflyAlgorithm:
    def __init__(self,sizepop,vardim,gene,MAXGEN,params):
        '''
        :param sizepop:种群数量
        :param vardim: 维度
        :param gene: 基因--任务调度顺序
        :param MAXGEN: 最大循环次数
        :param pareams: 参数 [beta,gamma,alpha]
        '''
        self.sizepop=sizepop
        self.vardim=vardim
        self.gene=gene
        self.MAXGEN = MAXGEN
        self.params = params
        self.population = [FAIndividual for i in range(self.sizepop)]
        self.fitness = np.zeros((self.sizepop, 1))
        self.trace = np.zeros((self.MAXGEN, 2))



    def initialize(self):
        for i in range(0,self.sizepop):
            ind=FAIndividual(self.vardim,self.gene)
            ind.generate()
            ind.calculateFitness()
            # print(ind.chrom)#True
            # ind.chrom=ind.chrom
            # self.population.append(ind)
            # self.population[i]=ind
            self.population[i]=ind
            self.fitness[i]=ind.fitness
        # print("初始化的fitness",self.fitness)

    def evaluate(self):
        #evaluation of the population fitnesses
        fitnessZone=[]
        for i in range(0, self.sizepop):
            self.population[i].calculateFitness()
            fitnessZone.append(self.population[i].fitness)
            # print(self.population[i].chrom)
            # print("种群计算fitness",self.population[i].fitness)
            # self.fitness[i] = self.population[i].fitness
        self.FitnessRenew(fitnessZone)

    def FitnessRenew(self,fitnessZone):
        # print("fitness before:",self.fitness)
        for i in range(len(fitnessZone)):
            self.fitness[i]=fitnessZone[i]
        # print("fitness after",self.fitness)

    def solve(self):
        '''
        evolution process of firefly algorithm
        '''
        self.t = 0
        self.initialize()
        self.evaluate()
        best = np.min(self.fitness)
        # print(best)
        bestIndex = np.argmin(self.fitness)
        # self.best = copy.deepcopy(self.population[bestIndex])
        self.best=self.population[bestIndex]
        # print(self.fitness)
        self.avefitness = np.mean(self.fitness)
        # self.avefitness=sum(self.fitness)/len(self.fitness)
        # self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
        self.trace[self.t,0]=self.best.fitness
        # self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
        self.trace[self.t,1]=self.avefitness
        # print(self.fitness)
        print("Generation %d: optimal function value is: %f; average function value is %f" % (
            self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        while self.t < self.MAXGEN - 1:
            # for x in range(sizepop):
            #     print(self.population[x].chrom)
            self.t += 1
            self.move()
            self.evaluate()
            best = np.min(self.fitness)
            bestIndex = np.argmin(self.fitness)
            # print(self.fitness)
            if best<self.best.fitness:#更新最优点
                self.best = copy.deepcopy(self.population[bestIndex])
            self.avefitness = np.mean(self.fitness)
            self.trace[self.t, 0] = self.best.fitness
            self.trace[self.t, 1] = self.avefitness
            # self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
            # self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
            # print(self.fitness)
            print("Generation %d: optimal function value is: %f; average function value is %f" % (
                self.t, self.trace[self.t, 0], self.trace[self.t, 1]))

        print("Optimal function value is: %f; " %
              self.trace[self.t, 0])
        print("Optimal solution is:")
        print(self.best.chrom)
        self.printResult()
        #########################
        # print(self.best.fitness)

# #群体靠拢
#     def move(self):
#         '''
#         move the a firefly to another brighter firefly
#         '''
#         best = np.min(self.fitness)
#         bestIndex = np.argmin(self.fitness)
#         self.best = copy.deepcopy(self.population[bestIndex])
#         NewFitness=[]
#         for i in range(0, self.sizepop):
#             if self.fitness[i]>best:
#                 HanMingR=0
#                 flagOfChange=[]
#                 ChangeZone=[]
#                 for n in range(self.vardim):
#                     if(self.population[i].chrom[n])==self.best.chrom[n]:
#                         flagOfChange.append(1)
#                     else:
#                         flagOfChange.append(0)
#                         ChangeZone.append(self.population[i].chrom[n])
#                         HanMingR+=1
#                 random.shuffle(ChangeZone)
#                 HanMingR2=0
#                 for n in range(self.vardim):
#                     if (self.population[i].chrom[n]) != self.best.chrom[n]:
#                         # flagOfChange.append(0)
#                         self.population[i].chrom[n]=ChangeZone[HanMingR2]
#                         HanMingR2 += 1
#                     if(HanMingR2==HanMingR):
#                         break
#
#                 self.population[i].calculateFitness()
#             NewFitness.append(self.population[i].fitness)
#         self.FitnessRenew(NewFitness)
#
#         # print("Move After fitness",self.fitness)
#         for i in range(self.sizepop):
#             ran=random.random()
#             if(ran<self.params[2]):
#                 random.shuffle(self.gene)
#                 self.population[i].chrom = self.gene[:]
#                 self.population[i].calculateFitness()
#                 self.fitness[i] = self.population[i].fitness

#全员移动第二版
    def move(self):
        #move the a firefly to another brighter firefly
        NewFitness=[]
        for i in range(0, self.sizepop):
            for j in range(0,self.sizepop):
                if self.population[i].fitness>self.population[j].fitness:
                    HanMingR=0
                    flagOfChange=[]
                    ChangeZone=[]
                    for n in range(self.vardim):
                        if(self.population[i].chrom[n])==self.population[j].chrom[n]:
                            flagOfChange.append(1)
                        else:
                            flagOfChange.append(0)
                            ChangeZone.append(self.population[i].chrom[n])
                            HanMingR+=1
                    # print(HanMingR)
                    while(1):
                        random.shuffle(ChangeZone)
                        HanMingR2=0
                        for n in range(self.vardim):
                            if (self.population[i].chrom[n]) != self.population[j].chrom[n]:
                                # flagOfChange.append(0)
                                self.population[i].chrom[n]=ChangeZone[HanMingR2]
                                HanMingR2 += 1
                            if(HanMingR2==HanMingR):
                                break
                        HanMingCompare=0
                        for n in range(self.vardim):
                            if (self.population[i].chrom[n]) != self.population[j].chrom[n]:
                                HanMingCompare += 1
                        if(HanMingCompare<HanMingR or HanMingCompare==0):
                            break
                # self.population[i].calculateFitness()
                # self.fitness[i] = self.population[i].fitness

                self.population[i].calculateFitness()
            NewFitness.append(self.population[i].fitness)
        self.FitnessRenew(NewFitness)

        # print("Move After fitness",self.fitness)
        NewFitness1=[]
        for i in range(self.sizepop):
            ran=random.random()
            if(ran<self.params[2]):
                random.shuffle(self.gene)
                self.population[i].chrom = self.gene[:]
            self.population[i].calculateFitness()
            # self.fitness[i] = self.population[i].fitness
            NewFitness1.append(self.population[i].fitness)
        self.FitnessRenew(NewFitness1)

    def printResult(self):
        '''
        plot the result of the firefly algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Firefly Algorithm for function optimization")
        plt.legend()
        plt.show()


class FAIndividual:
    #种群个体
    def __init__(self,vardim,gene):
        self.vardim=vardim
        self.gene=gene
        self.isDone = np.zeros(((task_Num), (task_No)))
        self.DoneTime = np.zeros((task_Num, task_No))
        self.readyTime = np.zeros(server_Num)
        self.fitness=0
        self.trials=0
        self.chrom=None

    def generate(self):
        random.shuffle(self.gene)
        self.chrom=self.gene[:]
        # print("success")

    #使用server的ready时间和计算速度计算任务
    def deal(self,n,choose,startTime):
        if(startTime>self.readyTime[choose]):
            self.readyTime[choose]=startTime
        if(self.isDone[n][0]==0):
            self.DoneTime[n][0]=self.readyTime[choose]+testTask[n].size[0]/testServer[choose].speed
            # print(self.readyTime[choose]+testTask[n].size[0]/testServer[choose].speed)
            self.readyTime[choose] = self.DoneTime[n][0]
            self.isDone[n][0]=1
        else:
            for i in range(len(testTask[n].size)):
                if(self.isDone[n][i]==1):
                    continue
                else:
                    if(self.DoneTime[n][i-1]>self.readyTime[choose]):
                        self.DoneTime[n][i]=self.DoneTime[n][i-1]+testTask[n].size[i]/testServer[choose].speed
                        self.readyTime[choose] = self.DoneTime[n][i]
                        self.isDone[n][i]=1
                    else:
                        self.DoneTime[n][i]=self.readyTime[choose]+testTask[n].size[i]/testServer[choose].speed
                        self.readyTime[choose]=self.DoneTime[n][i]
                        self.isDone[n][i]=1
                    # print(server.readyTime)
                    # print(i)
                    break
        # print(self.DoneTime[n])

    def calculateTime(self):
        startTime=[None for i in range(len(self.chrom))]
        for i in range(len(self.chrom)):
            if (i >= 1):
                if (self.chrom[i] == self.chrom[i - 1]):
                    startTime[i]=self.readyTime[lastServer]
                    self.deal(self.chrom[i],lastServer,startTime[i])
                else:
                    # 找出时间最小的testserver的索引
                    startTime[i]=startTime[i-1]
                    minTime = 100000000
                    for j in range(len(testServer)):
                        if self.readyTime[j] < minTime:
                            min = self.readyTime[j]
                            choose = j
                    self.deal(self.chrom[i],choose,startTime[i])
                    lastServer=choose
            else:
                startTime[0]=0
                self.deal(self.chrom[i],0,startTime[0])
                lastServer = 0

    def theEndTime(self):
        self.calculateTime()
        endTime = []
        for i in range(len(self.DoneTime)):
            endTime.append(self.DoneTime[i][task_No - 1])
        average = sum(endTime) / len(endTime)
        maxx = max(endTime)
        return maxx

    def calculateFitness(self):
        self.isDone = np.zeros(((task_Num), (task_No)))
        self.DoneTime = np.zeros((task_Num, task_No))
        self.readyTime = np.zeros(server_Num)
        self.fitness=self.theEndTime()
        # print(self.fitness)


if __name__=="__main__":

    #获取数据
    testTask = loadTask("data/task.json")
    task_Num=len(testTask)
    task_No=len(testTask[0].isDone)
    testServer=loadServer("data/server.json")
    server_Num=len(testServer)

    sizepop=15#种群数量80

    #获得标准情况任务的排序
    standred=[]
    for j in range(task_Num):
        for i in range(task_No):
            standred.append(int(j))
    vardim=len(standred)

    fa=FireflyAlgorithm(sizepop,len(standred),standred,50,[1.0,0.001,0.00001])
    # print(fa.fitness)
    # fa.initialize()
    fa.solve()
    # for i in range(sizepop):
    #     print(fa.population[i].chrom)
    # fa.solve()
