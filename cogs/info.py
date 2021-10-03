import discord
from discord.ext import commands
from datetime import datetime
from utils.views import Delete

class Informative(commands.Cog):
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
        msg=await ctx.send(embed=embed,view=view)
        await view.wait()
        if view.value is True:
            await msg.delete()

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
        msg=await ctx.send(embed=embed,view=view)
        await view.wait()
        if view.value is True:
            await msg.delete()

def setup(client):
    client.add_cog(Informative(client))