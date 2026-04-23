import discord
from discord.ext import commands
import os

TOKEN = os.environ.get("DISCORD_TOKEN")

# Configuration des intentions (intents)
intents = discord.Intents.default()
intents.members = True  # Nécessaire pour détecter les nouveaux membres
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ──────────────────────────────────────────
# PERSONNALISE TON MESSAGE ICI ↓
# ──────────────────────────────────────────

def creer_message_bienvenue(member: discord.Member) -> discord.Embed:
    """Crée l'embed de bienvenue envoyé en message privé au nouveau membre."""

    embed = discord.Embed(
        title=f"👋 Saluuut bienvenue sur {member.guild.name} 🫐 !",
        description=(
            f"Salut **{member.display_name}**, ravi de t'accueillir parmi nous ! \n\n"
            f"Voici quelques infos pour bien démarrer :\n\n"
            f"📌 **Lis les règles** pour connaître les règles du serveur.\n"
            f"🎭 **Choisis tes rôles** pour personnaliser ton expérience.\n"
            f"Pour accéder à l'ensemble du serveur (et aux salons NSFW 👀), merci de passer par la vérification.\n"
            f"💬 Pour ce faire il faut ouvrir un ticket Et suivre les instructions du salon vérif https://discord.com/channels/1387001877316501574/1394800529661624400"
            f"⚠️ Sans vérif = pas d’accès complet"
            f"N'hésite pas à poser tes questions, on est là pour t'aider ! 😊"
        ),
        color=discord.Color.purple()
    )

    # Photo de profil du nouveau membre en thumbnail
    embed.set_thumbnail(url=member.display_avatar.url)

    # Bannière ou image du serveur (optionnel)
    if member.guild.banner:
        embed.set_image(url=member.guild.banner.url)

    embed.set_footer(
        text=f"Serveur : {member.guild.name} • {member.guild.member_count} membres",
        icon_url=member.guild.icon.url if member.guild.icon else None
    )

    return embed


# ──────────────────────────────────────────
# ÉVÉNEMENTS DU BOT
# ──────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user} (ID: {bot.user.id})")
    print(f"📡 Présent sur {len(bot.guilds)} serveur(s)")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="les nouveaux arrivants 👋"
        )
    )


@bot.event
async def on_member_join(member: discord.Member):
    """Déclenché quand un nouveau membre rejoint le serveur."""
    print(f"➡️  {member} a rejoint {member.guild.name}")

    embed = creer_message_bienvenue(member)

    # 1) Envoi en message privé au nouveau membre
    try:
        await member.send(embed=embed)
        print(f"✉️  Message privé envoyé à {member}")
    except discord.Forbidden:
        # L'utilisateur a désactivé les MPs → on envoie dans le salon de bienvenue
        print(f"⚠️  Impossible d'envoyer un MP à {member} (MPs désactivés)")

    # 2) (Optionnel) Envoi également dans un salon public du serveur
    #    Décommente les lignes ci-dessous et remplace CHANNEL_ID par l'ID de ton salon
    #
    # channel_id = 123456789012345678  # ← Remplace par l'ID de ton salon #bienvenue
    # channel = member.guild.get_channel(channel_id)
    # if channel:
    #     await channel.send(
    #         content=f"Bienvenue {member.mention} ! 🎉",
    #         embed=embed
    #     )


# ──────────────────────────────────────────
# COMMANDES UTILITAIRES (optionnel)
# ──────────────────────────────────────────

@bot.command(name="ping")
async def ping(ctx):
    """Vérifie que le bot est en ligne."""
    await ctx.send(f"🏓 Pong ! Latence : {round(bot.latency * 1000)} ms")


@bot.command(name="testbienvenue")
@commands.has_permissions(administrator=True)
async def test_bienvenue(ctx):
    """Permet à un admin de tester le message de bienvenue sur lui-même."""
    embed = creer_message_bienvenue(ctx.author)
    try:
        await ctx.author.send(embed=embed)
        await ctx.send("✅ Message de bienvenue envoyé en MP !", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ Impossible d'envoyer un MP (vérifie tes paramètres de confidentialité).")


# ──────────────────────────────────────────
# LANCEMENT DU BOT
# ──────────────────────────────────────────

if __name__ == "__main__":
    bot.run(TOKEN)
