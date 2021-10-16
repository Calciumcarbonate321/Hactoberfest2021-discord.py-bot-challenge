from attr import fields
import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import aiohttp
import functools
from typing import Union

class ImageManipulation(commands.Cog):
    def __init__(self,client):
        self.client=client
        self.session=aiohttp.ClientSession(loop=client.loop)

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        avatar_url = user.avatar.url
        async with self.session.get(avatar_url) as r:
            avatar_bytes = await r.read()
        return avatar_bytes
    
    def wantedimage(self,avatar):
        path = './assets/wanted.jpg'
        with Image.open(path) as wimg:
            with Image.open(avatar) as pfp:
                pfp=pfp.resize((111,111))
                wimg.paste(pfp,(33,98))
                buffer=BytesIO()
                wimg.save(buffer,"png")
                buffer.seek(0)
                return buffer   

    def worryimage(self,avatar):
        path = './assets/worry.jpg'
        with Image.open(path) as wimg:
            with Image.open(avatar) as pfp:
                pfp=pfp.resize((63,63))
                wimg.paste(pfp,(68,14))
                buffer=BytesIO()
                wimg.save(buffer,"png")
                buffer.seek(0)
                return buffer



    @commands.command()
    async def wanted(self,ctx,member:Union[discord.User, discord.Member]=None):
        user = ctx.message.author if member is None else member
        avatar = BytesIO(await user.display_avatar.read())
        partialfunc=functools.partial(self.wantedimage,avatar)
        buffer=await self.client.loop.run_in_executor(None,partialfunc)
        await ctx.send(file=discord.File(fp=buffer,filename="wanted.png"))

    @commands.command()
    async def worry(self,ctx,member:Union[discord.User, discord.Member]=None):
        user=ctx.message.author if member is None else member
        avatar=BytesIO(await user.display_avatar.read())
        partialfunc=functools.partial(self.worryimage,avatar)
        buffer=await self.client.loop.run_in_executor(None,partialfunc)
        await ctx.send(file=discord.File(fp=buffer,filename="worry.png"))


def setup(client):
    client.add_cog(ImageManipulation(client))