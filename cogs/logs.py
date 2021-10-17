import discord
from discord.ext import commands 
import json
from datetime import datetime
class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.group(name='logs', invoke_without_command=True)
    async def logs(self,ctx):
        try:    
            detect = open("./logchan.json")
            object = json.load(detect)
            guild = ctx.guild
            chan= object[str(guild.id)]
            chan = discord.utils.get(guild.channels,id=chan)
            embed=discord.Embed(title="logging channel settuped for the guild",
            description=f"{chan.mention} ", color=0x04fb42)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="logs channel not settuped", description=f"Not sending changes in any channel", color=0xFE0000)
            embed.set_footer(text=f'Use (v!logs add #channel) command if you want to setup logs')
            await ctx.send(embed=embed)

    @logs.command()
    async def add(self,ctx,channel:discord.TextChannel):
        cdata = open("./logchan.json", "r")
        channel_object = json.load(cdata)
        cdata.close()
        guild = ctx.guild
        channel_object[guild.id] = channel.id
        cdata = open("./logchan.json", "w")
        json.dump(channel_object, cdata,indent=4)
        cdata.close()

        embed=discord.Embed(title="Log channel added successfully ", description=f"sending changes in {channel.mention} from now", color=0x04fb42)
        embed.set_footer(text=f'Setted By - {ctx.author}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @logs.command()
    async def remove(self,ctx):
        try:
            with open("./logchan.json","r") as f:
                roles = json.load(f)
            guild = ctx.guild
            roles.pop(str(guild.id))
            with open("./logchan.json","w") as f:
                json.dump(roles,f,indent=4)

            embed=discord.Embed(title="Removed", description=f"Succesfuly disabled channel logging", color=0xFE0000)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="Failed", description=f"Not found", color=0xFE0000)
            await ctx.send(embed=embed) 


    @commands.Cog.listener()
    async def on_member_update(self,before,after):
                  if before.display_name != after.display_name:
                    detect = open("./logchan.json")
                    object = json.load(detect)
                    guild = after.guild
                    chan= object[str(guild.id)]           
                    chan = discord.utils.get(guild.channels,id=chan)
                    log_channel = chan
                    embed = discord.Embed(tittle='Member Update',
                        description='Nickname changed',
                        color=after.colour,
                        timestamp=datetime.utcnow())

                    fields = [("Before",before.display_name,False),
                                ("After",after.display_name,False)]
                    for name, value, inline in fields:                 
                        embed.add_field(name=name,value=value,inline=inline)
                    await log_channel.send(embed=embed)

    


def setup(bot):
    bot.add_cog(logs(bot)) 
