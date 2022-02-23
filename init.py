import random
import pickle

server_Num = 5 #服务器个数
task_Num = 42  # 任务个数
task_No = 18  # 依赖关系任务的长度

class task:
    def __init__(self,size,isDone,DoneTime):
        self.size=size
        self.isDone=isDone
        self.DoneTime=DoneTime

    #使用server的ready时间和计算速度计算任务
    def deal(self,server):
        if(self.isDone[0]==0):
            self.DoneTime[0]=server.readyTime+self.size[0]/server.speed
            server.readyTime = self.DoneTime[0]
            print(server.readyTime)
            print("0")
            self.isDone[0]=1
        else:
            for i in range(len(self.size)):
                if(self.isDone[i]==1):
                    continue
                else:
                    if(self.DoneTime[i-1]>server.readyTime):
                        self.DoneTime[i]=self.DoneTime[i-1]+self.size[i]/server.speed
                        server.readyTime = self.DoneTime[i]
                        self.isDone[i]=1
                    else:
                        self.DoneTime[i]=server.readyTime+self.size[i]/server.speed
                        server.readyTime=self.DoneTime[i]
                        self.isDone[i]=1
                    # print(server.readyTime)
                    # print(i)
                    break

class server:
    def __init__(self,speed,readyTime):
        self.speed=speed
        self.readyTime=readyTime

#读取数据
def loadTask(dir):
    Task=[]
    with open(dir, 'rb') as file:
        for i in range(task_Num):
            obj = pickle.load(file)
            Task.append(obj)
    return Task

#读取数据
def loadServer(dir):
    server=[]
    with open(dir, 'rb') as file:
        for i in range(server_Num):
            obj = pickle.load(file)
            server.append(obj)
    return server

if __name__=="__main__":
    # 初始化部分
    # clearData

    testServer = [server for i in range(server_Num)]
    for i in range(server_Num):
        speed = random.randint(100, 10000)
        testServer[i] = server(speed, 0)

    for i in range(len(testServer)):
        with open('data/server.json','ab') as file:
            pickle.dump(testServer[i], file)
    readServer = []
    # with open('data/server.json','rb') as file:
    #     for i in range(len(testServer)):
    #         obj=pickle.load(file)
    #         readServer.append(obj)
    # for ser in readServer:
    #     print("speed:{} readyTime:{}".format(ser.speed,ser.readyTime))

    testTask = [task for i in range(task_Num)]
    for i in range(task_Num):
        size = []
        isDone = []
        DoneTime = []
        for j in range(task_No):
            sizei = random.randint(10, 10000)
            isDonei = 0
            time = -1
            size.append(sizei)
            isDone.append(isDone)
            DoneTime.append(time)
        testTask[i] = task(size, isDone, DoneTime)
    for i in range(len(testTask)):
        with open('data/task.json','ab') as file:
            pickle.dump(testTask[i], file)
    readTask = []
    # with open('data/task.json','rb') as file:
    #     for i in range(len(testTask)):
    #         obj=pickle.load(file)
    #         readTask.append(obj)


    # for i in range(task_Num):
    #     print(testTask[i].size)
    # for i in range(server_Num):
    #     print(testServer[i].speed)