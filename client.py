import random
from game import WINDOWWIDTH,WINDOWHEIGHT,sequenceIntialization,screen

#손님 클래스(손님 위치/종류/피격 판정/애니메이션 출력)
class Client: #손님 객체 오른쪽에서 왼쪽으로 움직여야만 하며 콜라이더를 포함하고있어야함

    clientSaveY=0 #이전생성손님의 생성y좌표를 저장하여 다음생성 손님과 스프라이트겹침을 피함

    def __init__(self,speed):

        self.CLIENTTYPE = random.randint(0, 2) #손님 종류

        #print("타입 : {} 손님 ".format(self.CLIENTTYPE))
        if self.CLIENTTYPE==0 :
            self.clientsizeX = 270
            self.clientsizeY = 120
            self.MOVESPEED = speed
            self.standardY = 60
        elif self.CLIENTTYPE==1:
            self.clientsizeX = 166
            self.clientsizeY = 184
            self.MOVESPEED=speed*1.5
            self.standardY = 60
        elif self.CLIENTTYPE==2:
            self.clientsizeX = 205
            self.clientsizeY = 65
            self.MOVESPEED = speed*0.5
            self.standardY = 20

        self.getScore = self.MOVESPEED * 1500 #득점은 스피드와 비례
        self.r_pos = [WINDOWWIDTH+self.clientsizeX,random.randrange(100,450,90)] #y위치는 초기에 랜덤좌표지정
        while self.r_pos[1]== Client.clientSaveY:
            self.r_pos[1] = random.randrange(100,450,90)
            print("좌표같으므로 변경 지정{}".format(self.r_pos))
        Client.clientSaveY = self.r_pos[1]
        self.pos = [self.r_pos[0]-(self.clientsizeX/2),self.r_pos[1]-(self.clientsizeY/2)] #출력위치
        self.level = 5
        self.colider = [self.pos[0]+(self.clientsizeX/2),self.pos[1]+(self.clientsizeY/2)] #마우스 피격가능좌표

        self.isClear=False #레시피 완성되었으면 True
        self.isMissing=False #플레이어가 재료를 잘못 던졌을 때
        self.isHitting=False #플레이어가 재료를 잘 던졌을 때

        self.idlecount=0
        self.missingcount=0
        self.hittingcount=0

        self.isdead=False #사라질 객체
        # 우주선(손님) 애니메이션 시퀀스
        self.clientdirectory = "resource/image/client/"
        self.clientname = ["HappyDolphin","UFJ","dduck"]

        self.idle = []  # sequence 30
        self.hit = []
        self.miss = []

        self.effect=[]
        self.effect = sequenceIntialization(self.effect,5,"resource/image/client/hiteffect/",3)
        self.effectcount =0

        # 우주선(손님) 애니메이션 시퀀스 초기화
        self.idle = sequenceIntialization(self.idle, 15, \
                                                 "resource/image/client/" + self.clientname[self.CLIENTTYPE] + "/idle/", 2)
        self.hit = sequenceIntialization(self.hit, 8, \
                                                "resource/image/client/" + self.clientname[self.CLIENTTYPE] + "/hit/", 2)
        self.miss = sequenceIntialization(self.miss, 15, \
                                                 "resource/image/client/" + self.clientname[self.CLIENTTYPE] + "/miss/", 2)

    def mouseDetect(self,mousepos):
        if mousepos[0] > self.pos[0] and mousepos[0] < self.pos[0] + self.clientsizeX and \
                mousepos[1] > self.pos[1] and mousepos[1] < self.pos[1] + self.clientsizeY and self.isClear == False:
            return True
        else:
            return False

    def update(self):
        if self.isHitting == True:
            if self.hittingcount < 7:
                self.hittingcount += 1
                screen.blit(self.hit[self.hittingcount // 1], self.pos)
                if self.effectcount<5:
                    screen.blit(self.effect[self.effectcount//1],(self.pos[0],self.pos[1]-(1700/self.standardY)))
                    self.effectcount += 1
            elif self.hittingcount>=7:
                screen.blit(self.hit[6], self.pos)
                self.hittingcount = 0
                self.isHitting=False
                self.effectcount=0
        elif self.isMissing == True:
            if self.missingcount<14:
                self.missingcount+=1
                screen.blit(self.miss[self.missingcount//1],self.pos)
            elif self.missingcount>=14:
                self.missingcount=0
                self.isMissing=False
        elif self.isClear == True:
            self.idlecount += 1
            if self.idlecount >= 14:
                self.idlecount = 0
            self.pos[0] -= (self.MOVESPEED) * 6
            screen.blit(self.idle[self.idlecount // 1], self.pos)  # 화면 출력
        else :
            self.idlecount+=1
            if self.idlecount>=14 :
                self.idlecount=0
            self.r_pos[0] -= self.MOVESPEED
            self.pos[0] -= self.MOVESPEED
            screen.blit(self.idle[self.idlecount // 1], self.pos)
        if self.pos[0] < 0 - self.clientsizeX:  # 손님이 화면 밖으로 나간다면
            self.isdead = True