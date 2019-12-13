import random
from client import *
from recipe import *
from game import WINDOWWIDTH,WINDOWHEIGHT

#손님 공장 클래스 (손님 생성과 삭제 관리)
class ClientManager:
    def __init__(self):
        self.cycle=0
        self.delay=120
        self.client=[]
        self.recipelst=[]
        self.gameout=False

    def resetclient(self):
        for i in range(0,len(self.client)):
            self.client.pop()
            self.recipelst.pop()
        self.cycle=0
        self.delay=120
        self.gameout=False

    def clientoutput(self,ui):
        self.cycle+=1
        if self.cycle%self.delay==0 and len(self.client)<8: #4초에 한번, 클라이언트의 전체 수가 8보다 작다면
            randomi = random.randint(0,0) #1/2의 확률로
            if randomi==0:
                ui.timeout=1
                self.client.append(Client(2)) #손님을 등장시킨다 실제 빌드시 스피드는 1로할것
                self.recipelst.append(Recipe(5))
                self.cycle+=1
            if len(self.client)>4:
                self.delay = 240 #개체수가 너무 많으면 딜레이 조정
            else :
                self.delay = 120
        elif self.cycle%self.delay==0 and len(self.client)>=8: #클라이언트의 전체 수가 8보다 클 경우(스크린에 꽉 차있는경우)
            tmp = 0
            for i in range(0,len(self.client)):
                if self.client[i].isdead==True:
                    self.client[i] = Client(2) #새 손님으로 교체 실제 빌드시 스피드는 1로할것
                    self.recipelst[i] = Recipe(5)
                    tmp+=1
                if tmp == 3 :
                    break
        if len(self.client)>=1 : #손님이 화면에 있다면 모든 손님을 왼쪽으로 이동시킨다
            for i in range(0,len(self.client)-1):
                self.client[i].update()
                self.recipelst[i].update(self.client[i])

    def sceneend(self):
        for i in range(0,len(self.client)-1):
            if self.client[i].r_pos[0]>0 :
                self.client[i].MOVESPEED=10
            else:
                self.client[i].MOVESPEED=0

