import wavelink
from discord.ext import commands

class Music(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def cog_check(self, ctx):
        if not ctx.guild:
            await ctx.send('Music commands are not available in Private Messages.')
            return False
        return True

    async def connect_nodes(self):
        await self.bot.wait_until_ready()

        self.bot.wlink=await wavelink.NodePool.create_node(bot=self.bot,
                                            host='HOST',
                                            port=PORT,
                                            password='PASSWORD')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')

    @commands.command(name="play",aliases=["p"],help="Play a song with the given search query.If not connected, connect to our voice channel.")
    async def play(self, ctx, *,search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            await ctx.send("empty q")
            await vc.play(search)
            return
        vc.queue.put(search)
        await ctx.send(f"Started playing {search}")
    
    @commands.group(name="queue",aliases=["q"],help="Displays the current queue.")
    async def q(self,ctx):
        p=self.bot.wlink.get_player(ctx.guild)
        await ctx.send(p.queue)

    @q.command(name="clear",help="Clears the queue.")
    async def cq(self,ctx):
        p=self.bot.wlink.get_player(ctx.guild)
        await p.clear()
        await ctx.message.add_reaction("👌")
        await ctx.send("Cleared the queue.")

    @commands.command(name="skip",aliases=["next"],help="Skips the current audio.")
    async def _skip(self,ctx):
        p=self.bot.wlink.get_player(ctx.guild)
        nt=p.queue.get()
        await p.play(nt)
        await ctx.send(f"now playing {nt}")

    @commands.command(name="stop",help="Stops the player.")
    async def stop(self,ctx):
        player=self.bot.wlink.get_player(ctx.guild)
        await player.stop() 
        await ctx.message.add_reaction("👌")
        await ctx.send("Successfully stopped.")

    @commands.command(name="pause",help="Pauses the player, can be resumed later.")
    async def pause(self,ctx):
        player=self.bot.wlink.get_player(ctx.guild)
        if player.is_paused():
            return await ctx.send("Player is already paused.")
        await player.pause()
        await ctx.message.add_reaction("👌")
        await ctx.send("Successfully paused.")   

    @commands.command(name="resume",help="Resumes a paused player.")
    async def pause(self,ctx):
        player=self.bot.wlink.get_player(ctx.guild)
        if not player.is_paused():
            return await ctx.send("The player is not paused.")
        await player.pause()
        await ctx.message.add_reaction("👌")
        await ctx.send("Successfully resumed.") 

    @commands.command(name="disconnect",help="Disconnects the bot from the vc.")
    async def discon(self,ctx):
        player=self.bot.wlink.get_player(ctx.guild)
        await player.disconnect(force=True)
        await ctx.message.add_reaction("👌")
        await ctx.send("Successfully disconnected :+1:")
    
    

def setup(client):
    client.add_cog(Music(client))
