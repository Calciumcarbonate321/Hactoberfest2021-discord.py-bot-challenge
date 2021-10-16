import discord
from discord.ext import commands
import json

class Events(commands.Cog):
    def __init__(self,client):
        self.bot = client


    @commands.Cog.listener()
    async def on_member_join(self,member):
        detectjoin = open("./autorole.json")
        object = json.load(detectjoin)
        guild = member.guild
        role= object[str(guild.id)]
        role = discord.utils.get(guild.roles,id=role)
        await member.add_roles(role)


def setup(client):
    client.add_cog(Events(client)) 
