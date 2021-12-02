import discord
from discord.ext import commands,menus
from discord import ui
from itertools import starmap,chain
from datetime import datetime
from utils.views import Delete
from utils.buttons import LinkButton


class Informative(commands.Cog):
    """Some informative commands regarding the bot and the user."""
    def __init__(self,client):
        self.client=client

    @commands.command(name="uptime",help="This command shows how much time the bot has been online for.")
    async def uptime(self,ctx):
        ctime=datetime.utcnow()
        elapsed=ctime-self.client.starttime
        seconds = elapsed.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        embed=discord.Embed(title="Bot's uptime",description="Bot has been running for {}d {}h {}m {}s".format(elapsed.days, hours, minutes, seconds))
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        view=Delete(ctx.author)
        await ctx.send(embed=embed,view=view)


    @commands.command()
    async def userinfo(self,ctx, user: discord.Member = None): 
        if isinstance(ctx.channel,discord.DMChannel):
            await ctx.send("This command can only be used in servers,sorry.You can do e!invite to get my invite.")
        if user is None:
            user = ctx.author
        print(user)
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        if user.avatar:
            embed.set_author(name=str(user), icon_url=user.avatar.url)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join(
            str(p[0]).replace("_", " ").title()
            for p in user.guild_permissions
            if p[1]
        )

        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        view=Delete(ctx.author)
        await ctx.send(embed=embed,view=view)

    @commands.command(name="invite")
    async def invite(self,ctx):
        inv=await self.client.get_invite()
        view=discord.ui.View()
        view.add_item(LinkButton("Invite link",url=inv))
        embed=discord.Embed(title="Bot invite",description="Click on the button below to invite me.")
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.me.avatar.url)
        await ctx.send(embed=embed,view=view)

    @commands.command(name="source",help="Shows the source code of specified command.")
    async def source(self,ctx,*,command:str=None):
        if command is None:
        
    
def setup(client):
    client.add_cog(Informative(client))
