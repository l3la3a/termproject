from game import screen
import pygame
from soundmanager import buttonSelectSound,buttonMouseOnSound
"""
클릭 가능하고 마우스오버시 인터랙션이 있는 버튼 클래스
생성 시 기본적으로 좌표와 너비높이, 버튼의 idle이미지 이름(png까지포함)을 파라미터로 줘야함
또한 버튼 사용시 image_mouseOn 리스트에 버튼 마우스오버 시퀀스들 모두 담아 사용할것 (미리 초기화 안할 시 에러남)

객체 생성 후, 사용시 
이벤트 핸들러의 mousepos 감지부에 isMouseOn()을 작성,
click 이벤트에 다음과 같이 작성하면 버튼의 역할 끝
if button객체명.mouseOn==True:
    (마우스 클릭 이후의 이벤트적기)
"""

class Button():
    def __init__(self,posx,posy,width,height,imgName):
        self.isActivated=True #버튼 클릭 가능/불가능상태 구분 (트랜지션상태에서는 반드시 불가능해야함)
        self.pos=[0,0]
        self.pos[0] = posx
        self.pos[1] = posy
        self.width=width
        self.height = height
        self.image_idle = pygame.image.load("resource/image/button/"+imgName)
        self.image_mouseOn=[] #버튼 사용시 이 리스트 반드시 채워서 사용할 것
        self.mouseOn=False
        self.anicount=0
        self.btSound=False

    def reset(self):
        self.anicount=0

    def isMouseOn(self,mousepos):
        if self.isActivated==True:
            if self.pos[0] < mousepos[0] < self.pos[0]+self.width:
                if self.pos[1] < mousepos[1] < self.pos[1]+self.height:
                    self.mouseOn=True
                    if self.btSound == False:
                        buttonMouseOnSound.play()
                        self.btSound = True
                    return True
                else:
                    self.btSound=False
                    self.mouseOn=False
                    return False
            else:
                self.btSound=False
                self.mouseOn=False
                return False
        else :
            self.btSound=False
            return False

    def update(self):
        if self.mouseOn:
            screen.blit(self.image_mouseOn[self.anicount],self.pos)
            self.anicount+=1
            if self.anicount>=len(self.image_mouseOn):
                self.anicount=0
        elif not self.mouseOn:
            screen.blit(self.image_idle, self.pos)
        else:
            screen.blit(self.image_idle, self.pos)
