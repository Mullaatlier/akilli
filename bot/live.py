import discord
from discord.ext import commands, tasks
import asyncio

# Gerekli intents'leri ayarlıyoruz
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Botun prefiksi ve tanımı
bot = commands.Bot(command_prefix='!', intents=intents)

# Oluşturulan odaları izlemek için bir sözlük oluşturuyoruz
user_rooms = {}

@bot.event
async def on_ready():
    print('Bot is ready!')
    clean_channel.start()  # Temizlik görevini başlat

# Ses kanalına katılma ve özel oda oluşturma işlemleri
@bot.event
async def on_voice_state_update(member, before, after):
    target_voice_channel_id = 1245318877865312338  # Hedef ses kanalının ID'si
    if after.channel and after.channel.id == target_voice_channel_id:
        # Kullanıcı daha önce bir oda oluşturmuşsa
        if member.id in user_rooms:
            await member.move_to(user_rooms[member.id]['voice_channel'])
        else:
            guild = member.guild
            category = discord.utils.get(guild.categories, name=f"{member.name}'nin Seraları")
            if category is None:
                category = await guild.create_category(name=f"{member.name}'nin Seraları")
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(connect=True)
            }
            
            new_voice_channel = await category.create_voice_channel(name="Odanız", overwrites=overwrites)
            new_text_channel = await category.create_text_channel(name="Sera Kontrol", overwrites=overwrites)
            
            # Loglar için ek bir metin kanalı oluştur
            log_overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),  # Tüm kullanıcılara mesaj gönderme iznini kaldır
                member: discord.PermissionOverwrite(connect=True),  # Kullanıcıya bağlanma izni ver
                bot.user: discord.PermissionOverwrite(view_channel=True),  # Botun log kanalını görmesine izin ver
                member: discord.PermissionOverwrite(view_channel=True, send_messages=False)  # Kullanıcının log kanalını görmesine ve mesaj yazmasına izin verme
            }
            log_channel = await category.create_text_channel(name=f"{member.name}-log", overwrites=log_overwrites)
            
            await member.move_to(new_voice_channel)
            await new_text_channel.send(f"{member.mention}, hoş geldiniz! Bu sizin özel odanız.")

            user_rooms[member.id] = {
                'voice_channel': new_voice_channel,
                'text_channel': new_text_channel,
                'log_channel': log_channel
            }

            role = await guild.create_role(name=f"{member.name}'nin Serası")
            await member.add_roles(role)
            
            await new_voice_channel.set_permissions(role, connect=True)
            await new_text_channel.set_permissions(role, read_messages=True, send_messages=True)

            print(f"{member.name} adlı kullanıcı belirli bir ses kanalına katıldı, özel oda oluşturuldu, rol verildi ve izinler ayarlandı.")

# Metin kanalına yazılan her şeyi log kanalına aktarma
@bot.event
async def on_message(message):
    # Diğer botların mesajlarını da loglamak için ek kontrol
    if message.author.bot:
        log_channel = None
        for room in user_rooms.values():
            if message.channel.id == room['text_channel'].id:
                log_channel = room['log_channel']
                break
        
        if log_channel and message.channel.id != log_channel.id:
            log_message = f"{message.author.name}#{message.author.discriminator}: {message.content}"
            await log_channel.send(log_message)
    
    await bot.process_commands(message)

# Metin kanalını belirli aralıklarla temizleme işlevi
@tasks.loop(seconds=80)
async def clean_channel():
    for room in user_rooms.values():
        await room['text_channel'].purge(limit=100)

# Komut listesi
@bot.command('komutlar')
async def komutlar(ctx):
    komut_listesi = (
        "Komut Listesi\n\n"
        "🌀 Fan Kontrol Komutları\n"
        "> !fanac - Fanı açar\n"
        "> !fankapat - Fanı kapatır\n\n"
        "💡 Lamba Kontrol Komutları\n"
        "> !lambaac - Lambayı açar\n"
        "> !lambakapat - Lambayı kapatır\n\n"
        "💧 Su Kontrol Komutları\n"
        "> !suac - Suyu açar\n"
        "> !sukapat - Suyu kapatır\n\n"
        "🌡️ Durum Bilgisi Komutları\n"
        "> !sicaklik - Sıcaklığı gösterir\n"
        "> !nem - Nem oranını gösterir\n"
        "> !isik - Işık seviyesini gösterir\n"
        "> !topraknem - Toprak nemini gösterir\n"
        "> !suseviyesi - Su seviyesini gösterir\n"
        "> !sensor - Sensör bilgilerini gösterir\n\n"

        ":desktop:  Destek Odasına Bağlanma\n"
        "> !destek - Sizi Canlı Desteğe Götürür \n"
    )
    await ctx.send(komut_listesi)

# Destek komutu
@bot.command()
async def destek(ctx):
    guild = ctx.guild
    user = ctx.author
    channel = discord.utils.get(guild.voice_channels, id=1245333962348564490)  # Hedef ses kanalı

    if channel:
        try:
            await user.move_to(channel)
            await ctx.send(f"{user.mention}, destek odasına taşındınız!")
        except discord.errors.HTTPException:
            await ctx.send("Herhangibir ses kanalına girip tekrar deneyin.")

# Token ile botu başlat
bot.run('MTI0NDA3ODkzNzc2NDY1OTI3NQ.Geaz5g.8lsbmZT7xXIhxEi2c04_mOJyq0LQNlBFtFFvEk')