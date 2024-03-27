import discord
from discord.ext import commands
# import main
import ragMain
import secret
 
TOKEN = secret.TOKEN
CHANNEL_ID = secret.CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠에 대한 접근 활성화
intents.messages = True  # 메시지 읽기 권한 활성화

bot = commands.Bot(command_prefix='*', intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:  # 채널이 존재하는지 확인
        await channel.send('안녕하세요.\n **🤖임시 개장 신촌 정보 GPT 🤖** 입니다.\n"알려줘"를 메세지에 포함시켜서 icpc 신촌 정보 검색 부탁드립니다!')


# 테스트
@bot.command()
async def TODO(ctx):
    await ctx.send('- 신촌 관련 문서 학습시키기(RAG) ✅  \n- 카카오톡 api 연결하기\n- 서버 올리기')

@bot.event
async def on_message(message):
    # 봇 자신이 보낸 메시지는 무시
    if message.author == bot.user:
        return

    # 사용자가 보낸 메시지 내용 출력
    # print(f'Message from {message.author}: {message.content}')
    #server_nickname = message.author.nick if message.author.nick else message.author.name
    
    # 간단한 응답 보내기
    if ('알려줘') in message.content:
        #print(server_nickname) #
        AImessage = ragMain.invoke_chain(message.content) # 질문 gpt 전송
        await message.channel.send(AImessage)

    # 이 코드는 커스텀 커맨드도 정상적으로 작동하게 함
    await bot.process_commands(message)

bot.run(TOKEN)
