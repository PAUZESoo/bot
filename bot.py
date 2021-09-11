import discord, os, asyncio, random, json, yaml
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from apiRequest import riotAPIRequest

bot = commands.Bot(command_prefix = '~')
 
status = cycle(["~도움 명령어를 입력해주세요"])

apiCall = riotAPIRequest(os.environ['riotapiKey'])

tierScore = {
    'default' : 0,
    'IRON' : 1,
    'BRONZE' : 2,
    'SILVER' : 3,
    'GOLD' : 4,
    'PLATINUM' : 5,
    'DIAMOND' : 6,
    'MASTER' : 7,
    'GRANDMASTER' : 8,
    'CHALLENGER' : 9
}

def tierCompare(solorank,flexrank):
    #solorank is higher
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    #flexrank is higher
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    # same
    else:
        return 2

@bot.event
async def on_ready():
    change_status.start()    # 봇이 on_ready 상태라면, change_message 함수 실행

@tasks.loop(seconds=5)    # n초마다 다음 메시지 출력
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event    
async def on_message(message):        

  if message.content == "~도움":
      embed = discord.Embed(title="명령어 리스트: ~도움, ~사다리, ~전적, ~모스트" , descrioption = "용도에 맞는 명령어를 입력해주세요.", color=0x00ff00)
      embed.add_field(name="~롤 본인계급", value="롤 듀오를 구합니다", inline=False)
      embed.add_field(name="~철권 본인계급", value="철권 플매를 구합니다", inline=False)
      embed.add_field(name="~스팀 해당게임", value="해당 게임을 같이할 플레이어를 구합니다", inline=False)
      embed.add_field(name="~사다리 이름/결과", value="~사다리 A B C/꽝 꽝 당첨 ※띄어쓰기,/ 주의", inline=False)
      embed.add_field(name="~전적 (소환사 이름 - 띄어쓰기 붙여쓰기 상관없습니다)", value = "해당 소환사의 전적을 검색합니다.", inline=False)
      embed.add_field(name="~모스트 (소환사 이름 - 띄어쓰기 붙여쓰기 상관없습니다)", value = "해당 소환사의 모스트 픽을 검색합니다.", inline=False)

      await message.delete()
      await message.channel.send(embed=embed)
        


  if message.content.startswith("~롤"):
        grade = message.content.split()
        try:
          embed = discord.Embed(title=":bell: 함께할 소환사님 구합니다 :bell:", description="League of Legends",  color=0x00ff00)

          embed.add_field(name="소환사명", value=message.author.display_name, inline=True)
          embed.add_field(name="계급", value=grade[1], inline=True)

          embed.set_thumbnail(url=message.author.avatar_url)
          embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
          await message.delete()
          msg = await message.channel.send(embed=embed)
          await msg.add_reaction("⏰")
          await asyncio.sleep(120)
          await msg.delete()
        except IndexError:
          await message.channel.send("계급을 써주세요. 예시) ~롤 다이아")

  if message.content.startswith("~철권"):
        grade = message.content.split()
        try:
          embed = discord.Embed(title=":bell: 플매하실분 구합니다 :bell:", description="TEKKEN 7",  color=0x00ff00)
          embed.add_field(name="닉네임", value=message.author.display_name, inline=True)
          embed.add_field(name="계급", value=grade[1], inline=True)
          embed.set_thumbnail(url=message.author.avatar_url)
          embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
          await message.delete()
          msg = await message.channel.send(embed=embed)
          await msg.add_reaction("⏱️")
          await asyncio.sleep(120)
          await msg.delete()

        except IndexError:
          await message.channel.send("계급을 써주세요. 예시) ~철권 황금단")
    

  if message.content.startswith("~스팀"):
        grade = message.content.split()
        try:
          embed = discord.Embed(title=":bell: 같이하실분 구합니다 :bell:", description="STEAM GAME",  color=0x00ff00)

          embed.add_field(name="닉네임", value=message.author.display_name, inline=True)
          embed.add_field(name="게임명", value=grade[1], inline=True)

          embed.set_thumbnail(url=message.author.avatar_url)
          embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
          await message.delete()
          msg = await message.channel.send(embed=embed)
          await msg.add_reaction("⏲️")
          await asyncio.sleep(120)
          await msg.delete()
          
        except IndexError:
          await message.channel.send("게임을 써주세요. 예시) ~스팀 배그")

  if message.content.startswith("~사다리"):
    team = message.content[5:]
    peopleteam = team.split("/")
    people = peopleteam[0]
    team = peopleteam[1]
    person = people.split(" ")
    teamname = team.split(" ")
    random.shuffle(teamname)
    result = ""
    for i in range(0, len(person)):
      result = result + person[i] + " =====> " + teamname[i] + "\n"
    
    embed = discord.Embed(title=":bell: 사다리타기 결과입니다. :bell:", description = result,  color=0x00ff00)
    embed.set_footer(text = "결과값이 이상하면 띄어쓰기와 /를 정확히 입력해주세요. ~도움 참조"+ "\n"+"메세지 5분 뒤 삭제")
    embed.set_thumbnail(url="https://blog.kakaocdn.net/dn/dalaQ0/btqEcUgGSgb/Xkmr2DKrtyh8pz4wc1Cwz0/img.png")
    msg = await message.channel.send(embed=embed)
    await asyncio.sleep(300)
    await message.delete()
    await msg.delete()
    
  if message.author == bot.user:
        return

  if message.content.startswith("~전적"):
      try:
          if len(message.content.split(" ")) == 1:
              embed = discord.Embed(title="❌소환사 이름이 입력되지 않았습니다.", description="", color=0x5CD1E5)
              embed.add_field(name="~전적 소환사이름", value="소환사 이름을 입력해주세요.", inline=False)
              embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
              msgg = await message.channel.send(embed=embed)
              await asyncio.sleep(120)
              await msgg.delete()
          else:
              playerNickname = ' '.join((message.content).split(' ')[1:])
              #Return false if summoner not exist
              getPersonalRecordBox = apiCall.getPersonalGameRecord(playerNickname)
              if not getPersonalRecordBox:
                  embed = discord.Embed(title="❌해당 닉네임의 소환사가 존재하지 않습니다.", description="", color=0x5CD1E5)
                  embed.add_field(name="소환사의 이름을 확인해주세요.", value="올바른 소환사의 이름을 입력해주세요.", inline=False)
                  embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                  msgg = await message.channel.send(embed=embed)
                  await asyncio.sleep(120)
                  await msgg.delete()
              else:
                  record = getPersonalRecordBox["Record"]
                  keys = record.keys()
                  mastery = getPersonalRecordBox["ChampionMastery"]
                  if len(record) == 2:
                      solowinRatio = int((record['Personal/Duo Rank']['win'] / (record['Personal/Duo Rank']['win'] + record['Personal/Duo Rank']['loss'])) * 100)
                      flexwinRatio = int((record['Flex 5:5 Rank']['win'] / (record['Flex 5:5 Rank']['win'] + record['Flex 5:5 Rank']['loss'])) * 100)
                      solotier = record['Personal/Duo Rank']['tier']
                      flextier = record['Flex 5:5 Rank']['tier']
                      tc = tierCompare(solotier,flextier)
                      thumbnail = "lorem ipsum"
                      # Compare tier
                      if tc == 0:
                          thumbnail = solotier
                      elif tc == 1:
                          thumbnail = flextier
                      else:
                          thumbnail = solotier
                      embed = discord.Embed(title="⚔️소환사 \"" + playerNickname + "\" 님의 전적검색", description="", color=0x5CD1E5)
                      embed.add_field(name=f"솔로랭크 : {record['Personal/Duo Rank']['tier']} {record['Personal/Duo Rank']['rank']}", value=f"{record['Personal/Duo Rank']['leaguepoint']} LP / {record['Personal/Duo Rank']['win']}W {record['Personal/Duo Rank']['loss']}L / Win Ratio {solowinRatio}%", inline=False)
                      embed.add_field(name=f"자유 5:5 랭크 : {record['Flex 5:5 Rank']['tier']} {record['Flex 5:5 Rank']['rank']}", value=f"{record['Flex 5:5 Rank']['leaguepoint']} LP / {record['Flex 5:5 Rank']['win']}W {record['Flex 5:5 Rank']['loss']}L / Win Ratio {flexwinRatio}%", inline=False)
                      embed.add_field(name=f"모스트 챔피언 : {mastery['championname']}",value=f"Proficiency Level : {mastery['championlevel']}.Lv / Champion Point : {mastery['championpoint']}pt")
                      embed.set_thumbnail(url=f"https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_{thumbnail}.png?raw=true")
                      embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                      msgg = await message.channel.send(embed=embed)
                      await asyncio.sleep(120)
                      await msgg.delete()
                      
                  elif len(record) == 0:
                      embed = discord.Embed(title="⚔️소환사 \"" + playerNickname + "\" 님의 전적검색", description="", color=0x5CD1E5)
                      embed.add_field(name="솔로랭크 : Unranked", value="언랭크", inline=False)
                      embed.add_field(name="Flex 5:5 Rank : Unranked", value="언랭크", inline=False)
                      embed.set_thumbnail(url="https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_DEFAULT.png?raw=true")
                      embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                      msgg = await message.channel.send(embed=embed)
                      await asyncio.sleep(120)
                      await msgg.delete()
                      
                  elif len(record) == 1 and "Personal/Duo Rank" not in keys:
                      flexwinRatio = int((record['Flex 5:5 Rank']['win'] / (record['Flex 5:5 Rank']['win'] + record['Flex 5:5 Rank']['loss'])) * 100)
                      embed = discord.Embed(title="⚔️소환사 \"" + playerNickname + "\" 님의 전적검색", description="", color=0x5CD1E5)
                      embed.add_field(name="솔로랭크 : Unranked", value="언랭크", inline=False)
                      embed.add_field(name=f"자유 5:5 랭크 : {record['Flex 5:5 Rank']['tier']} {record['Flex 5:5 Rank']['rank']}", value=f"{record['Flex 5:5 Rank']['leaguepoint']} LP / {record['Flex 5:5 Rank']['win']}W {record['Flex 5:5 Rank']['loss']}L / Win Ratio {flexwinRatio}%", inline=False)
                      embed.add_field(name=f"모스트 챔피언 : {mastery['championname']}",value=f"Proficiency Level : {mastery['championlevel']}.Lv / Champion Point : {mastery['championpoint']}pt")
                      embed.set_thumbnail(url=f"https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_{record['Flex 5:5 Rank']['tier']}.png?raw=true")
                      embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                      msgg = await message.channel.send(embed=embed)
                      await asyncio.sleep(120)
                      await msgg.delete()
                      
                  elif len(record) == 1 and "Flex 5:5 Rank" not in keys:
                      solowinRatio = int((record['Personal/Duo Rank']['win'] / (record['Personal/Duo Rank']['win'] + record['Personal/Duo Rank']['loss'])) * 100)
                      embed = discord.Embed(title="⚔️소환사 \"" + playerNickname + "\" 님의 전적검색", description="", color=0x5CD1E5)
                      embed.add_field(name=f"솔로랭크 : {record['Personal/Duo Rank']['tier']} {record['Personal/Duo Rank']['rank']}", value=f"{record['Personal/Duo Rank']['leaguepoint']} LP / {record['Personal/Duo Rank']['win']}W {record['Personal/Duo Rank']['loss']}L / Win Ratio {solowinRatio}%", inline=False)
                      embed.add_field(name="자유 5:5 랭크 : Unranked", value="Unranked", inline=False)
                      embed.add_field(name=f"모스트 챔피언 : {mastery['championname']}",value=f"Proficiency Level : {mastery['championlevel']}.Lv / Champion Point : {mastery['championpoint']}pt")
                      embed.set_thumbnail(url=f"https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_{record['Personal/Duo Rank']['tier']}.png?raw=true")
                      embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                      msgg = await message.channel.send(embed=embed)
                      await asyncio.sleep(120)
                      await msgg.delete()
                              
      except BaseException as e:
          embed = discord.Embed(title="❌오류 발생!", description="", color=0x5CD1E5)
          embed.add_field(name="오류가 발생했습니다!", value="제가 만든게 아니라 못 고칩니다...", inline=False)
          embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
          msgg = await message.channel.send(embed=embed)
          await asyncio.sleep(120)
          await msgg.delete()
          
  if message.content.startswith("~모스트"):
      try:
          if len(message.content.split(" ")) == 1:
              embed = discord.Embed(title="❌소환사 이름이 입력되지 않았습니다.", description="", color=0x5CD1E5)
              embed.add_field(name="~모스트 소환사이름", value="소환사 이름을 입력해주세요.", inline=False)
              embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
              msgg = await message.channel.send(embed=embed)
              await asyncio.sleep(120)
              await msgg.delete()
          else:
              playerNickname = ' '.join((message.content).split(' ')[1:])
              getMasteryBox = apiCall.getPersonalChampionMasteries(playerNickname)
              keys = list(getMasteryBox.keys())
              if not getMasteryBox:
                  embed = discord.Embed(title="❌해당 닉네임의 소환사가 존재하지 않습니다.", description="", color=0x5CD1E5)
                  embed.add_field(name="소환사의 이름을 확인해주세요.", value="존재하지 않는 소환사 입니다.", inline=False)
                  embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                  msgg = await message.channel.send(embed=embed)
                  await asyncio.sleep(120)
                  await msgg.delete()
              else:
                  embed = discord.Embed(title=f"소환사 \"{playerNickname}\" 님의 Most Top 3", description="", color=0x5CD1E5)
                  count = 1
                  thumbnail = 'lorem ipsum'
                  for i in getMasteryBox:
                      key = keys[count - 1]
                      p = getMasteryBox[key]
                      embed.add_field(name=f"모스트{count} : {key}", value=f"숙련도 레벨 : {p['championlevel']}.Lv / Champion Point : {p['championpoint']}pt",inline=False)
                      if count == 1:
                          thumbnail = p['championImage']
                      else:
                          pass
                      count += 1
                  embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/11.13.1/img/champion/{thumbnail}")
                  embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
                  msgg = await message.channel.send(embed=embed)
                  await asyncio.sleep(120)
                  await msgg.delete()
      except BaseException as e:
            embed = discord.Embed(title="❌오류 발생!", description="", color=0x5CD1E5)
            embed.add_field(name="오류가 발생했습니다!", value="제가 만든게 아니라 못 고칩니다...", inline=False)
            embed.set_footer(text = "2분 뒤 자동 삭제 됩니다.")
            msgg = await message.channel.send(embed=embed)
            await asyncio.sleep(120)
            await msgg.delete()


      await bot.process_commands(message)
      return
  await bot.process_commands(message)



@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        return None

    if str(reaction) == "⏰":
      msgg = await reaction.message.channel.send(user.mention + "님과 듀오가 성사되었습니다.")
      await asyncio.sleep(120)
      await msgg.delete()

    if str(reaction) == "⏱️":
        msgg = await reaction.message.channel.send(user.mention + "님과 플매가 성사되었습니다.")
        await asyncio.sleep(120)
        await msgg.delete()

    if str(reaction) == "⏲️":
        msgg = await reaction.message.channel.send(user.mention + "님과 함께 플레이 할수 있습니다.")
        await asyncio.sleep(120)
        await msgg.delete() 
    


@bot.command()
@commands.has_any_role("⚔️마스터", "🦊서브 마스터", "🦁 간부")
async def 방송부여(ctx, member: discord.Member):
    guild = ctx.guild
    방송역할 = discord.utils.get(ctx.guild.roles, name = "방송")
    if discord.utils.get(guild.roles, name = "방송"):
        await member.add_roles(방송역할)
        await ctx.send(f'{member.mention} 방송 역할이 부여됐습니다')
        await bot.get_channel(882599757955104810).send(f'{member.display_name} 님에게 방송 역할을 부여했습니다. 역할삭제 로그가 없으면 삭제해주세요')

@방송부여.error
async def 방송부여_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("명령을 실행하실 권한이 없습니다.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("유저를 넣지 않으셨습니다.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("유저를 넣어주세요.")


@bot.command()
@commands.has_any_role("⚔️마스터", "🦊서브 마스터", "🦁 간부")
async def 방송제거(ctx, member: discord.Member):
    guild = ctx.guild
    방송역할 = discord.utils.get(ctx.guild.roles, name = "방송")
    if discord.utils.get(ctx.guild.roles, name = "방송"):
        await member.remove_roles(방송역할)
        await ctx.send(f'{member.mention} 방송 역할이 제거됐습니다')
        await bot.get_channel(882599757955104810).send(f'{member.display_name} 님의 방송 역할을 삭제했습니다.')

@방송제거.error
async def 방송제거_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("명령을 실행하실 권한이 없습니다.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("닉네임을 넣지 않으셨습니다.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("올바른 닉네임을 넣어주세요.")


bot.run(os.environ['BOT_TOKEN'])