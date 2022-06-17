class WaitingQueue:
    def __init__(self):
        self.waitingQueue=[]

    def addToQueue(self,name:tuple)->int:
        if not name in self.waitingQueue:
            self.waitingQueue.append(name)
        return self.waitingQueue.index(name)

