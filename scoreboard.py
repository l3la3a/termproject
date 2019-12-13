import pygame
from game import screen,sequenceIntialization
import random
from button import *
from soundmanager import resultScoreSound, resultTotalScoreSound
class Scoreboard:
    def __init__(self,score1,score2,miss,level): #프로토타입은 순서대로 ui.allocscore, ui.score, 0, 0으로 적으면됨
        self.score = [score1,score2,miss,score2-miss,0,0]

        if score1<=score2-miss:
        
            self.clear=True
        else:
            self.clear=False

        self.level = level
        self.font = pygame.font.Font('resource/font/DungGeunMo.ttf',15)
        self.scorefont = pygame.font.Font('resource/font/DungGeunMo.ttf',40)
        self.texts=["","","","","",""]
        self.tmptext=""
        self.textsep=15
        self.tmpnum=0
        self.scoresign=pygame.image.load("resource/image/scoreboard/scoresign.png") #점수표 안내
        self.daysign = pygame.image.load("resource/image/scoreboard/day.png") #하단 통과여부 옆 사인\
        self.daynumbers=[pygame.image.load("resource/image/ui/a_1.png"),\
                         pygame.image.load("resource/image/ui/a_2.png"),\
                         pygame.image.load("resource/image/ui/a_3.png")]
        self.daypos=[(51,406),(111,432)]

        self.comment=[[self.font.render("인공지능보다 ", True, (243,214, 246)), \
                       self.font.render("잘 하시네요.. 역시", True, (243, 214, 246)), \
                       self.font.render("자연지능은 다르구나", True, (243,214, 246))],\
                      [self.font.render("재료가 튼튼하죠?", True, (243,214, 246)),\
                       self.font.render("최근에 빵소재를", True, (243,214, 246)),\
                       self.font.render("기가스틸로 바꿔", True, (243,214, 246)),\
                       self.font.render("버렸거든요.", True, (243,214, 246))], \
                      [self.font.render("재료를 부드럽게 ", True, (243,214, 246)),\
                       self.font.render("던져주세요. 자꾸", True,(243,214, 246)), \
                       self.font.render("'살아있는 재료협회'", True, (243, 214, 246)), \
                       self.font.render("에서 민원이 와요.", True,(243,214, 246))],
                      [self.font.render("이런 일 얼마주면 계속", True, (243,214, 246)),\
                       self.font.render("할 거예요? 시간제한", True, (243,214, 246)),\
                       self.font.render("내로 키보드와 마우스", True, (243,214, 246)),\
                       self.font.render("깔짝이는 일이요!", True, (243,214, 246))], \
                      [self.font.render( "취업난 시즌에는", True, (243,214, 246)),\
                       self.font.render( "역시 일하는 게임을", True, (243,214, 246)),\
                       self.font.render( "해야죠!", True, (243,214, 246))], \
                      [self.font.render("라떼는 말이예요..", True, (243,214, 246)), \
                       self.font.render("3초면 10만 손님을", True, (243,214, 246)), \
                       self.font.render("버거드렸거든요.", True, (243, 214, 246)),\
                       self.font.render("물론 꿈속에서..", True, (243, 214, 246))
                       ]]
        self.commentary=random.randint(0,len(self.comment)-1)

        self.scoreboardpanel=[]
        self.scoreboardpanel=sequenceIntialization(self.scoreboardpanel,60,"resource/image/scoreboard/scoreboard_idle/",3)
        self.scoreboardtransition=[]
        self.scoreboardtransition=sequenceIntialization(self.scoreboardtransition,60,"resource/image/scoreboard/scoreboard_transition/",3)
        self.sasc=0 #scoreboard animation sequence count
        self.sctransend=False #sequence front transition(scoreboard transition) end value

        self.failAndPass=[] #fail or pass 이미지, # 0:fail, 1:pass
        for i in range(0,2):
            if i==0:
                tmplst=[]
                tmplst=sequenceIntialization(tmplst,30,"resource/image/scoreboard/failpanel_idle/",3)
            elif i==1:
                tmplst=[]
                tmplst=sequenceIntialization(tmplst,30,"resource/image/scoreboard/passpanel_idle/",3)
            self.failAndPass.append(tmplst)
        self.failAndPassTransition=[] #fail or pass transition
        for i in range(0,2):
            if i==0:
                tmplst=[]
                tmplst=sequenceIntialization(tmplst,27,"resource/image/scoreboard/failpanel_transition/",3)
            elif i==1:
                tmplst=[]
                tmplst=sequenceIntialization(tmplst,27,"resource/image/scoreboard/passpanel_transition/",3)
            self.failAndPassTransition.append(tmplst)
        self.fnpcount=0 #failandpass text animationcount
        self.fnppos=(140,395)

        self.mouseOn=[0,0,0] #버튼 위로 마우스가 올라가면 1, 아니면0

        self.outputend=False #점수 애니메이션 종료
        self.timer=0
        self.scoreappear=0 #스코어가 1개씩 천천히 나타나도록 단계를 지정
        self.pause = False #Pause가 클릭에의해 True가되면 배경갱신을 제외한 모든 이벤트 중지
        self.scoreOutputHeight=40 #점수 출력 간격
        self.outputHeight = 20 # 버튼 사이 간격조정 출력 높이


        # 출력 위치좌표
        self.scoreOutputpos=(305,251)
        self.commentpos=(466,265)
        self.buttonpos=[[self.commentpos[0]-20,self.commentpos[1]+self.outputHeight*5.5],\
                        [self.commentpos[0]-20,self.commentpos[1]+self.outputHeight*7.5],\
                        [self.commentpos[0]-20,self.commentpos[1]+self.outputHeight*9.5]] #0,1,2마우스 클릭 판정위치.
        self.buttonSize=[192,37]
        self.button = [(Button(self.buttonpos[0][0],self.buttonpos[0][1],self.buttonSize[0],self.buttonSize[1],"sc_button0.png"),Button(self.buttonpos[0][0],self.buttonpos[0][1],self.buttonSize[0],self.buttonSize[1],"sc_button1.png")),\
                       Button(self.buttonpos[1][0],self.buttonpos[1][1],self.buttonSize[0],self.buttonSize[1],"sc_button2.png"),\
                       Button(self.buttonpos[2][0],self.buttonpos[2][1],self.buttonSize[0],self.buttonSize[1],"sc_button3.png")]
        self.buttonInit()
        self.buttonTransition=[]
        for i in range(0,3):
            tmplst=[]
            tmplst = sequenceIntialization(tmplst,7,"resource/image/button/sc_button"+(str)(i+1)+"transition/",3)
            self.buttonTransition.append(tmplst)

    def buttonInit(self):
        #버튼 이미지 ((다음날로반투명,다음날로투명),다시하기,메인으로)
        self.button[0][1].image_mouseOn=sequenceIntialization(self.button[0][1].image_mouseOn,15,"resource/image/button/sc_button"+(str)(1)+"mouseOn/",3)
        self.button[1].image_mouseOn = sequenceIntialization(self.button[1].image_mouseOn, 15,
                                                                "resource/image/button/sc_button" + (str)(2) + "mouseOn/", 3)
        self.button[2].image_mouseOn = sequenceIntialization(self.button[2].image_mouseOn, 15,
                                                             "resource/image/button/sc_button" + (str)(
                                                                 3) + "mouseOn/", 3)
    def scoreboardreset(self):
        self.clear = True
        self.outputend=False
        self.tmpnum=0
        self.fnpcount = 0
        self.timer=0
        self.scoreappear=0
        self.sasc = 0
        self.sctransend=False
        self.pause = False
        self.commentary=random.randint(0,len(self.comment)-1)

    def update(self):

        if self.sctransend==False:
            screen.blit(self.scoreboardtransition[self.sasc], (0, 0))
            self.sasc+=1
            if self.sasc>58:
                self.sctransend=True
                self.sasc=0
        elif self.sctransend==True:
            screen.blit(self.scoreboardpanel[self.sasc],(0,0)) #마지막 프레임 거슬리니 시간나면 수정할것
            self.sasc+=1
            if self.sasc>59:
                self.sasc=0

        if self.outputend==False:
            self.timer+=1

        if self.scoreappear>5:
            print(self.scoreappear)
            self.scoreappear=0

        self.tmptext = (str)(self.tmpnum)
        if self.scoreappear<4:
            self.texts[self.scoreappear] = self.scorefont.render(self.tmptext, True, (243,214,246))
        elif self.scoreappear>=4:
            self.texts[3] = self.scorefont.render((str)(self.score[3]), True, (255,238,32))
        if self.scoreappear <= 4:
            for i in range(0, len(self.score)):
                if self.scoreappear == i:
                    if self.tmpnum < self.score[i]:
                        self.tmpnum += 1
                    if self.scoreappear>1:
                        screen.blit(self.scoresign,(65, 256))
                        screen.blit(self.daysign,self.daypos[0])
                        screen.blit(self.daynumbers[self.level],self.daypos[1])
                    for j in range(0, i):
                        screen.blit(self.texts[j],
                                    (self.scoreOutputpos[0], self.scoreOutputpos[1] + self.scoreOutputHeight * j))
                    if self.scoreappear==4:
                        if self.clear == False:  # 할당점수에 못미침
                            screen.blit(self.failAndPassTransition[0][self.fnpcount],
                                        (self.fnppos[0] + 20, self.fnppos[1] + 10))
                        elif self.clear == True:  # 할당점수를 넘김
                            screen.blit(self.failAndPassTransition[1][self.fnpcount],
                                        (-50, 170))
                        self.fnpcount += 1
                        if self.fnpcount > 26:
                            self.fnpcount = 0
        elif self.scoreappear==5:
            self.outputend = True  # 점수 갱신 애니메이션은 중단,코멘트 및 버튼 출력
            screen.blit(self.scoresign, (65, 256))
            screen.blit(self.daysign, self.daypos[0])
            screen.blit(self.daynumbers[self.level], self.daypos[1])
            screen.blit(self.texts[0], self.scoreOutputpos)
            screen.blit(self.texts[1],
                            (self.scoreOutputpos[0], self.scoreOutputpos[1] + self.scoreOutputHeight * 1))
            screen.blit(self.texts[2],
                            (self.scoreOutputpos[0], self.scoreOutputpos[1] + self.scoreOutputHeight * 2))
            screen.blit(self.texts[3],
                            (self.scoreOutputpos[0], self.scoreOutputpos[1] + self.scoreOutputHeight * 3))
            if self.clear==False:  # 할당점수에 못미침
                screen.blit(self.failAndPass[0][self.fnpcount],
                            (self.fnppos[0]+20,self.fnppos[1]+10))
                    #  0버튼 반투명 출력
                self.button[0][0].update()
            elif self.clear==True:  # 할당점수를 넘김
                screen.blit(self.failAndPass[1][self.fnpcount],
                                self.fnppos)
                    # 0버튼 정상 출력
                self.button[0][1].update()
            self.fnpcount+=1
            if self.fnpcount>29:
                self.fnpcount=0
            self.button[1].update()
            self.button[2].update()

            for i in range(0,len(self.comment[self.commentary])):
                screen.blit(self.comment[self.commentary][i],(self.commentpos[0],self.commentpos[1]+i*20))


        if self.timer%15==0:
            self.tmpnum=0
            if self.timer<90:
                if self.timer<=60:
                    resultScoreSound.play()
                elif self.timer>60:
                    resultTotalScoreSound.play()
                self.scoreappear+=1
                self.fnpcount=0

            for i in range(0,len(self.texts)-1):
                if i < self.scoreappear:
                    if (i==2)==False:
                        self.texts[i] = self.scorefont.render((str)(self.score[i]), True, (243,214,246))
                    elif i==2:
                        self.texts[i] = self.scorefont.render((str)(self.score[i]), True, (255,42,140))
                    elif i==3:
                        self.texts[i] = self.scorefont.render((str)(self.score[i]), True, (255,238,32))

            #버튼 2,3출력
            #mouseOn,click이벤트에 따라 색상다르게 나타낼것

            # (만일 버튼 or 다른곳을 한번 누른다면 빠르게 점수갱신 애니메이션 스킵하게 할 수 있을까)
            # 다음날로or다시하기or메인으로 중 하나의 버튼을 누르면 이 객체는 사라진다.(del 이용)

