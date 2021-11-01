import discord
from discord.ext import commands
from replit import db
import time
import random
import json
from io import BytesIO
from datetime import datetime
from cogs.help import BotHelp
import asyncio
import aiohttp
import aiosqlite
from urllib.parse import urlencode
from utils.views import Delete


def get_prefix(client, message):
  try:
      with open('assets/prefixes.json', 'r',encoding='utf8') as r:
          prefixes = json.load(r)
          return prefixes[str(message.guild.id)]
      
  except KeyError: 
      with open('assets/prefixes.json', 'r',encoding='utf8') as k:
          prefixes = json.load(k)
      prefixes[str(message.guild.id)] = '.'

      with open('assets/prefixes.json', 'w',encoding='utf8') as j:
          j.write(json.dumps(prefixes,indent=4))

      with open('assets/prefixes.json', 'r',encoding='utf8') as t:
          prefixes = json.load(t)
          return prefixes[str(message.guild.id)]
      return '.'

class bot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.starttime=datetime.utcnow()
    self.session=aiohttp.ClientSession()

  async def get_invite(self):
    appinfo=await self.application_info()
    appid=appinfo.id
    scopes = ('bot', 'applications.commands')
    query = {
              "client_id": appid,
              "scope": "+".join(scopes),
              "permissions": 8
          }
    return f"https://discordapp.com/oauth2/authorize?{urlencode(query, safe='+')}"
      



client = bot(command_prefix = get_prefix, case_insensitive=True,intents=discord.Intents.all())

async def startup():
  await client.wait_until_ready()
  client.db=await aiosqlite.connect("./data/bank.db")
  await client.db.execute("CREATE TABLE IF NOT EXISTS bankdata (userid int,wallet int,bankbal int,daily int)")

blacklisted_words = [' fuck ', ' bitch ', ' prick ', ' cum ',  'pussy ', ' dick ', ' penis ', ' cunt ',' ass ',' asshole ',' nigga ',' chutia ',' chutiya ',' sex ',' porn ',' boob ',' vagina ']

client.help_command=BotHelp()

async def load_cogs():
  await client.wait_until_ready()
  cogs=[
            "cogs.info",
            "cogs.general",
            "cogs.errors",
            "cogs.api",
            "cogs.music",
            "cogs.mod",
            "cogs.economy",
            "cogs.roles",
            "cogs.events",

            "jishaku"
    ]
  for i in cogs:
    client.load_extension(i)
    print("loaded ",i)


@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
  if 'hack' in msg.content.lower():
     await msg.channel.send("wtf")
  else:
    for word in blacklisted_words:
      if word in msg.content.lower():
        try:
          await msg.delete()
        except:
          pass
        embed=discord.Embed(title='Bad word usage',description=str(msg.author)+'. Hey, thats a bad word!',color=discord.Colour.red())
        embed.set_thumbnail(url=msg.author.avatar.url)
        await msg.channel.send(embed=embed)
  await client.process_commands(msg)
'''
  @client.event
  async def on_command_error(ctx, exc):
    if isinstance(exc, commands.CommandOnCooldown):
      if exc.retry_after > 60 and exc.retry_after < 3600:
        embed=discord.Embed(title='Command on cooldown',description=f'This command is on cooldown. Try again in {exc.retry_after/60:,.2f}m.',color=discord.Colour.red())
      elif exc.retry_after > 3600:
        embed=discord.Embed(title='Command on cooldown',description=f'This command is on cooldown. Try again in {exc.retry_after/3600:,.2f}h.',color=discord.Colour.red())
      else:
        embed=discord.Embed(title='Command on cooldown',description=f'This command is on cooldown. Try again in {exc.retry_after:,.2f}s.',color=discord.Colour.red())
      await ctx.send(embed=embed)
    else:
      await ctx.send(exc)
      traceback.print_exc()


  await client.process_commands(msg)
'''
ruleslist = [
    'Must tos follow discord ToS',
    'No Spam or flooding the chat with messages. Do not type in ALL CAPS.',
    'No heated arguments to other people in the chat.',
    'No adult (18+), explicit, or controversial messages.',
    'No racism or degrading content.', '5. No excessive cursing.',
    'No advertising  (Only with Permission).', '7. No referral links.',
    'No begging or repeatedly asking for help in the chat. ',
    'No offensive names.',
    'Do not perform or promote the intentional use of glitches, hacks, bugs, and other exploits that will cause an incident within the community and other players.',
    'Do not argue with staff. Decisions are final.',
    'Please avoid Mentioning higher authorities.'
]

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='.help'))
  print("We have logged in as {0.user}".format(client))

'''
@client.command()
async def fight(ctx,member:discord.Member=None):
  if member is None:
    user = ctx.message.author
  else:
    user = member
  wanted_img = Image.open('./assets/anime fight.jpg')
  asset = user.avatar.url_as(size=128)
  author_asset = ctx.message.author.avatar.url_as(size=128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  author_data = BytesIO(await author_asset.read())
  author_pfp = Image.open(author_data)

  pfp = pfp.resize((84,84))
  author_pfp = author_pfp.resize((84,84))
  wanted_img.paste(pfp(38,13))
  wanted_img.save('.assets/profile.jpg')
  wanted_img.paste(author_pfp,(212,16))
  wanted_img.save('.assets/profile.jpg')
  await ctx.send(file=discord.File('.assets/profile.jpg'))
'''

@client.command(aliases=['regulations'])
async def rule(ctx,*,number=1):
  string2 = str(ruleslist[int(number)-1])
  embed = discord.Embed(title='Rule '+str(number)+':',description=string2,color=discord.Colour.blue())
  await ctx.send(embed=embed)

@client.command(name="ee")
async def testin(ctx):
  view=discord.ui.View()
  button=discord.ui.Button(label="this is a button")
  async def callbac(interaction:discord.Interaction):
    await interaction.response.send_message("responded")
  button.callback=callbac
  view.add_item(button)

  await ctx.send("hello",view=view)
@client.command(aliases=['w'])
async def warn(ctx,member : discord.Member,*,reason='No reason provided'):
  embed = discord.Embed(title='Warn', description=str(member)+' has been warned for '+reason,color=discord.Colour.dark_gold())
  embed2 = discord.Embed(title='Warn', description='You have been warned for '+reason,color=discord.Colour.dark_gold())
  await member.send(embed=embed2)
  await ctx.send(embed=embed)
  with open('.assets/warnings.json', 'r') as f:
    warning_dict = json.load(f)
  if str(ctx.guild.id) not in warning_dict:
    warning_dict[str(ctx.guild.id)] = {str(member):1}
  elif str(member) not in warning_dict[str(ctx.guild.id)]:
    warning_dict[str(ctx.guild.id)][str(member)] = 1
  else:
    warning_dict[str(ctx.guild.id)][str(member)] += 1
  with open('.assets/warnings.json','w') as f:
    json.dump(warning_dict, f)

@client.command()
async def warnings(ctx,member:discord.Member):
  
  no_of_warnings = str(db[str(member)])
  embed = discord.Embed(title='Warnings',description=member+ ' has received '+no_of_warnings+' warnings.',color=discord.Colour.gold())
  await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member:discord.Member,*,reason='No reason provided'):
  muted_role = ctx.guild.get_role(796759065177882625)
  await member.add_roles(muted_role)
  embed2 = discord.Embed(title='You got muted',description='You have been muted in the Chill Zone for '+reason,color=discord.Colour.dark_orange())
  await member.send(embed=embed2)
  string = str(member)+' has been muted for '+reason
  embed = discord.Embed(title='Mute', description = string , color = discord.Colour.green())
  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member:discord.Member):
  muted_role = ctx.guild.get_role(796759065177882625)
  await member.remove_roles(muted_role)
  embed = discord.Embed(title='Unmute',description=str(member)+' has been unmuted!',color=discord.Colour.dark_green())
  
  await ctx.send(embed=embed)

@client.command()
async def dm(ctx,member:discord.Member,*,message=''):
  if ctx.message.author.guild_permissions.administrator:
    if message == '':
      embed = discord.Embed(title='Bruh.',description='Bruh you actually need to send a message',color=discord.Colour.red())
      await ctx.send(embed=embed)
    else:
      await member.send(message)
  
      if 'hack' in message.lower():
        await ctx.message.author.send('Oh you are a hacker? Imma mute u for 10secs.')
        muted_role = ctx.guild.get_role(796759065177882625)
        await ctx.message.author.add_roles(muted_role)
        time.sleep(10)
        await ctx.message.author.remove_roles(muted_role)

  else:
    embed = discord.Embed(title='Missing Perms', description='You dont have permission to do that! You need the "Administrator" permission to execute this command.',color=discord.Colour.greyple())
    await ctx.send(embed=embed)

@client.command(name='curse')
async def curse(ctx,user : discord.Member = None):
    curse=[
        'sent to the locker of Davy Jones',
        'falled into the worlds end',
        'boiled in oil',
        'eaten by dogs',
        'kicked from the plane',
        'smashed by Hulk',
        'burried in black coffin',
        'touched by monster of hell',
        'magically killed with elder wand',
        'rat made whole in there pant',]
    if user is None:
        await ctx.send('Please mention a use like `.cures @member`')
    else:
        await ctx.send(f'`{user.name}` is cursed and {random.choice(curse)}')
      
@client.command()
async def ping(ctx):
  ping = 'Pong! {0}'.format(client.latency*1000)
  embed =  discord.Embed(title='Ping', description=ping,color = discord.Colour.green())
  await ctx.send(embed=embed,view=Delete(ctx.author))


@client.command()
async def poll(ctx,option1,option2,*,question):
  channel = ctx.channel
  embed = discord.Embed(title=str(question),color=discord.Colour.red())
  embed.add_field(name='Option 1',value = '```'+str(option1)+'```',inline=True)
  embed.add_field(name='Option 2',value='```'+str(option2)+'```',inline=True)
  sender=str(ctx.message.author)
  embed.set_footer(text=sender,icon_url=ctx.message.author.avatar.url)
  message_ = await channel.send(embed=embed)
  await message_.add_reaction('1️⃣')
  await message_.add_reaction('2️⃣')

@client.command()
async def coinflip(ctx):
  ht = ['heads','tails']
  random_ht = random.choice(ht)
  embed = discord.Embed(title=random_ht.capitalize(),description='The coin landed on the side of '+random_ht+'!',color=discord.Colour.red())
  
  await ctx.send(embed=embed)

@client.command()
async def highlow(ctx,member:discord.Member,number):
  
  choose = random.randrange(1,101)
  await ctx.send(member.mention+', enter your number in the chat now!')
  def check(m):
    return m.author == member and type(int(m.content)) is int
  msg = await client.wait_for('message',check=check)

  if abs(choose - abs(int(msg.content))) > abs(choose - abs(int(number))):
    embed = discord.Embed(title=str(ctx.message.author)+"'s highlow game",description=str(member)+' won the game!',color=discord.Colour.magenta())
  elif abs(choose - abs(int(msg.content))) < abs(choose - abs(int(number))):
    embed = discord.Embed(title=str(ctx.message.author)+"'s highlow game",description=str(ctx.message.author)+' won the game!',color=discord.Colour.magenta())
  else:
    embed = discord.Embed(title="Error",description='Uh oh! Something went wrong!',color=discord.Colour.lighter_grey())
  await ctx.send(embed=embed)
  


@client.command()
async def ability(ctx,*,ability):
  ability = ability.replace(' ','-')
  
  URL = 'https://pokeapi.co/api/v2/ability/'+str(ability).lower()
  async with aiohttp.request('GET',URL,headers={}) as response:
    data = await response.json()
    
    if str(ability) == 'prism-armor':
      ability_data = data['effect_entries'][0]['short_effect']
    else:
      ability_data = data['effect_entries'][1]['short_effect']
    
    
    
    embed=discord.Embed(title='Ability Data of '+str(ability).title(),color=discord.Colour.blue())
    embed.add_field(name='Data',value=ability_data)
    
    await ctx.send(embed=embed)
      

@client.command()
async def typechart(ctx):
  embed = discord.Embed(title='Type Chart for Pokemon',color=discord.Colour.red())
  embed.set_image(url='https://img.pokemondb.net/images/typechart.png')
  await ctx.send(embed=embed)

@client.command(aliases=['pkcmds'])
async def pokecommands(ctx):
  embed=discord.Embed(title='Pokemon comands',color=discord.Colour.blue())
  embed.add_field(name='e!poke {pokemon}',value='Pulls up the info of a specified pokemon.',inline=False)
  embed.add_field(name='e!ability {ability}',value='Pulls up the info of a specified ability.',inline=False)
  await ctx.send(embed=embed)

@client.command()
async def warns(ctx,member:discord.Member):
  with open('.assets/warnings.json','r') as f:
    warning_dict = json.load(f)
  if str(ctx.guild.id) not in warning_dict:
      
    embed = discord.Embed(title=str(member)+'\'s warns',description=str(member)+' has 0 warnings.',color=discord.Colour.gold())

  else:
    no_of_warns = warning_dict[str(ctx.guild.id)][str(member)]
    embed = discord.Embed(title=str(member)+'\'s warns',description=str(member)+' has '+str(no_of_warns)+' warnings.',color=discord.Colour.gold())
  await ctx.send(embed=embed)



'''

@client.command()
async def jobs(ctx, page=1):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    if 'job' not in data[str(ctx.message.author)]:
      data[str(ctx.message.author)]['job'] = 'none'
      with open('.assets/currency.json','w') as f:
        json.dump(data, f)
    if int(page) == 1:
    
      embed=discord.Embed(title='Jobs List',color=discord.Colour.purple())
      embed.add_field(name='Street Sweeper - 1000 coins',value='ID: sweeper',inline=False)
      embed.add_field(name='Janitor - 1500 coins',value='ID: janitor',inline=False)
      embed.add_field(name='Teacher - 2500 coins',value='TD: teacher', inline=False)
      embed.add_field(name='Principal - 5000 coins',value='ID: principal',inline=False)
      embed.add_field(name='Doctor - 10000 coins',value='ID: doctor',inline=False)
      embed.add_field(name='CEO - 50000 coins',value='ID: ceo',inline=False)
      embed.add_field(name='CEO Of Microsoft - 100000 coins',value='ID: mic_ceo',inline=False)
    if data[str(ctx.message.author)]['job'] == 'none':
      embed.set_footer(text='You havent got a job yet! Use e!apply {job} to apply for one!\nBEWARE: THE BETTER THE JOB, THE MORE\nTHE CHANCE OF GETTING DECLINED.\nCOOLDOWN IS 12HRS')
    else:
      embed.set_footer(text='You are working as: '+data[str(ctx.message.author)]['job'].capitalize()+'\nBEWARE: THE BETTER THE JOB, THE MORE\nTHE CHANCE OF GETTING DECLINED.\nCOOLDOWN IS 12HRS')
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def apply(ctx, job):  # sourcery no-metrics
  with open('.assets/currency.json','r') as f:
      data = json.load(f)
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    approve = discord.Embed(title='Approval',description='Your application has been approved!',color=discord.Colour.red())
    deny = discord.Embed(title='Denial',description='Your application has been denied!',color=discord.Colour.red())
    
    chance = random.randrange(1, 101)
    defa = 'none'
    multi = data[str(ctx.message.author)]['multiplier']
    if job == 'sweeper':
      await ctx.send(embed=approve)
      defa = 'sweeper'
    if job == 'janitor':
      await ctx.send(embed=approve)
      defa = 'janitor'
    if job == 'teacher':
      if chance-multi <= 75:
        await ctx.send(embed=approve)
        defa = 'teacher'
      else:
        await ctx.send(embed=deny)
    if job == 'principal':
      if chance-multi <= 50:
        await ctx.send(embed=approve)
        defa = 'principal'
      else:
        await ctx.send(embed=deny)
    if job == 'doctor':
      if chance-multi <= 30:
        await ctx.send(embed=approve)
        defa = 'doctor'
      else:
        await ctx.send(embed=deny) 
    if job == 'ceo':
      if chance-multi <= 10:
        await ctx.send(embed=approve)
        defa = 'ceo'
      else:
        await ctx.send(embed=deny) 
    if job == 'mic_ceo':
      if chance-multi <= 1:
        await ctx.send(embed=approve)
        defa = 'mic_ceo'
      else:
        await ctx.send(embed=deny) 
    data[str(ctx.message.author)]['job'] = str(defa)
    with open('.assets/currency.json','w') as f:
      json.dump(data, f)

@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def work(ctx):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  with open('.assets/work_list.json','r') as f:
    work_list = json.load(f)
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    if data[str(ctx.message.author)]['job'] == 'none':
      embed=discord.Embed(title='Unemployed',description='You dont currently have a job!',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      payment = int(work_list[data[str(ctx.message.author)]['job']] + ((data[str(ctx.message.author)]['multiplier']/100)*work_list[data[str(ctx.message.author)]['job']]))
      await ctx.send('You worked hard and received **'+str(payment)+'** coins!')
      data[str(ctx.message.author)]['wallet_balance'] += payment
      with open('.assets/currency.json','w') as f:
        json.dump(data, f)'''

'''

@client.command()
async def shop(ctx,page=1):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    
    data[str(ctx.message.author)]['multiplier'] = 0
    
    pages_list = [1]
    if page not in pages_list:
      embed=discord.Embed(title='Page does not exist',description='The page you are tryng to search for does not exist!',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      if page == 1:
        embed=discord.Embed(title='Shop',color=discord.Colour.purple())
        embed.add_field(name='Banknote',value='Increases your risk/reward ratio in investing!\nCost: 10000 coins.\nID: banknote',inline=False)
        embed.add_field(name='Cheddar',value='Gives you a multiplier boost of 1%!\nCost: 20000 coins.\nID: cheddar',inline=False)
        embed.add_field(name='Laptop',value='Allows you to invest!\nCost: 25000 coins.\nID: laptop',inline=False)
        embed.add_field(name='Kalashnikov',value='Increases your robbery money by 50%!\nCost: 100000 coins.\nID: kalashnikov',inline=False)

      with open('.assets/currency.json','w') as f:
        json.dump(data, f)
      await ctx.send(embed=embed)

@client.command()
async def buy(ctx,objecto=None,amount=1):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    if objecto is None:
      embed=discord.Embed(title='Object not found',description='You actually need to buy something, dumdum.',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      if objecto == 'banknote':
        if data[str(ctx.message.author)]['wallet_balance'] < 10000*amount:
          embed=discord.Embed(title='Not enough money',description='You dont have enough money to purchase this item!',color=discord.Colour.lighter_grey())
        else:

          if 'Banknote' not in data[str(ctx.message.author)]['inventory']:
            data[str(ctx.message.author)]['inventory']['Banknote'] = {'ID':'banknote','amount':amount}
          else:
            data[str(ctx.message.author)]['inventory']['Banknote']['amount'] += amount
          embed=discord.Embed(title='Purchase Successful',description='You successfully purchased '+str(amount)+' banknote(s)!',color=discord.Colour.magenta())
          data[str(ctx.message.author)]['wallet_balance'] -= 10000*amount
      if objecto == 'cheddar':
        if data[str(ctx.message.author)]['wallet_balance'] < 20000*amount:
          embed=discord.Embed(title='Not enough money',description='You dont have enough money to purchase this item!',color=discord.Colour.lighter_grey())
        else:
          if 'Cheddar' not in data[str(ctx.message.author)]['inventory']:
            data[str(ctx.message.author)]['inventory']['Cheddar'] = {'ID':'cheddar','amount':amount}
          else:
            data[str(ctx.message.author)]['inventory']['Cheddar']['amount'] += amount
          embed=discord.Embed(title='Purchase Successful',description='You successfully purchased '+str(amount)+' cheddar cheese(s)!',color=discord.Colour.magenta())
          data[str(ctx.message.author)]['wallet_balance'] -= 20000*amount
      if objecto == 'laptop':
        if data[str(ctx.message.author)]['wallet_balance'] < 25000*amount:
          embed=discord.Embed(title='Not enough money',description='You dont have enough money to purchase this item!',color=discord.Colour.lighter_grey())
        else:
          if 'Laptop' not in data[str(ctx.message.author)]['inventory']:
            data[str(ctx.message.author)]['inventory']['Laptop'] = {'ID':'laptop','amount':amount}
          else:
            data[str(ctx.message.author)]['inventory']['Laptop']['amount'] += amount
      if objecto == 'kalashnikov':
        if data[str(ctx.message.author)]['wallet_balance'] < 100000*amount:
          embed=discord.Embed(title='Not enough money',description='You dont have enough money to purchase this item!',color=discord.Colour.lighter_grey())
        else:
          if 'Kalashnikov' not in data[str(ctx.message.author)]['inventory']:
            data[str(ctx.message.author)]['inventory']['Kalashnikov'] = {'ID':'kalashnikov','amount':amount}
          else:
            data[str(ctx.message.author)]['inventory']['Kalashnikov']['amount'] += amount
          embed=discord.Embed(title='Purchase Successful',description='You successfully purchased '+str(amount)+' kalashkikov(s)!',color=discord.Colour.magenta())
          data[str(ctx.message.author)]['wallet_balance'] -= 25000*amount
      with open('.assets/currency.json','w') as f:
        json.dump(data, f)
      await ctx.send(embed=embed)

@client.command(aliases=['inv'])
async def inventory(ctx,page=1):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    pages_list = [1]
    if page not in pages_list:
      embed=discord.Embed(title='Page does not exist',description='The page you are tryng to search for does not exist!',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      if 'Cheddar' in data[str(ctx.message.author)]['inventory']:
        data[str(ctx.message.author)]['multiplier'] = data[str(ctx.message.author)]['inventory']['Cheddar']['amount']
      if page == 1:
        
        embed=discord.Embed(title='Inventory',color=discord.Colour.gold())
        if 'Banknote' in data[str(ctx.message.author)]['inventory']:
          embed.add_field(name='Banknote',value='Owned: '+str(data[str(ctx.message.author)]['inventory']['Banknote']['amount']),inline=False)
        if 'Cheddar' in data[str(ctx.message.author)]['inventory']:
           embed.add_field(name='Cheddar Cheese',value='Owned: '+str(data[str(ctx.message.author)]['inventory']['Cheddar']['amount']),inline=False)
           data[str(ctx.message.author)]['multiplier'] = data[str(ctx.message.author)]['inventory']['Cheddar']['amount'] 
        if 'Laptop' in data[str(ctx.message.author)]['inventory']:
           embed.add_field(name='Laptop',value='Owned: '+str(data[str(ctx.message.author)]['inventory']['Laptop']['amount']),inline=False)
        if 'Kalashnikov' in data[str(ctx.message.author)]['inventory']:
           embed.add_field(name='Kalashnikov',value='Owned: '+str(data[str(ctx.message.author)]['inventory']['Kalashnikov']['amount']),inline=False)
      with open('.assets/currency.json','w') as f:
        json.dump(data, f)
      await ctx.send(embed=embed)
    
@client.command()
async def invest(ctx):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    if 'Laptop' not in data[str(ctx.message.author)]['inventory']:
      embed=discord.Embed(title='No laptop',description='You actually need something to invest on, dumdum.',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      #⏫
      #⏬
      string = ''
      emojis = ['⏬','⏫']
      choice = ['up','down']
      if 'Banknote' in data[str(ctx.message.author)]['inventory']:  
        if_invested = random.randrange(3000, 10001) * data[str(ctx.message.author)]['inventory']['Banknote']['amount']
      else:
        if_invested = random.randrange(3000, 10001)
      randomc = random.choice(choice)
      limit = 5
      itera = 0
      while itera < limit:
        random_emoji = random.choice(emojis)
        string = string+random_emoji
        itera += 1
      await ctx.send('Which way will the stonks go?\n'+string)
      def check(m):
        return m.author == ctx.message.author
      

      msg = await client.wait_for('message',check=check)
      
      if msg.content.lower() == randomc:
        embed=discord.Embed(title='Yay!',description='You invested! You got $'+str(if_invested)+'!',color=discord.Colour.teal())
        data[str(ctx.message.author)]['wallet_balance'] += if_invested
      else:
        
        if data[str(ctx.message.author)]['wallet_balance'] < if_invested:
          bal = str(data[str(ctx.message.author)])['wallet_balance'] 
          data[str(ctx.message.author)]['wallet_balance'] = 0
          embed=discord.Embed(title='Aww!',description='You couldn\'t invest! You lost $'+str(bal)+'!',color=discord.Colour.teal())
        else:
          data[str(ctx.message.author)]['wallet_balance'] -= if_invested
          embed=discord.Embed(title='Aww!',description='You couldn\'t invest! You lost $'+str(if_invested)+'!',color=discord.Colour.teal())
      with open('.assets/currency.json','w') as f:
        json.dump(data, f)
      await ctx.send(embed=embed)

@client.command()
async def sell(ctx, objecto=None, amount=1):
  with open('.assets/currency.json','r') as f:
    data = json.load(f)
  with open('.assets/prices.json','r') as f:
    prices = json.load(f)

  
  if str(ctx.message.author) not in data:
    embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
    await ctx.send(embed=embed)
  else:
    if objecto is None:
      embed=discord.Embed(title='No object given',description='Give an effing object, dumdum!',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      price = (prices[objecto]/2)*amount
      data[str(ctx.message.author)]['inventory'][objecto.capitalize()]['amount'] -= amount
      data[str(ctx.message.author)]['wallet_balance'] += price
      embed=discord.Embed(title='Sale successful',description='You successfuly sold '+str(amount)+' '+objecto+'(s)!',color=discord.Colour.gold())
      await ctx.send(embed=embed)
      with open('.assets/currency.json','w') as f:
        json.dump(data, f)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def chore(ctx):
  try:

    with open('.assets/currency.json','r') as f:
      data = json.load(f)
    with open('.assets/prices.json','r') as f:
      prices = json.load(f)

  
    if str(ctx.message.author) not in data:
      embed=discord.Embed(title='Error',description='You need to register for the game to play it! Do ```e!start``` to register!',color=discord.Colour.lighter_grey())
      await ctx.send(embed=embed)
    else:
      #chore_list = ['clean','cook','wash']
      chore_list = ['wash','clean','cook']
      random_chore = random.choice(chore_list)
      def check(m):
        return m.author == ctx.message.author
      payment = random.randrange(3000, 5001)
      yay = discord.Embed(title='Yay!',description='You did a chore and got $'+str(payment)+'!',color=discord.Colour.teal())
      no = discord.Embed(title='Aww!',description='You could not do the chore, so you didn\'nt get anything! Sad life...',color=discord.Colour.teal())
    
      if random_chore == 'clean':
      
      
        await ctx.send('Type \'sweep\' in the chat 5 times! Go Go Go!')
        msg = await client.wait_for('message',check=check)
        if msg.content.count('sweep') == 5:
          await ctx.send(embed=yay)
          data[str(ctx.message.author)]['wallet_balance'] += payment
        else:
          await ctx.send(embed=no)
      if random_chore == 'cook':
        await ctx.send('Emoji match! Type the emoji below in the chat now!')
        await ctx.send('\n🍳')
        msg = await client.wait_for('message',check=check)
        if '🍳' in msg.content:
          await ctx.send(embed=yay)
          data[str(ctx.message.author)]['wallet_balance'] += payment
        else:
          await ctx.send(embed=no)
      if random_chore == 'wash':
        steps = ['put soap','rub','dry','leave for 30 mins','put on pile']
        steps2 = ['put soap','rub','leave for 30 mins','dry','put on pile']
        randomized = []
        random2 = random.choice(steps2)
        randomized.append(random2)
        steps2.remove(random2)
        random2 = random.choice(steps2)
        randomized.append(random2)
        steps2.remove(random2)
        random2 = random.choice(steps2)
        randomized.append(random2)
        steps2.remove(random2)
        random2 = random.choice(steps2)
        randomized.append(random2)
        steps2.remove(random2)
        random2 = random.choice(steps2)
        randomized.append(random2)
        steps2.remove(random2)






        
        string = ''
        for items in randomized:
          string += items
          string += '\n'
        await ctx.send('Sequence the following!\n\nMake sure to seperate all the phrases with a **\'/\'**!\n\n```'+string.title()+'```')
        msg = await client.wait_for('message',check=check)
        inputs = []
        if msg.content.count('/') < 4:
          await ctx.send(embed=no)
        else:
          inputs = msg.content.split('/')
          
          string = ''
          for items in inputs:
            if items == steps[inputs.index(items)]:
              string += 'n'
            else:
              await ctx.send(embed=no)



        
          if string.count('n') == 5:
            await ctx.send(embed=yay)
            data[str(ctx.message.author)]['wallet_balance'] += payment
      if random_chore == 'feed':
        sayings = ['C\mere doggo!','Stop right there!','I\'ve got some tasty food for you!']
        random_saying = random.choice(sayings)
        msg = await client.wait_for('message',check=check)
        if msg.content == random_saying:
          await ctx.send(embed=yay)
        else:
          await ctx.send(embed=no)

      with open('.assets/currency.json','w') as f:
        json.dump(data, f)
  except Exception as f:
    await ctx.send(f)
    print(f)
    traceback.print_exc()
'''

client.loop.create_task(load_cogs())
client.loop.create_task(startup())
client.run('TOKEN')
