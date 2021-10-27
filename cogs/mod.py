import discord
from discord.ext import commands
from discord.utils import get
import json

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command(name="ban",help="This command can be used to ban someone from the server, the bot and you need to have 'ban members' permission.")
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ban(self,ctx,member:discord.Member,*,reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.ban(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.send(f"Banned {member} successfully.")
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")

    @commands.command(name="kick",help="This command can be used to kick someone from the server, the bot and you need to have 'kick members' permission.")
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def kick(self,ctx,member:discord.Member,*,reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.kick(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.send(f"Kicked {member} successfully.")
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")

    @commands.command(name="purge",aliases=["clear"],help="You can use this to clear bulk messages, maximum limit is 500 messages.")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def purge(self, ctx, amount: int = 10):
        if amount <= 500:
            e = await ctx.channel.purge(limit=amount)
            await ctx.send("Successfully purged `{len(e)}` messages")
        else:
            await ctx.reply("Sorry, the maximum amount of messages you can purge is 500, please run the multiple times if you wish to purge more.")
            self.client.get_command("purge").reset_cooldown(ctx)

    @commands.command(name="setnick",aliases=["nick"],help="Changes the nick name of the specified person, defaults to `no nick` if a nickname isn't specified.")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nickname: str = "no nick"):
        if ctx.author.top_role.position > member.top_role.position:
            await member.edit(nick=nickname)
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")

    @commands.command(name="unban",help="Unbans a member from the server, you must provide a valid user id.")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)    
    @commands.cooldown(1,5,commands.BucketType.user)
    async def unban(self,ctx,memberid:int=None):
        member = discord.Object(id=memberid) 
        try:
            await ctx.guild.unban(member)
        except:
            await ctx.send("Sorry, a user with that id was not found or isn't a previously banned member.")

    @commands.command(name="setprefix",help="This command changes the bot's prefix for the server.")
    @commands.has_permissions(administrator=True)
    async def setprefix(ctx, prefix):
        with open('./assets/prefixes.json','r')as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = str(prefix)
        with open('.assets/prefixes.json','w') as f:
            json.dump(prefixes,f)
        embed = discord.Embed(title='Prefix for this server changed',description='Prefix for this server has been changed to '+str(prefix)+'.',color=discord.Colour.purple())
        await ctx.send(embed=embed)

    @commands.group()
    async def slowmode(self,ctx, seconds: int=5):   
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @slowmode.command()
    async def remove(self,ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send('removed slowmode for the channel')

    @commands.command(name="pin",help="Pins the message with the specified ID to the current channel")
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, id:int):      
        message = await ctx.channel.fetch_message(id)
        await message.pin()
        await ctx.send("Successfully pinned that msg")

    @commands.command(name="unpin",help="Unpins the message with the specified ID from the current channel")
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, id:int):
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=id)
        await message.unpin()
        await ctx.send("Successfully unpinned that msg")
        
        
    @commands.command(name="removereactions",help="Clear reactions from a message in the current channel")
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id:int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")


def setup(client):
    client.add_cog(Moderation(client))
