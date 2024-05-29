import discord
from discord.ext import commands
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = 'MTI0NTM3NTc3MDQ2NjA2MjQ0MA.Gw_2F2.VNnPMgXVTUz-B4kH5IGnVNEy0Y8Vrk0UdcjwEQ'
CHANNEL_ID = 1245345004797300797  # Metin kanalınızın ID'sini buraya yazın

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

@bot.event
async def on_member_join(member):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Üye Eylemi: {member} sunucuya katıldı.')
    except Exception as e:
        print(f'Hata oluştu (on_member_join): {e}')
        logging.error(f'Hata oluştu (on_member_join): {e}')

@bot.event
async def on_member_remove(member):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Üye Eylemi: {member} sunucudan ayrıldı.')
    except Exception as e:
        print(f'Hata oluştu (on_member_remove): {e}')
        logging.error(f'Hata oluştu (on_member_remove): {e}')

@bot.event
async def on_member_ban(guild, user):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Üye Eylemi: {user} sunucudan yasaklandı.')
    except Exception as e:
        print(f'Hata oluştu (on_member_ban): {e}')
        logging.error(f'Hata oluştu (on_member_ban): {e}')

@bot.event
async def on_member_unban(guild, user):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Üye Eylemi: {user} sunucudan yasağı kaldırıldı.')
    except Exception as e:
        print(f'Hata oluştu (on_member_unban): {e}')
        logging.error(f'Hata oluştu (on_member_unban): {e}')

@bot.event
async def on_member_update(before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if before.roles != after.roles:
            await channel.send(f'Üye Eylemi: {after} rolleri güncellendi.')
    except Exception as e:
        print(f'Hata oluştu (on_member_update): {e}')
        logging.error(f'Hata oluştu (on_member_update): {e}')

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if before.channel != after.channel:
            if after.channel is not None:
                await channel.send(f'Üye Eylemi: {member} {after.channel.name} adlı ses kanalına katıldı.')
            if before.channel is not None:
                await channel.send(f'Üye Eylemi: {member} {before.channel.name} adlı ses kanalından ayrıldı.')
    except Exception as e:
        print(f'Hata oluştu (on_voice_state_update): {e}')
        logging.error(f'Hata oluştu (on_voice_state_update): {e}')

@bot.event
async def on_message_delete(message):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Mesaj Eylemi: Bir mesaj silindi.')
    except Exception as e:
        print(f'Hata oluştu (on_message_delete): {e}')
        logging.error(f'Hata oluştu (on_message_delete): {e}')

@bot.event
async def on_message_edit(before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Mesaj Eylemi: Bir mesaj düzenlendi.')
    except Exception as e:
        print(f'Hata oluştu (on_message_edit): {e}')
        logging.error(f'Hata oluştu (on_message_edit): {e}')

@bot.event
async def on_raw_message_delete(payload):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Mesaj Eylemi: Bir mesaj silindi.')
    except Exception as e:
        print(f'Hata oluştu (on_raw_message_delete): {e}')
        logging.error(f'Hata oluştu (on_raw_message_delete): {e}')

@bot.event
async def on_raw_message_edit(payload):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Mesaj Eylemi: Bir mesaj düzenlendi.')
    except Exception as e:
        print(f'Hata oluştu (on_raw_message_edit): {e}')
        logging.error(f'Hata oluştu (on_raw_message_edit): {e}')

@bot.event
async def on_reaction_add(reaction, user):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Mesaj Eylemi: Bir mesaja tepki eklendi.')
    except Exception as e:
        print(f'Hata oluştu (on_reaction_add): {e}')
        logging.error(f'Hata oluştu (on_reaction_add): {e}')

@bot.event
async def on_reaction_remove(reaction, user):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Mesaj Eylemi: Bir mesajdan tepki kaldırıldı.')
    except Exception as e:
        print(f'Hata oluştu (on_reaction_remove): {e}')
        logging.error(f'Hata oluştu (on_reaction_remove): {e}')

@bot.event
async def on_guild_role_create(role):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Rol Eylemi: {role.name} adında yeni bir rol oluşturuldu.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_role_create): {e}')
        logging.error(f'Hata oluştu (on_guild_role_create): {e}')

@bot.event
async def on_guild_role_delete(role):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Rol Eylemi: {role.name} adındaki bir rol silindi.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_role_delete): {e}')
        logging.error(f'Hata oluştu (on_guild_role_delete): {e}')

@bot.event
async def on_guild_role_update(before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if before.name != after.name:
            await channel.send(f'Rol Eylemi: {after.name} adındaki bir rolün adı değiştirildi.')
        if before.color != after.color:
            await channel.send(f'Rol Eylemi: {after.name} adındaki bir rolün rengi değiştirildi.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_role_update): {e}')
        logging.error(f'Hata oluştu (on_guild_role_update): {e}')

@bot.event
async def on_guild_channel_create(channel):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Kanal Eylemi: {channel.name} adında yeni bir kanal oluşturuldu.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_channel_create): {e}')
        logging.error(f'Hata oluştu (on_guild_channel_create): {e}')

@bot.event
async def on_guild_channel_delete(channel):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Kanal Eylemi: {channel.name} adındaki bir kanal silindi.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_channel_delete): {e}')
        logging.error(f'Hata oluştu (on_guild_channel_delete): {e}')

@bot.event
async def on_guild_channel_update(before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if before.name != after.name:
            await channel.send(f'Kanal Eylemi: {after.name} adındaki bir kanalın adı değiştirildi.')
        if before.topic != after.topic:
            await channel.send(f'Kanal Eylemi: {after.name} adındaki bir kanalın konusu değiştirildi.')
        if before.position != after.position:
            await channel.send(f'Kanal Eylemi: {after.name} adındaki bir kanalın pozisyonu değiştirildi.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_channel_update): {e}')
        logging.error(f'Hata oluştu (on_guild_channel_update): {e}')

@bot.event
async def on_guild_update(before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if before.name != after.name:
            await channel.send(f'Sunucu Eylemi: Sunucu adı değiştirildi: {after.name}')
        if before.region != after.region:
            await channel.send(f'Sunucu Eylemi: Sunucu bölgesi değiştirildi: {after.region}')
        if before.afk_channel != after.afk_channel:
            await channel.send(f'Sunucu Eylemi: Sunucu AFK kanalı değiştirildi: {after.afk_channel}')
        if before.afk_timeout != after.afk_timeout:
            await channel.send(f'Sunucu Eylemi: Sunucu AFK zaman aşımı değiştirildi: {after.afk_timeout} saniye')
        if before.owner != after.owner:
            await channel.send(f'Sunucu Eylemi: Sunucu sahibi değiştirildi: {after.owner}')
    except Exception as e:
        print(f'Hata oluştu (on_guild_update): {e}')
        logging.error(f'Hata oluştu (on_guild_update): {e}')

@bot.event
async def on_guild_emojis_update(guild, before, after):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        for emoji in before:
            if emoji not in after:
                await channel.send(f'Emoji Eylemi: {emoji.name} adlı emoji sunucudan kaldırıldı.')
        for emoji in after:
            if emoji not in before:
                await channel.send(f'Emoji Eylemi: {emoji.name} adlı yeni bir emoji sunucuya eklendi.')
    except Exception as e:
        print(f'Hata oluştu (on_guild_emojis_update): {e}')
        logging.error(f'Hata oluştu (on_guild_emojis_update): {e}')

bot.run(TOKEN)



