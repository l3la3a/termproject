
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN,KEYUP,K_SPACE,K_TAB
import random


pygame.init()
WINDOWWIDTH = 702
WINDOWHEIGHT = 600
INGREDIENTSWIDTH = 117
INGREDIENTSHEIGHT = 160

screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption(" S S B S ")
pygame.display.set_icon(pygame.image.load("resource/image/icon.png"))
fpsClock = pygame.time.Clock()

ground = [[WINDOWHEIGHT-99,WINDOWHEIGHT-125]]#roomnubmer / top,bottom

def sequenceIntialization(spritelist,sequencesize,directory,flag): #시퀀스 초기화 (시퀀스 담을 리스트, 시퀀스 총 수,경로,자릿수)
    for i in range(0,sequencesize):
       spritelist.append(pygame.image.load(directory+ str(i).zfill(flag)+".png"))
    return spritelist


from transition import *
from player import *
from ui import *
from background import *
from clientmanager import *
from gamestate import *
from scoreboard import *
from characterSelect import *
from story import *
from soundmanager import *

def titlebuttonset(titlebutton):
    titlebutton[0].image_mouseOn = sequenceIntialization(titlebutton[0].image_mouseOn, 30,
                                                         "resource/image/button/mt_button0mouseOn/", 3)
    titlebutton[1].image_mouseOn = sequenceIntialization(titlebutton[1].image_mouseOn, 30,
                                                     "resource/image/button/mt_button1mouseOn/", 3)

def ready(time,waittingtime): # 트랜지션에 사용됨.
    if time>waittingtime:
        return True
    else :
        return False


def main():

    ingState=0 #탭키로 식재 구역번호구분
    ingtype=0 #식재별 구분

    #객체 생성
    ui= 0
    player = Player(0,72,99,12,1)  #플레이어 타입, 너비,높이,스피드,최대 가질 수 있는 재료 수
    titlebutton = [Button(453,313,230,60,"mt_button0.png"),Button(453,373,230,60,"mt_button1.png")] #시작,끝내기버튼
    titlebuttonset(titlebutton)
    background = Background()
    clientmanager = ClientManager()
    characterselect = 0
    intro = 0
    outtro = 0
    #result = Scoreboard(0,0,0,0)

    ing_take=[pygame.image.load("resource/image/ingredients/single/01.png"),\
              pygame.image.load("resource/image/ingredients/single/02.png"),\
              pygame.image.load("resource/image/ingredients/single/03.png"),\
              pygame.image.load("resource/image/ingredients/single/04.png"),\
              pygame.image.load("resource/image/ingredients/single/05.png"),\
              pygame.image.load("resource/image/ingredients/single/06.png"),\
              pygame.image.load("resource/image/ingredients/single/07.png"),\
              pygame.image.load("resource/image/ingredients/single/08.png"),\
              pygame.image.load("resource/image/ingredients/single/09.png"),\
              pygame.image.load("resource/image/ingredients/single/10.png"),\
              pygame.image.load("resource/image/ingredients/single/11.png"),\
              pygame.image.load("resource/image/ingredients/single/12.png")]

    mousepos=[0,0]
    game = GameState()
    transition = Transition()
    game.gamestate=False
    game.gamescene=0
    if game.gamescene==0:
        background.setbackground("maintitle/")
    elif game.gamescene==1:
        background.setbackground("playing/")
    elif game.gamescene==2:
        background.setbackground("scoreoutput/")
    result = Scoreboard(0,0,0,0)
    play=False

    while True:
        """게임 메인루프"""
        # 게임씬 0 : 메인타이틀/캐릭터 선택화면/인트로+게임설명
        if game.gamescene == 0 :
            # event handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                mousepos = pygame.mouse.get_pos()
                if game.subgamescene==0:
                    if titlebutton[0].isMouseOn(mousepos)==True:

                        titlebutton[0].mouseOn=True
                        titlebutton[1].mouseOn=False
                    elif titlebutton[1].isMouseOn(mousepos)==True:

                        titlebutton[0].mouseOn = False
                        titlebutton[1].mouseOn = True
                    elif titlebutton[0].isMouseOn(mousepos)==False and \
                        titlebutton[1].isMouseOn(mousepos)==False :
                        titlebutton[0].mouseOn = False
                        titlebutton[1].mouseOn=False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if titlebutton[0].mouseOn==True:
                            # 버튼 선택효과음
                            buttonSelectSound.play()
                            musicStop()
                            play = False
                            print("캐릭터 선택 창 진입")
                            game.subgamescene=1
                            characterselect = CharacterSelect()
                            characterselect.sequenceinit()
                        elif titlebutton[1].mouseOn==True:
                            # 버튼 선택효과음
                            buttonSelectSound.play()
                            musicStop()
                            play = False
                            print("게임 종료")
                            pygame.quit()
                            sys.exit()
                elif game.subgamescene==1:
                    characterselect.isMouseOn(mousepos)
                    for i in range(0,2):
                        characterselect.introbutton[i].isMouseOn(mousepos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if characterselect.isCheckboxSelected==False:
                            if characterselect.cButtonMouseOn==1:
                                characterselect.cButtonCount=0
                                characterselect.cButtonSelected=1
                                # 캐릭터 선택효과음
                                characterSelectSound.play()
                            elif characterselect.cButtonMouseOn==2:
                                characterselect.cButtonCount=0
                                characterselect.cButtonSelected=2
                                # 캐릭터 선택효과음
                                characterSelectSound.play()
                        if characterselect.cButtonSelected!=0 and characterselect.isCheckboxMouseOn==True:
                            if characterselect.isCheckboxSelected==False:
                                # 체크 효과음
                                checkboxSelectSound.play()
                                characterselect.isCheckboxSelected=True
                                from datetime import datetime
                                tmptext="{}월 {}일 {}시 {}분 {}초, 캐릭터 선택을 확정했습니다.".format(datetime.now().month,datetime.now().day,datetime.now().hour,datetime.now().minute,datetime.now().second)
                                characterselect.checkboxConfirmtext= tmptext
                                print(characterselect.checkboxConfirmtext)
                                characterselect.introbutton[0].isActivated = True
                                characterselect.introbutton[1].isActivated = True
                                characterselect.checkboxConfirmtextrender = characterselect.cfont.render(characterselect.checkboxConfirmtext, True,
                                                                                   (255, 210, 37))
                            elif characterselect.isCheckboxSelected==True:
                                #체크 해제 효과음
                                checkboxDeselectSound.play()
                                characterselect.introbutton[0].isActivated = False
                                characterselect.introbutton[1].isActivated = False
                                characterselect.isCheckboxSelected=False
                                characterselect.checkboxConfirmtext=""
                        if characterselect.introbutton[0].mouseOn==True:
                            buttonSelectSound.play()
                            musicStop()
                            play = False
                            print("인트로시작")
                            intro = Story(0)
                            intro.textOutputActivated=True

                            game.subgamescene=2
                        elif characterselect.introbutton[1].mouseOn==True:
                            buttonSelectSound.play()
                            musicStop()
                            play = False

                            print("게임시작")
                            ui = UI(5)
                            game.subgamescene=3
                elif game.subgamescene==2:
                    if intro.canButtonWatch==True:
                        for i in range(0,len(intro.buttons)):
                            intro.buttons[i].isMouseOn(mousepos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if intro.iscredit==False:
                            intro.isClick()
                            storyClickSound.play()
                        if intro.canButtonWatch==True:
                            if intro.buttons[0].mouseOn==True:
                                buttonSelectSound.play()
                                intro.reset()
                                print("인트로다시보기")
                                break
                            elif intro.buttons[1].mouseOn==True:
                                buttonSelectSound.play()
                                game.subgamescene=3
                                ui = UI(5)
                                print("인트로를 통한 게임시작")
                                musicStop()
                                play = False

                            elif intro.buttons[2].mouseOn==True:
                                buttonSelectSound.play()
                                print("크레딧보기")
                                musicStop()
                                play = False

                                intro.iscredit=True
                    if intro.iscredit==True:
                        if event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                print("누르고있음")
                                intro.ScrollSpeedUp = True
                        if event.type == KEYUP:
                            if event.key == K_SPACE:
                                intro.ScrollSpeedUp = False
            if game.subgamescene==3 and transition.transitionEnd == False:
                transition.transitionUpdateFront()
            elif game.subgamescene==3 and transition.transitionEnd == True:
                print("트랜지션true")
                game.gamescene = 1
                intro = 0
                background.setbackground("playing/")
                player = Player(characterselect.cButtonSelected-1, 72, 99, 12, 1)
                ui.character=characterselect.cButtonSelected-1
                del characterselect
                game.gamestate=True
                game.mainstate=False
                transition.reset()

            # backgrounddraw
            if game.subgamescene==0:
                if play==False:
                    musicPlay("MainTheme")
                    play=True
                background.backgroundLayerupdate(0)
                for i in range(0, len(titlebutton)):
                    titlebutton[i].update()
            elif game.subgamescene==1:
                if play==False:
                    musicPlay("characterselect")
                    play=True
                characterselect.update()
            elif game.subgamescene==2:
                screen.fill((0,0,0))
                intro.updateStoryScene()
                if intro.iscredit==True:
                    if play==False:
                        musicPlay("credit")
                        play=True
                else:
                    if play == False:
                        musicPlay("intro")
                        play = True
                if intro.iscreditEnd==True:
                    musicStop()
                    play=False
                    game.subgamescene=0
                    intro=0
            pygame.display.update()
            fpsClock.tick(30)

        #게임씬 1 (게임 진행 씬)
        elif game.gamescene==1:
            for event in pygame.event.get(): #event handler
                if event.type == QUIT:
                    print("exit to button")
                    pygame.quit()
                    sys.exit()
                if game.gamestate==True:
                    if player.takestate!=0 and event.type == pygame.MOUSEBUTTONDOWN: #식재료 던지기
                        mousepos=pygame.mouse.get_pos()
                        player.isClicking = True
                    if player.takestate!=0 and event.type == pygame.MOUSEBUTTONUP:
                        mousepos = pygame.mouse.get_pos()
                        player.isClicking = False
                        player.isThrowing = True
                        allmiss = False
                        for i in range(0,len(clientmanager.client)): #마우스 히트 범위판정
                            if clientmanager.client[i].mouseDetect(mousepos):
                                allmiss=True
                                if  clientmanager.recipelst[i].ishit(player.takestate):
                                    shootSound.play()
                                    clientmanager.client[i].isHitting=True
                                    if clientmanager.recipelst[i].isClear():
                                        clientmanager.client[i].isClear=True
                                        ui.score += 1
                                else :
                                    clientmanager.client[i].isMissing=True
                                    ui.miss+=1
                                    missingSound.play()
                        if allmiss==False:
                            missingSound.play()
                            #print("{}번째 클라이언트 상태 : {}".format(i,client[i].isHitting))

                if event.type == KEYDOWN:
                    player.isMoving=True
                    if event.key == K_TAB:
                        openAndCloseSound.play()
                        if player.ingNum==0:
                            print("식재 넘버 변경")
                            player.ingNum=1
                        elif player.ingNum==1:
                            print("식재 넘버 변경")
                            player.ingNum=0
                    if event.key == ord('a'):
                        player.stopR = False
                        player.moveRight = False
                        player.moveLeft = True
                    elif event.key == ord('d'):
                        player.moveRight = True
                        player.stopL = False
                        player.moveLeft = False
                    if event.key == K_SPACE:
                        if player.takestate==0:
                            player.isTaking = True
                            player.setTakenfood(ingtype)
                            takeSound.play()
                        else:
                            print("재료 소지중 : ",player.takestate)
                if event.type == KEYUP:
                    if event.key == ord('a') :
                        player.moveLeft = False
                        player.stopL = True
                    elif event.key == ord('d'):
                        player.moveRight = False
                        player.stopR = True
                    if player.stopL == False and player.stopR == False:
                        player.isMoving=False
                    player.walkcount =0
            # bacground music play
            if play == False:
                rsgSound.play()
                musicPlay("playing")
                play = True
            # backgrounddraw
            background.backgroundLayerupdate(1)
            clientmanager.clientoutput(ui)
            background.updatefrontofClientLayer(player.ingNum)

            ingtype = player.foodtype(background) #플레이어 위치 별 식재종류값
            player.update(mousepos,ing_take,ingtype)  # 캐릭터 업데이트
            ui.update(ui.score) #UI 업데이트

            if ui.timeout==2: #시간 끝났을때의 처리
                if clientmanager.gameout==False:
                    timesupSound.play()
                    clientmanager.sceneend()
                    transition.transitionEnd=False
                    transition.sequencenum=0
                    clientmanager.gameout=True

                game.tmptime+=1
                if game.tmptime>90:
                    if transition.transitionEnd==False:
                        transition.transitionUpdateFront()
                    elif transition.transitionEnd==True:
                        musicStop()
                        play=False

                        clientmanager.resetclient()
                        result = Scoreboard(ui.allocscore, ui.score, ui.miss, ui.day)
                        game.gamestate=False
                        background.setbackground("scoreoutput/")
                        game.gamescene=2
                        game.settimer()
                        transition.reset()
            if ui.timeout!=2 and transition.transitionEnd==False:
                transition.transitionUpdateBack()

            pygame.display.update()
            fpsClock.tick(30) #

        #게임씬 2 (스코어보드 판)
        elif game.gamescene==2: #scoreboard(game result) scene
            # backgrounddraw
            background.backgroundLayerupdate(2)
            result.update()
            if play == False:
                musicPlay("scoreboard")
                play = True
            for event in pygame.event.get():  # event handler
                if event.type == QUIT:
                    print("exit to button")
                    pygame.quit()
                    sys.exit()
                mousepos = pygame.mouse.get_pos()
                if result.button[0][1].isMouseOn(mousepos)==True:
                    result.button[0][1].mouseOn = True
                    result.button[1].mouseOn=False
                    result.button[2].mouseOn=False
                elif result.button[1].isMouseOn(mousepos)==True:
                    result.button[0][1].mouseOn = False
                    result.button[1].mouseOn=True
                    result.button[2].mouseOn=False
                elif result.button[2].isMouseOn(mousepos)==True:
                    result.button[0][1].mouseOn = False
                    result.button[1].mouseOn=False
                    result.button[2].mouseOn=True
                elif result.button[0][1].isMouseOn(mousepos)==False and \
                        result.button[1].isMouseOn(mousepos)==False and \
                        result.button[2].isMouseOn(mousepos)==False :
                    result.button[0][1].mouseOn = False
                    result.button[1].mouseOn=False
                    result.button[2].mouseOn=False
                if event.type == pygame.MOUSEBUTTONDOWN:  # 클릭
                    if result.button[0][1].mouseOn==True:
                        buttonSelectSound.play()
                        #버튼 비활성화
                        result.button[0][1].isActivated=False
                        result.button[1].isActivated=False
                        result.button[2].isActivated=False

                        # 레벨증가 / ui 리셋
                        ui.day+=1
                        ui.reset()
                        if ui.day>=3:
                            musicStop()
                            play=False
                            game.gamescene=3
                            outtro=Story(1)
                            game.subgamescene = 0
                            background.setbackground("maintitle/")
                            intro = 0
                            break
                        else:
                            game.gamestate = True
                            transition.reset()
                            game.tmptime = 0
                    elif result.button[1].mouseOn==True:
                        buttonSelectSound.play()
                        # 버튼 비활성화
                        result.button[0][1].isActivated = False
                        result.button[1].isActivated = False
                        result.button[2].isActivated = False

                        #ui리셋
                        ui.reset()
                        transition.reset()
                        game.gamestate=True
                        game.tmptime=0
                    elif result.button[2].mouseOn==True:
                        buttonSelectSound.play()
                        # 버튼 비활성화
                        result.button[0][1].isActivated = False
                        result.button[1].isActivated = False
                        result.button[2].isActivated = False
                        transition.reset()
                        ui.reset()

                        game.mainstate = True
                        game.gamestate=False
                        game.tmptime=0
                        print("3")
                if event.type == pygame.MOUSEBUTTONUP:
                    result.button[0][1].mouseOn=False
                    result.button[1].mosueOn=False
                    result.button[2].mouseOn=False

            if game.gamestate==True:
                game.tmptime+=1
                transition.transitionUpdateFront()
                if game.tmptime >= 30:
                    musicStop()
                    play=False
                    result.scoreboardreset()
                    background.setbackground("playing/")
                    game.gamescene = 1
                    transition.reset()
                    game.settimer()
            elif game.mainstate==True:
                game.tmptime+=1
                transition.transitionUpdateFront()
                if game.tmptime>=30:
                    musicStop()
                    play=False

                    result.scoreboardreset()
                    background.setbackground("maintitle/")
                    game.gamescene=0
                    game.subgamescene=0
                    ui.day=0
                    characterselect = CharacterSelect()
                    transition.reset()
                    game.settimer()
            if ui.timeout==2 and transition.transitionEnd==False:
                transition.transitionUpdateBack()
            pygame.display.update()
            fpsClock.tick(30)

        elif game.gamescene==3:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if outtro.iscredit==False:
                        outtro.isClick()
                        storyClickSound.play()
                        if outtro.iscredit==True:
                            musicStop()
                            play=False
                if outtro.iscredit==True:
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            print("누르고있음")
                            outtro.ScrollSpeedUp = True
                    if event.type == KEYUP:
                        if event.key == K_SPACE:
                            outtro.ScrollSpeedUp = False
            if outtro.iscredit==False:
                # bacground music play
                if play == False:
                    musicPlay("outtro")
                    play = True
                outtro.updateStoryScene()
            else:
                if play==False:
                    musicStop()
                    musicPlay("credit")
                    play=True
                outtro.creditScrollupdate()
            if outtro.iscreditEnd==True:
                musicStop()
                play=False
                game.gamescene=0
                game.subgamescene=0
                outtro=0
            pygame.display.update()
            fpsClock.tick(30)

if __name__ == '__main__':
    main()





