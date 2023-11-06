import discord
import time
import re
import os  # default module
from dotenv import load_dotenv
import requests

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {'ids': 'litecoin', 'vs_currencies': 'usd'}

responsei = requests.get(url, params=params)
i2c_rate = 90
usdc_to_inr_rate = 73.0
if responsei.status_code == 200:
    data = responsei.json()
    ltc_price = data['litecoin']['usd']
else:
    print('not got data')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Game(name='Made By Google'))

async def is_owner(ctx):
    return ctx.author.id == 1166699997165801493

@bot.slash_command(name = "set_i2c", description = "set the rate of inr to crypto")
async def set_i2c(ctx, rate: float):
    global i2c_rate
    i2c_rate = rate
    await ctx.respond(f'i2c_rate set to **{i2c_rate}**')

@bot.slash_command(name = "i2c", description = "use it to get i2c perfect rate by entering inr")
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    usd_amount = amount / i2c_rate
    await ctx.respond(f"> __Given Amount Is Equivalent To__ = **${usd_amount:.2f}**")

@bot.slash_command(name = "set_c2i", description = "set the rate of cryto to inr")
async def set_usdc_to_inr_rate(ctx, rate: float):
    global usdc_to_inr_rate
    usdc_to_inr_rate = rate
    await ctx.respond(f'Usd to INR rate set to {usdc_to_inr_rate}')

@bot.slash_command(name = "c2i", description = "use it to get i2c perfect rate by entering inr")
async def c2i(ctx, amount: float):
    inr_amount = amount * usdc_to_inr_rate
    await ctx.respond(f"> **{amount}** USD is equivalent to ₹**{inr_amount:.2f}**")

@bot.slash_command(name="ltc", description="get the ltc price")
async def ltcp(ctx):
    await ctx.respond(f'THE PRICE OF LTC IS **{ltc_price}**')


class ltcbalance(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Ltcadress"))

    async def callback(self, interaction: discord.Interaction):
        ltcaddress = self.children[0].value
        response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
        if response.status_code == 200:
            data = response.json()
            balance = data['balance'] / 10 ** 8
            total_balance = data['total_received'] / 10 ** 8
            unconfirmed_balance = data['unconfirmed_balance'] / 10 ** 8
        else:
            print('there is an fetching error linme 141')

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        if cg_response.status_code == 200:
            usd_price = cg_response.json()['litecoin']['usd']
        else:
            print('ltc bal working')

        usd_balance = balance * usd_price
        usd_total_balance = total_balance * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price
        embed = discord.Embed(title="LTC BAL")
        embed.add_field(name='BAL IN USD', value=f'**{usd_balance:.2f}USD**', inline=True)
        embed.add_field(name='TOTAL NETWORTH', value=f'**{usd_total_balance:.2f}USD**', inline=True)
        embed.add_field(name='UNCONFIRMED BALANCE', value=f'**{usd_unconfirmed_balance:.2f}USD**', inline=True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1163042245373591632/1165249823730061322/1697886994017.jpg?ex=65462a77&is=6533b577&hm=b999a88620a221d39d55ae11dc37f6e44871e47f1a4b79f2c7c98580bc5b6e08&")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157697137547694150/1165496313476034610/imgonline-com-ua-ReplaceColor-oCkInAGTdjtIXhmD.jpg?ex=65471007&is=65349b07&hm=b7a5cdf2010341ed61943d7837704b7feb6f5fb2052f87ec89ad2817347b2e24&")
        await interaction.response.send_message(embeds=[embed])


@bot.slash_command()
async def checkbal(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = ltcbalance(title="Check the balance of your ltc address")
    await ctx.send_modal(modal)


class exhash(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="GIVE URL GET HASH"))

    async def callback(self, interaction: discord.Interaction):
        def extract_hash(url):
            parts = url.split('/')
            return parts[-1]

        # Example usage
        url1 = self.children[0].value
        result1 = extract_hash(url1)
        print(result1)

        embed = discord.Embed(title="THIS IS YOUR HASH")
        embed.add_field(name="YOUR HASH", value=f"**{result1}**")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1163042245373591632/1165249823730061322/1697886994017.jpg?ex=65462a77&is=6533b577&hm=b999a88620a221d39d55ae11dc37f6e44871e47f1a4b79f2c7c98580bc5b6e08&")
        await interaction.response.send_message(embeds=[embed])


@bot.slash_command()
async def extracthash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = exhash(title="Extract hash using slash")
    await ctx.send_modal(modal)

class checktransaction(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Check transaction of ltc using hash"))

    async def callback(self, interaction: discord.Interaction):
        transaction_hash = str(self.children[0].value)

        # Fetch transaction details from BlockCypher
        blockcypher_url = f"https://api.blockcypher.com/v1/ltc/main/txs/{transaction_hash}"
        response = requests.get(blockcypher_url)
        data = response.json()

        if "outputs" in data and len(data["outputs"]) > 0:
            confirmations = data["confirmations"]
            amount_in_ltc = data["outputs"][0]["value"] / 10 ** 8

            # Fetch current LTC to USD exchange rate from CoinGecko
            coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
            coingecko_response = requests.get(coingecko_url)
            coingecko_data = coingecko_response.json()
            if confirmations >= 1:
                confirmation_status = "<a:tick:1165503411693834240>"
            else:
                confirmation_status = "<:wrong:1165503543915053107>"

            if "litecoin" in coingecko_data and "usd" in coingecko_data["litecoin"]:
                ltc_to_usd = coingecko_data["litecoin"]["usd"]
                amount_in_usd = amount_in_ltc * ltc_to_usd
        embed = discord.Embed(title="HERE IS TRANSACTION DETAIL")
        embed.add_field(name="Amount in LTC", value=f"**{amount_in_ltc: .2f}LTC**", inline=True)
        embed.add_field(name="Amount in USD", value=f"**{amount_in_usd: .2f}$**", inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name="Status", value=f"\u200b**{confirmation_status}**", inline=True)
        embed.add_field(name="Confirmations", value=f"**{confirmations}**", inline=True)
        embed.set_author(name="PIRATE TRANSACTIONS", icon_url="https://media.discordapp.net/attachments/1163042245373591632/1165249823730061322/1697886994017.jpg?width=473&height=473")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1163042245373591632/1165249823730061322/1697886994017.jpg?ex=65462a77&is=6533b577&hm=b999a88620a221d39d55ae11dc37f6e44871e47f1a4b79f2c7c98580bc5b6e08&")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157697137547694150/1165496313476034610/imgonline-com-ua-ReplaceColor-oCkInAGTdjtIXhmD.jpg?ex=65471007&is=65349b07&hm=b7a5cdf2010341ed61943d7837704b7feb6f5fb2052f87ec89ad2817347b2e24&")
        await interaction.response.send_message(embeds=[embed])

@bot.slash_command()
async def checkconfirmations(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = checktransaction(title="GET FULL DETAILS ABOUT TRANSACTION")
    await ctx.send_modal(modal)

@bot.slash_command(name="calculate", description="Perform a calculation")
async def calculate(ctx, operation: str, num1: float, num2: float):
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            await ctx.respond("Error: Division by zero")
            return
    else:
        await ctx.respond("Invalid operator. Please choose from +, -, *, /")
        return
    
    await ctx.respond(f"***The result is: {result: .1f}***")


async def help(ctx):
    embed = discord.Embed(
        title="help",
        description="Get the bot usage",
        color=discord.Colour.red(),  # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="/checkbal",
                    value="**use this command enter you ltc adfress to get you balance of wallet**")

    embed.add_field(name="/checkconfirmations", value="**get details of the given hash of ltc**", inline=True)
    embed.add_field(name="/exthash", value="**get the hash from any transaction url**", inline=True)
    embed.add_field(name="/Ltc", value="**Get the price of ltc in $**", inline=True)
    embed.add_field(name="/Currency Exchnage", value="**Get the fiat convertion rate**", inline=True)

    embed.set_footer(text="From Team Pirate!")  # footers can have icons too
    embed.set_author(name="PIRATE TRANSACTIONS", icon_url="https://media.discordapp.net/attachments/1163042245373591632/1165249823730061322/1697886994017.jpg?width=473&height=473")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1163042245373591632/1165249823730061322/1697886994017.jpg?width=473&height=473")
    embed.set_image(url="https://media.discordapp.net/attachments/1157697137547694150/1165496313476034610/imgonline-com-ua-ReplaceColor-oCkInAGTdjtIXhmD.jpg?width=840&height=473")

    await ctx.respond("Here is Help Command .", embed=embed)  # Send the embed with some text

class Fiatexchange(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="FROM WHICH CURRENCY"))
        self.add_item(discord.ui.InputText(label="TO WHICH"))
        self.add_item(discord.ui.InputText(label="AMOUNT"))

    async def callback(self, interaction: discord.Interaction):
        from_currency = str(self.children[0].value).upper()

        to_currency = str(self.children[1].value).upper()
        amount = float(self.children[2].value)

        response = requests.get(
            f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")
        value = response.json()['rates'][to_currency]
        embed = discord.Embed(title="Exchange Result")
        embed.add_field(name="**VALUE**", value=f"{amount} {from_currency} is {value} {to_currency}", inline=True)
        embed.set_author(name="PIRATE TRANSACTIONS", icon_url="https://media.discordapp.net/attachments/1157697137547694150/1165496313476034610/imgonline-com-ua-ReplaceColor-oCkInAGTdjtIXhmD.jpg")
        await interaction.response.send_message(embeds=[embed])

@bot.slash_command()
async def currencyexchange(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = Fiatexchange(title="Get the exchange rate!! Not crypto")
    await ctx.send_modal(modal)

bot.run("MTE2NDc4OTYwOTEwOTEzMTI5NA.GPbwc8.HzbIuedxoWr-ajlE5K6UeTJTZ9ROcDqyyEg7xc")