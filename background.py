from game import sequenceIntialization,screen,WINDOWWIDTH,WINDOWHEIGHT,INGREDIENTSWIDTH,INGREDIENTSHEIGHT
import pygame

#배경 클래스(인게임 내 배경갱신)
class Background():

    def __init__(self):
        # 배경
        self.background = []

        self.backgroundCount = 0

        self.foodGround = pygame.image.load("resource/image/background/foodGround.png")
        self.backgroundCount=0

        self.SIDEPANELSIZE=21
        self.sidepanel = pygame.image.load("resource/image/ui/sidepanel.png")
        """
        self.ingredients = [pygame.image.load("resource/image/ingredients/ing_01.png"), \
                       pygame.image.load("resource/image/ingredients/ing_02.png"), \
                       pygame.image.load("resource/image/ingredients/ing_03.png"), \
                       pygame.image.load("resource/image/ingredients/ing_04.png"), \
                       pygame.image.load("resource/image/ingredients/ing_05.png"), \
                       pygame.image.load("resource/image/ingredients/ing_06.png")]  # 식재이미지
        
        
        """
        self.ingredients = []
        self.ingredients = sequenceIntialization(self.ingredients,8,"resource/image/ingredients/ingTrans/",3)
        self.ingredientsTrnasCount=0
        self.ingredientsOutputPos=[0,WINDOWHEIGHT-INGREDIENTSHEIGHT-8]
        self.ingredientsPos = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for i in range(0, len(self.ingredientsPos)):
            self.ingredientsPos[i] = [INGREDIENTSWIDTH * i, WINDOWHEIGHT - INGREDIENTSHEIGHT]


    def updatefrontofClientLayer(self,ingNum):
        # 손님 앞 레이어구조물 출력
        screen.blit(self.sidepanel, (0, 0))
        screen.blit(self.sidepanel, (WINDOWWIDTH - self.SIDEPANELSIZE, 0))
        screen.blit(self.foodGround, (0, WINDOWHEIGHT - 186))
        if ingNum==0 :
            if self.ingredientsTrnasCount==0:
                screen.blit(self.ingredients[0],self.ingredientsOutputPos)
            else:
                if self.ingredientsTrnasCount!=0:
                    self.ingredientsTrnasCount-=1
                    screen.blit(self.ingredients[self.ingredientsTrnasCount],self.ingredientsOutputPos)
        elif ingNum==1:
            if self.ingredientsTrnasCount==7:
                screen.blit(self.ingredients[7],self.ingredientsOutputPos)
            else:
                if self.ingredientsTrnasCount!=7:
                    self.ingredientsTrnasCount+=1
                    screen.blit(self.ingredients[self.ingredientsTrnasCount],self.ingredientsOutputPos)

    def setbackground(self,directory):
        while len(self.background)>0 : self.background.pop()
        self.background = sequenceIntialization(self.background, 60, "resource/image/background/"+directory, 3)

    def backgroundLayerupdate(self,gamescene):
        self.backgroundCount+=1
        if self.backgroundCount>=59:
            self.backgroundCount=0
        if gamescene==0:
            screen.blit(self.background[self.backgroundCount], (0, 0))
        elif gamescene==1:
            screen.blit(self.background[self.backgroundCount],(0,20))
        elif gamescene==2:
            screen.blit(self.background[self.backgroundCount], (0, 0))