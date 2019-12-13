
class GameState:
    def __init__(self):
        self.gamescene = 0  # 0 : 메인화면, 1 : 인게임, 2 : pause, 3 : 엔딩
        self.subgamescene=0
        # 메인화면에서 사용하는 서브게임씬. 0 : 타이틀, 1 : 캐릭터 선택, 2 : 인트로&게임설명 화면 3 : 인트로 종료
        self.gamelevel = 0
        self.mainstate = True
        self.gamestate = True
        self.timeout= False
        self.tmptime=0


    def settimer(self):
        self.tmptime=0
