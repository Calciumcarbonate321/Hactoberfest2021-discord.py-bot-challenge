import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    '''This cog has the bank commands of the bot economy'''
    def __init__(self,client):
        self.client=client

    async def get_wallet(self,user_id :int):
        async with self.client.db.execute(f"SELECT * FROM bankdata WHERE userid={user_id}") as cursor:
            e=await cursor.fetchone()
            return e[1]

    async def get_bal(self,user_id :int):
        async with self.client.db.execute(f"SELECT * FROM bankdata WHERE userid={user_id}") as cursor:
            e=await cursor.fetchone()
            return e[2]

    async def create_account(self,user_id):
        async with self.client.db.execute(f"SELECT * FROM bankdata WHERE userid={user_id}") as c:
            e=await c.fetchall()
            if len(e)==0:
                await self.client.db.execute(f"INSERT INTO bankdata (userid,wallet,bankbal,daily) VALUES ({user_id},0,0,0)")
                await self.client.db.commit()
            
    async def get_daily_streak(self,user_id):
        async with self.client.db.execute(f"SELECT * FROM bankdata WHERE userid={user_id}") as cursor:
            e=await cursor.fetchone()
            return e[3]

    async def update_daily_streak(self,user_id):
        current=await self.get_daily_streak(user_id)
        new=current+1
        await self.client.db.execute(f"UPDATE bankdata SET daily={new} WHERE userid={user_id}")
        await self.client.db.commit()
    
    async def get_bank_limit(self,user_id):
        return 1000000

    async def add_money(self,user_id,amount : int):
        current=await self.get_wallet(user_id)
        new=current+amount
        await self.client.db.execute(f"UPDATE bankdata SET wallet = {new} WHERE userid={user_id}")
        await self.client.db.commit()

    async def remove_money(self,user_id,amount : int):
        current=await self.get_wallet(user_id)
        new=current-amount
        await self.client.db.execute(f"UPDATE bankdata SET wallet = {new} WHERE userid={user_id}")
        await self.client.db.commit()
                
    async def add_money_bank(self,user_id,amount : int):
        current=await self.get_bal(user_id)
        new=current+amount
        await self.client.db.execute(f"UPDATE bankdata SET bankbal = {new} WHERE userid={user_id}")
        await self.client.db.commit()

    async def remove_money_bank(self,user_id,amount : int):
        current=await self.get_bal(user_id)
        new=current-amount
        await self.client.db.execute(f"UPDATE bankdata SET bankbal = {new} WHERE userid={user_id}")
        await self.client.db.commit()

    @commands.command(name='balance',aliases=['bal'],help="This command will show your bank and wallet details.")
    async def bank_balance(self,ctx,user : discord.User=None):
        if user is None:
            user=ctx.author
        userid=user.id
        await self.create_account(userid)

        wallet=await self.get_wallet(userid)
        bank_bal=await self.get_bal(userid)
        bank_limit=await self.get_bank_limit(userid)

        embed=discord.Embed(title=f"{user.name}'s bank")
        embed.add_field(name="Wallet",value=f"⌬`{wallet}`")
        embed.add_field(name="Bank",value=f"⌬`{bank_bal}`/`{bank_limit}`",inline=False)
        embed.set_footer(text=f"Command invoked by {ctx.author.name}",icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)        

    @commands.command(name="withdraw",aliases=['with'],help="You can use this command to withdraw money from your bank.(can use `max` or `all` instead of an amount to withdraw all the money.)")
    async def witho(self,ctx,amount :str=None):      
        userid=ctx.author.id
        await self.create_account(userid)
        if amount is None:
            await ctx.send("What are you withdrawing you idiot")
            return
        amount=amount.lower()
        if amount not in ["max", "all"]:
            try:
                amount=int(amount)
            except:
                await ctx.send("You haven't entered a valid number")
                return
            else:
                if amount<0:
                    await ctx.send("The amount that you want to withdraw must be a whole number greater than 0.")
                    return              

        if amount in ["max", "all"]:
            amount=await self.get_bal(userid)

        bankbal=await self.get_bal(userid)
        if amount>bankbal:
            await ctx.send(f"You don't even have that much money in your bank, you have only ⌬{bankbal}")
        else:
            await self.add_money(userid,amount)
            await self.remove_money_bank(userid,amount)
            await ctx.send(f"You have withdrawn ⌬{amount}, your current wallet balance is ⌬{await self.get_wallet(userid)} and you have ⌬{await self.get_bal(userid)} in your bank")
        return

    @commands.command(name="deposit",aliases=['dep'],help="You can use this command to deposit some money from your bank.(can use `max` or `all` instead of an amount to deposit maximum money.)")
    async def depo(self,ctx,amount :str=None):      
        userid=ctx.author.id
        await self.create_account(userid)
        if amount is None:
            await ctx.send("What are you depositing you idiot")
            return
        amount=amount.lower()
        if amount not in ["max", "all"]:
            try:
                amount=int(amount)
            except:
                await ctx.send("You haven't entered an invalid number")
                return
            else:
                if amount<0:
                    await ctx.send("The amount that you want to deposit must be a whole number greater than 0.")
                    return              

        if amount in ["max", "all"]:
            amount=await self.get_wallet(userid)
            amount=int(amount)

        bankbal=await self.get_bal(userid)
        banklimit=await self.get_bank_limit(userid)
        wallet=await self.get_wallet(userid)

        if amount>wallet:
            await ctx.send(f"You don't even have that much money in your wallet, you have only ⌬{wallet}")
        elif amount+bankbal>banklimit:
            new_amount=banklimit-bankbal
            await self.add_money_bank(userid,new_amount)
            await self.remove_money(userid,new_amount)
            await ctx.send("Your bank is now full")
        elif bankbal==banklimit:
            await ctx.send("You have a full bank kiddo")
        else:
            await self.add_money_bank(userid,amount)
            await self.remove_money(userid,amount)
            await ctx.send(f"You have deposited ⌬{amount}, your current wallet balance is ⌬{await self.get_wallet(userid)} and you have ⌬{await self.get_bal(userid)} in your bank")
        return

    @commands.command(name="share",aliases=['give'],help="You can share some bot currency to other users with this command.")
    async def givemoney(self,ctx,user: discord.User,amount : int=None):
        try:
            userid=user.id
            authid=ctx.author.id
            await self.create_account(userid)
            await self.create_account(authid)
            authbal=await self.get_wallet(authid)
            if authbal<amount:
                await ctx.send("You don't even have that much money bruh")
                return
            if user is None or amount is None:
                await ctx.send("The correct format to do this command is `>give @user amount`")
                return

            await self.add_money(userid,amount)
            await self.remove_money(authid,amount)
            await ctx.send(f"You gave ⌬{amount} to {user.name}")
        except:
            await ctx.send("There was some error when running this command,make sure the format is correct, the correct format : `>give @user amount`")

    @commands.command(name="beg",help="When you are desperate for bot currency, you can _beg_")
    @commands.cooldown(1,30,commands.BucketType.user)
    async def beg(self,ctx):
        userid=ctx.author.id
        payout = random.randint(0,800)
       
        payout = int(payout)
        
        if payout==0:
            embed=discord.Embed(title="Begging unsuccessful",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",color=discord.Colour.red())
            embed.add_field(name="Sadge",value="You earned nothing by begging")
            embed.set_footer(text="Try begging again after sometime",icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return 
        elif payout > 800:
            extra = (payout-800)
            extra = int(extra)
            tpo = (payout - extra)
            tpo = int(tpo)
            embed=discord.Embed(title="Begging successful",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",color=discord.Colour.red())
            embed.add_field(name="Nice job",value= f"You earned ⌬`{tpo}`by begging, and you get an additional ⌬`{extra}` since you have a *Lucky Charm*")
            embed.set_footer(text="Good job mate",icon_url=ctx.author.avatar.url)
            await self.add_money(userid,payout)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Begging successful",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",color=discord.Colour.red())
            embed.add_field(name="Nice job",value=f"You earned ⌬`{payout}`by begging")
            embed.set_footer(text="Good job mate",icon_url=ctx.author.avatar.url)
            await self.add_money(userid,payout)
            await ctx.send(embed=embed)

    @commands.command(name="gamble",aliases=['bet','rolls'],help="A simple gambling command where you can bet your bot currency.")
    async def gamble(self,ctx,amount : int=None):
        if amount is None:
            await ctx.semd("You should actually bet some money in this.")
        user_roll=random.randint(1,12)
        bot_roll=random.randint(1,12)
        payout=random.randint(50,200)
        userid=ctx.author.id
        balance=await self.get_wallet(userid)

        if balance<amount:
            await ctx.send("You don't have that much money")   
            return
        if amount<=0:
            await ctx.send("The bet amount should be greater than 0")
            return

        if user_roll>bot_roll:
            await self.add_money(userid,int(amount*payout/100))
            embed=discord.Embed(title=f"{ctx.author.name}'s winning gambling game",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",color=discord.Colour.green())
            embed.add_field(name=f"{ctx.author.name}",value=f"{user_roll}")
            embed.add_field(name=f"{str(self.client.user)[:-5]}",value=f"{bot_roll}")
            embed.add_field(name="Percent won",value=f"{payout}%")
            embed.add_field(name="Amount won",value=f"{int(amount*payout/100)}⌬")
            embed.set_footer(text="Congratulations on winning",icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        elif user_roll<bot_roll:
            await self.remove_money(userid,amount)
            embed=discord.Embed(title=f"{ctx.author.name}'s losing gambling game",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",color=discord.Colour.red())
            embed.add_field(name=f"{ctx.author.name}",value=f"{user_roll}")
            embed.add_field(name=f"{str(self.client.user)[:-5]}",value=f"{bot_roll}")
            embed.add_field(name=f"You lost ⌬{amount}",value="Better luck next time")
            embed.set_footer(text="F you lost",icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        elif user_roll==bot_roll:
            embed=discord.Embed(title=f"{ctx.author.name}'s tied gambling game",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",color=0xe67e22)
            embed.add_field(name=f"{ctx.author.name}",value=f"{user_roll}")
            embed.add_field(name=f"{str(self.client.user)[:-5]}",value=f"{bot_roll}")
            embed.add_field(name="That's a tie",value="You lost nothing nor did you gain anything")
            embed.set_footer(text="That was a dramatic tie",icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(name="rob",help="This command is used to rob an user of their bot currency, there is a chance that you will fail the robbery and will pay a fine to that user.")
    @commands.cooldown(1,30,type=commands.BucketType.user)
    async def rob(self,ctx,user : discord.User=None):
        if user is None:
            await ctx.send("Who are you robbing dum dum")
            return
        userid=user.id
        authid=ctx.author.id
        user_bal=await self.get_wallet(userid)
        auth_bal= await self.get_wallet(authid)

        if user_bal==0:
            await ctx.send(f"{user.name} doesn't even have money in their wallet")
            return

        isRobFailed=random.randint(0,5)
        if isRobFailed==0:
            amountlost=random.randint(0,auth_bal)
            await ctx.send(f"F you got caught while robbing and paid them ⌬{amountlost}")
            await self.remove_money(authid,amountlost)
            await self.add_money(userid,amountlost)
        else:
            amountgained=random.randint(0,user_bal)
            await ctx.send(f"You stole ⌬{amountgained} from {user.name}")
            await self.remove_money(userid,amountgained)
            await self.add_money(authid,amountgained)

    @commands.command(name="daily",help="This command can be used once every 24h, it gives you some coins and the number of coins depend on your daily streak.")
    @commands.cooldown(1,86400,commands.BucketType.user)
    async def daily(self,ctx):
        userid=ctx.author.id
        await self.create_account(userid)
        amount=10000
        streak=await self.get_daily_streak(userid)
        bonus=streak*100
        await self.update_daily_streak(userid)
        amount += bonus
        await self.add_money(userid,amount)

        embed=discord.Embed(title="Here are your daily coins", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description=f"**⌬{amount}** was placed in your wallet")
        embed.add_field(
            name='You can get atleast ⌬10000 by using this command once every 24 hours',
            value="The amount that you get depends on your daily streak",
            inline=False,
        )

        embed.set_footer(text=f"Current daily streak={await self.get_daily_streak(userid)}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))

        
