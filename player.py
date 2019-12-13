from game import WINDOWHEIGHT,WINDOWWIDTH,sequenceIntialization,screen
import pygame

#플레이어 클래스(캐릭터 이동/캐릭터가 든 식재/애니메이션 출력)
class Player:
    def __init__(self,characterType,pwidth,pheight,movespeed,maxing):
        if characterType==0:
            self.character="ghost/"
            self.animationstuff=[21,11,12,6] #idle,walk,take,throw animationsequence value (캐릭터마다 다르므로 따로설정)
        else :
            self.character="haloduck/"
            self.animationstuff = [21, 10, 10, 8]
        self.pwidth = pwidth
        self.pheight = pheight

        self.r_pos = [120 + (pwidth / 2), WINDOWHEIGHT - 120]  # 실제 판정 위치
        self.pos = [self.r_pos[0] - (pwidth / 2), self.r_pos[1]]  # print pos
        self.maxing=maxing #최대 집을 수 있는 재료 수

        # 움직임 처리
        self.moveLeft = False
        self.moveRight = False
        self.isMoving = False
        self.stopL = False
        self.stopR = True
        self.MOVESPEED = movespeed

        # 인터랙션 처리 (클릭,식재집기)
        self.isClicking = False
        self.isThrowing = False
        self.isTaking = False

        # 집고있는 식재 넘버
        self.ingNum = 0 #0이면 1-6, 1이면7-12번호의 재료를 보여줌. 탭키로 전환가능
        self.takestate = 0 #1부터 빵
        self.throwingCount=0 #음식 던지는 시퀀스 카운트, 다 던지면 takestate와 함께 0으로 초기화할것

        # 플레이어 애니메이션 시퀀스 리스트
        self.idleL = []
        self.idleR = []
        self.walkL = []
        self.walkR = []
        self.take = []
        self.throweffect = []
        self.throw = [pygame.image.load("resource/image/player/"+self.character+"click_L.png"), \
                 pygame.image.load("resource/image/player/"+self.character+"click_R.png")]  # 0 = l, 1 = R
        self.throwR = []
        self.throwL = []

        self.idleL = sequenceIntialization(self.idleL, self.animationstuff[0], "resource/image/player/"+self.character+"idleL/", 3)
        self.idleR = sequenceIntialization(self.idleR, self.animationstuff[0], "resource/image/player/"+self.character+"idleR/", 3)
        self.walkL = sequenceIntialization(self.walkL, self.animationstuff[1], "resource/image/player/"+self.character+"walkL/", 3)
        self.walkR = sequenceIntialization(self.walkR, self.animationstuff[1], "resource/image/player/"+self.character+"walkR/", 3)
        self.take = sequenceIntialization(self.take, self.animationstuff[2], "resource/image/player/"+self.character+"take/", 3)
        self.throweffect = sequenceIntialization(self.throweffect, 7, "resource/image/player/"+self.character+"clickeffect/", 3)
        self.throwR = sequenceIntialization(self.throwR, self.animationstuff[3], "resource/image/player/"+self.character+"throwR/", 3)
        self.throwL = sequenceIntialization(self.throwL, self.animationstuff[3], "resource/image/player/"+self.character+"throwL/", 3)

        # 애니메이션 시퀀스 카운팅값
        self.idlecount = 0
        self.walkcount = 0
        self.takecount = 0
        self.throwingcount = 0
        self.effectcount = 0

    def foodtype(self,background):
        # 식재구분
        if self.takestate == 0:
            if self.ingNum==0 :
                if self.r_pos[0] > background.ingredientsPos[0][0] and self.r_pos[0] < background.ingredientsPos[1][0]:
                    return 1 # bottom bread
                elif self.r_pos[0] > background.ingredientsPos[1][0] and self.r_pos[0] < background.ingredientsPos[2][0]:
                    return 2  # lettuce
                elif self.r_pos[0] > background.ingredientsPos[2][0] and self.r_pos[0] < background.ingredientsPos[3][0]:
                    return 3  # beef patty
                elif self.r_pos[0] > background.ingredientsPos[3][0] and self.r_pos[0] < background.ingredientsPos[4][0]:
                    return 4  # cheese
                elif self.r_pos[0] > background.ingredientsPos[4][0] and self.r_pos[0] < background.ingredientsPos[5][0]:
                    return 5  # chicken patty
                elif self.r_pos[0] > background.ingredientsPos[5][0] and self.r_pos[0] < WINDOWWIDTH:
                    return 6  # top bread
                else:
                    return 0
            elif self.ingNum==1:
                if self.r_pos[0] > background.ingredientsPos[0][0] and self.r_pos[0] < background.ingredientsPos[1][0]:
                    return 7 # tomato
                elif self.r_pos[0] > background.ingredientsPos[1][0] and self.r_pos[0] < background.ingredientsPos[2][0]:
                    return 8  # gingerbread
                elif self.r_pos[0] > background.ingredientsPos[2][0] and self.r_pos[0] < background.ingredientsPos[3][0]:
                    return 9  # oinon
                elif self.r_pos[0] > background.ingredientsPos[3][0] and self.r_pos[0] < background.ingredientsPos[4][0]:
                    return 10  # egg
                elif self.r_pos[0] > background.ingredientsPos[4][0] and self.r_pos[0] < background.ingredientsPos[5][0]:
                    return 11  # paprica
                elif self.r_pos[0] > background.ingredientsPos[5][0] and self.r_pos[0] < WINDOWWIDTH:
                    return 12  # cabbage
                else:
                    return 0
            else :
                return 0
        else:
            return 0

    def setTakenfood(self,ingredients):
        if type(ingredients)==type(1):
            self.takestate = ingredients
        else :
            print("ingtype이 int가 아니므로 예외처리됨.")

    def throwingskip(self):
        self.isThrowing = False
        self.isClicking=False
        self.throwingCount = 0
        self.takestate = 0
        self.throwingcount = 0
        self.takecount = 0
    def update(self,mousepos,ing_take,ingtype):

        #캐릭터 출력
        pos = [self.r_pos[0] - (self.pwidth / 2), self.r_pos[1]]

        if self.moveLeft == False and self.moveRight == False:
            self.isMoving = False

        # 애니메이션 시퀀스 진행 숫자 (걷기/기본)
        if self.walkcount + 1 >=10:
            self.walkcount=0
        if self.idlecount + 1 >=20:
            self.idlecount=0

        # 조준
        if self.isClicking==True and self.isThrowing==False:
            #마우스가 플레이어 기준 오른쪽 위치
            if self.r_pos[0]<=mousepos[0]:
                screen.blit(self.throw[1], pos)
                screen.blit(ing_take[self.takestate - 1], [pos[0]-20, pos[1] - self.pheight * 0.4])
            #마우스가 플레이어 기준 왼쪽 위치
            if self.r_pos[0]>mousepos[0]:
                screen.blit(self.throw[0], pos)
                screen.blit(ing_take[self.takestate - 1], [pos[0]+20, pos[1] - self.pheight * 0.4])
            if self.character==0:
                if self.effectcount<((len(self.throweffect)-1)*2):
                    self.effectcount+=1
                    screen.blit(self.throweffect[(int)(self.effectcount / 2)],
                                [self.r_pos[0] - 24, self.r_pos[1] + self.pheight * 0.6])

        # 식재 투척
        if self.isThrowing==True:
            self.effectcount=0
            if self.r_pos[0]<=mousepos[0] and self.throwingcount<len(self.throwR)-1:
                screen.blit(self.throwR[self.throwingcount], self.pos)
            #왼쪽으로 투척
            if self.r_pos[0]>mousepos[0] and self.throwingcount<len(self.throwL)-1:
                screen.blit(self.throwL[self.throwingcount], self.pos)
            self.throwingcount+=1
            if self.throwingCount < 3:
                self.throwingCount += 1
                screen.blit(ing_take[self.takestate - 1],
                            [((pos[0]+20) + ((mousepos[0] - pos[0]) / 3) * self.throwingCount)-60, \
                             ((pos[1] - self.pheight * 0.4) + (
                                         (mousepos[1] - (pos[1] - self.pheight * 0.4)) / 3) * self.throwingCount)-20])
            else :
                self.throwingskip()
            if self.throwingcount>=len(self.throwL):
                self.throwingskip()
            #오른쪽으로 투척

        # 식재 집기
        if self.isTaking==True:
            self.takecount+=1
            if self.isThrowing == False and self.isClicking==False:
                screen.blit(self.take[self.takecount // 1], self.pos)
            if self.takecount>=5 :
                self.isTaking=False
                self.takecount=0

        # 식재 출력
        if self.takestate!= 0 and self.isClicking==False and self.throwingCount ==0 :
                screen.blit(ing_take[self.takestate-1], [self.pos[0],self.pos[1]-self.pheight*0.3])

        # 캐릭터 애니메이션

        if self.isMoving==True:
            self.walkcount+=1
            if self.moveLeft:
                self.r_pos[0]-=self.MOVESPEED
                self.pos[0]-=self.MOVESPEED
                if self.r_pos[0] < 0-self.pwidth:
                    self.r_pos[0] = WINDOWWIDTH+self.pwidth
                    self.pos[0] = self.r_pos[0] - (self.pwidth / 2)
                if self.isClicking == False and self.isTaking == False and self.isThrowing==False:
                    screen.blit(self.walkL[self.walkcount//1],self.pos)
            if self.moveRight:
                self.r_pos[0] += self.MOVESPEED
                self.pos[0] += self.MOVESPEED
                if self.isClicking == False and self.isTaking == False and self.isThrowing==False:
                    screen.blit(self.walkR[self.walkcount//1],self.pos)
                if self.r_pos[0] > WINDOWWIDTH+self.pwidth:
                    self.r_pos[0]= 0-self.pwidth+1
                    self.pos[0] = self.r_pos[0] - (self.pwidth / 2)
        elif self.isMoving==False and self.isTaking==False and self.isClicking==False and self.isThrowing==False:
            self.idlecount+=1
            if self.stopL==True:
                screen.blit(self.idleL[self.idlecount//1],self.pos)
            else:
                screen.blit(self.idleR[self.idlecount//1],self.pos)