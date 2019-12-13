import pygame
import random
from game import screen,sequenceIntialization

# 손님 옆의 레시피
class Recipe: #손님객체를 따라다니며 각자 다른 레시피를 랜덤으로 갖게되어야함
    def __init__(self,ingMaxSize): #ingMaxSize : 가질 수 있는 재료의 최대 수 (레벨링 시 구분됨)
        self.ingMaxSize = ingMaxSize
        self.inglist=[] #재료 넘버링
        self.shotcount=0

        self.INGHEIGHT=10
        self.recipeContainer = pygame.image.load("resource/image/recipe/recipeContainer.png")
        self.testcont = pygame.image.load("resource/image/recipe/tesetcont.png")
        self.recipeing=[]
        self.recipeing=sequenceIntialization(self.recipeing,12,"resource/image/recipe/",2)
        self.transparentrecipeing = []
        self.transparentrecipeing=sequenceIntialization(self.transparentrecipeing,12,"resource/image/recipe/transparent/",2)
        self.makeRecipe()
    def ishit(self,ingtype):
        if self.shotcount<len(self.inglist):
            if self.inglist[self.shotcount]==ingtype-1:
                print("맞음")
                self.shotcount+=1
                return True
            else :
                print("틀렸다")
                return False
        else:
            return True
    def isClear(self):
        if len(self.inglist)==self.shotcount:

            return True
        else:
            return False
    def decideIng(self):
        tmp = random.randint(1, 11)
        while tmp == 5:
            tmp = random.randint(1, 11)
        return tmp
    def makeRecipe(self):
        if(self.ingMaxSize>=4):
            # 가장 하단 빵, 상단 빵을 제외한 나머지 재료를 최대 가질 수 있는 재료수에 맞게 레시피에 넘버링
            #i = random.randint(0,1)
            self.inglist.append(0) #하단빵
            tmp = self.decideIng()
            self.inglist.append(tmp)
            tmp = self.decideIng()
            self.inglist.append(tmp)
            print(self.inglist) # 재료 확인 터미널출력
            self.inglist.append(5) #상단빵
        return 0
    def update(self,client):
        #screen.blit(self.recipeContainer,(client.pos[0]-89,client.pos[1]+client.standardY-((self.ingMaxSize-1)*self.INGHEIGHT)-3))
        screen.blit(self.testcont,
                    (client.pos[0] - 89, client.pos[1] + client.standardY - ((self.ingMaxSize - 1) * self.INGHEIGHT)-5))
        for j in range(0, len(self.inglist)):
            if j < self.shotcount :
                screen.blit(self.recipeing[self.inglist[j]],(client.pos[0] - 80, client.pos[1] + client.standardY - (j * self.INGHEIGHT)))
            else :
                screen.blit(self.transparentrecipeing[self.inglist[j]],(client.pos[0] - 80, client.pos[1] + client.standardY - (j * self.INGHEIGHT)))