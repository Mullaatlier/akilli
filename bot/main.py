import discord
from discord.ext import commands, tasks
import serial
import time

try:
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Seri port açma hatası: {e}")

TOKEN = 'MTI0Mjg1NjM3MDcyMjU3MDMxMQ.GYWrBq.oQHP0S92QURSEgf_B_oqLVZmatLNQIIprbmusk'
channel_id = 1245394058122362957

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

fan_running = False

def send_command(command):
    if ser.is_open:
        ser.reset_input_buffer()
        ser.write(command)
        time.sleep(2)
        response = ser.readline().decode('utf-8').strip()
        return response
    else:
        return "Seri port açık değil."

def parse_sensor_data(response, sensor_type):
    try:
        value = response.split(':')[1].strip()
        if sensor_type == 'S':
            return float(value.split(' ')[0])
        elif sensor_type == 'T':
            return float(value.split(' ')[0])
        elif sensor_type == 'I':
            return float(value.split(' ')[0])
        elif sensor_type == 'W':
            return float(value.split(' ')[0])
        elif sensor_type == 'H':
            return float(value.split(' ')[0])
    except IndexError:
        print("Yanıt formatı uygun değil:", response)
        return None
    except ValueError:
        print("Yanıt değeri uygun bir sayısal değer değil:", response)
        return None

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    temperature_check.start()
    humidity_check.start()
    light_check.start()
    soil_moisture_check.start()
    water_level_check.start()

@bot.command(name='fanac')
async def fan_ac(ctx):
    response = send_command(b'1')
    await ctx.send(f'Fan açıldı. Yanıt: {response}')

@bot.command(name='fankapat')
async def fan_kapat(ctx):
    response = send_command(b'2')
    await ctx.send(f'Fan kapatıldı. Yanıt: {response}')

@bot.command(name='lambaac')
async def lamba_ac(ctx):
    response = send_command(b'5')
    await ctx.send(f'Lamba açıldı. Yanıt: {response}')

@bot.command(name='lambakapat')
async def lamba_kapat(ctx):
    response = send_command(b'6')
    await ctx.send(f'Lamba kapatıldı. Yanıt: {response}')

@bot.command(name='suac')
async def su_motoru_ac(ctx):
    response = send_command(b'3')
    await ctx.send(f'Su motoru açıldı. Yanıt: {response}')

@bot.command(name='sukapat')
async def su_motoru_kapat(ctx):
    response = send_command(b'4')
    await ctx.send(f'Su motoru kapatıldı. Yanıt: {response}')

@bot.command(name='sicaklik')
async def sicaklik(ctx):
    response = send_command(b'S')
    temperature = parse_sensor_data(response, 'S')
    await ctx.send(f'Son sıcaklık: {temperature}°C')

@bot.command(name='nem')
async def nem(ctx):
    response = send_command(b'H')
    humidity = parse_sensor_data(response, 'H')
    await ctx.send(f'Son nem: {humidity}%')

@bot.command(name='isik')
async def isik(ctx):
    response = send_command(b'I')
    light_level = parse_sensor_data(response, 'I')
    await ctx.send(f'Son ışık seviyesi: {light_level}')

@bot.command(name='topraknem')
async def topraknem(ctx):
    response = send_command(b'T')
    soil_moisture = parse_sensor_data(response, 'T')
    await ctx.send(f'Son toprak nemı: {soil_moisture}')

@bot.command(name='suseviyesi')
async def suseviyesi(ctx):
    response = send_command(b'W')
    water_level = parse_sensor_data(response, 'W')
    await ctx.send(f'Son su seviyesi: {water_level}')

@bot.command(name='sensor')
async def tum_veriler(ctx):
    response_s = send_command(b'S')
    response_t = send_command(b'T')
    response_i = send_command(b'I')
    response_w = send_command(b'W')
    response_h = send_command(b'H')

    temperature = parse_sensor_data(response_s, 'S')
    humidity = parse_sensor_data(response_h, 'H')
    light_level = parse_sensor_data(response_i, 'I')
    soil_moisture = parse_sensor_data(response_t, 'T')
    water_level = parse_sensor_data(response_w, 'W')

    await ctx.send(f'''
    Sıcaklık: {temperature}°C
    Nem: {humidity}%
    Işık Seviyesi: {light_level}
    Toprak Nemi: {soil_moisture}
    Su Seviyesi: {water_level}
    ''')


@tasks.loop(seconds=65)
async def temperature_check():
    channel = bot.get_channel(channel_id)
    response = send_command(b'S')
    temperature = parse_sensor_data(response, 'S')
    global fan_running
    if temperature > 30 and not fan_running:
        response = send_command(b'1')
        fan_running = True
        await channel.send(f"Sıcaklık {temperature}°C. Fan açıldı. Yanıt: {response}")
    elif temperature <= 30 and fan_running:
        response = send_command(b'2')
        fan_running = False
        await channel.send(f"Sıcaklık {temperature}°C. Fan kapatıldı. Yanıt: {response}")
    else:
        await channel.send(f"Sıcaklık {temperature}°C. Fan durumu: {'Gerekli' if fan_running else 'Gerek yok'}")

@temperature_check.before_loop
async def before_temperature_check():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send("Sıcaklık kontrolü başladı.")
    



@tasks.loop(seconds=66)
async def humidity_check():
    channel = bot.get_channel(channel_id)
    response = send_command(b'H')
    humidity = parse_sensor_data(response, 'H')
    if humidity >= 60:
        response = send_command(b'1')
        await channel.send(f"Nem {humidity}%. Fan açıldı. Yanıt: {response}")
    else:
        response = send_command(b'2')
        await channel.send(f"Nem {humidity}%.   nem normal.")

@humidity_check.before_loop
async def before_humidity_check():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send("Nem kontrolü başladı.")

@tasks.loop(seconds=67)
async def light_check():
    channel = bot.get_channel(channel_id)
    response = send_command(b'I')
    light_level = parse_sensor_data(response, 'I')
    if light_level <= 100:
        response = send_command(b'5')
        await channel.send(f"Işık seviyesi düşük. Lamba açıldı. Yanıt: {response}")
    else:
        response = send_command(b'6')
        await channel.send(f"Işık seviyesi normal.")

@light_check.before_loop
async def before_light_check():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send("Işık kontrolü başladı.")

@tasks.loop(seconds=68)
async def soil_moisture_check():
    channel = bot.get_channel(channel_id)
    response = send_command(b'T')
    soil_moisture = parse_sensor_data(response, 'T')
    if soil_moisture >= 1000:
        response = send_command(b'3')
        await channel.send(f"Toprak oldukça kuru, Su motoru açıldı. Yanıt: {response}")
    else:
        response = send_command(b'4')
        await channel.send(f"Toprak nemi normal.")

@soil_moisture_check.before_loop
async def before_soil_moisture_check():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send("Toprak nemi kontrolü başladı.")

@tasks.loop(seconds=69)
async def water_level_check():
    channel = bot.get_channel(channel_id)
    response = send_command(b'W')
    water_level = parse_sensor_data(response, 'W')
    if water_level <= 10:
        await channel.send("Su seviyesi düşük. Su bitiyor uyarı!!!!")
    else:
        await channel.send("Su seviyesi normal.")

@water_level_check.before_loop
async def before_water_level_check():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send("Su kontrolü başladı.")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Hata: {error}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author != bot.user:
        if ser.is_open:
            ser.reset_input_buffer()

bot.run(TOKEN)

