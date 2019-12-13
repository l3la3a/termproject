import pygame
from game import sequenceIntialization,screen,WINDOWHEIGHT,WINDOWWIDTH

#UI클래스(타이머 및 인게임 내 점수갱신)
class UI:
    def __init__(self,allocscore):
        self.score=0
        self.miss=0
        self.day=0 #레벨
        if allocscore==5:
            self.setTime = 30*10#30*60 #30fps = 1초
        elif allocscore ==7:
            self.setTime = 30*70
        else :
            self.setTime = 30*70
        self.timer = 0
        self.allocscore=allocscore #판당 할당점수
        self.timeout = 0 # 0 : ready, 1 : timethrow, 2 : timeout

        # ui패널 초기위치
        self.timerpos = [267, 15]
        self.daypos = [134, 15]
        self.scorepos = [581, 10]
        self.allocpos = [643, 10]

        # UI패널 스프라이트 초기화
        self.uidirectory = "resource/image/ui/"
        self.uipanel = pygame.image.load(self.uidirectory + "UIpanel.png")
        self.uipos = [0, 0]
        self.levels = []

        self.burgerstate = []
        self.character = 0 # 0 :ghost, 1:haloduck
        self.playerCharacter = [pygame.image.load(self.uidirectory + "ghost.png"),pygame.image.load(self.uidirectory+"haloduck.png")]  # 캐릭터 추가 시 더 넣을것
        self.timersprite = [pygame.image.load(self.uidirectory + "timer_left.png"),
                       pygame.image.load(self.uidirectory + "timer_middle.png"), \
                       pygame.image.load(self.uidirectory + "timer_right.png")]  # 0=왼쪽, 1=중간, 2=오른쪽
        self.timesup = []
        self.timesup = sequenceIntialization(self.timesup,60,self.uidirectory+"timeisup/",3)
        self.timesupcount=0
        self.RSG=[]
        self.RSG = sequenceIntialization(self.RSG,110,self.uidirectory+"RSG/",3)
        self.RSGcount=0
        self.allocscoresprite = []
        self.allocscoresprite = sequenceIntialization(self.allocscoresprite,10,self.uidirectory+"alloc/",3)

        #숫자
        self.levels = sequenceIntialization(self.levels, 5, self.uidirectory + "D_", 1)
        self.burgerstate = sequenceIntialization(self.burgerstate, 10, self.uidirectory + "a_", 1)

    def reset(self):
        self.timesupcount = 0
        self.RSGcount=0
        self.score=0
        self.miss=0

        if self.day==0: #allocscore=5
            self.allocscore=5
            self.setTime = 30*60#30*60 #30fps = 1초
        elif self.day==1: #allocscore=7
            self.allocscore=7
            self.setTime = 30*70#30*70
        else :              #allocscore=12
            self.allocscore=12
            self.setTime = 30*80#30*140
        self.timer = 0
        self.timeout = 0
        self.timersprite[1] = pygame.transform.scale(self.timersprite[1], (207, 21))

    def update(self,score):
        #UI출력
        if self.RSGcount<110:
            screen.blit(self.RSG[self.RSGcount],(0,100))
            self.RSGcount += 1
        screen.blit(self.uipanel,(0,0))
        screen.blit(self.playerCharacter[self.character],(0,0))
        # 타이머 관련 이벤트
        if self.timeout==1:
            scale=(int)(207*((self.setTime-self.timer)/self.setTime))
            screen.blit(self.timersprite[0],(self.timerpos[0],self.timerpos[1]))
            if scale>0 :
                self.timersprite[1] = pygame.transform.scale(self.timersprite[1], (scale,21))
                screen.blit(self.timersprite[1],(self.timerpos[0]+6,self.timerpos[1]))
                screen.blit(self.timersprite[2],(self.timerpos[0]+6+scale,self.timerpos[1]))
                self.timer += 1
            else:
                print("시간제한 끝")

                self.timeout=2

        elif self.timeout==0:
            screen.blit(self.timersprite[0], (self.timerpos[0], self.timerpos[1]))
            screen.blit(self.timersprite[1], (self.timerpos[0] + 6, self.timerpos[1]))
            screen.blit(self.timersprite[2], (self.timerpos[0] + 213, self.timerpos[1]))
        elif self.timeout==2:
            if self.timesupcount < 60:
                screen.blit(self.timesup[self.timesupcount],(0,100))
            self.timesupcount+=1
        screen.blit(self.levels[self.day],self.daypos) #레벨따라 0을 바꾸기

        if self.allocscore<10:
            screen.blit(self.allocscoresprite[self.allocscore],self.allocpos)
        elif self.allocscore>=10:
            screen.blit(self.allocscoresprite[self.allocscore%10],(self.allocpos[0]+5,self.allocpos[1]))
            screen.blit(self.allocscoresprite[(int)(self.allocscore/10)],(self.allocpos[0]-17,self.allocpos[1]))

        if score < 10:  # 아직 프로토타입이라 score 10 이상을 만들지않았습니다
            screen.blit(self.burgerstate[score], self.scorepos)
        elif score >=10 :
            screen.blit(self.burgerstate[score%10], (self.scorepos[0]+4,self.scorepos[1]))
            screen.blit(self.burgerstate[(int)(score/10)], (self.scorepos[0]-18,self.scorepos[1]))