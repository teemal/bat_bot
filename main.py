import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRole
import os
import datetime

TOKEN = os.getenv('BAT_TOKEN')
GUILD = 'BAT Brigade'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="|>", case_insensitive=True, intents=intents)
client = discord.Client(intents=intents)


@bot.command(name='ping', description="User sends `ping` and gets `pong!`")
async def ping(ctx):
    await ctx.send("pong!")


@commands.has_role('Admin')
@bot.command(name='war', description="is hell")
async def war(ctx):
    await ctx.send("https://img.search.brave.com/Hz_gINyouglL473i_m-w8pu5dF9M1AHeQAH88gvUics/fit/880/479/ce/1/aHR0cHM6Ly9pLmlt/Z2ZsaXAuY29tLzNm/ZWI0MC5qcGc")


@bot.command(
    name='top_invite_members',
    description="Get the top N number of invites to the server",
    help='Gives the top N inviters over M time'
)
@commands.has_role('Moderator')
async def top_invite_members(ctx):
    guild = ctx.guild
    print('getting invites...')
    msg_lst = ctx.message.content.split(' ')
    print('checking message...')
    msg = await handle_top_invite_messages(ctx, msg_lst)
    if msg == 1:
        return
    print('getting invites...')
    invites = await guild.invites()
    print('creating datetime object...')
    print(msg_lst)
    top_n = int(msg_lst[1])
    today = datetime.date.today()
    days = int(msg_lst[2])
    time_period = today - datetime.timedelta(days=days)
    members = []
    print('getting valid users...')
    for i in invites:
        inviter = i.inviter if guild in i.inviter.mutual_guilds else None
        time_threshold = True if i.created_at.date() >= time_period else None
        # admin_role not in member_roles or mod_role not in member_roles
        if inviter and time_threshold:
            if 'Admin' not in [role for role in guild.get_member(i.inviter.id).roles] or 'Moderator' not in [role for role in guild.get_member(i.inviter.id).roles] or 'Brave Team' not in [role for role in guild.get_member(i.inviter.id).roles]:
                members.append(
                    (
                        inviter, i.uses
                    )
                )
    print('Getting top members...')
    top_member_invites = sorted(members, key = lambda x: x[1], reverse = True)[:top_n]
    print('Creating response...')
    res = f'**Top {top_n} member invites in the last {days} days are:**\n'
    for i in top_member_invites:
        name = i[0].name
        invites = i[1]
        res += f'{name}: {invites}\n'
    print(res)
    await ctx.send(res)

async def handle_top_invite_messages(ctx, msg_lst):
    if len(msg_lst) != 3:
        await ctx.send(
            "This command takes 2 arguments, the number of top invites AND in what period of time (in days),"
            "IN THAT ORDER.\nExample: `$top_monthly_invites` 5 30 -- will return the top 5 inviters over the last 30 days"
        )
        return 1
    try:
        int(msg_lst[1])
        int(msg_lst[2])
    except ValueError:
        await ctx.send('This command\'s arguments are to be in integrer form, i.e. `$top_monthly_invites` 5 30')
        return 1


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRole):
        await ctx.send("Sorry, this command is for Admins only 😢")

bot.run(TOKEN)
