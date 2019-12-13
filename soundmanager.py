import pygame

"""
배경음악 관리 파일
배경음악 파일의 이름과 직결되므로 플레이가 필요한 구간에서
8줄부터 기재된 영어 문자열을 themeName파라미터로 줄것

> MainTheme #메인테마
> characterselect #캐릭터선택음악
> intro #인트로음악
> bam #인게임 플레이 음악
> scoreboard #결과판 음악
> outtro #아웃트로 음악

그외 선언된 음악은 효과음으로 , Sound를 뒤에 붙인 변수로 사용할것
사운드의 원본을 바꿔야할 경우 변수 이름 변경 없이 이 파일의 파일이름만 변경하면 됨
"""
play = False
rsgplay=False
timesupplay=False

takeSound = pygame.mixer.Sound("resource/sound/taking.wav")
shootSound =pygame.mixer.Sound("resource/sound/shoot.wav")
missingSound = pygame.mixer.Sound("resource/sound/missing.wav")

#식판 여닫는소리
openAndCloseSound = pygame.mixer.Sound("resource/sound/openNclose.wav")
#버튼클래스에 포함시켜 쓸 것
buttonSelectSound=pygame.mixer.Sound("resource/sound/buttonSelect.wav")
buttonMouseOnSound=pygame.mixer.Sound("resource/sound/pop.wav")

characterSelectSound = pygame.mixer.Sound("resource/sound/cSelect.wav")

checkboxSelectSound=pygame.mixer.Sound("resource/sound/okay.wav")
checkboxDeselectSound=pygame.mixer.Sound("resource/sound/cd.wav")
storyClickSound=pygame.mixer.Sound("resource/sound/er.wav")

rsgSound=pygame.mixer.Sound("resource/sound/rsgSound.wav")
timesupSound=pygame.mixer.Sound("resource/sound/timesup.wav")

#스코어보드 클래스에 포함시켜 쓸 것
resultScoreSound=pygame.mixer.Sound("resource/sound/score.wav")
resultTotalScoreSound=pygame.mixer.Sound("resource/sound/score2.wav")

def musicPlay(themeName):
    theme = pygame.mixer.music.load('resource/sound/'+themeName+'.mp3')
    pygame.mixer.music.play(-1)

def musicStop():
    pygame.mixer.music.stop()
