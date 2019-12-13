from game import sequenceIntialization, screen

class Transition:
    def __init__(self):
        self.time = 0
        self.transitionSequence=[]
        self.UItextSequence=[] # 대기중 텍스트 넣는곳
        self.transitionSequence=sequenceIntialization(self.transitionSequence,60,"resource/image/transition/",3)
        self.sequencenum=0
        self.transitionStart=False # 이 변수로 트랜지션여부 판단
        self.transitionEnd = False

    def reset(self):
        self.time = 0
        self.sequencenum = 0
        self.transitionStart = False
        self.transitionEnd = False
        screen.blit(self.transitionSequence[29], (0, 0))
        print("리셋")

    def transitionUpdateFront(self):
        if self.sequencenum<29:
            screen.blit(self.transitionSequence[self.sequencenum],(0,0)) #대기중 텍스트도 출력되어야함
        if self.transitionEnd==False:
            self.sequencenum+=1
            if self.sequencenum>=30:
                screen.blit(self.transitionSequence[29], (0, 0))  # 대기중 텍스트도 출력되어야함
                self.transitionEnd=True

    def transitionUpdateBack(self):
        if self.sequencenum<29:
            screen.blit(self.transitionSequence[self.sequencenum+30],(0,0)) #대기중 텍스트도 출력되어야함
        elif self.sequencenum>=30:
            self.transitionEnd=True
        if self.transitionEnd==False:
            self.sequencenum+=1
