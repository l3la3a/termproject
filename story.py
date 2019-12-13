from game import WINDOWWIDTH,WINDOWHEIGHT,screen,sequenceIntialization
import pygame
from storytext import *
from button import *
""" 
일러스트 컷씬이 포함된 스토리출력과 관련된 클래스
스토리 연출이 끝나면 반드시 객체를 지울것 (필요 시 재생성하여 사용)
스토리 연출을 더 넣고싶은경우 트랜지션과 함께 사용 
삽화 수를 더 늘리고싶은경우 self.illustlen을 수정할 것
"""

class Story:
    def __init__(self,scenename):
        self.scenename=scenename # (0 : 인트로, 1:아웃트로로 고정 지정되어있음. 혹시 추가 할 상황이 생긴다면 2부터 추가)
        self.illust =[]
        self.font = pygame.font.Font('resource/font/DungGeunMo.ttf',18)
        if self.scenename==0:
            self.illustlen=7
            self.control = pygame.image.load("resource/image/story/control.png")
            self.illustani = []
            self.illustanicount=0
            self.illustinit("intro/")

            self.canButtonWatch=False
            self.buttonpos=[WINDOWWIDTH/2-115,500] #center button
            self.buttons=[Button(self.buttonpos[0]-230,self.buttonpos[1],230,90,"str_button0.png"),\
                          Button(self.buttonpos[0],self.buttonpos[1],230,90,"str_button1.png"),\
                          Button(self.buttonpos[0]+230,self.buttonpos[1],230,90,"str_button2.png")]
            for i in range(0,len(self.buttons)):
                self.buttons[i].image_mouseOn=sequenceIntialization(self.buttons[i].image_mouseOn,16,"resource/image/button/str_button"+(str)(i)+"mouseOn/",3)

             # 인트로 총 7장
        elif self.scenename==1:
            self.illustlen=4 #아웃트로 총 4장
            self.illustinit("outtro/")

        self.illustpos=[50,100]
        self.count=0 #현재 진행된 삽화 페이지 수
        self.isSkip=False
        self.isPause=False
        self.isEnd=False

        #크레딧 관련
        self.credit = pygame.image.load("resource/image/story/credit.png")
        self.creditpos = [0, 0]
        self.iscredit = False
        self.iscreditEnd=False
        self.ScrollSpeedUp=False
        self.creditScrollSpeed = 2

        # 텍스트 출력 관련
        self.textOutputActivated=False
        self.textoutputterm = 3 #0.1초에 한 글자 출력
        # 컷씬과 함께 사용되는 설명 텍스트. 2차배열이며 앞번호=일러스트번호
        if scenename==0:
            self.textlst = introtxt
        elif scenename == 1:
            self.textlst = outtrotxt
        self.textcount=0 #현재 진행된 텍스트 줄의 개수
        self.textindex=0 #현재 출력된 글자 수
        self.textpos = [50,400]
        self.tmptext="" #실제 출력되고있는 현재 텍스트
        self.text= self.textlst[self.count][self.textcount] #실제 출력 할 텍스트 한 줄
        self.texts=self.textlst[self.count] #실제 출력 할 텍스트 한 더미
        # 스토리 컷씬은 검은배경+삽화+스크립트로 통일되며, 일반 스크립트 색상은 흰색, 대화는 금색으로 사용
        self.scriptcolor = (255,255,255)
        self.talkcolor=(255,211,1)
        self.color = self.scriptcolor


    def creditScrollupdate(self):
        if self.iscreditEnd==False:
            screen.blit(self.credit,self.creditpos)
            if self.ScrollSpeedUp==False:
                self.creditpos[1]-=self.creditScrollSpeed
            elif self.ScrollSpeedUp==True:
                self.creditpos[1] -= self.creditScrollSpeed*5
            if self.creditpos[1] < -3500:
                print("높이넘음")
                self.iscreditEnd=True

    def illustinit(self,directory):
        self.illust = sequenceIntialization(self.illust,self.illustlen,"resource/image/story/"+directory,3)
        if self.scenename==0:
            self.illustani = sequenceIntialization(self.illustani,144,"resource/image/story/intro/004/",3)

    def isClick(self):
        if self.isPause==False:
            try:
                if self.count<self.illustlen:
                    self.textcount+=1
                    self.tmptext=""
                    self.textindex=0
                    print(self.textcount)
                    # 클릭 음향 넣는것도 좋겠다.
                    if self.textcount>=len(self.texts):
                        self.count+=1
                        if self.scenename==0 and self.count==2:
                            self.color = self.talkcolor
                        self.textoutputterm=0
                        self.textcount=0
                        self.illustanicount=0
                        self.texts = self.textlst[self.count]
                    self.text = self.texts[self.textcount]
                    self.textOutputActivated=True
            except:
                print("정지")
                if self.scenename==0:
                    self.canButtonWatch=True
                self.count-=1
                self.texts = self.textlst[self.count]
                self.textcount=len(self.texts)
                self.textOutputActivated=False
                self.isPause=True
                if self.scenename==1:
                    self.isPause=True
                    self.iscredit=True

    def isSkip(self):
        self.count=len(self.illust)

    def reset(self):
        self.color = self.scriptcolor
        self.count=0
        self.textcount=0
        self.textindex=0
        self.textoutputterm=0
        self.textOutputActivated = False
        self.isPause=False
        self.tmptext = ""
        self.text= self.textlst[self.count][self.textcount] #실제 출력 할 텍스트 한 줄
        self.texts=self.textlst[self.count] #실제 출력 할 텍스트 한 더미
        if self.scenename==0:
            for i in range(0,len(self.buttons)):
                self.buttons[i].mouseOn=False
            self.canButtonWatch=False
        self.isSkip = False
        self.isEnd = False

    def updateStoryScene(self):
        screen.fill((0,0,0)) #검은배경
        if self.iscredit==False:
            if not self.isSkip:
                if self.count!=4 :
                    screen.blit(self.illust[self.count],self.illustpos)
                else :
                    screen.blit(self.illustani[self.illustanicount],self.illustpos)
                    screen.blit(self.control, (0, 30))
                    self.illustanicount+=1
                    if self.illustanicount>143:
                        self.illustanicount=0
                self.updateText()
            if self.scenename==0 and self.canButtonWatch==True:
                for i in range(0,len(self.buttons)):
                    self.buttons[i].update()
        elif self.iscredit==True:
            self.creditScrollupdate()


    def updateText(self):
        if self.textOutputActivated:
            self.textoutputterm+=1
            if self.textoutputterm%1==0:
                if self.textindex<len(self.text):
                    self.tmptext += self.text[self.textindex]
                    self.textindex += 1
                elif self.textindex>=len(self.text):
                    screen.blit((self.font.render(self.text[self.textcount], True, self.color)), (self.textpos[0],self.textpos[1]+(self.textcount)*25))
                    self.textOutputActivated=False
            screen.blit((self.font.render(self.tmptext, True, self.color)), (self.textpos[0],self.textpos[1]+(self.textcount)*25))
            if self.textindex!=0:
                for i in range(0, self.textcount):  # 이전에 출력된 같은컷씬의 텍스트
                    screen.blit((self.font.render(self.texts[i], True, self.color)), (self.textpos[0],self.textpos[1]+i*25))
        else:
            screen.blit((self.font.render(self.text, True, self.color)), (self.textpos[0],self.textpos[1]+(self.textcount)*25))
            if self.textindex!=0:
                for i in range(0, self.textcount):  # 이전에 출력된 같은컷씬의 텍스트
                    screen.blit((self.font.render(self.texts[i], True, self.color)), (self.textpos[0],self.textpos[1]+i*25))

