import discord, threading, sys, os, random
from discord.ext import commands
from datetime import datetime, timedelta
import tkinter as tk


bot_thread = None
is_bot_running = False

required_word = '감우'
optional_words = ['사랑해', '좋아해']
notgood_words =['안사랑해','안좋아해']

hogamdo_file = 'hogamdo.txt'
hogamdo = 0
birthday_month = 12
birthday_day = 2

intents = discord.Intents.default()
intents.messages = True  # 메시지 관련 이벤트를 수신
intents.message_content = True  # 메시지 내용을 수신
client = commands.Bot(command_prefix='!', intents=intents)
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def load_hogamdo():
    global hogamdo  # 전역 변수 hogamdo를 사용하도록 지정
    if os.path.exists(hogamdo_file):  # 'hogamdo'라는 이름의 텍스트 파일이 이미 존재한다면
        with open(hogamdo_file, 'r', encoding='utf-8') as file:
            try:
                hogamdo = int(file.read().strip())
            except ValueError:
                hogamdo = 0
    else:  # hogamdo.txt라는 이름의 텍스트 파일이 없다면
        with open(hogamdo_file, 'w', encoding='utf-8') as file:  # hogamdo.txt 파일을 새로 생성
            file.write('0')  # 초기 호감도 0으로 파일 생성

# 호감도 수치를 파일에 저장
def save_hogamdo():
    global hogamdo  # 전역 변수 hogamdo를 사용하도록 지정
    with open(hogamdo_file, 'w', encoding='utf-8') as file:
        file.write(str(hogamdo))

def days_until_birthday():
    today = datetime.now()
    current_year = today.year

    # 올해의 생일 날짜
    birthday = datetime(current_year, birthday_month, birthday_day)

    # 생일이 지났으면 내년 생일을 기준으로 계산
    if birthday < today:
        birthday = datetime(current_year + 1, birthday_month, birthday_day)

    # 생일까지 남은 날짜 계산
    days_left = (birthday - today).days
    return days_left

async def image(message, file_name):
    file_path = os.path.join(CURRENT_FOLDER, file_name)

    # 파일이 존재하는지 확인
    if os.path.isfile(file_path):
        # 파일이 있으면 업로드
        await message.channel.send(file=discord.File(file_path))
    else:
        # 파일이 없을 경우 오류 메시지
        await message.channel.send(f"'{file_name}' 파일을 찾을 수 없습니다.")

@client.event
async def on_ready():
    load_hogamdo()  # 봇이 실행되면 호감도 파일을 불러옴
    print(f'We have logged in as {client.user}')
    print(f'현재 호감도: {hogamdo}')

    # 봇의 다른 이벤트 및 명령어 정의
    # 예를 들어:
@client.event
async def on_message(message):

    if message.author == client.user:
        return  

    sheberid = 852054830402633729
    ifiid = 671296987458437120
    if message.content in ['감우야', '감우']:
        await message.channel.send(random.choice(['도움이 필요하신지...', '네, 여행자님.', '부르셨나요?']))
    if message.content == '감우야!':
        await message.channel.send("네! 여행자님!")
    if message.content == '수고했어':
        await message.channel.send("고맙습니다, 여행자님.")
    if message.content == '야자염소':
        await message.channel.send('자꾸 그러시면 곤란하다고요.')
    if message.content == '와 보소':
        await image(message,'gamuhate.jpg')
        await message.channel.send('저한테 하신 말씀 아니죠?')
    if message.content == '오랜만':
        await message.channel.send('오랜만에 뵙네요. 그동안 잘 지내셨죠?')
    if message.content == '잘자' and message.author.id == sheberid:
        await message.channel.send('좋은 꿈 꾸세요.')
        await client.close()
    if message.content == '잘자' and message.author.id == ifiid:
        await message.channel.send('좋은 꿈 꾸세요.')
        await client.close()
    if message.content == '바빠?':
        await message.channel.send(random.choice(['아뇨, 지금은 한가해요.', '지금은 휴식시간이에요.', '지금은 할 일이 없군요.']))
    if message.content == '저거 누구야':
        await message.channel.send(random.choice(['치치인 것 같은데요?', '굉장히 듬직해 보이는 분이 계세요.', '굉장히 아름다운 분이 계세요.']))
    if message.content == '뭐가 문제지':
        await message.channel.send(random.choice(['그러게요...', '잘 모르겠어요.']))

    if message.content.startswith('!사전'):
        await message.channel.send('잠시만요...')
        name = message.content[3:].strip()  # '!사전'의 길이는 3이므로 그 뒤의 내용을 가져옵니다.

    # 파일 경로를 찾기 위해 전체 디렉토리를 순회합니다.
        found = False
        for root, dirs, files in os.walk(os.path.expanduser("~")):  # 사용자 홈 디렉토리부터 시작
            if f'{name}.txt' in files:
                file_path = os.path.join(root, f'{name}.txt')
                found = True
                break

        if found:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()  # 파일 내용을 읽어옵니다.
            await message.channel.send(f"**{name}의 정보:**\n{content}")  # 읽어온 내용을 전송합니다.
        else:
            await message.channel.send(f"'{name}'에 대한 정보를 찾을 수 없습니다.")  # 파일이 없을 경우 메시지 전송
            
    global hogamdo
    
    # 필수 단어가 메시지에 포함되어 있는지 확인
    if required_word in message.content:
        # 선택 단어 중 하나라도 포함되어 있는지 확인
        if any(word in message.content for word in notgood_words):
            hogamdo -= 1  
            save_hogamdo()
            await message.channel.send(random.choice(['저와 같은 생각을 하고 계셨을줄은 미처 몰랐군요.','그, 그렇게 말씀하시면 아무리 저라도 조금 서운해질 것 같아요...']))
        elif any(word in message.content for word in optional_words):
            hogamdo_add = random.randint(3, 15)  # 호감도 증가량 3~15
            hogamdo += hogamdo_add  # 호감도 증가
            save_hogamdo()
            if hogamdo < 50:  # 호감도가 50 이하일때
                await message.channel.send(random.choice(['옛날 리월 사람들도 그렇게 말하곤 했어요.', '말씀은 감사해요, 여행자님. 하지만 전... 역시 부담스러워요.']) + f'\n현재호감도: {hogamdo}')  # 호감도가 낮을때의 답장들
            elif hogamdo >= 50 and hogamdo < 200:  # 호감도가 50이상 200 이하일때
                await message.channel.send(random.choice(['으읏, 그런 말은 조금 낯간지러운걸요.', '네?  ㅈ-제가 사랑스럽다구요? 전 볼폼없는 선인일 뿐인걸요.']) + f'\n현재호감도: {hogamdo}')  # 호감도가 중간일때의 답장들
            elif hogamdo >= 200:  # 호감도가 200 이상일때
                await message.channel.send(random.choice(['저도 여행자님이 제일 좋아요. 그러니 계속 함께 있어주실거죠?', '저도 어엿한 여행자님을 사랑해요. 그것도, 아주 많이요.']) + f'\n현재호감도: {hogamdo}')  # 호감도가 높을때의 답장들


        if found:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()  # 파일 내용을 읽어옵니다.
            await message.channel.send(file=discord.File(content))
            await message.channel.send(f"**{name}의 정보:**\n{content}")  # 읽어온 내용을 전송합니다.
        else:
            await message.channel.send(f"'{name}'에 대한 정보를 찾을 수 없습니다.")  # 파일이 없을 경우 메시지 전송
    
    if '감우 생일' in message.content:
        days_left = days_until_birthday()
        if days_left > 200:
            await message.channel.send(f'제 생일요..? 아직 {days_left}일이나 남았어요')
        elif days_left > 100:
            await message.channel.send(f'제 생일 말이에요? 아직 {days_left}일 남았어요')
        elif days_left > 50:
            await message.channel.send(f'제 생일요? 어느새 {days_left}일 밖에 안남았네요')
        elif days_left > 10:
            await message.channel.send(f'제 생일요? 이제 {days_left}일 만 더있으면 제 생일이에요!')
        elif days_left == 1:
            await message.channel.send(f'내일이 바로 제 생일이에요!')
        elif days_left == 0 and '축하' in message.content:
            user = message.author.display_name
            await message.channel.send(f'정말 고마워요 {user}님!')
        elif days_left ==0:
            await message.channel.send('오늘이 바로 제 생일이에요!')

client.run('MTI4OTU4NjQyMzg2Njg1NTUwNg.GJc17z.2nuGqIVcnncAYUymdtgRLiEWgisf79e5k79L9g')
#client.run('MTI4OTU4NjQyMzg2Njg1NTUwNg.GJc17z.2nuGqIVcnncAYUymdtgRLiEWgisf79e5k79L9g') 
