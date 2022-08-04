import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import asyncio
from mariocard import WelcomeCard



intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Online")
    await client.change_presence(activity=discord.Game(name=".help"))

#When member joins a server creates welcome card (on dedicated channel) and gives a role
@client.event
async def on_member_join(member,guild="pirate ship"):
    channel = discord.utils.get(member.guild.channels, id=965729503043264575)
    role = discord.utils.get(member.guild.roles, id=1000012414164672522)
    card = WelcomeCard()
    card.name = member
    card.server = guild
    card.avatar = member.avatar_url
    card.text = "Witaj na serwerze"
    card.is_rounded = True
    card.color = "green"
    card.path="https://ogrodniktomek.pl/wp-content/uploads/2011/08/kret.jpg"

    await member.add_roles(role)
    await channel.send(file = await card.create())


@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, id=910922235861172234)
    await channel.send(f"{member.name} nara!!")

#Draws a number from (low) to (high)
@client.command()
async def draw(ctx,low : int, high : int):
    if(low < high):
        number = random.randrange(low, high)
        await ctx.channel.send(number)
    else:
        await ctx.channel.send("Podano złą wartość")

@client.command()
async def klubowicz(ctx):
    ile = random.randint(0,100)
    if(ile>90):
        await ctx.send(f"Jesteś generałem klubu  R masz ({ile} %)")
        await ctx.send("https://cdn.discordapp.com/emojis/814171422069882891.webp")
    elif(ile<20):
        await ctx.send(f"Nie jesteś członkiem klubu R  :ninja:")
    else:
        await ctx.send(f"Jesteś członkiem klubu R w ({ile} %)")
        await ctx.send("https://cdn.discordapp.com/emojis/699788076951797851.webp")
    return ile

@client.command()
async def rasista(ctx):
    ile = random.randint(0,100)
    if(ile<75):
        await ctx.send("Brawo nie jesteś rasistą.")
        await ctx.send("https://cdn.discordapp.com/emojis/959811841108885565.webp")
    else:
        await ctx.send("Jesteś prawdziwym rasistą pogromcą murzynów.")
        await ctx.send("https://cdn.discordapp.com/emojis/859536686773174303.webp")

#Displays all commands includes aliases if someone missclicks :)
@client.command(aliases = ["hel[","hekp","gelp"])
@commands.cooldown(1, 30, commands.BucketType.user)
async def help(ctx):
    embed = discord.Embed(title="Pomoc", description="Komendy:", color=0x00eb3b)
    embed.add_field(name=".help", value="Pokazuje okienko z komendami", inline=True)
    embed.add_field(name=".ban", value="Ban użytkownika za nic (admin only)", inline=True)
    embed.add_field(name=".clear", value="Wyczyść wiadomości (admin only)",inline=True)
    embed.add_field(name=".kick", value="Kick użytkownika za nic (admin only)", inline=True)
    embed.add_field(name=".draw", value="Losuj liczbę np. !draw 0 100",inline=True)
    embed.add_field(name=".hello",value="Witam się z tobą :)", inline=True)
    embed.add_field(name=".play", value="Ustaw grę w jaką gram", inline=True)
    embed.add_field(name=".stream", value="Ustaw grę jaką streamuję",inline=True)
    embed.add_field(name=".listen", value="Ustaw muzykę jaką słucham",inline=True)
    embed.add_field(name=".watch", value="Ustaw film jaki oglądam",inline=True)
    embed.add_field(name=".kto",value="no kto", inline=True)
    embed.add_field(name=".klubowicz",value="Sprawdź czy nadajesz się do klubu.",inline=True)
    embed.add_field(name=".rasista", value="Sprawdź czy jesteś rasistą.", inline=True)
    await ctx.send(embed=embed)

#Ban command for user that have ban permission
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member,reason="ban za nic LIKE"):
    await member.ban(reason=reason)
    await ctx.channel.send(f"Zbanowano {member.mention} za {reason}")

#Kick command for user that have kick permission
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member,reason ="ban za nic LIKE"):
    await member.kick(reason=reason)
    await ctx.channel.send(f"Wyrzucono {member.mention} za: {reason} ")

#Changes bot status
@client.command()
async def play(ctx, *, game):
    await ctx.channel.send("Zmieniam...")
    await asyncio.sleep(3)
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game(name=game))
    await ctx.channel.send(f"Zmieniono grę na {game}")

#Changes bot status
@client.command()
async def stream(ctx, *, game):
    await ctx.channel.send("Zmieniam...")
    await asyncio.sleep(3)
    await client.change_presence(activity=discord.Streaming(name=game,url="https://www.twitch.tv/h2p_gucio"))
    await ctx.channel.send(f"Zmieniono grę na {game}")
#Changes bot status
@client.command()
async def listen(ctx, *, music):
    await ctx.channel.send("Zmieniam...")
    await asyncio.sleep(3)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=music))
    await ctx.channel.send(f"Zmieniono muzykę na {music}")

#Changes bot status
@client.command()
async def watch(ctx,*,film):
    await ctx.channel.send("Zmieniam...")
    await asyncio.sleep(3)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=film))
    await ctx.channel.send(f"Zmieniono film na {film}")

#Changes bot status
@client.command()
async def hello(ctx):
    tab = ["Hej","Siema","Witaj","Elo","Salam Alaykum","Yo Nigga", "Wassup"]
    await ctx.channel.send(random.choice(tab))

#Purge command (Clears chat for (value) messages) u need administrator permission
@client.command()
@has_permissions(administrator=True)
async def clear(ctx, value : int):
    await ctx.channel.purge(limit=value)
    await asyncio.sleep(1)
    await ctx.send("Usunięto")

#Unban command only for administrator
@client.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    if "#" in member:
        banned = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Odbanowałeś {user.name}")
    else:
        await ctx.send(f"Podaj nick w ten sposób: hexxie#2808")

@client.command()
async def kto(ctx):
    await ctx.channel.send("Niggas in paris  :sunglasses: :call_me: \nhttps://www.youtube.com/watch?v=gG_dA32oH44")

#Verify command that creates reaction role
@client.command()
@has_permissions(administrator=True)
async def verify(ctx):
    embed = discord.Embed(title="Weryfikacja", description="Aby się zweryfikować kliknij emotkę!", color=0x00eb3b)
    await ctx.channel.send(embed=embed)
    msg = await ctx.send("O tutaj!!!")
    await msg.add_reaction('✅')

#This command add role for member that clicked emote
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1000022302014062654:
        if payload.emoji.name == '✅':
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=1000017281499287552)
            await member.add_roles(role)

#Deletes role if u click again
@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 1000022302014062654:
        if payload.emoji.name == '✅':
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=1000017281499287552)
            await member.remove_roles(role)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Nie znaleziono komendy! Spróbuj .help")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Komenda jest na cooldownie.{error.retry_after:.3f}")

@play.error
async def play_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Nie podano nazwy gry!")

@stream.error
async def stream_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Nie podano gry jaką mam streamować!")

@listen.error
async def listen_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Nie podano muzyki jakiej mam słuchać!")

@watch.error
async def watch_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Nie podano filmu jaki mam oglądać")
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Nie podano osoby")

@kick.error
async def kick_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Nie podano osoby")



client.run("TOKEN")
