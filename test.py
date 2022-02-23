import numpy as np
import random
# task_Num=10
# task_No=5

# a=np.zeros((task_Num,task_No))
# print(a)
#
# lst=[0,1,2,3,4,5]
# for i in range(6):
#     lst.pop(len(lst)-1)
#     print(lst)
#
# startTime=[None for i in range(10)]
# print(startTime)

a=random.random()
print(a)

##全员移动第一版本
#     def move(self):
#         '''
#         move the a firefly to another brighter firefly
#         '''
#         for i in range(0,self.sizepop):
#             for j in range(0,self.sizepop):
#                 if self.fitness[j]<self.fitness[i]:
#                     HanMingR=0
#                     flagOfChange=[]
#                     ChangeZone=[]
#                     for n in range(self.vardim):
#                         if(self.population[i].chrom[n]==self.population[j].chrom[n]):
#                             flagOfChange.append(1)
#                             # print(ChangeZone)
#                         else:
#                             flagOfChange.append(0)
#                             ChangeZone.append(self.population[i].chrom[n])
#                             HanMingR+=1
#                     random.shuffle(ChangeZone)
#                     while(1):
#                         for n in range(self.vardim):
#                             if(flagOfChange[n]!=1):
#                                 # print(ChangeZone)
#                                 self.population[i].chrom[n]=ChangeZone[len(ChangeZone)-1]
#                                 ChangeZone.pop(len(ChangeZone)-1)
#                         for n in range(self.vardim):
#                             HanMingR2 = 0
#                             if (self.population[i].chrom[n] != self.population[j].chrom[n]):
#                                 HanMingR2 += 1
#                         if(HanMingR2<HanMingR):
#                             break
#                         if(HanMingR2==0):
#                             break
#                     self.population[i].calculateFitness()
#                     self.fitness[i] = self.population[i].fitness