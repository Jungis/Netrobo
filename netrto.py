import discord
import asyncio
import random
import openpyxl
from discord import Member
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime

countG = 0
client = discord.Client()
players = {}
queues= {}
musiclist=[]
mCount=1
searchYoutube={}
searchYoutubeHref={}

def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()

@client.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("------------------")
    await client.change_presence(game=discord.Game(name='넷상의 광장 | !명령어', type=1))



@client.event
async def on_message(message):

   

    if message.content.startswith("!명령어"):
        channel = message.channel
        embed = discord.Embed(
            title = '명령어',
            description = '현재 사용할 수 있는 명령어입니다.',
            colour = discord.Colour.blue()
        )

        #embed.set_footer(text = '끗')
        dtime = datetime.datetime.now()
        #print(dtime[0:4]) # 년도
        #print(dtime[5:7]) #월
        #print(dtime[8:11])#일
        #print(dtime[11:13])#시
        #print(dtime[14:16])#분
        #print(dtime[17:19])#초
        embed.set_footer(text=str(dtime.year)+"년 "+str(dtime.month)+"월 "+str(dtime.day)+"일 "+str(dtime.hour)+"시 "+str(dtime.minute)+"분 "+str(dtime.second)+"초")
        #embed.set_footer(text=dtime[0:4]+"년 "+dtime[5:7]+"월 "+dtime[8:11]+"일 "+dtime[11:13]+"시 "+dtime[14:16]+"분 "+dtime[17:19]+"초")
        embed.add_field(name='!모두모여', value='모두를 언급함', inline=False)
        embed.add_field(name='!노래', value='봇이 음성채널에 들어옴', inline=False)
        embed.add_field(name='!끄기', value='봇이 음성채널에 나감', inline=False)
        embed.add_field(name='!재생', value='!재생 유튜브링크 형식으로 적으면 유튜브 틀어줌', inline=False)
        embed.add_field(name='!일시정지', value='재생중인 유튜브 일시정지함', inline=False)
        embed.add_field(name='!다시재생', value='정지중인 유튜브 다시 재생함', inline=False)
        embed.add_field(name='!멈춰', value='재생,정지중인 유튜브 없어짐(영상목록 초기화)', inline=False)
        embed.add_field(name='!실시간검색어, !실검', value='!실시간검색어, !실검 이라고 적으면 네이버의 실시간 검색어 순위가 나타납니다.', inline=False)
        embed.add_field(name='!복권', value='랜덤으로 선정한 복권번호를 메시지로 보내줍니다.', inline=False)
        embed.add_field(name='!검색', value='!검색 검색할키워드 형식으로 입력하시면 유튜브 검색결과를 메시지로 보내줍니다.', inline=False)

        await client.send_message(channel,embed=embed)

    if message.content.startswith("!모두모여"):
        await client.send_message(message.channel, "@everyone")

    if message.content.startswith("!접속"):
        channel = message.author.voice.voice_channel
        server = message.server
        voice_client = client.voice_client_in(server)
        print("접속")
        print(voice_client)
        print("접속")
        if voice_client== None:
            await client.send_message(message.channel, '접속했습니다.') # 호오.... 나를 부르는건가? 네녀석.. 각오는 되있겠지?
            await client.join_voice_channel(channel)
        else:
            await client.send_message(message.channel, '이미 접속되어있습니다..') # 응 이미 들어와있어 응쓰게싸




    if message.content.startswith("!끄기"):
            server = message.server
            voice_client = client.voice_client_in(server)
            print("끄기")
            print(voice_client)
            print("끄기")
            if voice_client == None:
                await client.send_message(message.channel,'봇이 음성 채널에 접속하지 않았습니다.') # 원래나가있었음 바보녀석 니녀석의 죄는 "어리석음" 이라는 .것.이.다.
                pass
            else:
                await client.send_message(message.channel, '나갑니다') # 나가드림
                await voice_client.disconnect()


    if message.content.startswith("!재생"):

        server = message.server
        voice_client = client.voice_client_in(server)
        msg1 = message.content.split(" ")
        url = msg1[1]
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        print(player.is_playing())
        players[server.id] = player
        await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
        print(player.is_playing())
        player.start()




    if message.content.startswith("!일시정지"):
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="장비를 정비합니다"))
        players[id].pause()

    if message.content.startswith("!다시재생"):
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="다시재생한다!!!!"))
        players[id].resume()

    if message.content.startswith("!멈춰"):
        id = message.server.id
        await client.send_message(message.channel, embed=discord.Embed(description="세계의 시간은 멈춰있다..."))
        players[id].stop()
        print(players[id].is_playing())

    if message.content.startswith('!예약'):
        msg1 = message.content.split(" ")
        url = msg1[1]
        server = message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
        print(player)

        if server.id in queues:
            queues[server.id].append(player)
            print('if 1 '+str(queues[server.id])) #queues배열 확인
        else:
            queues[server.id] = [player] #딕셔너리 쌍 추가
            print('else 1' + str(queues[server.id]))#queues배열 확인
        await client.send_message(message.channel,'예약 완료\n')
        musiclist.append(url) #대기목록 링크


    if message.content.startswith('!대기목록'):

        server = message.server
        msg1 = message.content.split(" ")
        mList = msg1[1]
        num = 0
        bSize = len(musiclist)

        if mList =='보기':
            embed = discord.Embed(
                title='대기중인 곡 들',
                description='대기중.....',
                colour=discord.Colour.blue()
            )
            for i in musiclist:
                print('예약리스트 : ' + i)
                embed.add_field(name='대기중인 곡', value=i, inline=False)
            await client.send_message(message.channel, embed=embed)

        if mList =='취소':
            while num<bSize:
                del musiclist[0]
                num = num+1

            del queues[server.id]
            await client.send_message(message.channel,'예약중인 음악 모두 취소 완료')

        #if message.content.startswith('!'):






        await client.send_message(message.channel,embed=embed)


    if message.content.startswith('!실시간검색어') or message.content.startswith('!실검'):
        url = "https://www.naver.com/"
        html = urllib.request.urlopen(url)

        bsObj = bs4.BeautifulSoup(html, "html.parser")
        realTimeSerach1 = bsObj.find('div', {'class': 'ah_roll_area PM_CL_realtimeKeyword_rolling'})
        realTimeSerach2 = realTimeSerach1.find('ul', {'class': 'ah_l'})
        realTimeSerach3 = realTimeSerach2.find_all('li')


        embed = discord.Embed(
            title='네이버 실시간 검색어',
            description='실시간검색어',
            colour=discord.Colour.green()
        )
        for i in range(0,20):
            realTimeSerach4 = realTimeSerach3[i]
            realTimeSerach5 = realTimeSerach4.find('span', {'class': 'ah_k'})
            realTimeSerach = realTimeSerach5.text.replace(' ', '')
            realURL = 'https://search.naver.com/search.naver?ie=utf8&query='+realTimeSerach
            print(realTimeSerach)
            embed.add_field(name=str(i+1)+'위', value='\n'+'[%s](<%s>)' % (realTimeSerach, realURL), inline=False) # [텍스트](<링크>) 형식으로 적으면 텍스트 하이퍼링크 만들어집니다




        await client.send_message(message.channel, embed=embed)

    if message.content.startswith("!복권"):
        Text = ""
        number = [1, 2, 3, 4, 5, 6, 7]
        count = 0
        for i in range(0, 7):
            num = random.randrange(1, 46)
            number[i] = num
            if count >= 1:
                for i2 in range(0, i):
                    if number[i] == number[i2]:  # 만약 현재랜덤값이 이전숫자들과 값이 같다면
                        numberText = number[i]
                        print("작동 이전값 : " + str(numberText))
                        number[i] = random.randrange(1, 46)
                        numberText = number[i]
                        print("작동 현재값 : " + str(numberText))
                        if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
                            numberText = number[i]
                            print("작동 이전값 : " + str(numberText))
                            number[i] = random.randrange(1, 46)
                            numberText = number[i]
                            print("작동 현재값 : " + str(numberText))
                            if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
                                numberText = number[i]
                                print("작동 이전값 : " + str(numberText))
                                number[i] = random.randrange(1, 46)
                                numberText = number[i]
                                print("작동 현재값 : " + str(numberText))

            count = count + 1
            Text = Text + "  " + str(number[i])

        print(Text.strip())
        embed = discord.Embed(
            title="복권 숫자!",
            description=Text.strip(),
            colour=discord.Color.red()
        )
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!검색'):
        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]
        encText = Text

        chromedriver_dir = r'C:\selum\chromedriver_win32\chromedriver.exe' #크롬드라이버 경로
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get('https://www.youtube.com/results?search_query='+encText) #유튜브 검색링크
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'}) # a태그에서 video title 이라는 id를 찾음

        embed = discord.Embed(
            title="영상들!",
            description="검색한 영상 결과",
            colour=discord.Color.blue())

        for i in range(0, 5):
            entireNum = entire[i]
            entireText = entireNum.text.strip()  # 영상제목
            print(entireText)
            test1 = entireNum.get('href')  # 하이퍼링크
            print(test1)
            rink = 'https://www.youtube.com'+test1
           # embed.add_field(name=str(i+1)+'번째 영상',value=entireText + '\n링크 : '+rink)
            embed.add_field(name=str(i + 1) + '번째 영상', value='\n' + '[%s](<%s>)' % (entireText, rink),
                            inline=False)  # [텍스트](<링크>) 형식으로 적으면 텍스트 하이퍼링크 만들어집니다
            searchYoutubeHref[i] = rink
        await client.send_message(message.channel,embed=embed)

    if message.content.startswith('1'):

        if not searchYoutubeHref: #저장된 하이퍼링크가 없다면
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[0])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[0]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('2'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[1])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[1]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('3'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[2])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[2]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('4'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[3])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[3]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('5'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[4])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[4]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]


    if message.content.startswith('!이모티콘'):

        emoji = [" ꒰⑅ᵕ༚ᵕ꒱ ", " ꒰◍ˊ◡ˋ꒱ ", " ⁽⁽◝꒰ ˙ ꒳ ˙ ꒱◜⁾⁾ ", " ༼ つ ◕_◕ ༽つ ", " ⋌༼ •̀ ⌂ •́ ༽⋋ ",
                 " ( ･ิᴥ･ิ) ", " •ө• ", " ค^•ﻌ•^ค ", " つ╹㉦╹)つ ", " ◕ܫ◕ ", " ᶘ ͡°ᴥ͡°ᶅ ", " ( ؕؔʘ̥̥̥̥ ه ؔؕʘ̥̥̥̥ ) ",
                 " ( •́ ̯•̀ ) ",
                 " •̀.̫•́✧ ", " '͡•_'͡• ", " (΄◞ิ౪◟ิ‵) ", " ˵¯͒ བ¯͒˵ ", " ͡° ͜ʖ ͡° ", " ͡~ ͜ʖ ͡° ", " (づ｡◕‿‿◕｡)づ ",
                 " ´_ゝ` ", " ٩(͡◕_͡◕ ", " ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄ ", " ٩(͡ï_͡ï☂ ", " ௐ ", " (´･ʖ̫･`) ", " ε⌯(ง ˙ω˙)ว ",
                 " (っ˘ڡ˘ς) ", "●▅▇█▇▆▅▄▇", "╋╋◀", "︻╦̵̵̿╤──", "ー═┻┳︻▄", "︻╦̵̵͇̿̿̿̿══╤─",
                 " ጿ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ጿ ", "∑◙█▇▆▅▄▃▂", " ♋♉♋ ", " (๑╹ω╹๑) ", " (╯°□°）╯︵ ┻━┻ ",
                 " (///▽///) ", " σ(oдolll) ", " 【o´ﾟ□ﾟ`o】 ", " ＼(^o^)／ ", " (◕‿‿◕｡) ", " ･ᴥ･ ", " ꈍ﹃ꈍ "
                                                                                                 " ˃̣̣̣̣̣̣︿˂̣̣̣̣̣̣ ",
                 " ( ◍•㉦•◍ ) ", " (｡ì_í｡) ", " (╭•̀ﮧ •́╮) ", " ଘ(੭*ˊᵕˋ)੭ ", " ´_ゝ` ", " (~˘▾˘)~ "] # 이모티콘 배열입니다.

        randomNum = random.randrange(0, len(emoji)) # 0 ~ 이모티콘 배열 크기 중 랜덤숫자를 지정합니다.
        print("랜덤수 값 :" + str(randomNum))
        print(emoji[randomNum])
        await client.send_message(message.channel, embed=discord.Embed(description=emoji[randomNum])) # 랜덤 이모티콘을 메시지로 출력합니다.

    if message.content.startswith('!주사위'):

        randomNum = random.randrange(1, 7) # 1~6까지 랜덤수
        print(randomNum)
        if randomNum == 1:
            await client.send_message(message.channel, embed=discord.Embed(description=':game_die: '+ ':one:'))
        if randomNum == 2:
            await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':two:'))
        if randomNum ==3:
            await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':three:'))
        if randomNum ==4:
            await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':four:'))
        if randomNum ==5:
            await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':five:'))
        if randomNum ==6:
            await client.send_message(message.channel, embed=discord.Embed(description=':game_die: ' + ':six: '))

    if message.content.startswith('!타이머'):

        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]

        secint = int(Text)
        sec = secint

        for i in range(sec, 0, -1):
            print(i)
            await client.send_message(message.channel, embed=discord.Embed(description='타이머 작동중 : '+str(i)+'초'))
            time.sleep(1)

        else:
            print("땡")
            await client.send_message(message.channel, embed=discord.Embed(description='타이머 종료'))

    if message.content.startswith('!제비뽑기'):
        channel = message.channel
        embed = discord.Embed(
            title='제비뽑기',
            description='각 번호별로 번호를 지정합니다.',
            colour=discord.Colour.blue()
        )

        embed.set_footer(text='끗')


        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]
        print(Text.strip()) #입력한 명령어

        number = int(Text)

        List = []
        num = random.randrange(0, number)
        for i in range(number):
            while num in List:  # 중복일때만
                num = random.randrange(0, number)  # 다시 랜덤수 생성

            List.append(num)  # 중복 아닐때만 리스트에 추가
            embed.add_field(name=str(i+1) + '번째', value=str(num+1), inline=True)

        print(List)
        await client.send_message(channel, embed=embed)

    if message.content.startswith('!이미지'):

        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]
        print(Text.strip())  # 입력한 명령어

        randomNum = random.randrange(0, 40) # 랜덤 이미지 숫자

        location = Text
        enc_location = urllib.parse.quote(location) # 한글을 url에 사용하게끔 형식을 바꿔줍니다. 그냥 한글로 쓰면 실행이 안됩니다.
        hdr = {'User-Agent': 'Mozilla/5.0'}
        # 크롤링 하는데 있어서 가끔씩 안되는 사이트가 있습니다.
        # 그 이유는 사이트가 접속하는 상대를 봇으로 인식하였기 때문인데
        # 이 코드는 자신이 봇이 아닌것을 증명하여 사이트에 접속이 가능해집니다!
        url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + enc_location # 이미지 검색링크+검색할 키워드
        print(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser") # 전체 html 코드를 가져옵니다.
        # print(bsObj)
        imgfind1 = bsObj.find('div', {'class': 'photo_grid _box'}) # bsjObj에서 div class : photo_grid_box 의 코드를 가져옵니다.
        # print(imgfind1)
        imgfind2 = imgfind1.findAll('a', {'class': 'thumb _thumb'}) # imgfind1 에서 모든 a태그 코드를 가져옵니다.
        imgfind3 = imgfind2[randomNum]  # 0이면 1번째사진 1이면 2번째사진 형식으로 하나의 사진 코드만 가져옵니다.
        imgfind4 = imgfind3.find('img') # imgfind3 에서 img코드만 가져옵니다.
        imgsrc = imgfind4.get('data-source') # imgfind4 에서 data-source(사진링크) 의 값만 가져옵니다.
        print(imgsrc)
        embed = discord.Embed(
            colour=discord.Colour.green()
        )
        embed.add_field(name='검색 : '+Text, value='링크 : '+imgsrc, inline=False)
        embed.set_image(url=imgsrc) # 이미지의 링크를 지정해 이미지를 설정합니다.
        await client.send_message(message.channel, embed=embed) # 메시지를 보냅니다.


    if message.content.startswith('!members'):
        x = message.server.members
        for member in x:
            print(member.name)  # you'll just print out Member objects your way.

    if message.content.startswith('!반가워'):
        msg = '{0.author.mention} 나도반가워!'.format(message)
        await client.send_message(message.channel, msg)













client.run('NjA4Njk0OTIwNTYzMTMwMzc4.XUr5Zg.4VjvB_uJItZWHjkXOkR3mKrtphA')
