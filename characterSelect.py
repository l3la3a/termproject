from game import screen,WINDOWWIDTH,WINDOWHEIGHT,sequenceIntialization
import pygame
from button import *
from soundmanager import buttonMouseOnSound

class CharacterSelect:
    """
    캐릭터미리보기, 상단textbox, text를 출력하는 ui번들.
    사용후에는 반드시 객체삭제하고 재사용 필요시 재생성할것
    """
    def __init__(self):
        self.background = pygame.image.load("resource/image/background/background_01.png")
        self.cfont = pygame.font.Font('resource/font/DungGeunMo.ttf', 18)

        # 상단 타이틀
        self.title = pygame.image.load("resource/image/characterselect/textbox.png")
        self.titlepos=[6,0]
        self.titleposy=-50

        # 배경 위 판 (초기화 필요)
        self.panel=[]
        self.panelCount=0

        #캐릭터 위에 나타나는 선택 인터랙션,
        # #[0] 투명이미지 [1] 마우스오버시 나타나는 흰 테두리 이미지 [2] 선택시의 애니메이션 시퀀스 (초기화필요)
        self.cButton=[pygame.image.load("resource/image/characterselect/transperent.png"),\
                      pygame.image.load("resource/image/characterselect/selectline.png"),[]]
        self.cButtonCount=0 # 시퀀스카운트
        self.cButtonMouseOn=0 #0: 범위 외, 1:ghost캐릭터 범위, 2:haloduck 캐릭터 범위
        self.cButtonSelected=0 #0 : 미선택, 1 : ghost, 2 : haloduck
        self.cButtonpos=[137,134]
        self.cName=[[],[]]
        self.btSound=False

        # 캐릭터 프리뷰 이미지를 담는 리스트. 각각 [0] : 정지, [1] : idle이미지(초기화필요), [2] : 걷는이미지 (초기화필요) [3] : 반투명
        self.ghostpreview=[pygame.image.load("resource/image/player/ghost/idleR/000.png"),
                           [],[], pygame.image.load("resource/image/player/ghost/transparent.png")]
        self.haloduckpreview=[pygame.image.load("resource/image/player/haloduck/idleL/000.png"),
                              [],[], pygame.image.load("resource/image/player/haloduck/transparent.png")]
        self.cCharacterCount=0 #캐릭터 프리뷰 애니메이션시퀀스카운트
        self.previewpos=[228,203] #고스트캐릭터 위치, haloduck pos = ghostpos[0]+175
        self.crop=[pygame.image.load("resource/image/characterselect/crop1.png"),pygame.image.load("resource/image/characterselect/crop2.png")]

        # 캐릭터 선택 확정 체크박스
        self.checkbox=[pygame.image.load("resource/image/characterselect/checkbox0.png"),
                       pygame.image.load("resource/image/characterselect/checkbox1.png")]
        self.checkboxConfirmtext=""
        self.checkboxConfirmtextrender=self.cfont.render(self.checkboxConfirmtext, True, (255,210,37))
        self.isCheckboxMouseOn=False
        self.isCheckboxSelected=False
        self.checkboxpos=[-5,360]

        # 인트로/게임바로시작버튼

        self.introbuttonpos=[47,432] # 1버튼은 x좌표 +310
        self.introbutton=[Button(self.introbuttonpos[0],self.introbuttonpos[1],300,87,"intro_button0.png"),
                          Button(self.introbuttonpos[0]+310,self.introbuttonpos[1],300,87,"intro_button1.png")]
        self.introbutton[0].isActivated = False
        self.introbutton[1].isActivated = False
        self.buttoncap=[pygame.image.load("resource/image/characterselect/button0cap.png"),\
                        pygame.image.load("resource/image/characterselect/button1cap.png")] #버튼이 활성화되지 않았을 때 위에 씌우는 가림막이미지



        self.sequenceinit()

    def sequenceinit(self): #필요한 이미지시퀀스 초기화
        self.panel=sequenceIntialization(self.panel,30,"resource/image/characterselect/panel/",3)
        self.cButton[2]=sequenceIntialization(self.cButton[2],60,"resource/image/characterselect/select/",3)
        self.ghostpreview[1]=sequenceIntialization(self.ghostpreview[1],21,"resource/image/player/ghost/idleR/",3)
        self.haloduckpreview[1]=sequenceIntialization(self.haloduckpreview[1],21,"resource/image/player/haloduck/idleL/",3)
        self.ghostpreview[2]=sequenceIntialization(self.ghostpreview[2],11,"resource/image/player/ghost/walkR/",3)
        self.haloduckpreview[2]=sequenceIntialization(self.haloduckpreview[2],10,"resource/image/player/haloduck/walkL/",3)
        self.cName[0]=sequenceIntialization(self.cName[0],60,"resource/image/characterselect/ghosttext/",3)
        self.cName[1]=sequenceIntialization(self.cName[1],60,"resource/image/characterselect/haloducktext/",3)
        self.introbutton[0].image_mouseOn=sequenceIntialization(self.introbutton[0].image_mouseOn,30,"resource/image/button/intro_button0mouseOn/",3)
        self.introbutton[1].image_mouseOn = sequenceIntialization(self.introbutton[1].image_mouseOn, 30,
                                                       "resource/image/button/intro_button1mouseOn/", 3)

    def isMouseOn(self,mousepos):
        if mousepos[1] > self.previewpos[1] - 20 and mousepos[1] < self.previewpos[1] + 120:
            if mousepos[0]>self.previewpos[0]-20 and mousepos[0]<self.previewpos[0]+72+20:
                    self.cButtonMouseOn=1
                    if self.btSound==False:
                        buttonMouseOnSound.play()
                        self.btSound=True
            elif mousepos[0]>self.previewpos[0]+175-20 and mousepos[0]<self.previewpos[0]+175+72+20:
                    self.cButtonMouseOn=2
                    if self.btSound==False:
                        buttonMouseOnSound.play()
                        self.btSound=True
            else:
                self.btSound=False
                self.cButtonMouseOn=0
        else:
            self.btSound=False
            self.cButtonMouseOn=0

        if mousepos[0] > self.checkboxpos[0] and mousepos[0] < WINDOWWIDTH:
            if mousepos[1]>self.checkboxpos[1]-10 and mousepos[1] < self.checkboxpos[1]+40:
                self.isCheckboxMouseOn=True
            else:
                self.isCheckboxMouseOn=False
        else:
            self.isCheckboxMouseOn=False
    def update(self):
        screen.blit(self.background,(0,0))
        screen.blit(self.panel[self.panelCount],(0,0))
        if self.titleposy<=0 :
            self.titleposy+=9
            screen.blit(self.title,(self.titlepos[0],self.titlepos[1]+self.titleposy))
        else:
            screen.blit(self.title,self.titlepos)
        self.panelCount += 1
        if self.panelCount>=30:
            self.panelCount=0

        if self.cButtonSelected==0:
            if self.cButtonMouseOn==0:
                screen.blit(self.cButton[0],self.cButtonpos)
                screen.blit(self.ghostpreview[0], self.previewpos)
                screen.blit(self.haloduckpreview[0], (self.previewpos[0] + 175, self.previewpos[1]))
            elif self.cButtonMouseOn==1:
                if self.cCharacterCount>=20:
                    self.cCharacterCount=0
                screen.blit(self.cButton[1],self.cButtonpos)
                screen.blit(self.ghostpreview[1][self.cCharacterCount], self.previewpos)
                screen.blit(self.haloduckpreview[0], (self.previewpos[0] + 175, self.previewpos[1]))
                self.cCharacterCount += 1
            elif self.cButtonMouseOn==2:
                if self.cCharacterCount>=20:
                    self.cCharacterCount=0
                screen.blit(self.cButton[1],(self.cButtonpos[0]+175,self.cButtonpos[1]))
                screen.blit(self.ghostpreview[0], self.previewpos)
                screen.blit(self.haloduckpreview[1][self.cCharacterCount], (self.previewpos[0] + 175, self.previewpos[1]))
                self.cCharacterCount+=1
        elif self.cButtonSelected==1:
            screen.blit(self.crop[0],(0,150))
            screen.blit(self.ghostpreview[2][self.cCharacterCount],self.previewpos)
            if self.isCheckboxSelected==True:
                screen.blit(self.haloduckpreview[3],(self.previewpos[0]+175,self.previewpos[1]))
            else :
                if self.cButtonMouseOn==2:
                    screen.blit(self.cButton[1], (self.cButtonpos[0] + 175, self.cButtonpos[1]))
                screen.blit(self.haloduckpreview[0], (self.previewpos[0] + 175, self.previewpos[1]))
            self.cCharacterCount+=1
            if self.cCharacterCount>=11:
                self.cCharacterCount=0
            screen.blit(self.cButton[2][self.cButtonCount],self.cButtonpos)
            screen.blit(self.cName[0][self.cButtonCount], (198, 320))
            self.cButtonCount+=1
            if self.cButtonCount>=60:
                self.cButtonCount=30
        elif self.cButtonSelected==2:
            screen.blit(self.crop[1], (444, 150))
            if self.isCheckboxSelected == True:
                screen.blit(self.ghostpreview[3],self.previewpos)
            else :
                if self.cButtonMouseOn==1:
                    screen.blit(self.cButton[1], (self.cButtonpos[0], self.cButtonpos[1]))
                screen.blit(self.ghostpreview[0], self.previewpos)
            screen.blit(self.haloduckpreview[2][self.cCharacterCount],(self.previewpos[0]+175,self.previewpos[1]))
            self.cCharacterCount+=1
            if self.cCharacterCount>=10:
                self.cCharacterCount=0
            screen.blit(self.cButton[2][self.cButtonCount], (self.cButtonpos[0]+175,self.cButtonpos[1]))
            screen.blit(self.cName[1][self.cButtonCount],(373,310))
            self.cButtonCount+=1
            if self.cButtonCount >= 60:
                self.cButtonCount = 30
        if self.isCheckboxSelected==False:
            screen.blit(self.checkbox[0],self.checkboxpos)
        elif self.isCheckboxSelected==True:
            screen.blit(self.checkbox[1],self.checkboxpos)
            screen.blit(self.checkboxConfirmtextrender,(self.checkboxpos[0]+120,self.checkboxpos[1]+40))
        self.introbutton[0].update()
        self.introbutton[1].update()
        if self.introbutton[0].isActivated==False and self.introbutton[1].isActivated==False :
            screen.blit(self.buttoncap[0],self.introbuttonpos)
            screen.blit(self.buttoncap[1],(self.introbuttonpos[0]+310,self.introbuttonpos[1]))
